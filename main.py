import pygame
import threading
import numpy as np

from src.object import object
from src.objectFactory import objectFactory

pygame.init()
pygame.display.set_caption("Le Dot")


screenSize = (700, 500)
screen = pygame.display.set_mode(screenSize, pygame.RESIZABLE, 16)
screen.set_alpha(None)
pygame.mouse.set_cursor((8,8),(0,0),(0,0,0,0,0,0,0,0),(0,0,0,0,0,0,0,0))
clock = pygame.time.Clock()
__break = False

regenerate = pygame.USEREVENT + 1
pygame.event.set_allowed([pygame.QUIT, pygame.VIDEORESIZE, pygame.MOUSEMOTION, regenerate])
pygame.time.set_timer(regenerate, 50)
objFactory = objectFactory(limit=64, mode=0, bounds=screenSize)
mousePos=(0, 0)
while not __break:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # print("User asked to quit.")
            __break=True
        elif event.type == pygame.VIDEORESIZE:
            screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE | pygame.DOUBLEBUF)
            objFactory.bounds = (event.w, event.h)
        # elif event.type == pygame.KEYDOWN:
        #     print("User pressed a key.")
        # elif event.type == pygame.KEYUP:
        #     print("User let go of a key.")
        elif event.type == pygame.MOUSEMOTION:
            # print("%d %d" % event.pos)
            mousePos = event.pos
        # elif event.type == pygame.MOUSEBUTTONDOWN:
        #     print("User pressed a mouse button")
        elif event.type == regenerate:
            screen.fill((0, 0, 0))
            objFactory.recalculateObjects()
            width = np.ceil(objFactory.bounds[0]/2)
            height = np.ceil(objFactory.bounds[1]/2)
            first_distance=396
            second_distance=128

            points=[
                objFactory.pointArr(point=np.array(((width/4)*3, (height/2)*1)), first_distance=first_distance, second_distance=second_distance), # DOT 1
                objFactory.pointArr(point=np.array(((width/4)*5, (height/2)*1)), first_distance=first_distance, second_distance=second_distance), # DOT 2
                objFactory.pointArr(point=np.array(((width/4)*3, (height/2)*3)), first_distance=first_distance, second_distance=second_distance), # DOT 3
                objFactory.pointArr(point=np.array(((width/4)*5, (height/2)*3)), first_distance=first_distance, second_distance=second_distance), # DOT 4
                objFactory.pointArr(point=np.array(((width/2)*1, height)),       first_distance=first_distance, second_distance=second_distance), # MIDDLE DOT 1
                objFactory.pointArr(point=np.array(((width/2)*3, height)),       first_distance=first_distance, second_distance=second_distance), # MIDDLE DOT 2
                objFactory.pointArr(point=np.array((2,           2)),            first_distance=first_distance, second_distance=second_distance), # CORNER DOT 1
                objFactory.pointArr(point=np.array((2*width-2,   2)),            first_distance=first_distance, second_distance=second_distance), # CORNER DOT 2
                objFactory.pointArr(point=np.array((2,           2*height-2)),   first_distance=first_distance, second_distance=second_distance), # CORNER DOT 3
                objFactory.pointArr(point=np.array((2*width-2,   2*height-2)),   first_distance=first_distance, second_distance=second_distance), # CORNER DOT 4
                objFactory.pointArr(point=np.array((width,       height)),       first_distance=first_distance, second_distance=second_distance), # CENTER DOT 1
            ]

            if pygame.mouse.get_focused():
                points.append(objFactory.pointArr(point=np.array((mousePos[0], mousePos[1])), first_distance=512, second_distance=196))

            lines =  objFactory.getWeb(points)

            # PRINT WEB
            # Print lines
            for line in lines:
                pygame.draw.line(screen, (line.color ,line.color ,line.color ), (line.p0[0], line.p0[1]), (line.p1[0], line.p1[1]), 1)

            # Show static points
            for obj in points:
                pygame.draw.line(screen, (255, 255, 255), (obj.point[0]+2, obj.point[1]) , (obj.point[0]-2, obj.point[1]), 1)
                pygame.draw.line(screen, (255, 255, 255), (obj.point[0], obj.point[1]+2) , (obj.point[0], obj.point[1]-2), 1)

            # Show objects
            for obj in objFactory.objects:
                pygame.draw.line(screen, (obj.color ,obj.color ,obj.color), (obj.point[0]+2, obj.point[1]) , (obj.point[0]-2, obj.point[1]), 1)
                pygame.draw.line(screen, (obj.color ,obj.color ,obj.color), (obj.point[0], obj.point[1]+2) , (obj.point[0], obj.point[1]-2), 1)

    pygame.display.flip()
    clock.tick(45)
pygame.display.quit()
