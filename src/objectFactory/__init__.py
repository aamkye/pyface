import numpy as np
import collections
from src.counterDecorator import *
from src.object import object

class objectFactory:
    line=collections.namedtuple('Line', ['p0', 'p1', 'color'])
    newPoint=collections.namedtuple('Point', ['object', 'distance'])

    # Setters
    def setObjects(self, x: list):
        self.objects = x
        return self

    def setCounter(self, x: collections.Counter):
        self.counter = x
        return self

    def setLimit(self, x: int):
        self.limit = x
        return self

    def setBounds(self, x: np.array):
        self.bounds = x
        return self

    def setMaxConnectionsPerPoint(self, x: int):
        self.maxConnectionsPerPoint = x
        return self

    def setConnectionDistance(self, x: int):
        self.connectionDistance = x
        return self

    @calls.count
    def __init__(self,
            limit = 20,
            bounds = (900, 700),
            maxConnectionsPerPoint = 10,
            connectionDistance = 256):
        self.setObjects(list())
        self.setCounter(collections.Counter('id'))
        self.setLimit(limit)
        self.setBounds(bounds)
        self.setMaxConnectionsPerPoint(maxConnectionsPerPoint)
        self.setConnectionDistance(connectionDistance)

    @calls.count
    def create(self, **args) -> 'objectFactory':
        self.objects.append(object(id=self.counter['id'], **args))
        self.counter['id'] += 1
        return self

    @calls.count
    def recalculateObjects(self) -> 'objectFactory':
        # Delete dead objects.
        def transform(x):
            x.aliveTime -= 1
            return x

        def filter_dead(x):
            return x.aliveTime > 1

        self.setObjects([transform(o) for o in self.objects if filter_dead(o)])

        # Calculate new positions acording to speed and angle.
        for o in self.objects:
            o.calculateNewPos()

        # Remove unbound points (-1,-1) - (maxX, maxY)
        def filterUnbound(x):
            return x.point[0] > 0 and x.point[1] > 0 and \
                x.point[0] < self.bounds[0] and x.point[1] < self.bounds[1]

        self.setObjects([o for o in self.objects if filterUnbound(o)])

        # Create new objects to limit.
        while len(self.objects) < self.limit:
            self.create(
                point=np.array((
                    np.random.randint(0, self.bounds[0]),
                    np.random.randint(0, self.bounds[1]))))

        return self

    @calls.count
    def getDistance(self, p0:np.array, p1: np.array) -> int:
        return np.linalg.norm((p0 - p1))

    @calls.count
    def getClosestToPoint(self, point: np.array) -> list():
        objList = list()
        def filter(x):
            return x.point[0] < point[0] - self.connectionDistance or \
                x.point[0] > point[0] + self.connectionDistance or \
                x.point[1] < point[1] - self.connectionDistance or \
                x.point[1] > point[1] + self.connectionDistance

        for obj in [x for x in self.objects if not filter(x)]:
            objList.append(self.newPoint(obj, self.getDistance(obj.point, point)))

        return sorted(
            [n for n in objList if 0 < n.distance < self.connectionDistance],
            key = lambda p: p.distance)

    @calls.count
    def getColorByDistance(self, d0: int) -> int:
        return np.abs(np.ceil(255 - d0 / (self.connectionDistance / 255)))

    @calls.count
    def getWeb(self, point_array: [np.array]) -> list():
        lines = []

        for point_obj in point_array:
            for close_obj in self.getClosestToPoint(point_obj)[:self.maxConnectionsPerPoint]:
                color = self.getColorByDistance(close_obj.distance)
                lines.append(self.line(p0=point_obj, p1=close_obj.object.point, color=color))

                # for close_2nd_obj in self.getClosestToPoint(close_obj.object.point, point_obj.second_distance)[:self.maxFarPoints]:
                #     color_2nd = self.getColorByDistance(close_2nd_obj.distance, point_obj.second_distance)
                #     lines.append(self.line(p0=close_obj.object.point, p1=close_2nd_obj.object.point, color=color_2nd))

        return sorted(lines, key=lambda x: x.color)
