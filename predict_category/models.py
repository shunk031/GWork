from django.db import models
from django import forms
# Create your models here.


class InputURLForm(forms.Form):

    article_url = forms.CharField()
