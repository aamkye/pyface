import pytest
from src.object import object

# class Object(unittest.TestCase):
def test_instance():
    obj = object(0)
    assert(isinstance(obj, object))

def test_assign():
    obj = object(0)
    assert(obj.data['id'] == 0)
    assert(obj.data['x'] == 900)
    assert(obj.data['y'] == 700)
    assert(1 <= obj.data['size'] <= 10)
    assert(obj.data['speed'] == None)
    assert(obj.data['angle'] == None)
    assert(obj.data['angle'] == None)

@pytest.mark.parametrize(
    ('x','y','new_x','new_y','angle','speed'), [
        (100, 100, 110, 100,  90,  10),
        (100, 100, 107, 107,  45,  10),
        (  0,   0, -10, -10, 225,  14),
        (-10, -10, -20, -20, 225,  14),
        (  0, 100,   0,   0, 180, 100)
    ])
def test_compute_position(x, y, new_x, new_y, angle, speed):
    obj = object(0, x, y, None, speed, angle, 200, None)
    obj.calculateNewPos()
    assert(obj.data['x'] == new_x)
    assert(obj.data['y'] == new_y)
