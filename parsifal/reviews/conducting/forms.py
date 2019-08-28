# coding: utf-8

from django import forms
from django.contrib.auth.models import User

from parsifal.library.models import SharedFolder, Folder, Document

from django.utils.translation import ugettext as _
from django.utils.translation import ugettext_lazy as l_


class FolderForm(forms.ModelForm):
    name = forms.CharField(
            widget=forms.TextInput(attrs={ 'class': 'form-control input-sm', 'autocomplete': 'off' }), 
            max_length=50, 
            required=True
        )
    user = forms.ModelChoiceField(widget=forms.HiddenInput(), queryset=User.objects.all(), required=True)

    class Meta:
        model = Folder
        fields = ['name', 'user',]

    def clean(self):
        cleaned_data = super(FolderForm, self).clean()
        name = cleaned_data.get('name')
        user = cleaned_data.get('user')
        if Folder.objects.filter(name=name, user=user).exists():
            self.add_error('name', 'Folder with this name already exists.')


class SharedFolderForm(forms.ModelForm):
    class Meta:
        model = SharedFolder
        fields = ['name',]

class DocumentForm(forms.ModelForm):
    
    entry_type = forms.ChoiceField(widget=forms.Select(attrs={ 'class': 'form-control', 'style': 'width: 100%;' }), choices=Document.ENTRY_TYPES, label= _('Entry type'))
    bibtexkey = forms.CharField(label=_('BibTeX key'), widget=forms.TextInput(attrs={ 'class': 'form-control', 'style': 'width: 20%;' }), max_length=50, required=False)
    title = forms.CharField(widget=forms.Textarea(attrs={ 'class': 'form-control', 'rows': '1' }), max_length=255, required=False, label= _('title'))
    author = forms.CharField(widget=forms.Textarea(attrs={ 'class': 'form-control', 'rows': '1' }), max_length=500, required=False, label= _('author'))
    abstract = forms.CharField(widget=forms.Textarea(attrs={ 'class': 'form-control', 'rows': '3' }), max_length=4000, required=False, label= _('abstract'), help_text=_('Max. 4000 characters'))
    keywords = forms.CharField(widget=forms.Textarea(attrs={ 'class': 'form-control', 'rows': '1' }), max_length=500, required=False, label= _('keywords'))    
    year = forms.CharField(widget=forms.TextInput(attrs={ 'class': 'form-control', 'style': 'width: 20%;' }), max_length=10, required=False, label= _('year'))
    month = forms.CharField(widget=forms.TextInput(attrs={ 'class': 'form-control', 'style': 'width: 20%;' }), max_length=30, required=False, label= _('month'))

    booktitle = forms.CharField(label=_('Book title'), widget=forms.TextInput(attrs={ 'class': 'form-control' }), max_length=255, required=False)
    editor = forms.CharField(widget=forms.TextInput(attrs={ 'class': 'form-control' }), max_length=255, required=False, label= _('editor'))
    howpublished = forms.CharField(label=_('How it was published'), widget=forms.TextInput(attrs={ 'class': 'form-control' }), max_length=255, required=False)
    journal = forms.CharField(widget=forms.TextInput(attrs={ 'class': 'form-control' }), max_length=255, required=False, label= _('journal'))
    url = forms.CharField(label='URL', widget=forms.URLInput(attrs={ 'class': 'form-control' }), max_length=255, required=False)
    publisher = forms.CharField(widget=forms.TextInput(attrs={ 'class': 'form-control' }), max_length=255, required=False, label= _('publisher'))
    pages = forms.CharField(widget=forms.TextInput(attrs={ 'class': 'form-control', 'style': 'width: 20%;' }), max_length=255, required=False, label= _('pages'))
    number = forms.CharField(widget=forms.TextInput(attrs={ 'class': 'form-control', 'style': 'width: 20%;' }), max_length=255, required=False, label= _('number'))
    volume = forms.CharField(widget=forms.TextInput(attrs={ 'class': 'form-control', 'style': 'width: 20%;' }), max_length=255, required=False, label= _('volume'))
    edition = forms.CharField(widget=forms.TextInput(attrs={ 'class': 'form-control', 'style': 'width: 20%;' }), max_length=255, required=False, label= _('edition'))
    chapter = forms.CharField(widget=forms.TextInput(attrs={ 'class': 'form-control', 'style': 'width: 20%;' }), max_length=255, required=False, label= _('chapter'))

    address = forms.CharField(widget=forms.TextInput(attrs={ 'class': 'form-control' }), max_length=255, required=False, label= _('address'))  
    crossref = forms.CharField(label=_('Cross-reference'), widget=forms.TextInput(attrs={ 'class': 'form-control' }), max_length=255, required=False)
    institution = forms.CharField(widget=forms.TextInput(attrs={ 'class': 'form-control' }), max_length=255, required=False, label= _('institution'))
    organization = forms.CharField(widget=forms.TextInput(attrs={ 'class': 'form-control' }), max_length=255, required=False, label= _('organization'))
    school = forms.CharField(widget=forms.TextInput(attrs={ 'class': 'form-control' }), max_length=255, required=False, label= _('school'))
    series = forms.CharField(widget=forms.TextInput(attrs={ 'class': 'form-control' }), max_length=255, required=False, label= _('series'))
    language = forms.CharField(widget=forms.TextInput(attrs={ 'class': 'form-control' }), max_length=255, required=False, label= _('language'))

    coden = forms.CharField(widget=forms.TextInput(attrs={ 'class': 'form-control', 'style': 'width: 20%;' }), max_length=255, required=False, label= _('coden'))
    doi = forms.CharField(label='DOI', widget=forms.TextInput(attrs={ 'class': 'form-control', 'style': 'width: 20%;' }), max_length=50, required=False)
    isbn = forms.CharField(label='ISBN', widget=forms.TextInput(attrs={ 'class': 'form-control', 'style': 'width: 20%;' }), max_length=30, required=False)
    issn = forms.CharField(label='ISSN', widget=forms.TextInput(attrs={ 'class': 'form-control', 'style': 'width: 20%;' }), max_length=30, required=False)

    note = forms.CharField(widget=forms.TextInput(attrs={ 'class': 'form-control' }), max_length=255, required=False, label= _('note'))

    class Meta:
        model = Document
        fields = ['entry_type','bibtexkey', 'title', 'author', 'abstract', 'keywords', 'year', 'month', 'booktitle', 
                'editor', 'howpublished', 'journal', 'url', 'publisher', 'pages', 'number', 'volume', 
                'edition', 'chapter', 'address', 'crossref', 'institution', 'organization', 'school', 
                'series', 'language', 'coden', 'doi', 'isbn', 'issn', 'note']
