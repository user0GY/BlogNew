from django.contrib import admin

from BlogNew.custom_site import custom_site
from apps.config.models import Link,SideBar
# Register your models here.

@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    list_display = ('title','href','status','weight','create_time')
    fields = ('title','href','status','weight')

    def save_model(self, request, obj, form, change):
        obj.author=request.user
        return super(LinkAdmin, self).save_model(request, obj, form, change)


@admin.register(SideBar)
class SideBarAdmin(admin.ModelAdmin):
    list_display = ('title', 'tpye', 'content','create_time')
    fields = ('title', 'tpye', 'content')

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        return super(SideBarAdmin, self).save_model(request, obj, form, change)

custom_site.register(SideBar)
custom_site.register(Link)