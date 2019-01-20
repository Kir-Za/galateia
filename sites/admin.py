from django.contrib import admin
from sites.models import Site, TmpContent

# Register your models here.
admin.site.register(TmpContent)
admin.site.register(Site)