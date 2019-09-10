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
    
    entry_type = forms.ChoiceField(widget=forms.Select(attrs={ 'class': 'form-control form-type generic', 'style': 'width: 100%;' }), choices=(Document.ENTRY_TYPES), label= _('Entry type'))
    bibtexkey = forms.CharField(label=_('BibTeX key'), widget=forms.TextInput(attrs={ 'class': 'form-control', 'style': 'width: 20%;' }), max_length=50, required=False)
    title = forms.CharField(widget=forms.Textarea(attrs={ 'class': 'form-control article article-r book book-r booklet booklet-r inbook inbook-r incollection incollection-r inproceedings inproceedings-r manual manual-r mastersthesis mastersthesis-r misc phdthesis phdthesis-r proceedings proceedings-r techreport techreport-r unpublished unpublished-r', 'rows': '1' }), max_length=255, required=False, label= _('title'))
    author = forms.CharField(widget=forms.Textarea(attrs={ 'class': 'form-control article article-r book book-r booklet inbook inbook-r incollection incollection-r inproceedings inproceedings-r manual mastersthesis mastersthesis-r misc phdthesis phdthesis-r unpublished  unpublished-r', 'rows': '1' }), max_length=500, required=False, label= _('author'))
    
    year = forms.CharField(widget=forms.TextInput(attrs={ 'class': 'form-control article article-r book book-r booklet inbook inbook-r incollection incollection-r inproceedings inproceedings-r manual mastersthesis mastersthesis-r misc phdthesis phdthesis-r proceedings proceedings-r techreport techreport-r unpublished', 'style': 'width: 20%;' }), max_length=10, required=False, label= _('year'), help_text='Required')
    month = forms.CharField(widget=forms.TextInput(attrs={ 'class': 'form-control article book booklet inbook incollection inproceedings manual mastersthesis misc phdthesis proceedings techreport unpublished', 'style': 'width: 20%;' }), max_length=30, required=False, label= _('month'))

    booktitle = forms.CharField(label=_('Book title'), widget=forms.TextInput(attrs={ 'class': 'form-control incollection incollection-r inproceedings inproceedings-r' }), max_length=255, required=False)
    editor = forms.CharField(widget=forms.TextInput(attrs={ 'class': 'form-control book book-r inbook inbook-r incollection inproceedings proceedings' }), max_length=255, required=False, label= _('editor'))
    howpublished = forms.CharField(label=_('How it was published'), widget=forms.TextInput(attrs={ 'class': 'form-control booklet misc' }), max_length=255, required=False)
    journal = forms.CharField(widget=forms.TextInput(attrs={ 'class': 'form-control article article-r' }), max_length=255, required=False, label= _('journal'))
    url = forms.CharField(label='URL', widget=forms.URLInput(attrs={ 'class': 'form-control' }), max_length=255, required=False)
    publisher = forms.CharField(widget=forms.TextInput(attrs={ 'class': 'form-control article book book-r inbook inbook-r incollection incollection-r inproceedings proceedings' }), max_length=255, required=False, label= _('publisher'))
    pages = forms.CharField(widget=forms.TextInput(attrs={ 'class': 'form-control inbook inbook-r incollection inproceedings', 'style': 'width: 20%;' }), max_length=255, required=False, label= _('pages'))
    number = forms.CharField(widget=forms.TextInput(attrs={ 'class': 'form-control article book inbook incollection inproceedings proceedings', 'style': 'width: 20%;' }), max_length=255, required=False, label= _('number'))
    volume = forms.CharField(widget=forms.TextInput(attrs={ 'class': 'form-control article book incollection inproceedings proceedings', 'style': 'width: 20%;' }), max_length=255, required=False, label= _('volume'))
    edition = forms.CharField(widget=forms.TextInput(attrs={ 'class': 'form-control book inbook inbook incollection manual', 'style': 'width: 20%;' }), max_length=255, required=False, label= _('edition'))
    chapter = forms.CharField(widget=forms.TextInput(attrs={ 'class': 'form-control inbook inbook-r incollection', 'style': 'width: 20%;' }), max_length=255, required=False, label= _('chapter'))

    address = forms.CharField(widget=forms.TextInput(attrs={ 'class': 'form-control book booklet inbook incollection inproceedings manual mastersthesis phdthesis proceedings' }), max_length=255, required=False, label= _('address'))  
    crossref = forms.CharField(label=_('Cross-reference'), widget=forms.TextInput(attrs={ 'class': 'form-control' }), max_length=255, required=False)
    institution = forms.CharField(widget=forms.TextInput(attrs={ 'class': 'form-control techreport techreport-r' }), max_length=255, required=False, label= _('institution'))
    organization = forms.CharField(widget=forms.TextInput(attrs={ 'class': 'form-control inproceedings manual proceedings' }), max_length=255, required=False, label= _('organization'))
    school = forms.CharField(widget=forms.TextInput(attrs={ 'class': 'form-control mastersthesis mastersthesis-r phdthesis phdthesis-r' }), max_length=255, required=False, label= _('school'))
    series = forms.CharField(widget=forms.TextInput(attrs={ 'class': 'form-control book inbook incollection inproceedings proceedings' }), max_length=255, required=False, label= _('series'))
    
    abstract = forms.CharField(widget=forms.Textarea(attrs={ 'class': 'form-control article generic', 'rows': '3' }), max_length=4000, required=False, label= _('abstract'), help_text=_('Max. 4000 characters'))
    keywords = forms.CharField(widget=forms.Textarea(attrs={ 'class': 'form-control article generic', 'rows': '1' }), max_length=500, required=False, label= _('keywords'))    
    
    language = forms.CharField(widget=forms.TextInput(attrs={ 'class': 'form-control generic' }), max_length=255, required=False, label= _('language'))
    coden = forms.CharField(widget=forms.TextInput(attrs={ 'class': 'form-control generic', 'style': 'width: 20%;' }), max_length=255, required=False, label= _('coden'))
    doi = forms.CharField(label='DOI', widget=forms.TextInput(attrs={ 'class': 'form-control generic', 'style': 'width: 20%;' }), max_length=50, required=False)
    isbn = forms.CharField(label='ISBN', widget=forms.TextInput(attrs={ 'class': 'form-control generic', 'style': 'width: 20%;' }), max_length=30, required=False)
    issn = forms.CharField(label='ISSN', widget=forms.TextInput(attrs={ 'class': 'form-control generic', 'style': 'width: 20%;' }), max_length=30, required=False)

    note = forms.CharField(widget=forms.TextInput(attrs={ 'class': 'form-control' }), max_length=255, required=False, label= _('note'))

    class Meta:
        model = Document
        fields = ['entry_type','bibtexkey', 'title', 'author', 'abstract', 'keywords', 'year', 'month', 'booktitle', 
                'editor', 'howpublished', 'journal', 'url', 'publisher', 'pages', 'number', 'volume', 
                'edition', 'chapter', 'address', 'crossref', 'institution', 'organization', 'school', 
                'series', 'language', 'coden', 'doi', 'isbn', 'issn', 'note']
