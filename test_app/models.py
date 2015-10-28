# -*- coding: utf-8 -*-
from django.db.models import Model, QuerySet, ManyToManyField
from django.utils.encoding import force_text
from itsawrap import WrappingQuerySet, WrappingManager


class Example(Model):
    wrapping_manager = WrappingManager()
    wrapping_queryset = WrappingQuerySet.as_manager()
    normal_queryset = QuerySet.as_manager()

    def __str__(self):
        return force_text(getattr(self, 'pk', None))

    class Meta:
        ordering = ('-pk',)


class ExampleRelation(Model):
    fk = ManyToManyField('test_app.Example', null=True)

    wrapping_manager = WrappingManager()
    wrapping_queryset = WrappingQuerySet.as_manager()
    normal_queryset = QuerySet.as_manager()

    def __str__(self):
        return force_text(getattr(self, 'pk', None))

    class Meta:
        ordering = ('-pk',)
