from __future__ import unicode_literals

from django.db import models


class ArchiveManager(models.Manager):
    def get_query_set(self):
        return super(ArchiveManager, self).get_query_set().filter(
            deleted_at__isnull=True)

    def deleted(self):
        return super(ArchiveManager, self).get_query_set()
