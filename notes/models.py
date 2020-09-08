from django.db import models
from django.template.defaultfilters import slugify
from datetime import datetime
import random

class Note(models.Model):

    title = models.TextField(max_length=500)
    summary = models.TextField(max_length=5000)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

class Paragraph(models.Model):
    description = models.TextField(max_length=500, null=True, blank=True)
    content = models.TextField(max_length=2000)
    note = models.ForeignKey(Note, on_delete=models.CASCADE, related_name='paragraphs')
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)
