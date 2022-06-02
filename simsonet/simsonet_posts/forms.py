from django import forms
from tinymce.widgets import TinyMCE
from . import models


class PostForm(forms.ModelForm):
    class Meta:
        model = models.Post
        fields = ('content', 'owner', 'wall', 'reply_to', 'repost_of', )
        widgets = {
            'content': TinyMCE(),
            'owner': forms.HiddenInput(),
            'wall': forms.HiddenInput(),
            'reply_to': forms.HiddenInput(),
            'repost_of': forms.HiddenInput(),
        }
