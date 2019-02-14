from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token

from sites.models import Site
from users.models import UserSite

User = get_user_model()


class BaseSetupCase(APITestCase):
    def setUp(self):
        # create users
        self.dummy_username = "TestUser"
        self.dummy_email = "user@galateia.ru"
        self.dummy_password = "dummy_user_password"
        self.dummy_user = User.objects.create_user(
            username= self.dummy_username,
            email=self.dummy_email,
            password=self.dummy_password,
            user_type=User.USER,
        )
        self.bot_username = "TestBot"
        self.bot_email = "bot@galateia.ru"
        self.bot_password = "bot_password"
        self.bot_user = User.objects.create_user(
            username=self.bot_username,
            email=self.bot_email,
            password=self.bot_password,
            user_type=User.ACTOR,
        )

        self.main_site_target_url = 'https://tass.ru/ekonomika'
        self.main_site, created = Site.objects.get_or_create(target_url=self.main_site_target_url, is_active=True)
        self.off_site_target_url = 'https://tass.ru/politika'
        self.off_site, created = Site.objects.get_or_create(target_url=self.off_site_target_url, is_active=False)

        self.site_interface, created = UserSite.objects.get_or_create(
            site=self.main_site,
            user=self.dummy_user,
            key_words="тест, успешно, прошел",
            exclude_words="ошибка"
        )

        # client authorization
        self.dummy_client = APIClient()
        self.dummy_token, created = Token.objects.get_or_create(user=self.dummy_user)
        self.bot_client = APIClient()
        self.bot_token, created = Token.objects.get_or_create(user=self.bot_user)

    def tearDown(self):
        self.dummy_user .logout()
        self.bot_user.logout()
        User.objects.all().delete()
        UserSite.objects.all().delete()
        Site.objects.all().delete()
