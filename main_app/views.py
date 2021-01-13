from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template.defaulttags import register
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

from .models import Pokemon
from .forms import Pokemon_Form

import pokebase as pb
import requests
import json

from pokebase import cache
cache.API_CACHE

# Create your views here.

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

def home(request):
    return HttpResponse('Pokemon Test, working')

def about(request):
    return render(request, 'about.html')

# ==== Signup Route ====
def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('pokemon_index')
        else:
            error_message = 'Invalid sign up - try again'
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html')

@login_required
def pokemon_index(request):
    if request.method == 'POST':
        pokemon_form = Pokemon_Form(request.POST)
        if pokemon_form.is_valid():
            pokemon = pokemon_form.save(commit=False)
            pokemon.user = request.user
            pokemon.save()
            return redirect('pokemon_index')
    # charmander = pb.pokemon('charmander').url
    # print(charmander)
    # http://pokeapi.co/api/v1/pokemon/4/

    pokemons = Pokemon.objects.all()
    # filter to only users's pokemon instead of all in db
    # pokemons = Pokemon.object.filter(user=request.user) 
    pokemon_img = {}
    for pokemon in pokemons:
        base_url = 'http://pokeapi.co/api/v1/pokemon/'
        check_url = base_url + pokemon.name.lower()
        response = requests.get(check_url)
        # Checks if URL status is good to assign img url, if bad then default pokeball img url
        if response.status_code == 200:
            data = json.loads(response.text)
            print(data['name'])
            url = pb.pokemon(pokemon.name.lower()).sprites.other.dream_world.front_default
        else:
            print('An error occured querying the API')
            url = 'https://i.pinimg.com/originals/2b/46/73/2b4673e318ab94da17bbf9eaad5b80d6.png' # previously'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/items/poke-ball.png'
        pokemon_img[pokemon.name] = url

        


    pokemon_form = Pokemon_Form()
    context = {'pokemons': pokemons, 'pokemon_form': pokemon_form, 'pokemon_img': pokemon_img }
    return render(request, 'pokemon/index.html', context)

def pokemons_detail(request, pokemon_id):
    pokemon = Pokemon.objects.get(id=pokemon_id)
    # REVIEW: pokemon_img code here, create own def? as is used in both details and index?
    pokemon_img = {}
    base_url = 'http://pokeapi.co/api/v1/pokemon/'
    check_url = base_url + pokemon.name.lower()
    response = requests.get(check_url)
    # Checks if URL status is good to assign img url, if bad then default pokeball img url
    if response.status_code == 200:
        data = json.loads(response.text)
        print(data['name'])
        url = pb.pokemon(pokemon.name.lower()).sprites.other.dream_world.front_default
    else:
        print('An error occured querying the API')
        url = 'https://i.pinimg.com/originals/2b/46/73/2b4673e318ab94da17bbf9eaad5b80d6.png' # previously'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/items/poke-ball.png'
    pokemon_img[pokemon.name] = url
    context = {'pokemon': pokemon, 'pokemon_img': pokemon_img}
    return render(request, 'pokemon/detail.html', context)

def pokemon_edit(request, pokemon_id):
    pokemon = Pokemon.objects.get(id=pokemon_id)

    if request.method == 'POST':
        pokemon_form = Pokemon_Form(request.POST, instance=pokemon)
        if pokemon_form.is_valid:
            pokemon_form.save()
            return redirect('pokemons_detail', pokemon_id = pokemon.id)

    pokemon_form = Pokemon_Form(instance=pokemon)
    context = {'pokemon': pokemon, 'pokemon_form': pokemon_form}
    return render(request, 'pokemon/edit.html', context)

def pokemon_delete(request, pokemon_id):
    Pokemon.objects.get(id=pokemon_id).delete()
    return redirect('pokemon_index')