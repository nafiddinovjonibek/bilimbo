from django import template

from home.tts import speech_url

register = template.Library()
register.filter('savol_ovozi', speech_url)
