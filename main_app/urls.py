from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('pokemon/', views.pokemon_index, name='pokemon_index'),
    path('pokemon/<int:pokemon_id>/', views.pokemons_detail, name='pokemons_detail'),
]