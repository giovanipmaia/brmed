import datetime as dt

from django.test import TestCase
from workadays import workdays as wd


class IndexTest(TestCase):

    def setUp(self):
        self.resp = self.client.get('/desafio/')

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

