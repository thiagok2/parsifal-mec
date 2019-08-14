# coding: utf-8

from django import forms

from parsifal.reviews.models import Review

from django.utils.translation import ugettext as _

class ReviewSettingsForm(forms.ModelForm):
    name = forms.SlugField(
            widget=forms.TextInput(attrs={ 'class': 'form-control' }), 
            label='URL',
            help_text=_('Only letters, numbers, _or - are allowed.'),
            max_length=255)

    class Meta:
        model = Review
        fields = ['name',]
