# -*- coding: utf-8 -*-
from wrapt import ObjectProxy
from itsawrap import wrap, unwrap
from test_app.models import Example, ExampleRelation
import pytest


class Wrapper(ObjectProxy):
    def is_wrapped_up(self):
        return True


class Wrapper2(ObjectProxy):
    def can_be_unwrapped(self):
        return True


@pytest.yield_fixture
def single_obj():
    obj = Example()
    obj.save()
    rel = ExampleRelation()
    rel.save()
    rel.fk.add(obj)
    try:
        yield rel
    finally:
        obj.delete()


@pytest.mark.django_db
def test_result_equality(single_obj):
    got = ExampleRelation.wrapping_queryset.wrap(Wrapper, Wrapper2)
    got_set = set(got)
    expected = ExampleRelation.normal_queryset.filter(pk=single_obj.pk)
    expected_set = set(expected)
    assert got_set == expected_set


@pytest.mark.django_db
def test_item_gets_wrapped(single_obj):
    got = ExampleRelation.wrapping_queryset.wrap(Wrapper).wrap(Wrapper2).get()
    assert got.pk == single_obj.pk
    assert got.is_wrapped_up() is True
    assert got.can_be_unwrapped() is True
    assert isinstance(got, ExampleRelation) is True
    assert isinstance(got, Wrapper2) is True


@pytest.mark.django_db
def test_item_gets_wrapped_and_then_unwrapped(single_obj):
    got = ExampleRelation.wrapping_queryset.wrap(Wrapper).wrap(Wrapper2).unwrap(Wrapper2, Wrapper).get()
    assert got.pk == single_obj.pk
    assert hasattr(got, 'is_wrapped_up') is False
    assert hasattr(got, 'can_be_unwrapped') is False
    assert isinstance(got, ExampleRelation) is True
    assert isinstance(got, Wrapper2) is False
    assert isinstance(got, Wrapper) is False


@pytest.mark.django_db
def test_cant_unwrap_none():
    with pytest.raises(ValueError):
        got = ExampleRelation.wrapping_queryset.wrap(Wrapper).unwrap(None)


@pytest.mark.django_db
def test_wrapping_resets(single_obj):
    qs1 = ExampleRelation.wrapping_queryset.wrap(Wrapper).all()
    qs2 = qs1.wrap(None)
    got = qs2.get()
    assert got.pk == single_obj.pk
    assert isinstance(got, ExampleRelation) is True
    assert isinstance(got, Wrapper) is False
    assert hasattr(got, 'is_wrapped_up') is False


@pytest.mark.django_db
def test_manual_wrapping(single_obj):
    got = ExampleRelation.wrapping_queryset.wrap(Wrapper).wrap(Wrapper2).get()
    me = wrap(single_obj, Wrapper, Wrapper2)
    assert got.pk == me.pk
    assert got.is_wrapped_up() is True
    assert got.can_be_unwrapped() is True
    assert me.is_wrapped_up() is True
    assert me.can_be_unwrapped() is True
    assert isinstance(got, ExampleRelation) is True
    assert isinstance(got, Wrapper2) is True
    assert isinstance(me, ExampleRelation) is True
    assert isinstance(me, Wrapper2) is True
    assert got == me


@pytest.mark.django_db
def test_manual_wrapping_and_unwrapping():
    got = wrap(Example(), Wrapper, Wrapper2)
    assert isinstance(got, Example) is True
    assert got.is_wrapped_up() is True
    assert got.can_be_unwrapped() is True
    got2 = unwrap(got)
    assert isinstance(got2, Example) is True
    assert hasattr(got2, 'is_wrapped_up') is False
    assert hasattr(got2, 'can_be_unwrapped') is False


@pytest.mark.django_db
def test_wrapping_relations(single_obj):
    got = ExampleRelation.wrapping_queryset.wrap(Wrapper).get()
    assert got.is_wrapped_up() is True
    assert hasattr(got, 'can_be_unwrapped') is False
    other_wrapped = got.fk.wrap(Wrapper2).get()
    assert other_wrapped.can_be_unwrapped() is True
    assert hasattr(other_wrapped, 'is_wrapped_up') is False


@pytest.mark.django_db
def test_wrapping_relations_prefetch(single_obj):
    got = ExampleRelation.wrapping_queryset.wrap(Wrapper).prefetch_related('fk').get()
    assert got.is_wrapped_up() is True
    assert hasattr(got, 'can_be_unwrapped') is False
    other_wrapped = got.fk.wrap(Wrapper2).get()
    assert other_wrapped.can_be_unwrapped() is True
    assert hasattr(other_wrapped, 'is_wrapped_up') is False
