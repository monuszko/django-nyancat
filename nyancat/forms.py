import re

from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import Video


class VideoForm(forms.Form):
    url = forms.URLField()

    def clean_url(self):
        '''Extract the v=blah part of the youtube video.'''
        data = self.cleaned_data['url']
        if not data.startswith('https://www.youtube.com/'):
            raise ValidationError(_('Invalid value'), code='notyoutube')

        data = re.search('[?&]v=([_a-zA-Z0-9-]+)', data)
        if not data:
            raise ValidationError(_('Invalid value'), code='novideo')

        return data.groups(1)[0]
