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
def test_recalculate(mode, limit, count):
    obj = objectFactory(limit=limit, mode=mode)
    obj.recalculateObjects()
    assert(len(obj.objects) == count)
