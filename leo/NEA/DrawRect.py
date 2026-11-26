'''

this is the class for rect or square objects

'''

from DrawObjectBase import DrawObjectBase
from random import randint

class DrawRect(DrawObjectBase):
    def __init__(self, mousePos, mousePos2, client):
        super().__init__(client, mousePos, mousePos2, 'R', (randint(0,255),randint(0,255),randint(0,255)))