from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from bootstrap_modal_forms.mixins import PopRequestMixin, CreateUpdateAjaxMixin
from bootstrap_modal_forms.forms import BSModalForm

from .models import Shop


class BookForm(BSModalForm):
    #publication_date = forms.DateField(
    #    error_messages={'invalid': 'Enter a valid date in YYYY-MM-DD format.'}
    #)
    
    class Meta:
        model = Shop
        exclude = ['timestamp']


class CustomUserCreationForm(PopRequestMixin, CreateUpdateAjaxMixin,
                             UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']


class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']


class SetPathForm(PopRequestMixin, CreateUpdateAjaxMixin,
                             UserCreationForm):
    class Meta:
        #model = Shop
        #fields = ['path']
        #exclude = ['timestamp']
        model = User
        fields = ['username', 'password1', 'password2']
        

