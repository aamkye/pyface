import numpy as np
from src.counterDecorator import *

class object:
    @calls.count
    def __init__(self,
            id,
            point = np.array((0,0)),
            speed = None,
            angle = None,
            aliveTime = None,
            color = None):
        self.id = id
        self.point = point
        self.speed = speed if speed is not None else np.random.randint(1, 2)
        self.angle = angle if angle is not None else np.random.randint(0, 359)
        self.aliveTime = aliveTime if aliveTime is not None else np.random.randint(100, 800)
        self.color = color if color is not None else np.random.randint(128, 254)
        self.trajectory = None
        self.conected = False

    @calls.count
    def getTrajectory(self):
        angle = float(self.angle)
        delta_y = self.speed * np.cos(np.radians(angle))
        delta_x = self.speed * np.sin(np.radians(angle))
        self.trajectory = np.array((delta_x, delta_y))

    @calls.count
    def calculateNewPos(self) -> 'object':
        if(self.trajectory is None):
            self.getTrajectory()
        self.point[0] = np.round(self.point[0] + self.trajectory[0])
        self.point[1] = np.round(self.point[1] + self.trajectory[1])

        return self
