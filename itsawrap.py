# -*- coding: utf-8 -*-
import logging
from django.db.models import QuerySet, Manager


logger = logging.getLogger(__name__)
__all__ = ['wrap', 'WrappingQuerySet', 'WrappingManager']


def wrap(to_be_wrapped, *wrappers):
    for wrapper in wrappers:
        to_be_wrapped = wrapper(to_be_wrapped)
    return to_be_wrapped


def unwrap(wrapped):
    while hasattr(wrapped, '__wrapped__'):
        wrapped = wrapped.__wrapped__
    return wrapped


class WrappingQuerySet(QuerySet):
    def __init__(self, *args, **kwargs):
        super(WrappingQuerySet, self).__init__(*args, **kwargs)
        self._wrappers = ()

    def _clone(self, **kwargs):
        clone = super(WrappingQuerySet, self)._clone(**kwargs)
        clone._wrappers = self._wrappers
        return clone

    def wrap(self, *wrappers):
        clone = self._clone()
        if wrappers == (None,):
            clone._wrappers = ()
        else:
            clone._wrappers = clone._wrappers + wrappers
        return clone

    def unwrap(self, *wrappers):
        if wrappers == (None,):
            raise ValueError("Can't unwrap using `None` as an argument")
        wrapper_count = len(self._wrappers)
        wrappers_to_change = list(self._wrappers)
        for wrapper in wrappers:
            assert wrapper in wrappers_to_change, \
                "Expected to find %(wrap)r in existing %(count)d wrappers" % {
                    'wrap': wrapper, 'count': wrapper_count,
                }
            wrappers_to_change.remove(wrapper)
        assert len(wrappers_to_change) != wrapper_count, \
            "Nothing was removed from %(count)d the wrappers" % {
                'count': wrapper_count,
            }
        clone = self._clone()
        clone._wrappers = tuple(wrappers_to_change)
        return clone

    def iterator(self):
        iterable = super(WrappingQuerySet, self).iterator()
        for item in iterable:
            if self._wrappers:
                yield wrap(item, *self._wrappers)
            else:
                yield item


class WrappingManager(Manager):
    _queryset_class = WrappingQuerySet

    def get_queryset(self):
        kws = {'model': self.model, 'using': self._db}
        if hasattr(self, '_hints'):  # pragma: no cover
            kws.update(hints=self._hints)
        return self._queryset_class(**kws)

    get_query_set = get_queryset

    def wrap(self, *wrappers):
        return self.get_queryset().wrap(*wrappers)
