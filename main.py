import pygame
import random
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
clock = pygame.time.Clock()
__break = False

regenerate = pygame.USEREVENT + 1
pygame.time.set_timer(regenerate, 15)
objFactory = objectFactory(limit=50, mode=0, bounds=screenSize)

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
            print("%d %d" % event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            print("User pressed a mouse button")
        elif event.type == regenerate:
            screen.fill((0, 0, 0))
            objFactory.recalculateObjects()
            for obj in objFactory.objects:
                pygame.draw.line(screen, (obj.data['color'] ,obj.data['color'] ,obj.data['color'] ), (obj.data['x']+3, obj.data['y']) , (obj.data['x']-3, obj.data['y']), obj.data['size'])
                pygame.draw.line(screen, (obj.data['color'] ,obj.data['color'] ,obj.data['color'] ), (obj.data['x'], obj.data['y']+3) , (obj.data['x'], obj.data['y']-3), obj.data['size'])

    pygame.display.flip()
    clock.tick(60)
pygame.display.quit()
