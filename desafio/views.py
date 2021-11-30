from django.shortcuts import render
from .models import Cotacao, Moeda
from .forms import FiltroCotacoesForm
from django.conf import settings
import json
import requests
import datetime as dt
from workadays import workdays as wd


def index(request):
    qs_cotacoes = Cotacao.objects.all()
    hoje = dt.datetime.now()
    data_inicial = wd.workdays(hoje, -5, country='England')
    data_final = wd.workdays(hoje, -1, country='England')

    # se o usuário selecionou as datas pelo formulário
    if request.method == 'POST' and 'range_datas' in request.POST:
        range_datas = request.POST.get('range_datas')
        data1 = dt.datetime.strptime(range_datas.split(' - ')[0], '%d/%m/%Y')
        data2 = dt.datetime.strptime(range_datas.split(' - ')[1], '%d/%m/%Y')
        # valida as datas pra corrigir o bug encontrado
        if data1 < hoje:
            data_inicial = data1
        if data2 < hoje:
            data_final = data2

    cotacoes = {
        'BRL' : {'name': 'BRL', 'data': list()},
        'EUR': {'name': 'EUR', 'data': list()},
        'JPY': {'name': 'JPY', 'data': list()},
    }
    datas = []
    range_datas = []
    count = 0
    data = data_inicial
    while data != data_final:
        # procura os últimos dias úteis na Inglaterra pois o VAT só tem resultados para os dias útei de lá
        data = wd.workdays(data_inicial, count, country='England')
        datas.append(data.strftime('%d/%m/%Y'))
        # consulta a base de dados
        qs_cotacoes = qs_cotacoes.filter(data=data)
        if qs_cotacoes.exists():
            for cotacao in qs_cotacoes:
                cotacoes[cotacao.moeda.abreviatura]['data'].append(cotacao.valor)
        # se não existe cotação salva na base consulta a api e já salva na base
        else:
            # monta a url de consulta
            url = f'{settings.API_VAT_URL}?base={settings.API_VAT_BASE}&date={data.strftime("%Y-%m-%d")}'
            response = requests.get(url).json()
            rates = response['rates']
            if data.strftime('%Y-%m-%d') == response['date']:
                for rate in rates:
                    # filtra pra pegar apenas as moedas BRL, EUR e JPY
                    if rate in ['BRL', 'EUR', 'JPY']:
                        cotacoes[rate]['data'].append(rates[rate])
                        moeda, created = Moeda.objects.get_or_create(abreviatura=rate)                    
                        Cotacao.objects.create(
                            moeda=moeda,
                            data=data,
                            valor=rates[rate],
                        )

        count += 1

    # monta o highchart
    chart = {
        'chart': {'type': 'column'},
        'title': { 'text': 'Cotação das moedas com base no Dólar' },
        'subtitle': { 'text': 'Fonte: https://www.vatcomply.com/'},
        'yAxis': { 'title': { 'text': 'Valor' }},
        'xAxis': { 'categories': datas},
        'series': [cotacoes[cotacao] for cotacao in cotacoes],
        'legend': { 
            'layout': 'vertical',
            'align': 'right',
            'verticalAlign': 'middle'
        },
        'responsive': {
            'rules': [{
                'condition': { 'maxWidth': '500'},
                'chartOptions': {
                    'legend': {
                        'layout': 'horizontal',
                        'align': 'center',
                        'verticalAlign': 'bottom'
                    }
                }
            }]
        }
    }

    context = {
        'chart': json.dumps(chart), 
        'data_inicial': f'{data_inicial.strftime("%d/%m/%Y")}', 
        'data_final': f'{data_final.strftime("%d/%m/%Y")}',
        'hoje': hoje,
    }
    return render(request, 'desafio/index.html', context)