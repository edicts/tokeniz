from __future__ import unicode_literals

from django import forms

from common import models as common_models


class AddressForm(forms.ModelForm):
    class Meta:
        model = common_models.Address
        exclude = ('is_primary',)


class PhoneNumberForm(forms.ModelForm):
    class Meta:
        model = common_models.PhoneNumber


class NoteForm(forms.ModelForm):
    class Meta:
        model = common_models.Note
        fields = (
            'django_content_type',
            'object_id',
            'body',
            'auth_user',
        )


class AuthForm(forms.Form):
    username = forms.CharField(required=True, max_length=255)
    password = forms.CharField(max_length=16, widget=forms.PasswordInput)
