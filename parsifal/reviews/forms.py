# coding: utf-8
from django import forms

from django.utils.translation import ugettext as _
from django.utils.translation import ugettext_lazy as l_

from parsifal.reviews.models import Review, ArticleFile


class CreateReviewForm(forms.ModelForm):
    title = forms.CharField(
            widget=forms.TextInput(attrs={ 'class': 'form-control', 'placeholder': l_('Systematic literature review\'s title') }, ),
            max_length=255, label=l_('Title'))
    description = forms.CharField(
            widget=forms.Textarea(attrs={ 'class': 'form-control', 'placeholder': l_('Give a brief description of your systematic literature review') }),
            max_length=500,
            help_text=l_('Try to keep it short, max 500 characters'),
            required=False,
            label=l_('Description'))

    class Meta:
        model = Review
        fields = ['title', 'description',]


class ReviewForm(forms.ModelForm):
    title = forms.CharField(
            widget=forms.TextInput(attrs={ 'class': 'form-control' }),
            max_length=255,
            label=l_('Title'))
    description = forms.CharField(
            widget=forms.Textarea(attrs={ 'class': 'form-control expanding', 'rows': '4' }),
            max_length=500,
            required=False,
            label=l_('Description'))

    class Meta:
        model = Review
        fields = ['title', 'description',]

class ArticleUploadForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ArticleUploadForm, self).__init__(*args, **kwargs)

        self.fields['article_file'].widget.attrs['class'] = 'form-control'

    def clean(self):
        cleaned_data = self.cleaned_data
        if not self.instance.id and not cleaned_data.has_key('article_file'):
            self._errors["article_file"] = self.error_class([_('This field is required.')])
        else:
            filename = cleaned_data['article_file'].name.lower()
            fileext  = filename[filename.rfind('.'):] if '.' in filename else None

            if not fileext or fileext not in ('.pdf'):
                self._errors["article_file"] = self.error_class([_('File extension not allowed, use only .pdf')])
                del self.cleaned_data["article_file"]

        return cleaned_data

    class Meta:
        model = ArticleFile
        fields = ['article_file']
