from django.urls import path

from .views import add_todo, delete_todo, update_todo

urlpatterns = [
    path('add-todo/', add_todo, name='add_todo'),
    path('update/<int:pk>/', update_todo, name='update_todo'),
    path('delete/<int:pk>/', delete_todo, name='delete_todo')
]