from django import forms

from parsifal.reviews.models import Keyword

from django.utils.translation import ugettext as _
from django.utils.translation import ugettext_lazy as l_


class KeywordForm(forms.ModelForm):

    description = forms.CharField(
            widget=forms.TextInput(attrs={ 'class': 'form-control' }),
            max_length=200,
            required=True,
            label=_('Description')
        )
    related_to = forms.ChoiceField(
            widget=forms.Select(attrs={ 'class': 'form-control' }),
            choices=Keyword.RELATED_TO,
            required=False,
            label=_('Related to')
        )

    class Meta:
        model = Keyword
        fields = ['description', 'related_to', ]

class SynonymForm(forms.ModelForm):

    description = forms.CharField(
            widget=forms.TextInput(attrs={ 'class': 'form-control input-sm' }),
            max_length=200,
            required=True,
            label=_('Description')
        )

    class Meta:
        model = Keyword
        fields = ['description',]

