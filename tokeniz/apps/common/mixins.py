from __future__ import unicode_literals
import datetime

from django.db import models

from common import managers as common_managers


class DirtyFieldsMixin(object):
    def __init__(self, *args, **kwargs):
        super(DirtyFieldsMixin, self).__init__(*args, **kwargs)
        self._reset_state()

    def _reset_state(self, *args, **kwargs):
        self._original_state = self._as_dict()

    def _as_dict(self):
        return dict([(f.name, getattr(self, f.name)) for f in
                     self._meta.local_fields if not f.rel])

    def get_dirty_fields(self):
        new_state = self._as_dict()
        return dict([(key, value) for key, value in
                     self._original_state.iteritems()
                     if value != new_state[key]])

    def is_dirty(self):
        if not self.pk:
            return True
        return {} != self.get_dirty_fields()


class ArchiveMixin(models.Model):
    deleted_at = models.DateTimeField(null=True, blank=True)
    objects = common_managers.ArchiveManager()
    all_objects = models.Manager()

    class Meta:
        abstract = True

    def delete(self, using=None):
        from django.db import router
        from django.db.models import signals
        using = using or router.db_for_write(self.__class__, instance=self)

        assert self._get_pk_val() is not None, \
            '{0} object\'s pk {1} is set to None.'.format(
                self._meta.object_name, self._meta.pk.attname)

        if not self.deleted_at:
            signals.pre_delete.send(
                sender=self.__class__, instance=self, using=using)

            self.deleted_at = datetime.datetime.now()
            self.save(using=using)

            signals.post_delete.send(
                sender=self.__class__, instance=self, using=using)

    def really_delete(self, using=None):
        super(ArchiveMixin, self).delete(using=using)


class TimestampMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
