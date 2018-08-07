import random
from collections import Counter
from src.object import object


class objectFactory:
    data = {'limit':None, 'bounds':None, 'mode': 0}
    modeOptions = [0.93, 0.74, 0.65]
    objects = list()
    counter = Counter('id')

    def __init__(self, limit=20, bounds=(900,700), mode=0):
        self.data = {'limit': limit, 'bounds': bounds, 'mode': mode}

    def create(self, **args):
        obj = object(id=self.counter['id'], **args)
        self.counter['id'] += 1
        self.objects.append(obj)

    def recalculateObjects(self):
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
        while len(self.objects) / self.data['limit'] <= self.modeOptions[self.data['mode']]:
            self.create(
                x=random.randrange(0, self.data['bounds'][0]),
                y=random.randrange(0, self.data['bounds'][1]))






#
