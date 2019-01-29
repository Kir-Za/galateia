from django.contrib import admin
from sites.models import Site, Article

@admin.register(Site)
class SiteAdmin(admin.ModelAdmin):
    fields = ('target_urls', 'is_active', ('news_portal', 'news_department'), 'key_words', 'exclude_words')
    list_display = ('target_urls', 'is_active')


@admin.register(Article)
class SiteAdmin(admin.ModelAdmin):
    fields = ('link', 'news_title', 'main_text')
    list_display = ('news_title',)
    readonly_fields = ('link', 'news_title', 'main_text')

    def news_title(self, inctance):
        return inctance.content.get('news_title', '- - -')

    def main_text(self, inctance):
        return inctance.content.get('main_text', '- - -')

    news_title.short_description = "Заголовок"
    main_text.short_description = "Основной текст"
