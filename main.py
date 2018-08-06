from src.objectFactory import *

factory = objectFactory()

factory.create()
factory.create()

print(len(factory.objects))
