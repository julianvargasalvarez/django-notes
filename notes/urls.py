from django.urls import path

from .views import notes

urlpatterns = [
    path('', notes.NotesListView.as_view(), name='index'),
    path('create/', notes.create, name='create'),
    path('new/', notes.new, name='new'),
    path('<int:note_id>/edit', notes.edit, name='edit_note'),
    path('<int:note_id>', notes.show, name='show'),
    path('<int:note_id>/update/', notes.update, name='update'), #put

]
