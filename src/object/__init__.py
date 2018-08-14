import numpy as np

class object:
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

    def calculateNewPos(self) -> 'object':
        # Gatger old data
        old_x = self.point[0]
        old_y = self.point[1]

        angle = float(self.angle)
        # Compute the change in position
        delta_y = self.speed * np.cos(np.radians(angle))
        delta_x = self.speed * np.sin(np.radians(angle))
        # Add that to the existing position
        self.point[0] = np.round(old_x + delta_x)
        self.point[1] = np.round(old_y + delta_y)

        return self
