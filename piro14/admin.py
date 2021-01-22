from django.contrib import admin
from piro14.models import *

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ['creator', 'opponent', 'winner', 'current_turn', 'created_at']

# Register your models here.
