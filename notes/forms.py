from django import forms
from .models import Note, Paragraph

class NoteForm(forms.ModelForm):
    title = forms.CharField(max_length=100)
    class Meta:
        model = Note
        fields = ('title', 'summary',)

class ParagraphForm(forms.ModelForm):
    description = forms.CharField(max_length=100)
    class Meta:
        model = Paragraph
        fields = ('description', 'content',)
