from __future__ import unicode_literals

import copy
import json

from django.test import TestCase
from django.test.client import RequestFactory

from api import views
from leads import models as leads_models
from common import models as common_models
from contracts import models as contracts_models


class LeadCreateViewTest(TestCase):
    fixtures = ["test_relationships_data", "test_common_data",
        "test_location_data", "test_contracts_data", "test_products_data",
        "test_user_data", "test_session_data",
        "test_lead_data"]

    base_test_data = {
        'city': 'Salt Lake City', 'first_name': 'Testfirst',
        'last_name': 'TestLast', 'military_status': '',
        'country': 'US',
        'phone': '801-555-1212', 'state': 'UT',
        'postal_code': '84101', 'address1': '123 Test St.',
        'email': 'test@test.com'}

    def setUp(self):
        self.test_data = copy.copy(self.base_test_data)
        self.factory = RequestFactory()
        self.view = views.LeadCreateView()

    def tearDown(self):
        pass

    def _send_lead_post_request(self, data=base_test_data):
        req = self.factory.post('/api/v1/leads/submit', data)
        return self.view.post(req)

    def _lead_from_response(self, resp):
        json_data = json.loads(resp.content)
        return leads_models.Lead.objects.get(
            pk=int(json_data['data']['lead_id']))

    def test_response_is_json(self):
        resp = self._send_lead_post_request()
        json.loads(resp.content)

    def test_lead_without_offer_created(self):
        resp = self._send_lead_post_request()
        lead = self._lead_from_response(resp)
        self.assertIsInstance(lead, leads_models.Lead)
        self.assertIsNone(lead.offer)

    def test_lead_with_offer_created(self):
        self.test_data['offer_id'] = 1
        self.test_data['region'] = 'UT'
        self.test_data['high_school_grad_year'] = 1998
        resp = self._send_lead_post_request(self.test_data)
        lead = self._lead_from_response(resp)
        self.assertIsInstance(lead, leads_models.Lead)
        self.assertIsInstance(lead.offer, contracts_models.Offer)

    def test_missing_offer_fields(self):
        self.test_data['offer_id'] = 1
        # Expects 'region' and 'high_school_grad_year'
        resp = self._send_lead_post_request(self.test_data)
        parsed = json.loads(resp.content)
        error_fields = [e['field'] for e in parsed['data']['errors']]

        self.assertFalse(parsed['success'])
        self.assertIn('region', error_fields)
        self.assertIn('high_school_grad_year', error_fields)

    def test_lead_info_created(self):
        resp = self._send_lead_post_request()
        lead = self._lead_from_response(resp)
        self.assertIsInstance(lead.info, leads_models.Information)
        self.assertEquals(lead.info.first_name,
                self.base_test_data['first_name'])
        self.assertEquals(lead.info.last_name,
                self.base_test_data['last_name'])

    def test_phone_created(self):
        resp = self._send_lead_post_request()
        lead = self._lead_from_response(resp)
        self.assertIsInstance(lead.info.phone, common_models.PhoneNumber)

    def test_address_created(self):
        resp = self._send_lead_post_request()
        lead = self._lead_from_response(resp)
        self.assertIsInstance(lead.info.address, common_models.Address)

    def test_missing_info_returns_json_error(self):
        del self.test_data['first_name']
        resp = self._send_lead_post_request(self.test_data)
        parsed = json.loads(resp.content)
        self.assertFalse(parsed['success'])
        error_fields = [e['field'] for e in parsed['data']['errors']]
        self.assertIn('first_name', error_fields)
