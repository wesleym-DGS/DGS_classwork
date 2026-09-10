import socket
import sys
import json
import pygame

class Client:
    def __init__(self):
        pygame.init()
        self.server_address = ('localhost', 5555)
        self.screenW = 800
        self.screenH = 600
        self.screen = pygame.display.set_mode((self.screenW, self.screenH))
        pygame.display.set_caption('Multiplayer Game')
        self.clock = pygame.time.Clock()
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.client.connect((self.server_address[0], self.server_address[1]))
        except socket.error as e:
            print(e)
            sys.exit()
        self.render_list = []
        self.game = True

    def receive(self, sock):
        buffer = ''
        while '\n' not in buffer:
            chunck = sock.recv(1024).decode('utf-8')
            if not chunck:
                return None
            buffer += chunck
        return buffer.split()

    def check_quit(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game = False

    def render(self):
        self.screen.fill((0,0,0))
        for x in

class Player:
    def __init__(self, screenW, screenH):
        self.pos = pygame.Vector2(screenW/2, screenH/2)
        self.keys = pygame.key.get_pressed()

    def move(self):
        self.move = pygame.Vector2(0,0)

        if self.keys[pygame.K_LEFT]:
            self.move.x -= 1
        if self.keys[pygame.K_RIGHT]:
            self.move.x += 1
        if self.keys[pygame.K_UP]:
            self.move.y-= 1
        if self.keys[pygame.K_DOWN]:
            self.move.y+= 1
        if self.move.length() > 0:
            self.move = self.move.normalize()



