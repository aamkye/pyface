import numpy as np
import collections
from src.object import object

class objectFactory:
    line=collections.namedtuple('Line', ['p0', 'p1', 'color'])
    pointArr=collections.namedtuple('PointArr', ['point', 'first_distance', 'second_distance'])

    def __init__(self,
            limit = 20,
            bounds = (900,700),
            mode = 0):
        self.limit = limit
        self.bounds = bounds
        self.mode = mode
        self.objects = list()
        self.modeOptions = [0.93, 0.74, 0.65]
        self.counter = collections.Counter('id')

    def create(self, **args) -> 'objectFactory':
        self.objects.append(object(id=self.counter['id'], **args))
        self.counter['id'] += 1

    def recalculateObjects(self) -> 'objectFactory':
        # Delete dead objects.
        def transform(x):
            x.aliveTime -= 1
            return x

        def filter_dead(x):
            return x.aliveTime > 1

        self.objects = [transform(o) for o in self.objects if filter_dead(o)]

        # Calculate new positions acording to speed and angle.
        for o in self.objects:
            o.calculateNewPos()

        # Remove unbound points (-1,-1) - (maxX, maxY)
        def filter_unbound(x):
            return x.point[0] > 0 and \
                x.point[1] > 0 and \
                x.point[0] < self.bounds[0] and \
                x.point[1] < self.bounds[1]

        self.objects = [o for o in self.objects if filter_unbound(o)]

        # Create new objects to limit.
        while len(self.objects) / self.limit <= self.modeOptions[self.mode]:
            self.create(
                point=np.array((
                    np.random.randint(0, self.bounds[0]),
                    np.random.randint(0, self.bounds[1])))
            )

    def getClosestToPoint(self, point, dist) -> list():
        return sorted(
            [n for n in self.objects if 0 < np.linalg.norm((n.point - point)) < dist],
            key = lambda p: np.linalg.norm((p.point - point))
        )

    # p0 - Point0 (x, y)
    # p1 - Point1 (x, y)
    # d0 - Distance between p0 nad p1
    def getColorByDistance(self, p0, p1, d0) -> int:
        return np.abs(np.ceil(255 - np.linalg.norm((p0 - p1)) / (d0 / 255)))

    def getWeb(self, point_array, maxClosePoints=16, maxFarPoints=3) -> list():
        lines=[]
        threads=[]
        for point_obj in point_array:
            for close_obj in self.getClosestToPoint(point_obj.point, point_obj.first_distance)[:maxClosePoints]:
                color = self.getColorByDistance(point_obj.point, close_obj.point, point_obj.first_distance)
                lines.append(self.line(p0=point_obj.point, p1=close_obj.point, color=color))
                for close_2nd_obj in self.getClosestToPoint(close_obj.point, point_obj.second_distance)[:maxFarPoints]:
                    lines.append(self.line(p0=close_obj.point, p1=close_2nd_obj.point, color=color))
        return sorted(lines, key=lambda x: x.color)
