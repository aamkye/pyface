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
        (np.array((250, 250)), np.array((250, 251)), 10),
        (np.array((250, 250)), np.array((250, 251)), 100),
        (np.array((250, 250)), np.array((250, 251)), 1000),
        (np.array((250, 250)), np.array((250, 251)), 10000)
    ])
def test_recalculate_distance(point, min_point, limit):
    obj = objectFactory(limit=limit)
    obj.create(point=point, speed=0, angle=0)
    obj.recalculateObjects()
    test = obj.getClosestToPoint(point=min_point, dist=256)
    np.testing.assert_array_equal(test[0].point, point)

@pytest.mark.parametrize(
    ('point_num', 'lines_num', 'maxClosePoints', 'maxFarPoints', 'first_distance', 'second_distance'), [
        (5, 15, 20, 2, 10240, 10240),
        (10, 30, 20, 2, 10240, 10240)
    ])
def test_get_web(point_num, lines_num, maxClosePoints, maxFarPoints, first_distance, second_distance):
    obj = objectFactory(limit=point_num)
    obj.recalculateObjects()
    lines = obj.getWeb(
        [
            obj.pointArr(
                point=np.array((0,0)),
                first_distance=first_distance,
                second_distance=second_distance
            )
        ],
        maxClosePoints=maxClosePoints,
        maxFarPoints=maxFarPoints
    )
    assert(len(lines) == lines_num)

@pytest.mark.parametrize(
    ('p0', 'p1', 'first_distance', 'color'), [
        (np.array((0, 0)), np.array((0, 10)), 10, 0),
        (np.array((0, 0)), np.array((0, 10)), 40, 192),
        (np.array((0, 0)), np.array((0, 10)), 100, 230),
        (np.array((0, 0)), np.array((0, 10)), 512, 251),
        (np.array((0, 0)), np.array((0, 255)), 256, 1),
        (np.array((0, 0)), np.array((0, 192)), 256, 64),
        (np.array((0, 0)), np.array((0, 64)), 256, 192),
        (np.array((0, 0)), np.array((0, 32)), 256, 224),
    ])
def test_color_range(p0, p1, first_distance, color):
    obj = objectFactory()
    assert(obj.getColorByDistance(p0, p1, first_distance) == color)
