from __future__ import unicode_literals

from django.core import validators
from django.db import models
from django.contrib.contenttypes import generic


from common import models as common_models
from common.mixins import ArchiveMixin, TimestampMixin
from common import constants as common_constants
from relationships import constants as relationships_constants


class Client(TimestampMixin, ArchiveMixin, common_models.BaseModel):
    name = models.CharField(
        max_length=255, blank=False, db_index=True,
        verbose_name="Client Name")
    slug = models.SlugField(db_index=True)
    status = models.CharField(
        max_length=100, choices=relationships_constants.CLIENT_STATUS_CHOICES)
    twitter_handle = models.CharField(max_length=100, blank=True)
    notes = generic.GenericRelation(
        common_models.Note, content_type_field='django_content_type')

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return '{0}'.format(self.name)

    @property
    def is_active(self):
        return self.status == relationships_constants.CLIENT_STATUS_ACTIVE

    @property
    def aliases(self):
        return self.alias_set.all()


class ClientPhoneNumber(common_models.PhoneNumber):
    parent = models.OneToOneField(
        common_models.PhoneNumber, parent_link=True,
        related_name='clientphonenumber_ptr')
    client = models.ForeignKey(Client, related_name='phonenumber_set')

    @property
    def notes_create_for(self):
        return self.client


class ClientAddress(common_models.Address):
    parent = models.OneToOneField(
        common_models.Address, parent_link=True,
        related_name='clientaddress_ptr')
    client = models.ForeignKey(Client, related_name='address_set')

    @property
    def notes_create_for(self):
        return self.client


class ClientAlias(TimestampMixin, common_models.BaseModel):
    client = models.ForeignKey(Client, related_name='alias_set')
    alias = models.CharField(
        max_length=100, db_index=True, blank=False, null=False)

    @property
    def notes_create_for(self):
        return self.client

    def __unicode__(self):
        return self.alias


class ClientWebsite(TimestampMixin, common_models.BaseModel):
    client = models.ForeignKey(Client, related_name='website_set')
    title = models.CharField(max_length=255, blank=False, null=False)
    url = models.URLField(
        blank=False, null=False,
        validators=[validators.URLValidator])

    @property
    def notes_create_for(self):
        return self.client

    def __unicode__(self):
        return '{0}: {1}'.format(self.title, self.url)


class Contact(TimestampMixin, ArchiveMixin, common_models.BaseModel):
    client = models.ForeignKey('relationships.Client')
    user_profile = models.OneToOneField(
        'accounts.UserProfile', blank=True, null=True)
    firstname = models.CharField('First name', max_length=255, blank=False)
    lastname = models.CharField('Last name', max_length=255, blank=False)
    job_title = models.CharField(max_length=100, blank=True, null=True)
    twitter_handle = models.CharField(max_length=50, blank=True, null=True)
    notes = generic.GenericRelation(
        common_models.Note, content_type_field='django_content_type')

    class Meta:
        ordering = ['firstname']

    @property
    def name(self):
        return '{0} {1}'.format(self.firstname, self.lastname)

    @property
    def hours_available(self):
        return ContactHoursAvailable.objects.filter(contact=self)

    @property
    def emails(self):
        return self.email_set.all()

    @property
    def phone_numbers(self):
        return self.phonenumber_set.all()

    @property
    def notes_create_for(self):
        return self.client

    def __unicode__(self):
        return '{0} {1}'.format(self.firstname, self.lastname)


class ContactPhoneNumber(common_models.PhoneNumber):
    parent = models.OneToOneField(
        common_models.PhoneNumber, parent_link=True,
        related_name='contactphonenumber_ptr')
    contact = models.ForeignKey(Contact, related_name='phonenumber_set')

    def get_notes_message(self, mtype):
        return '{0} phone number for contact {1}'.format(
            mtype.capitalize(), self.contact)

    @property
    def notes_create_for(self):
        return self.contact


class ContactAddress(common_models.Address):
    parent = models.OneToOneField(
        common_models.Address, parent_link=True,
        related_name='contactaddress_ptr')
    contact = models.ForeignKey(Contact, related_name='address_set')

    def get_notes_message(self, mtype):
        return '{0} address for contact {1}'.format(
            mtype.capitalize(), self.contact)

    @property
    def notes_create_for(self):
        return self.contact


class ContactEmail(TimestampMixin, common_models.BaseModel):
    contact = models.ForeignKey(Contact, related_name='email_set')
    email = models.EmailField(max_length=100)
    is_primary = models.BooleanField(default=False)

    @property
    def client(self):
        return self.contact.client

    def get_notes_message(self, mtype):
        return '{0} email for contact: {1}'.format(
            mtype.capitalize(), self.contact)

    @property
    def notes_create_for(self):
        return self.client

    def __unicode__(self):
        return '{0} {1} <{2}>'.format(
            self.contact.firstname, self.contact.lastname, self.email)


class ContactHoursAvailable(TimestampMixin, common_models.BaseModel):
    contact = models.ForeignKey(Contact, related_name="hoursavailable_set")
    weekday = models.PositiveSmallIntegerField(
        choices=common_constants.DAYS_OF_WEEK_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __unicode__(self):
        return '{0}: {1} {2} available on {3} from {4} to {5}'.format(
            self.contact.client.name, self.contact.firstname,
            self.contact.lastname, self.get_weekday_display(),
            self.start_time, self.end_time)

    class Meta:
        ordering = ['weekday', 'start_time', 'end_time']
