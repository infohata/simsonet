from django.conf import settings
from django.db import models
from tinymce.models import HTMLField
from django.utils.translation import gettext_lazy as _


class Friend(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        verbose_name=_("user"), 
        on_delete=models.CASCADE,
        related_name='friend_requests',
    )
    friend = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        verbose_name=_("friend"), 
        on_delete=models.CASCADE,
        related_name='friends',
    )
    is_accepted = models.BooleanField(_("accepted"), default=False)
    is_blocked = models.BooleanField(_("blocked"), default=False)
    request_message = HTMLField(_("request message"), blank=True, null=True)
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated_at"), auto_now=True)

    def __str__(self):
        return f'{self.user} {_("friendship with")} {self.friend}'

    class Meta:
        verbose_name = _('friend')
        verbose_name_plural = _('friends')
        unique_together = ('user', 'friend', )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.is_accepted:
            try:
                counterparty = Friend.objects.get(
                    user=self.friend, 
                    friend=self.user
                )
            except Friend.DoesNotExist:
                counterparty = Friend.objects.create(
                    user=self.friend,
                    friend=self.user,
                    is_accepted=True,
                )
            else:
                if not counterparty.is_accepted:
                    counterparty.is_accepted = True
                    counterparty.is_blocked = False
                    counterparty.save()

    def delete(self, *args, **kwargs):
        user = self.friend
        friend = self.user
        print(self.user, self.friend)
        super().delete(*args, **kwargs)
        Friend.objects.filter(
            user=user, 
            friend=friend,
            is_blocked=False,
        ).delete()
