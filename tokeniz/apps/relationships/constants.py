from __future__ import unicode_literals

CLIENT_STATUS_ACTIVE = 'active'
CLIENT_STATUS_INACTIVE = 'inactive'
CLIENT_STATUS_ARCHIVED = 'archived'
CLIENT_STATUS_DELETED = 'deleted'

CLIENT_STATUS_CHOICES = (
        (CLIENT_STATUS_ACTIVE, 'Active'),
        (CLIENT_STATUS_INACTIVE, 'Inactive'),
        (CLIENT_STATUS_ARCHIVED, 'Archived'),
        (CLIENT_STATUS_DELETED, 'Deleted'),
)
