import random
import math

class object:
    data = {
        'id':None,
        'x':None,
        'y':None,
        'speed':None,
        'angle':None,
        'aliveTime':None,
        'color':None
    }

    def __init__(self, id, x=900, y=700, size=random.randrange(1, 10), speed=None, angle=None, aliveTime=None, color=None):
        self.data = {'id':id, 'x':x, 'y':y, 'size':size, 'speed':speed, 'angle':angle, 'aliveTime':aliveTime, 'color':color}

    def calculateNewPos(self):
        old_x, old_y = self.data['x'], self.data['y']
        angle = float(self.data['angle'])
        # Compute the change in position
        delta_y = self.data['speed'] * math.cos(math.radians(angle))
        delta_x = self.data['speed'] * math.sin(math.radians(angle))
        # Add that to the existing position
        self.data['x'] = round(old_x + delta_x)
        self.data['y'] = round(old_y + delta_y)

    def getPos(self):
        print("%0.2f, %0.2f" % self.data['x'], self.data['y'])
