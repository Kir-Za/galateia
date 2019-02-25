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
