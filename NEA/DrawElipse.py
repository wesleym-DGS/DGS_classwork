'''

this is the class for elips or circular objects

'''

from DrawObjectBase import DrawObjectBase
from random import randint

class DrawElipse(DrawObjectBase):
    def __init__(self, mousePos, mousePos2, client):
        super().__init__(client, mousePos, mousePos2, 'E', (randint(0,255),randint(0,255),randint(0,255)))