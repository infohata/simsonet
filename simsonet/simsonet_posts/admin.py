from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from . import models


class PostAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at', 'updated_at', )
    fieldsets = (
        (_('What is it all about?'), {
            "fields": (
                'content',
            ),
        }),
        (_('General info'), {
            "fields": (
                ('owner', 'wall', ),
                ('reply_to', 'repost_of', ),
                ('created_at', 'updated_at', 'pin_to_top', ),
            ),
        }),
    )
    list_display = ('content', 'owner', 'created_at', 'pin_to_top', 'wall', )
    list_display_links = ('created_at', )
    list_filter = ('owner', 'pin_to_top', 'created_at', 'wall', )
    search_fields = ('content', )


admin.site.register(models.Post, PostAdmin)
admin.site.register(models.Wall)
