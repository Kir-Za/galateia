from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token

from sites.models import Site, UserSite, Article, UserArticle

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
            key_words="ввоз, запрет, фтс",
            exclude_words="проект"
        )

        self.first_article, created = Article.objects.get_or_create(
            link='https://tass.ru/ekonomika/6126020',
            has_prices=False,
            has_percents=False,
            frequent_words='ввоз, запрет, консервированных, путем, стран, товаров, фтс, предлагается, продукции',
            content={
                'target': 'https://tass.ru/ekonomika',
                'abstract': 'В ведомстве сообщили, что письмо с перечнем продукции ...',
                'main_text': 'МОСКВА, 16 февраля. /ТАСС/. Федеральная таможенная служба (ФТС) России предложила ...',
                'news_link': 'https://tass.ru/ekonomika/6126020',
                'news_title': 'ФТС предложила расширить перечень продуктов, запрещенных к ввозу в РФ из ряда других ...'
            }
        )
        self.second_article, created = Article.objects.get_or_create(
            link='https://tass.ru/ekonomika/6127831',
            has_prices=True,
            has_percents=True,
            frequent_words='проекту, ранее, российских, россия, февраля, tawazun, кортеж, проект, aurus, автомобилей',
            content={
                'target': 'https://tass.ru/ekonomika',
                'abstract': 'Мировая премьера автомобиля запланирована на март 2019 года',
                'main_text': 'АБУ-ДАБИ, 17 февраля. /ТАСС/. Российский лимузин Aurus (ранее - проект "Кортеж") ... ',
                'news_link': 'https://tass.ru/ekonomika/6127831',
                'news_title': 'Лимузин Aurus представили на IDEX-2019'
            },
        )

        self.first_estimate, created = UserArticle.objects.get_or_create(
            article=self.first_article,
            user=self.dummy_user,
            user_estimation=UserArticle.VERY_GOOD
        )

        self.second_estimate, created = UserArticle.objects.get_or_create(
            article=self.second_article,
            user=self.dummy_user,
            user_estimation=UserArticle.VERY_BAD
        )

        # client authorization
        self.dummy_client = APIClient()
        self.dummy_token, created = Token.objects.get_or_create(user=self.dummy_user)
        self.dummy_client.credentials(HTTP_AUTHORIZATION='Token ' + str(self.dummy_token))
        self.bot_client = APIClient()
        self.bot_token, created = Token.objects.get_or_create(user=self.bot_user)
        self.bot_client.credentials(HTTP_AUTHORIZATION='Token ' + str(self.bot_token))

    def tearDown(self):
        self.dummy_client.logout()
        self.bot_client.logout()
        UserArticle.objects.all().delete()
        UserSite.objects.all().delete()
        Article.objects.all().delete()
        Site.objects.all().delete()
        User.objects.all().delete()

