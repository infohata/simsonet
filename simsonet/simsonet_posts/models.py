from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from tinymce.models import HTMLField


class Wall(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='walls',
        verbose_name=_('owner'),
    )
    name = models.CharField(_('name'), max_length=255, default=_('Personal'), db_index=True)
    pin_to_top = models.BooleanField(_('pin to top'), default=False)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True, db_index=True)

    def __str__(self):
        return f'{self.name} {_("of")} {str(self.owner)}'

    class Meta:
        verbose_name = _('wall')
        verbose_name_plural = _('walls')
        ordering = ('pin_to_top', 'created_at', )
        unique_together = ('owner', 'name', )


class Post(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name=_('owner'),
    )
    content = HTMLField(_('content'))
    wall = models.ForeignKey(
        Wall, 
        verbose_name=_("wall"), 
        on_delete=models.CASCADE,
        related_name='posts',
        null=True,
        blank=True,
    )
    pin_to_top = models.BooleanField(_('pin to top'), default=False)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True, db_index=True)
    reply_to = models.ForeignKey(
        "Post", 
        verbose_name=_("reply to"), 
        on_delete=models.SET_NULL,
        related_name='replies',
        null=True,
        blank=True,
    )
    repost_of = models.ForeignKey(
        "Post", 
        verbose_name=_("repost of"), 
        on_delete=models.SET_NULL,
        related_name='reposts',
        null=True,
        blank=True,
    )

    def __str__(self):
        return f'{str(self.created_at)}, {str(self.owner)}'

    def get_absolute_url(self):
        return reverse("post_detail", kwargs={"pk": self.pk})

    class Meta:
        verbose_name = _('post')
        verbose_name_plural = _('posts')
        ordering = ('pin_to_top', 'created_at', )


class Like(models.Model):
    post = models.ForeignKey(
        Post, 
        verbose_name=_("post"), 
        on_delete=models.CASCADE, 
        related_name='likes'
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        verbose_name=_("owner"), 
        on_delete=models.CASCADE, 
        related_name='likes'
    )
    created_at = models.DateTimeField(_('created at'), auto_now_add=True, db_index=True)

    def __str__(self):
        return f'{str(self.post)} {str(self.owner)} {str(self.created_at)}'
    
    class Meta:
        verbose_name = 'like'
        verbose_name_plural = 'likes'
        unique_together = ('post', 'owner', )
