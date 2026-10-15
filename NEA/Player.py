'''
this is going to be the main class for the player object. It is going to need to use the Base class as its parent class
'''

from Base import Base

class Player(Base):
    def __init__(self):
        super().__init__((0,0), 'C')