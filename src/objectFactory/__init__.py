import random
from math import sqrt
from collections import Counter
from src.object import object


class objectFactory:
    """objectFactory is patterned object factory for centralized management of
    objects"""

    data = {'limit':None, 'bounds':None, 'mode': 0}
    modeOptions = [0.93, 0.74, 0.65]
    objects = list()
    counter = Counter('id')

    def __init__(self, limit=20, bounds=(900,700), mode=0):
        """Default constructor"""
        self.data = {'limit': limit, 'bounds': bounds, 'mode': mode}

    def create(self, **args) -> 'objectFactory':
        """Creates object by passing all args to default constructor of
        object"""
        obj = object(id=self.counter['id'], **args)
        self.counter['id'] += 1
        self.objects.append(obj)

    def recalculateObjects(self) -> 'objectFactory':
        """Recalculates objects in self.objects by its aliveTime, bound
        position and creates new objects if limit not reached"""
        # Delete dead objects.
        def transform(x):
            x.data['aliveTime'] -= 1
            return x

        def filter_dead(x):
            return x.data['aliveTime'] > 1

        self.objects = [transform(o) for o in self.objects if filter_dead(o)]

        # Calculate new positions acording to speed and angle.
        for o in self.objects:
            o.calculateNewPos()

        # Remove unbound points (-1,-1) - (maxX, maxY)
        def filter_unbound(x):
            return x.data['x'] > 0 and \
                x.data['y'] > 0 and \
                x.data['x'] < self.data['bounds'][0] and \
                x.data['y'] < self.data['bounds'][1]

        self.objects = [o for o in self.objects if filter_unbound(o)]

        # Create new objects to limit.
        while len(
            self.objects) / self.data['limit'] <= \
            self.modeOptions[self.data['mode']
        ]:
            self.create(
                x=random.randrange(0, self.data['bounds'][0]),
                y=random.randrange(0, self.data['bounds'][1])
            )

    def getSortedByDistance(self, x, y, dist) -> list():
        """Returns sorted by distance to point list"""
        return sorted(
            [n for n in self.objects if sqrt((n.data['x'] - x)**2 + (n.data['y'] - y)**2) < dist],
            key = lambda p: sqrt((p.data['x'] - x)**2 + (p.data['y'] - y)**2)
        )





#
