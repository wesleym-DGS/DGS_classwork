import random

import pygame

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()
        self.running = True
        self.dt = 0.016  # Default to ~60 FPS time step for frame 1
        self.strength = 1

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def render(self, entity_list):
        self.screen.fill((0, 0, 0))
        # Draw player circle (radius 15)
        for x in entity_list:
            pygame.draw.circle(self.screen, (0, 128, 255), (int(x.x), int(x.y)), 15)
            pygame.display.flip()

    def apply_gravity(self, pos):
        return pos.y - self.strength * self.dt

class Entity:
    def __init__(self, x, y):
        self.pos = pygame.Vector2(x, y)
        self.speed = 300  # Pixels per second
        self.move_vector = pygame.Vector2(random.randint(0, 100), random.randint(0, 100))
        self.list_of_entities = []
        self.list_of_entities.append(self)

    def move(self, dt):

        # Normalize diagonal movement so moving diagonally isn't faster
        if self.move_vector.length() > 0:
            move_vector = self.move_vector.normalize()

        # Update position
        self.pos += self.move_vector * self.speed * dt

        # Keep player within screen boundaries (800x600 screen)
        self.pos.x = max(15, min(785, self.pos.x))
        self.pos.y = max(15, min(585, self.pos.y))



class Player(Entity):
    def move(self, dt):
        keys = pygame.key.get_pressed()

        # Calculate direction movement
        move_vector = pygame.Vector2(0, 0)
        if keys[pygame.K_w]:
            move_vector.y -= 1
        if keys[pygame.K_s]:
            move_vector.y += 1
        if keys[pygame.K_a]:
            move_vector.x -= 1
        if keys[pygame.K_d]:
            move_vector.x += 1

        # Normalize diagonal movement so moving diagonally isn't faster
        if move_vector.length() > 0:
            move_vector = move_vector.normalize()

        # Update position
        self.pos += move_vector * self.speed * dt

        # Keep player within screen boundaries (800x600 screen)
        self.pos.x = max(15, min(785, self.pos.x))
        self.pos.y = max(15, min(585, self.pos.y))

game = Game()
player = Player(400, 300)
entity = Entity(300, 300)

while game.running:
    game.check_events()
    player.move(game.dt)
    game.render([player.pos, entity.pos])

    for x in range(len(entity.list_of_entities)):
        entity.list_of_entities[x].pos = game.apply_gravity(entity.list_of_entities[x].pos)

    # Tick clock and safely convert ms to seconds, capping max dt to 0.1s
    ms = game.clock.tick(60)
    game.dt = min(ms / 1000.0, 0.1)

pygame.quit()