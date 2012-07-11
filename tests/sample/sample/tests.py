from sets import Set
from time import time
from django.utils import unittest
from sample.models import Foo, Bar
from parallelized_querysets import *


class TestCore(unittest.TestCase):

    def setUp(self):
        Foo(attribute1=4).save()
        Foo(attribute1=12).save()

    def tearDown(self):
        Foo.objects.all().delete()

    def test_transparency(self):
        self.assertEqual(Foo.objects.count(), 2)
        self.assertEqual(len(parallelized_queryset(Foo.objects.all())), 2)

    def test_filter(self):
        self.assertEqual(len(parallelized_queryset(Foo.objects.filter(attribute1=12))), 1)
        self.assertEqual(len(parallelized_queryset(Foo.objects.filter(attribute1=2))),  0)

    def test_high_number_processes(self):
        res = parallelized_queryset(Foo.objects.filter(attribute1=12), processes=20)
        self.assertEqual(len(res), 1)

    def test_apply_none(self):
        for x in range(100):
            Foo(attribute1=x).save()
        res = parallelized_queryset(Foo.objects.all(), function=lambda x: None)
        self.assertEqual(len(res), 0)

    def test_apply_attr(self):
        for x in range(100):
            Foo(attribute1=x).save()
        self.assertEqual(Foo.objects.all().count(), 102)
        res = parallelized_queryset(Foo.objects.all(),
                                    function=lambda x: x.pk)
        self.assertEqual(len(res), 102)
        self.assertEqual(len(Set(res)), 102)

    def test_multiple_querysets_same_object(self):
        querysets = [
            Foo.objects.filter(attribute1=4),
            Foo.objects.filter(attribute1=12),
        ]
        self.assertEqual(len(parallelized_multiple_querysets(querysets)), 2)

        querysets = [
            Foo.objects.filter(attribute1=4),
            Foo.objects.filter(attribute1=0),
        ]
        self.assertEqual(len(parallelized_multiple_querysets(querysets)), 1)

    def test_multiple_querysets_differnt_objects(self):
        Bar(attribute2=3).save()

        querysets = [
            Foo.objects.filter(attribute1=4),
            Bar.objects.filter(attribute2=3),
        ]
        self.assertEqual(len(parallelized_multiple_querysets(querysets)), 2)

        querysets = [
            Foo.objects.filter(attribute1=0),
            Bar.objects.filter(attribute2=3),
        ]
        self.assertEqual(len(parallelized_multiple_querysets(querysets)), 1)
