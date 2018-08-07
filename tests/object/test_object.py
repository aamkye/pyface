import pytest
from src.object import object

def test_instance():
    obj = object(0)
    assert(isinstance(obj, object))

def test_assign():
    obj = object(0)
    assert(obj.data['id'] == 0)
    assert(obj.data['x'] == 0)
    assert(obj.data['y'] == 0)
    assert(obj.data['size'] != None and 1 <= obj.data['size'] <= 10)
    assert(obj.data['speed'] != None and 1 <= obj.data['speed'] <= 100)
    assert(obj.data['angle'] != None and 0 <= obj.data['angle'] <= 359)
    assert(obj.data['aliveTime'] != None and 10 <= obj.data['aliveTime'] <= 750)

@pytest.mark.parametrize(
    ('x','y','new_x','new_y','angle','speed', 'retry'), [
        (100, 100,  100,  100,  90,  10, 0),
        (100, 100,  107,  107,  45,  10, 1),
        (  0,   0,  -20,  -20, 225,  14, 2),
        (-10, -10, -100, -100, 225,  14, 9),
        (  0, 100,    0, -400, 180, 100, 5)
    ])
def test_compute_position(x, y, new_x, new_y, angle, speed, retry):
    obj = object(0, x, y, None, speed, angle, 200)
    for a in range(0, retry):
        obj.calculateNewPos()
    assert(obj.data['x'] == new_x)
    assert(obj.data['y'] == new_y)
