from collections import OrderedDict

from django.contrib.auth import get_user_model
from django.urls import reverse

from sites.tests.base_test import BaseSetupCase


User = get_user_model()


class ArticlesTests(BaseSetupCase):
    def setUp(self):
        super().setUp()

    def test_user_sites(self):
        """Тестирование сайтов выбранных пользователями, ключевых слов"""
        prefer_site_list = reverse('list_prefer', kwargs={'pk': self.dummy_user.pk})
        response = self.dummy_client.get(prefer_site_list)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [OrderedDict([('pk', self.site_interface.pk), ('site', self.main_site.pk)])])
        prefer_key_words = reverse('detail_prefer',
                                   kwargs={'pk': self.dummy_user.pk, 'interface_id': self.site_interface.pk})
        response = self.dummy_client.get(prefer_key_words)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {
            'pk': self.site_interface.pk,
            'site': self.main_site.pk,
            'key_words': ['ввоз', 'запрет', 'фтс'],
            'exclude_words': ['проект']
        })

    def test_user_estimation(self):
        """Тестирование пользовательских оценок статей"""
        estimation_list = reverse('est-list')
        response = self.dummy_client.get(estimation_list)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[1].get('user'), self.dummy_user.pk)
        self.assertEqual(response.data[1].get('article'), self.second_article.pk)
        self.assertEqual(response.data[1].get('user_estimation'), 'vb')
        estimation_detail = reverse('est-detail', kwargs={'pk': self.second_estimate.pk})
        response = self.dummy_client.get(estimation_detail)
        self.assertEqual(response.status_code, 200)
        response_data = response.data
        response_data.pop('id')
        self.assertEqual(response_data, {
            'user': self.dummy_user.pk,
            'article': self.second_article.pk,
            'user_estimation': 'vb'}
        )
        estimation_var = {'user_estimation': 'vg'}
        response = self.dummy_client.patch(estimation_detail, estimation_var)
        response_data = response.data
        response_data.pop('id')
        self.assertEqual(response.data, {
            'user': self.dummy_user.pk,
            'article': self.second_article.pk,
            'user_estimation': 'vg'}
        )
        response = self.dummy_client.delete(estimation_detail)
        self.assertEqual(response.status_code, 204)
        new_estimation = {'user': self.dummy_user.pk, 'article': self.second_article.pk, 'user_estimation': 'bd'}
        response = self.dummy_client.post(estimation_list, new_estimation)
        self.assertEqual(response.status_code, 201)
        response_data = response.data
        response_data.pop('id')
        self.assertEqual(response_data, {
            'user': self.dummy_user.pk,
            'article': self.second_article.pk,
            'user_estimation': 'bd'}
        )
