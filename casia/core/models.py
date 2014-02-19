# -*- coding: utf-8 -*-

# This file is part of Casia - CAS server based on Django
# Copyright (C) 2013 Mateusz Małek

# Casia is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# You should have received a copy of the GNU Affero General Public License
# along with Casia. If not, see <http://www.gnu.org/licenses/>.

from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models.manager import EmptyManager
from django.utils import six
from django.utils.translation import ugettext_lazy as _

from casia.core.managers import ServicePermissionManager


def _service_get_all_permissions(user, obj):
    permissions = set()
    return permissions


def _service_has_perm(self, perm, obj=None):
    return False


def _service_has_module_perms(user, app_label):
    return False


class ServicePermissionsMixin(models.Model):
    is_trusted = models.BooleanField()
    service_permissions = models.ManyToManyField('ServicePermission',
        verbose_name=_('service permissions'), blank=True,
        help_text=_('Specific permissions for this service.'),
        related_name="service_set", related_query_name="service")

    class Meta:
        abstract = True

    def get_all_permissions(self, obj=None):
        return _service_get_all_permissions(self, obj)

    def has_perm(self, perm, obj=None):
        if self.is_active and self.is_trusted:
            return True

        return _service_has_perm(self, perm, obj)

    def has_perms(self, perm_list, obj=None):
        for perm in perm_list:
            if not self.has_perm(perm, obj):
                return False
        return True

    def has_module_perms(self, app_label):
        if self.is_active and self.is_superuser:
            return True

        return _service_has_module_perms(self, app_label)


class ServicePermission(models.Model):
    name = models.CharField(_('name'), max_length=50)
    content_type = models.ForeignKey(ContentType)
    codename = models.CharField(_('codename'), max_length=100)
    objects = ServicePermissionManager()

    class Meta:
        verbose_name = _('service permission')
        verbose_name_plural = _('service permissions')
        unique_together = (('content_type', 'codename'),)
        ordering = ('content_type__app_label', 'content_type__model',
                    'codename')

    def __str__(self):
        return "%s | %s | %s" % (
            six.text_type(self.content_type.app_label),
            six.text_type(self.content_type),
            six.text_type(self.name))

    def natural_key(self):
        return (self.codename,) + self.content_type.natural_key()
    natural_key.dependencies = ['contenttypes.contenttype']


class Service(ServicePermissionsMixin):
    name = models.CharField(max_length=255)
    description = models.TextField()
    is_active = models.BooleanField()

    def __unicode__(self):
        return self.name

    def is_unknown(self):
        return False

    def is_authenticated(self):
        return True


class UnknownService(object):
    id = None
    pk = None
    name = ''
    is_active = False
    is_trusted = False
    _service_permissions = EmptyManager(ServicePermission)

    def __init__(self):
        pass

    def __str__(self):
        return 'UnknownService'

    def __eq__(self, other):
        return isinstance(other, self.__class__)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return 1  # instances always return the same hash value

    def save(self):
        raise NotImplementedError

    def delete(self):
        raise NotImplementedError

    def _get_service_permissions(self):
        return self._service_permissions
    service_permissions = property(_get_service_permissions)

    def get_all_permissions(self, obj=None):
        return _service_get_all_permissions(self, obj=obj)

    def has_perm(self, perm, obj=None):
        return _service_has_perm(self, perm, obj=obj)

    def has_perms(self, perm_list, obj=None):
        for perm in perm_list:
            if not self.has_perm(perm, obj):
                return False
        return True

    def has_module_perms(self, module):
        return _service_has_module_perms(self, module)

    def is_unknown(self):
        return True

    def is_authenticated(self):
        return False