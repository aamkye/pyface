import pygame
import random
from math import sqrt
from math import ceil
from src.object import object
from src.objectFactory import objectFactory

# BLACK    = (   0,   0,   0)
# WHITE    = ( 255, 255, 255)
# RED      = ( 255,   0,   0)
# GREEN    = (   0, 255,   0)
# BLUE     = (   0,   0, 255)

pygame.init()
pygame.display.set_caption("Le Dot")

screenSize = (700, 500)
screen = pygame.display.set_mode(screenSize, pygame.RESIZABLE)
pygame.mouse.set_cursor((8,8),(0,0),(0,0,0,0,0,0,0,0),(0,0,0,0,0,0,0,0))
clock = pygame.time.Clock()
__break = False

regenerate = pygame.USEREVENT + 1
pygame.time.set_timer(regenerate, 50)
objFactory = objectFactory(limit=96, mode=0, bounds=screenSize)
mousePos=(0, 0)
while not __break:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print("User asked to quit.")
            __break=True
        elif event.type == pygame.VIDEORESIZE:
            screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            objFactory.data['bounds'] = (event.w, event.h)
        elif event.type == pygame.KEYDOWN:
            print("User pressed a key.")
        elif event.type == pygame.KEYUP:
            print("User let go of a key.")
        elif event.type == pygame.MOUSEMOTION:
            # print("%d %d" % event.pos)
            mousePos = event.pos
        elif event.type == pygame.MOUSEBUTTONDOWN:
            print("User pressed a mouse button")
        elif event.type == regenerate:
            screen.fill((0, 0, 0))
            objFactory.recalculateObjects()
            def drawWeb(point_a, point_b, distance_long, distance_short):
                # Get closest x in reverse sequence - from farest to closest. and conenct to mouse
                for obj in objFactory.getSortedByDistance(point_a, point_b, distance_long)[16::-1]:
                    color = ceil(255 - sqrt((obj.data['x'] - point_a)**2 + (obj.data['y'] - point_b)**2) / (distance_long / 255))
                    # print(color)
                    if(color < 0):
                        color = abs(color)
                    pygame.draw.aaline(screen, (color, color, color), (obj.data['x'], obj.data['y']), (point_a, point_b), 1)

                    # Get y closest elements and connect it to object connected to mouse.
                    for nd_obj in objFactory.getSortedByDistance(obj.data['x'], obj.data['y'], distance_short)[3::-1]:
                        pygame.draw.aaline(screen, (color, color, color), (obj.data['x'], obj.data['y']), (nd_obj.data['x'], nd_obj.data['y']), 1)

                # Draw mouse point
                pygame.draw.line(screen, (255 ,255 ,255), (point_a+2, point_b) , (point_a-2, point_b), 1)
                pygame.draw.line(screen, (255 ,255 ,255), (point_a, point_b+2) , (point_a, point_b-2), 1)
            # Show if mouse within window

            width = ceil(objFactory.data['bounds'][0]/2)
            height = ceil(objFactory.data['bounds'][1]/2)
            if pygame.mouse.get_focused():
                drawWeb(mousePos[0], mousePos[1], 512, 196)
            # else:
            #     drawWeb(2*width, 2*height, 512, 196)

            for obj in objFactory.objects:
                pygame.draw.line(screen, (obj.data['color'] ,obj.data['color'] ,obj.data['color'] ), (obj.data['x']+1, obj.data['y']) , (obj.data['x']-1, obj.data['y']), obj.data['size'])
                pygame.draw.line(screen, (obj.data['color'] ,obj.data['color'] ,obj.data['color'] ), (obj.data['x'], obj.data['y']+1) , (obj.data['x'], obj.data['y']-1), obj.data['size'])


            # for a in range(0,5):
            #     for b in range(0,5):
            #         drawWeb(a*width, b*height, 512, 196)

            # a = random.randrange(0,5)
            # b = random.randrange(0,5)

            # Center
            drawWeb(width-128, height-128, 256, 128)
            drawWeb(width+128, height-128, 256, 128)
            drawWeb(width-128, height+128, 256, 128)
            drawWeb(width+128, height+128, 256, 128)

            # Left & right
            drawWeb(width+396, height, 256, 128)
            drawWeb(width-396, height, 256, 128)

            # Corners
            drawWeb(2, 2, 512, 196)
            drawWeb(2*width-2, 2, 512, 196)
            drawWeb(2, 2*height-2, 512, 196)
            drawWeb(2*width-2, 2*height-2, 512, 196)

    pygame.display.flip()
    clock.tick(60)
pygame.display.quit()
