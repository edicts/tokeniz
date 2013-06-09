from __future__ import unicode_literals

from django import forms

from relationships import models as relationships_models
from common import models as common_models
from common import forms as common_forms


class MassAddCreditCards(common_forms.AuthForm, forms.Form):
    number = forms.CharField(required=True, max_length=20)
    address = forms.ModelChoiceField(
        queryset=common_models.Address.objects, required=True)
    uid = forms.CharField(required=False, max_length=255)
    username = forms.CharField(required=True, max_length=255)
    password = forms.CharField(max_length=16, widget=forms.PasswordInput)


class Client(common_forms.AuthForm, forms.Form):
    id = forms.ModelChoiceField(
        queryset=relationships_models.Client.objects, required=True)
    username = forms.CharField(required=True, max_length=255)
    password = forms.CharField(max_length=16, widget=forms.PasswordInput)


class CreditCard(common_forms.AuthForm, forms.Form):
    token = forms.CharField(required=True, max_length=255)
    username = forms.CharField(required=True, max_length=255)
    password = forms.CharField(max_length=16, widget=forms.PasswordInput)
