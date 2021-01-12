from django.forms import ModelForm
from .models import Pokemon

class Pokemon_Form(ModelForm):
    class Meta:
        model = Pokemon
        fields = ['name', 'level', 'type', 'description']