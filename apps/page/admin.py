from django.contrib import admin

from apps.page.models import Page, Post, Tag


class PageAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'is_private')
    list_filter = ('owner', 'is_private')


class PostAdmin(admin.ModelAdmin):
    list_display = ('content', 'page', 'created_at')
    list_filter = ('page', 'created_at')


admin.site.register(Page, PageAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Tag)
