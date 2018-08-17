import pygame
import threading
import time
import numpy as np
from src.counterDecorator import *
from decimal import Decimal

from src.object import object
from src.objectFactory import objectFactory

pygame.init()
pygame.display.set_caption("Le Dot")


screenSize = (700, 500)
screen = pygame.display.set_mode(screenSize, pygame.RESIZABLE)
screen.set_alpha(None)
# pygame.mouse.set_cursor((8,8),(0,0),(0,0,0,0,0,0,0,0),(0,0,0,0,0,0,0,0))
clock = pygame.time.Clock()
__break = False

pygame.event.set_allowed([pygame.QUIT, pygame.VIDEORESIZE, pygame.MOUSEMOTION, pygame.KEYDOWN])
objFactory = objectFactory(limit=128, bounds=screenSize, maxConnectionsPerPoint=10, connectionDistance=256)
mousePos=(0, 0)
run = False
myfont = pygame.font.SysFont("Ubuntu Mono", 14)
framerate = 25
lines = list()
start = 0
end = 0
diff = 0
delay = 0

while not __break:
    start = time.time()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # print("User asked to quit.")
            __break=True
            pygame.display.quit()
            quit()
        elif event.type == pygame.VIDEORESIZE:
            screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE | pygame.DOUBLEBUF)
            objFactory.bounds = (event.w, event.h)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                run ^= True
            elif event.key == pygame.K_q:
                objFactory.objects = list()
            elif event.key == pygame.K_a:
                objFactory.limit += 16
            elif event.key == pygame.K_z:
                if objFactory.limit <= 32:
                    objFactory.limit = 32
                else:
                    objFactory.limit -= 16
        #     print("User pressed a key.")
        # elif event.type == pygame.KEYUP:
        #     print("User let go of a key.")
        # elif event.type == pygame.MOUSEMOTION:
        #     # print("%d %d" % event.pos)
        #     mousePos = event.pos
        # elif event.type == pygame.MOUSEBUTTONDOWN:
        #     print("User pressed a mouse button")

    if run:
        screen.fill((0, 0, 0))
        objFactory.recalculateObjects()
        width = np.ceil(objFactory.bounds[0]/2)
        height = np.ceil(objFactory.bounds[1]/2)

        points=[
            # np.array(((width/4)*3, (height/2)*1)) # DOT 1
            # np.array(((width/4)*5, (height/2)*1)) # DOT 2
            # np.array(((width/4)*3, (height/2)*3)) # DOT 3
            # np.array(((width/4)*5, (height/2)*3)) # DOT 4
            # np.array(((width/2)*1, height))       # MIDDLE DOT 1
            # np.array(((width/2)*3, height))       # MIDDLE DOT 2
            # np.array((2,           2))            # CORNER DOT 1
            # np.array((2*width-2,   2))            # CORNER DOT 2
            # np.array((2,           2*height-2))   # CORNER DOT 3
            # np.array((2*width-2,   2*height-2))   # CORNER DOT 4
            # np.array((width,       height))       # CENTER DOT 1
        ]

        for x in objFactory.objects[:48]:
            points.append(x.point)

        # if pygame.mouse.get_focused():
            # points.append(np.array((mousePos[0], mousePos[1])))

        lines =  objFactory.getWeb(points)
        # PRINT WEB
        # Print lines
        for line in lines:
            pygame.draw.line(screen, (line.color ,line.color ,line.color ), (line.p0[0], line.p0[1]), (line.p1[0], line.p1[1]), 1)

        # Show static points
        # for obj in points:
        #     pygame.draw.line(screen, (255, 255, 255), (obj.point[0]+2, obj.point[1]) , (obj.point[0]-2, obj.point[1]), 1)
        #     pygame.draw.line(screen, (255, 255, 255), (obj.point[0], obj.point[1]+2) , (obj.point[0], obj.point[1]-2), 1)

        # Show objects
        for obj in objFactory.objects:
            pygame.draw.line(screen, (obj.color ,obj.color ,obj.color), (obj.point[0]+2, obj.point[1]) , (obj.point[0]-2, obj.point[1]), 1)
            pygame.draw.line(screen, (obj.color ,obj.color ,obj.color), (obj.point[0], obj.point[1]+2) , (obj.point[0], obj.point[1]-2), 1)

        prints = [
            "Total math operations: %.2E" %(Decimal(calls.sum()),),
            "Target framerate:      %.1d" %(int(framerate),),
            "Total points:          %.1d" %(len(objFactory.objects),),
            "Total lines:           %.1d" %(len(lines),),
            "Connection distance:   %.1d" %(objFactory.connectionDistance,),
            "Max connections:       %.1d" %(objFactory.maxConnectionsPerPoint,),
            "Delay:                 %.1d" %(delay*1000,),
        ]

        for key, value in enumerate(prints):
            screen.blit(myfont.render(value, 1, (255,255,0)), (11, 11*(key+1)))

        pygame.display.flip()

    end = time.time()
    diff = end - start
    delay = 1.0 / framerate - diff

    if delay > 0:
        time.sleep(delay)
