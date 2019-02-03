from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import User, UserSite


class UserSiteInline(admin.TabularInline):
    model = UserSite
    fields = ('site', ('key_words', 'exclude_words'))
    max_num = 1


@admin.register(User)
class UserAdmin(UserAdmin):
    inlines = [
        UserSiteInline
    ]
