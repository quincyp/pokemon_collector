from django.shortcuts import render, redirect
from django.http import HttpResponse

from .models import Pokemon
from .forms import Pokemon_Form

# Create your views here.
def home(request):
    return HttpResponse('Pokemon Test, working')

def about(request):
    return render(request, 'about.html')

def pokemon_index(request):
    if request.method == 'POST':
        pokemon_form = Pokemon_Form(request.POST)
        if pokemon_form.is_valid():
            pokemon_form.save()
            return redirect('pokemon_index')

    pokemons = Pokemon.objects.all()
    pokemon_form = Pokemon_Form()
    context = {'pokemons': pokemons, 'pokemon_form': pokemon_form}
    return render(request, 'pokemon/index.html', context)

def pokemons_detail(request, pokemon_id):
    pokemon = Pokemon.objects.get(id=pokemon_id)
    context = {'pokemon': pokemon}
    return render(request, 'pokemon/detail.html', context)