from django import forms

from django.utils.translation import ugettext as _
from django.utils.translation import ugettext_lazy as l_

from parsifal.reviews.models import Review, ArticleFile


class CreateReviewForm(forms.ModelForm):
    title = forms.CharField(
            widget=forms.TextInput(attrs={ 'class': 'form-control', 'placeholder': _('Systematic literature review\'s title') }, ),
            max_length=255, label=_('Title'))
    description = forms.CharField(
            widget=forms.Textarea(attrs={ 'class': 'form-control', 'placeholder': _('Give a brief description of your systematic literature review') }),
            max_length=500,
            help_text=_('Try to keep it short, max 500 characters :)'),
            required=False,
            label=_('Description'))

    class Meta:
        model = Review
        fields = ['title', 'description',]


class ReviewForm(forms.ModelForm):
    title = forms.CharField(
            widget=forms.TextInput(attrs={ 'class': 'form-control' }),
            max_length=255,
            label=_('Description'))
    description = forms.CharField(
            widget=forms.Textarea(attrs={ 'class': 'form-control expanding', 'rows': '4' }),
            max_length=500,
            required=False,
            label=_('Description'))

    class Meta:
        model = Review
        fields = ['title', 'description',]

class ArticleUploadForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ArticleUploadForm, self).__init__(*args, **kwargs)

        self.fields['article_file'].widget.attrs['class'] = 'form-control'

    class Meta:
        model = ArticleFile
        fields = ['article_file']
