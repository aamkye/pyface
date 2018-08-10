import pytest

from src.object import object
from src.objectFactory import objectFactory

def test_instance():
    obj = objectFactory()
    assert(isinstance(obj, objectFactory))

def test_assign():
    obj = objectFactory()
    assert(obj.data['limit'] == 20)
    assert(obj.data['bounds'] == (900,700))

@pytest.mark.parametrize(
    ('mode', 'limit','count'), [
        (0, 100, 94),
        (1, 100, 75),
        (2, 100, 66)
    ])
def test_recalculate_objects(mode, limit, count):
    obj = objectFactory(limit=limit, mode=mode)
    obj.recalculateObjects()
    assert(len(obj.objects) == count)

@pytest.mark.parametrize(
    ('x', 'y', 'min_x','min_y', 'limit'), [
        (250, 250, 250, 250, 10),
        (250, 250, 250, 250, 100),
        (250, 250, 250, 250, 1000),
        (250, 250, 250, 250, 10000)
    ])
def test_recalculate_distance(x, y, min_x, min_y, limit):
    obj = objectFactory(limit=limit)
    obj.create(x=min_x, y=min_y, speed=0)
    obj.recalculateObjects()
    test = obj.getSortedByDistance(x, y, 256)
    assert(test[0].data['x'] == min_x)
    assert(test[0].data['y'] == min_y)
