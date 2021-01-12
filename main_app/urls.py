from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('pokemon/', views.pokemon_index, name='pokemon_index'),
    path('pokemon/<int:pokemon_id>/', views.pokemons_detail, name='pokemons_detail'),
    path('pokemon/<int:pokemon_id>/edit', views.pokemon_edit, name='pokemon_edit'),
    path('pokemon/<int:pokemon_id>/delete', views.pokemon_delete, name='pokemon_delete'),
]