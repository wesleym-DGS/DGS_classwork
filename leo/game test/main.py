'''

the goal is the make a simple game just because

'''

import pygame

def fuck_off(thing):
    print(f'{thing}fuck off')


class Main:
    def __init__(self, text, text2):
        self.hp = 10
        self.helpmeiminpaincuzofthisguy = 'fuck off'

    def helpmeiminpaincuzofthisguy(self):
        return self.helpmeiminpaincuzofthisguy



obj = Main('me','you')

print(obj.hp)
fuck_off(obj.helpmeiminpaincuzofthisguy)

