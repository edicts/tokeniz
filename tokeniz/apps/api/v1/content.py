from __future__ import unicode_literals

from django.views.generic.base import View

from api import forms as api_forms
from api import utils as api_utils


class Client(View):
    def get(self, request, *args, **kwargs):
        form = api_forms.Client(request.GET)
        if form.is_valid():
            response = dict()
            return api_utils.json_response(
                request, success=True, response=response)
        else:
            return api_utils.json_response(
                request, success=False, errors=form.errors)


class CreditCard(View):
    def get(self, request, *args, **kwargs):
        form = api_forms.CreditCard(request.GET)
        if form.is_valid():
            response = dict()
            return api_utils.json_response(
                request, success=True, response=response)
        else:
            return api_utils.json_response(
                request, success=False, errors=form.errors)
