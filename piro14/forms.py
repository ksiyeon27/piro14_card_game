
from django import forms
from .models import *


class GameForm(forms.ModelForm):
    class Meta:
        model = Game
        # fields='__all__'
        fields = ['creator','creator_card', 'opponent']
        

