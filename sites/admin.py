from django.contrib import admin
from sites.models import Site, TmpContent

@admin.register(Site)
class SiteAdmin(admin.ModelAdmin):
    fields = ('target_urls', 'is_active', ('news_portal', 'news_department'), 'key_words', 'exclude_words')
    list_display = ('target_urls', 'is_active')


@admin.register(TmpContent)
class SiteAdmin(admin.ModelAdmin):
    fields = ('link', 'title', 'abstract', 'body')
    list_display = ('title', 'target_site')
    readonly_fields = ('link', 'title', 'abstract', 'body')
