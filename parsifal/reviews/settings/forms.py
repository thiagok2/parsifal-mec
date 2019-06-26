# coding: utf-8

from django import forms

from parsifal.reviews.models import Review


class ReviewSettingsForm(forms.ModelForm):
    name = forms.SlugField(
            widget=forms.TextInput(attrs={ 'class': 'form-control' }), 
            label='URL',
            help_text='Apenas letras, números, _ou - são permitidos.',
            max_length=255)

    class Meta:
        model = Review
        fields = ['name',]
