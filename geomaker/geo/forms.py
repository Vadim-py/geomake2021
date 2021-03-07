from django import forms
from django.forms import ModelForm
from .models import Article

class Form(ModelForm):
  x = forms.IntegerField()
  y = forms.IntegerField()
  class Meta:
    model = Article
    fields = ['file_obj']