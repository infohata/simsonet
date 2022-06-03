from django import forms
from tinymce.widgets import TinyMCE
from . import models


class FriendRequestCreateForm(forms.ModelForm):
    class Meta:
        model = models.Friend
        fields = ('friend', 'request_message', )
        widgets = {
            'friend': forms.HiddenInput(),
            'request_message': TinyMCE(),
        }
