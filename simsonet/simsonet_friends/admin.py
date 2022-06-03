from django.contrib import admin
from . import models


class FriendAdmin(admin.ModelAdmin):
    list_display = ('user', 'friend', 'is_accepted', 'is_blocked', 'created_at', )
    list_display_links = ('user', 'friend', )
    list_filter = ('is_accepted', 'is_blocked', 'created_at', )


admin.site.register(models.Friend, FriendAdmin)
