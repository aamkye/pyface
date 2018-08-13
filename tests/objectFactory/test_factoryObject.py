import pytest
import numpy as np

from src.object import object
from src.objectFactory import objectFactory

def test_instance():
    obj = objectFactory()
    assert(isinstance(obj, objectFactory))

def test_assign():
    obj = objectFactory()
    assert(obj.limit == 20)
    assert(obj.bounds == (900,700))

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
    ('point', 'min_point', 'limit'), [
        (np.array((250, 250)), np.array((251, 251)), 10),
        (np.array((250, 250)), np.array((251, 251)), 100),
        (np.array((250, 250)), np.array((251, 251)), 1000),
        (np.array((250, 250)), np.array((251, 251)), 10000)
    ])
def test_recalculate_distance(point, min_point, limit):
    obj = objectFactory(limit=limit)
    obj.create(point=point, speed=0, angle=0)
    obj.recalculateObjects()
    test = obj.getClosestToPoint(point=min_point, dist=256)
    print(test[0])
    np.testing.assert_array_equal(test[0].point, point)

def test_get_web():
    maxClosePoints=3
    obj = objectFactory()
    obj.create(point=np.array((40,40)), speed=0)
    obj.create(point=np.array((60,60)), speed=0)
    obj.create(point=np.array((80,80)), speed=0)
    lines = obj.getWeb(
        [
            obj.pointArr(
                point=np.array((0,0)),
                first_distance=256,
                second_distance=96
            )
        ],
        maxClosePoints=maxClosePoints,
        maxFarPoints=1
    )
    assert(len(lines) == 2*maxClosePoints)
