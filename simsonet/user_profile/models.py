from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _
from PIL import Image


class UserProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='user_profile',
        verbose_name=_('user'),
    )
    picture = models.ImageField(_('picture'), upload_to='user_profile/pictures', null=True, blank=True)

    def __str__(self):
        return str(self.user)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.picture:
            picture = Image.open(self.picture.path)
            if picture.width > 300 or picture.height > 300:
                output_size = (300, 300)
                picture.thumbnail(output_size)
                picture.save(self.picture.path)
