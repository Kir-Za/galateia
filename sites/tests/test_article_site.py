from collections import OrderedDict

from django.contrib.auth import get_user_model
from django.urls import reverse

from sites.tests.base_test import BaseSetupCase


User = get_user_model()


class ArticlesTests(BaseSetupCase):
    def setUp(self):
        super().setUp()

    def test_sites_list(self):
        """Тестирование списка доступных сайтов для парсинга"""
        list_url = reverse('list_sites')
        response = self.dummy_client.get(list_url)
        self.assertEqual(response.status_code, 200)
        link_dict = {response.data[0].get('target_url'): response.data[0].get('is_active'),
                     response.data[1].get('target_url'): response.data[1].get('is_active')}
        self.assertTrue(link_dict[self.main_site_target_url])
        self.assertFalse(link_dict[self.off_site_target_url])

    def test_article(self):
        """Тестирование списка и детальной информации по имеющимся статьям"""
        list_article = reverse('list_articles')
        response = self.dummy_client.get(list_article)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data,
            [OrderedDict([
                ('pk', self.first_article.pk),
                ('link', 'https://tass.ru/ekonomika/6126020'),
                ('title', 'ФТС предложила расширить перечень продуктов, запрещенных к ввозу в РФ из ряда других ...'),
                ('has_prices', False),
                ('has_percents', False),
                ('frequent_words',
                    'ввоз, запрет, консервированных, путем, стран, товаров, фтс, предлагается, продукции')]),
            OrderedDict([
                ('pk', self.second_article.pk),
                ('link', 'https://tass.ru/ekonomika/6127831'),
                ('title', 'Лимузин Aurus представили на IDEX-2019'),
                ('has_prices', True),
                ('has_percents', True),
                ('frequent_words',
                    'проекту, ранее, российских, россия, февраля, tawazun, кортеж, проект, aurus, автомобилей')])
            ]
        )
        detail_article = reverse('detail_article', kwargs={'pk': self.first_article.pk})
        response = self.dummy_client.get(detail_article)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {
            'content': {
                'target': 'https://tass.ru/ekonomika',
                'abstract': 'В ведомстве сообщили, что письмо с перечнем продукции ...',
                'main_text': 'МОСКВА, 16 февраля. /ТАСС/. Федеральная таможенная служба (ФТС) России предложила ...',
                'news_link': 'https://tass.ru/ekonomika/6126020',
                'news_title': 'ФТС предложила расширить перечень продуктов, запрещенных к ввозу в РФ из ряда других ...'
            },
            'has_prices': False,
            'has_percents': False,
            'frequent_words': 'ввоз, запрет, консервированных, путем, стран, товаров, фтс, предлагается, продукции'
        })
