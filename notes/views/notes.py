from django.db import transaction
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import inlineformset_factory
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from django.views.decorators.http import require_POST, require_GET, require_http_methods
from django.views.generic import ListView, CreateView, UpdateView, DetailView

from notes.forms import NoteForm, ParagraphForm
from notes.models import Note, Paragraph
from notes.serializers import NoteSerializer

import time

class NotesListView(LoginRequiredMixin, ListView):
    template_name = 'index.html'
    model = Note
    context_object_name = 'note'

    def get_context_data(self, *args, **kwargs):
        context = super(NotesListView, self).get_context_data(*args, **kwargs)
        context['count'] = 0
        context['notes'] = self.get_queryset()
        return context


class NoteCreateView(LoginRequiredMixin, CreateView):
    model = Note
    template_name = 'new.html'
    form_class = NoteForm

    def get_success_url(self):
        return reverse_lazy('update', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        ParagraphFormSet = inlineformset_factory(Note, Paragraph, fields=('description', 'content',), extra=3, can_delete=False)
        data = super(NoteCreateView, self).get_context_data(**kwargs)
        if self.request.POST:
            data['paragraphs_form_set'] = ParagraphFormSet(self.request.POST)
        else:
            data['paragraphs_form_set'] = ParagraphFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        paragraphs = context['paragraphs_form_set']

        with transaction.atomic():
            self.object = form.save()

            if paragraphs.is_valid():
                paragraphs.instance = self.object
                paragraphs.save()
                messages.add_message(self.request, messages.INFO, "Nota guardada")

        return super(NoteCreateView, self).form_valid(form)

class NoteUpdateView(LoginRequiredMixin, UpdateView):
    model = Note
    form_class = NoteForm
    template_name = 'update.html'

    def get_context_data(self, **kwargs):
        ParagraphFormSet = inlineformset_factory(Note, Paragraph, fields=('description', 'content',), extra=3, can_delete=False)
        data = super(NoteUpdateView, self).get_context_data(**kwargs)
        if self.request.POST:
            data['paragraphs_form_set'] = ParagraphFormSet(self.request.POST, instance=self.object)
        else:
            data['paragraphs_form_set'] = ParagraphFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        paragraphs = context['paragraphs_form_set']

        with transaction.atomic():
            self.object = form.save()
            if paragraphs.is_valid():
                paragraphs.instance = self.object
                paragraphs.save()
                messages.add_message(self.request, messages.INFO, "Nota guardada")

        return super(NoteUpdateView, self).form_valid(form)

    def get_success_url(self):
        self.success_url = reverse_lazy('update', kwargs={'pk': self.object.pk})
        return self.success_url

class NoteDetailView(DetailView):
    model = Note
    template_name = 'show.html'
    slug_url_kwarg = 'slug'
    slug_field = 'slug'
    context_object_name = 'note'
