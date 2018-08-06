import pytest
import unittest

from src.object import object
from src.objectFactory import objectFactory

class testObjectFactory(unittest.TestCase):
    def test_instance(self):
        obj = objectFactory()
        assert(isinstance(obj, objectFactory))

    def test_assign(self):
        obj = objectFactory()
        assert(obj.data['limit'] == 20)
        assert(obj.data['bounds'] == (900,700))

    def test_recalculate_single(self):
        obj = objectFactory()
        obj.create(aliveTime=4)
        for a in range(4):
            obj.recalculateObjects()
        assert(len(obj.objects) == 0)

    def test_recalculate_many(self):
        obj = objectFactory()
        obj.create(aliveTime=4)
        obj.create(aliveTime=3)
        obj.create(aliveTime=2)
        for a in range(3):
            obj.recalculateObjects()
        assert(len(obj.objects) == 1)
