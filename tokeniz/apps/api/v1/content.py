from __future__ import unicode_literals

from django.views.generic.base import View

from api.v1 import forms as api_forms
from common import utils as common_utils


class Client(View):
    def get(self, request, *args, **kwargs):
        form = api_forms.Client(request.GET)
        if form.is_valid():
            response = dict()
            return common_utils.json_response(
                request, success=True, response=response)
        else:
            return common_utils.json_response(
                request, success=False, errors=form.errors)


class CreditCard(View):
    def get(self, request, *args, **kwargs):
        form = api_forms.CreditCard(request.GET)
        if form.is_valid():
            response = dict()
            return common_utils.json_response(
                request, success=True, response=response)
        else:
            return common_utils.json_response(
                request, success=False, errors=form.errors)
