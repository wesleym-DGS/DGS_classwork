import pygame

'''

the goal here is to make a simple version of the rendering pipline for my overarching nea project

'''

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()
        self.running = True
        self.dt = 0.016
        self.gameItemList = []

    def apply_gravity(self, items):
        for item in self.gameItemList:
            item.pos[1] += item.speed * self.dt

    def update_all(self, render):
        for item in self.gameItemList:
            item.update(render)

    def flush_lists(self, lists):
        lists.clear()

    def event_checks(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

class Render:
    def __init__(self, screen):
        self.screen = screen
        self.renderList = []

    def render(self):
        self.screen.fill((0,0,0))
        for item in self.renderList:
            if item.type == 'R':
                pygame.draw.rect(self.screen, item.color, item.rect)
            else:
                pygame.draw.ellipse(self.screen, item.color, item.rect)

        pygame.display.flip()

class Player:
    def __init__(self, gameItemList):
        self.pos = pygame.Vector2(380, 50)
        self.type = 'P'
        self.speed = 50
        self.color = (100, 100, 100)
        self.rect = pygame.Rect(self.pos.x - 15, self.pos.y - 15, 30, 30)
        gameItemList.append(self)

    def update(self, render):
        self.rect.x = int(self.pos.x - 15)
        self.rect.y = int(self.pos.y - 15)
        render.renderList.append(self)

game = Game()
render = Render(game.screen)
player = Player(game.gameItemList)

while game.running:
    game.event_checks()
    game.flush_lists(render.renderList)
    game.apply_gravity(game.gameItemList)
    game.update_all(render)
    render.render()
    ms = game.clock.tick(60)
    game.dt = min(ms / 1000.0, 0.1)

pygame.quit()