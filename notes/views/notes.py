from django.views.generic.base import TemplateView
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.forms import inlineformset_factory
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.http import require_POST, require_GET, require_http_methods
from django.views.generic import ListView

from notes.forms import NoteForm, ParagraphForm
from notes.models import Note, Paragraph
from notes.serializers import NoteSerializer


import time

class NotesListView(ListView):
    template_name = 'index.html'
    model = Note
    context_object_name = 'note'

    def get_context_data(self, *args, **kwargs):
        context = super(NotesListView, self).get_context_data(*args, **kwargs)
        context['count'] = 0
        context['notes'] = self.get_queryset()
        return context


def create(request):
    note = NoteForm(request.POST)
    if note.is_valid():
        note.save()

        ParagraphFormSet = inlineformset_factory(Note, Paragraph, fields=('description', 'content',),)
        paragraphs_form_set = ParagraphFormSet(request.POST, instance=note.instance)
        if paragraphs_form_set.is_valid():
            paragraphs_form_set.save()
            messages.add_message(request, messages.INFO, "Nota guardada")
        else:
            print(paragraphs_form_set.errors)
        return redirect(reverse('edit_note', args=[note.instance.id]))
    else:
        return render(request, 'new.html', context={'note':note})

def new(request):
    time.sleep(2)
    note_form = NoteForm()
    ParagraphFormSet = inlineformset_factory(Note, Paragraph, fields=('description', 'content',),  extra=3, can_delete=False)
    paragraphs_form_set = ParagraphFormSet()
    return render(request, 'new.html',
        context={'note_form':note_form,
            'paragraphs_form_set':paragraphs_form_set,
            'url': '/notes/create/',
            'verb':'post'})

def edit(request, note_id):
    note_form = NoteForm(instance=Note.objects.get(pk=note_id))
    ParagraphFormSet = inlineformset_factory(Note, Paragraph, form=ParagraphForm, fields=('description', 'content',),  extra=3, can_delete=False)
    paragraphs_form_set = ParagraphFormSet(instance=note_form.instance)
    return render(request, 'edit.html',
        context={'note_form':note_form,
            'paragraphs_form_set':paragraphs_form_set,
            'url':'/notes/'+str(note_id)+'/update/', 'verb':'post'})

@require_GET
def show(request, note_id):
    return HttpResponse(note_id)

def update(request, note_id):
    note_form = NoteForm(request.POST, instance=Note.objects.get(pk=note_id))
    if note_form.is_valid():
        note_form.save()
        return redirect('index')
    else:
        return render(request, 'edit.html', context={'note_form':note_form, 'url':'/notes/'+str(note_id)+'/update/', 'verb':'post'})

