from __future__ import unicode_literals
import json

from django import http

from api import constants as api_constants

def json_response(request, success=True, **extra):
    mimetype = api_constants.JSON_MIMETYPE
    data = json.dumps(
        {'data': extra, 'success': success}, sort_keys=True, indent=2)

    # JSONP feature
    if request.GET.get('callback', None):
        mimetype = api_constants.JSONP_MIMETYPE
        data = '{0}({1})'.format(request.GET.get('callback'), data)
    return http.HttpResponse(data, mimetype=mimetype)

