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
    ('point', 'minPoint', 'limit'), [
        (np.array((250, 250)), np.array((250, 251)), 10),
        (np.array((250, 250)), np.array((250, 251)), 100),
        (np.array((250, 250)), np.array((250, 251)), 1000),
        (np.array((250, 250)), np.array((250, 251)), 10000)
    ])
def test_recalculate_distance(point, minPoint, limit):
    obj = objectFactory(limit=limit)
    obj.create(point=point, speed=0, angle=0)
    obj.recalculateObjects()
    test = obj.getClosestToPoint(point=minPoint)
    np.testing.assert_array_equal(test[0].object.point, point)

@pytest.mark.parametrize(
    ('pointNum', 'maxConnectionsPerPoint', 'connectionDistance'), [
        (5, 20, 10240),
        (10, 20, 10240)
    ])
def test_get_web(pointNum, maxConnectionsPerPoint, connectionDistance):
    obj = objectFactory(
        limit=pointNum,
        maxConnectionsPerPoint=maxConnectionsPerPoint,
        connectionDistance=connectionDistance)
    obj.recalculateObjects()
    lines = obj.getWeb(
        [
            np.array((0,0)),
        ],
    )
    assert(len(lines) == pointNum)

@pytest.mark.parametrize(
    ('p0', 'p1', 'connectionDistance', 'color'), [
        (np.array((0, 0)), np.array((0, 10)), 10, 0),
        (np.array((0, 0)), np.array((0, 10)), 40, 192),
        (np.array((0, 0)), np.array((0, 10)), 100, 230),
        (np.array((0, 0)), np.array((0, 10)), 512, 251),
        (np.array((0, 0)), np.array((0, 255)), 256, 1),
        (np.array((0, 0)), np.array((0, 192)), 256, 64),
        (np.array((0, 0)), np.array((0, 64)), 256, 192),
        (np.array((0, 0)), np.array((0, 32)), 256, 224),
    ])
def test_color_range(p0, p1, connectionDistance, color):
    obj = objectFactory(connectionDistance=connectionDistance)
    assert(obj.getColorByDistance(obj.getDistance(p0, p1)) == color)
