from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from tinymce.models import HTMLField


class Wall(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='walls',
        verbose_name=_('owner'),
    )
    name = models.CharField(_('name'), max_length=255)
    pin_to_top = models.BooleanField(_('pin to top'), default=False)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)


class Post(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='walls',
        verbose_name=_('owner'),
    )
    content = HTMLField(_('content')),
    wall = models.ForeignKey(
        Wall, 
        verbose_name=_("wall"), 
        on_delete=models.CASCADE,
        related_name='posts',
        null=True,
        blank=True,
    )
    pin_to_top = models.BooleanField(_('pin to top'), default=False)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_add=True)
    reply_to = models.ForeignKey(
        "Post", 
        verbose_name=_("reply_to"), 
        on_delete=models.SET_NULL,
        related_name='replies',
        null=True,
        blank=True,
    )
    repost_of = models.ForeignKey(
        "Post", 
        verbose_name=_("repost_of"), 
        on_delete=models.SET_NULL,
        related_name='reposts',
        null=True,
        blank=True,
    )
