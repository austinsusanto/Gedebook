from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from main.models import Product


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ["name", "amount", "description"]

class GedebookUserCreationForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super(GedebookUserCreationForm, self).__init__(*args, **kwargs)

        field_names = ["username", "password1", "password2"]
        for field_name in field_names:
            self.fields[field_name].help_text = None
