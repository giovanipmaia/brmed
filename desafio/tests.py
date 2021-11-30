import datetime as dt

from django.test import TestCase
from workadays import workdays as wd
from .forms import FiltroCotacoesForm


class IndexTest(TestCase):

    def setUp(self):
        self.resp = self.client.post('/desafio/')

    def test_get(self):
        """
        GET / teste básico de acesso a url
        """
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        """
        Verificação do template usado
        """
        self.assertTemplateUsed(self.resp, 'desafio/index.html')

    def test_rule(self):
        """
        Sem nenhuma informação deve trazer a cotação dos últimos 5 dias úteis        
        """
        hoje = dt.datetime.now()
        for dia in range(-5, 0):
            data = wd.workdays(hoje, dia, country='England')
            'Procura a data na tela'
            self.assertContains(self.resp, data.strftime('%d/%m/%Y'))

    def test_datas_futuras(self):
        """
        O sistema não deve permitir que o usuário realize consulta em datas futuras
        """
        hoje = dt.datetime.now()
        obj = dict(
            range_datas=f'{wd.workdays(hoje, 1, country="England").strftime("%d/%m/%Y")} - {wd.workdays(hoje, 3, country="England").strftime("%d/%m/%Y")}'
        )
        response = self.client.post(f'/desafio/', obj)
        for dia in range(1, 3):
            data = wd.workdays(hoje, dia, country='England')
            'Procura a data na tela'
            self.assertNotContains(response, data.strftime('%d/%m/%Y'))
