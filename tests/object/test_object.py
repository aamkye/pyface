import pytest
import numpy as np

from src.object import object

def test_instance():
    obj = object(0)
    assert(isinstance(obj, object))

def test_assign():
    obj = object(0)
    assert(obj.id == 0)
    np.testing.assert_array_equal(obj.point, np.array((0,0)))
    assert(obj.size != None and 1 <= obj.size <= 10)
    assert(obj.speed != None and 1 <= obj.speed <= 100)
    assert(obj.angle != None and 0 <= obj.angle <= 359)
    assert(obj.aliveTime != None and 100 <= obj.aliveTime <= 800)

@pytest.mark.parametrize(
    ('point','new_point','angle','speed', 'retry'), [
        (np.array((100, 100)), np.array(( 100,  100)),  90,  10, 0),
        (np.array((100, 100)), np.array(( 107,  107)),  45,  10, 1),
        (np.array((  0,   0)), np.array(( -20,  -20)), 225,  14, 2),
        (np.array((-10, -10)), np.array((-100, -100)), 225,  14, 9),
        (np.array((  0, 100)), np.array((   0, -400)), 180, 100, 5)
    ])
def test_compute_position(point, new_point, angle, speed, retry):
    obj = object(id=0, point=point, speed=speed, angle=angle, aliveTime=10)
    for a in range(0, retry):
        obj.calculateNewPos()
    np.testing.assert_array_equal(obj.point, new_point)
