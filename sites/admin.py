from django.contrib import admin
from sites.models import Site, Article, UserArticle, UserSite


@admin.register(Site)
class SiteAdmin(admin.ModelAdmin):
    fields = ('target_url', 'is_active', ('news_portal', 'news_department'))
    list_display = ('target_url', 'is_active')


class UserArticleAdmin(admin.StackedInline):
    max_num = 1
    model = UserArticle

    def get_field_queryset(self, db, db_field, request):
        query = super().get_field_queryset(db, db_field, request)
        if db_field.name == 'user' and not request.user.is_superuser:
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


@admin.register(UserSite)
class UserSiteAdmin(admin.ModelAdmin):
    list_display = ('site', 'user')
    fields = ('site', ('key_words', 'exclude_words'))

    def get_queryset(self, request):
        query = super().get_queryset(request)
        if not request.user.is_superuser:
            return query.filter(user=request.user) if query else query
        return query

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.user_id = request.user.pk
        super().save_model(request, obj, form, change)
