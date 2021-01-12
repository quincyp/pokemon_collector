from django.shortcuts import render, redirect
from django.http import HttpResponse

from .models import Pokemon

# Create your views here.
def home(request):
    return HttpResponse('Pokemon Test, working')

def about(request):
    return render(request, 'about.html')

def pokemon_index(request):
    pokemons = Pokemon.objects.all()
    context = {'pokemons': pokemons}
    return render(request, 'pokemon/index.html', context)

def pokemons_detail(request, pokemon_id):
    pokemon = Pokemon.objects.get(id=pokemon_id)
    context = {'pokemon': pokemon}
    return render(request, 'pokemon/detail.html', context)