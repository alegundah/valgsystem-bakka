from django import forms

from . import models

class LoginForm(forms.Form):
    username = forms.CharField(label="Tast inn utdelt kode", max_length=10, min_length=10)

