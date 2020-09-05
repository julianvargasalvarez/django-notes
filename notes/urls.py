from django.urls import path

from .views import notes

urlpatterns = [
    path('', notes.NotesListView.as_view(), name='index'),
    path('create/', notes.NoteCreateView.as_view(), name='create'),
    path('<int:pk>/update', notes.NoteUpdateView.as_view(), name='update'),

]
