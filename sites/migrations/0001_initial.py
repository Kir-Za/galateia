# Generated by Django 2.1.5 on 2019-01-05 09:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Site',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key_word', models.CharField(max_length=50, verbose_name='Ключевое слово для поиска')),
                ('support_word', models.CharField(blank=True, default='', max_length=50, verbose_name='Вспомогательное слово для поиска')),
                ('target_urls', models.URLField(verbose_name='Целевой url')),
                ('is_active', models.BooleanField(default=True, verbose_name='Актуальный для парсинга сайт')),
            ],
            options={
                'verbose_name': 'Целевой сайт',
                'verbose_name_plural': 'Целевые сайты',
            },
        ),
        migrations.CreateModel(
            name='TmpContent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link', models.URLField(verbose_name='Адрес')),
                ('title', models.CharField(max_length=200, verbose_name='Заголовок')),
                ('body', models.TextField(verbose_name='Тело статьи')),
                ('target_site', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='sites.Site', verbose_name='Корневой сайт')),
            ],
        ),
    ]
