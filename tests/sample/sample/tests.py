from sets import Set
from time import time, sleep
from collections import Counter
from django.utils import unittest
from sample.models import Foo, Bar
from parallelized_querysets import *


class TestCore(unittest.TestCase):

    def setUp(self):
        Foo(attribute1=4).save()
        Foo(attribute1=12).save()

    def tearDown(self):
        Foo.objects.all().delete()

    def test_data(self):
        for x in range(5):
            Foo(attribute1=x).save()

        def f(proc, row):
            if not proc.data.has_key('foo'):
                proc.data['foo'] = 0
            proc.data['foo'] += 1
            return proc.data['foo']

        expected = [1, 1, 1, 1, 2, 3, 4]
        self.assertEqual(Counter(expected),
                         Counter(parallelized_queryset(Foo.objects.all(),
                                                       function=f)))

    def test_hooks(self):
        for x in range(10):
            Foo(attribute1=x).save()

        def init(proc):
            proc.data['max'] = 0

        def end(proc):
            return proc.data['max']

        def f(proc, x):
            proc.data['max'] = max(proc.data['max'], x.attribute1)


        res = parallelized_queryset(Foo.objects.all(), function=f,
                                    init_hook=init, end_hook=end)

        self.assertEqual(Counter(res), Counter([9, 3, 12, 6]))


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
        res = parallelized_queryset(Foo.objects.all(), function=lambda p,x: None)
        self.assertEqual(len(res), 0)

    def test_apply_attr(self):
        for x in range(100):
            Foo(attribute1=x).save()
        self.assertEqual(Foo.objects.all().count(), 102)
        res = parallelized_queryset(Foo.objects.all(),
                                    function=lambda p,x: x.pk)
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
