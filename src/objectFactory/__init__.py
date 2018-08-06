from collections import Counter
from src.object import object

class objectFactory:
    data = {'limit':None, 'bounds':None}
    objects = list()
    counter = Counter('id')

    def __init__(self, limit=20, bounds=(900,700)):
        self.data = {'limit': limit, 'bounds': bounds}

    def create(self, x=None, y=None, size=None, speed=None, angle=None, aliveTime=None, color=None):
        obj = object(self.counter['id'], x, y, size, speed, angle, aliveTime, color)
        self.counter['id'] += 1
        self.objects.append(obj)
        print(obj)

    def recalculateObjects(self):
        # Delete dead objects
        def decrement(x):
            x.data['aliveTime'] -= 1
            return x

        self.objects = [decrement(o) for o in self.objects if o.data['aliveTime'] > 1]

        # temp = []
        # for o in self.objects:
        #     o.data['aliveTime'] -= 1
        #     if o.data['aliveTime'] > 0:
        #         temp.append(o)
        # self.objects = temp

        # Calculate new positions acording to speed and angle.








#
