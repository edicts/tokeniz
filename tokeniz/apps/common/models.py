from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType

from common import constants as common_constants
from mixins import TimestampMixin
from common.country import COUNTRY_CHOICES


class BaseModel(models.Model):

    def __unicode__(self):
        raise NotImplementedError('The subclass must override this method.')

    class Meta:
        abstract = True


class PhoneNumber(TimestampMixin, BaseModel):
    DEFAULT_TYPE = 'work'

    phone_type = models.CharField(
        max_length=100, choices=common_constants.PHONE_NUMBER_TYPE_CHOICES,
        default=DEFAULT_TYPE, blank=True)
    number = models.CharField(max_length=100)
    extension = models.CharField(max_length=30, null=True, blank=True)

    def __unicode__(self):
        ext = self.extension
        if not ext:
            ext = ''
        return '{0}: {1} {2}'.format(
            self.phone_type,
            self.number,
            ext,
        )

    def update_from_dict(self, data):
        self.number = data.get('number', None)
        self.phone_type = data.get('phone_type', self.DEFAULT_TYPE)
        self.extension = data.get('extension', None)


class Address(TimestampMixin, BaseModel):
    is_primary = models.BooleanField(default=False)
    address1 = models.CharField(
        "Address", max_length=100, null=True, blank=True)
    address2 = models.CharField(
        "Address line 2", max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    subnational = models.CharField(
        "State/Province", max_length=100, null=True, blank=True)
    postal_code = models.CharField(max_length=15, null=True, blank=True)
    country = models.CharField(
        max_length=30, choices=COUNTRY_CHOICES,
        null=True, blank=True, default="US")

    def __unicode__(self):
        address2 = self.address2
        if not address2:
            address2 = ''
        return '{0} {1}, {2}, {3}, {4} {5}'.format(
            self.address1,
            address2,
            self.city,
            self.subnational,
            self.postal_code,
            self.country,
        )

    def update_from_dict(self, data, is_primary=False):
        self.is_primary = is_primary
        self.address1 = data.get('address1', None)
        self.address2 = data.get('address2', None)
        self.city = data.get('city', None)
        self.subnational = data.get('subnational', None)
        self.postal_code = data.get('postal_code', None)
        self.country = data.get('country', None)


class Note(TimestampMixin, BaseModel):
    auth_user = models.ForeignKey(User)
    django_content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField(blank=False, db_index=True)
    obj = generic.GenericForeignKey('django_content_type', 'object_id')
    body = models.TextField(max_length=255, blank=False)

    def __unicode__(self):
        return '{0} ({1}) - {2}'.format(
            self.auth_user.username,
            self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            self.body[0:16] + "...")

    @classmethod
    def add(cls, created_by, created_for, message):
        content_type = ContentType.objects.get_for_model(created_for)

        note = cls.objects.create(
            auth_user=created_by, body=message,
            django_content_type=content_type, object_id=created_for.id,
            obj=created_for,
        )
        return note
