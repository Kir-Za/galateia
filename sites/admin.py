from django.contrib import admin
from sites.models import Site, Article
from users.models import UserArticle


@admin.register(Site)
class SiteAdmin(admin.ModelAdmin):
    fields = ('target_url', 'is_active', ('news_portal', 'news_department'))
    list_display = ('target_url', 'is_active')


class UserArticleAdmin(admin.StackedInline):
    max_num = 1
    model = UserArticle

    def get_field_queryset(self, db, db_field, request):
        query = super().get_field_queryset(db, db_field, request)
        if db_field.name == 'user':
            query = query.filter(pk=request.user.pk)
        return query


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    fields = ('link', 'news_title', 'main_text')
    list_display = ('news_title',)
    readonly_fields = ('link', 'news_title', 'main_text')
    inlines = [
        UserArticleAdmin
    ]

    def news_title(self, inctance, *args, **kwargs):
        return inctance.content.get('news_title', '- - -')

    def main_text(self, inctance):
        return inctance.content.get('main_text', '- - -')

    news_title.short_description = "Заголовок"
    main_text.short_description = "Основной текст"
