import random
import itertools
import pygame

'''

the goal is to make a simple ball game that uses physics

'''

class Game:
    def __init__(self):
        pygame.init()
        self.game = True
        self.screen = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()
        self.dt = 0.016
        self.renderList = []

    def checks(self, button):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if button.hitbox.collidepoint(event.pos):
                    button.pressed(self)

    def render(self):
        self.screen.fill((0, 0, 0))
        for item in self.renderList:
            pygame.draw.circle(self.screen, item.colour, (int(item.pos.x), int(item.pos.y)), item.radius)
        pygame.display.flip()

    def apply_gravity(self, strength):
        for entity in self.renderList:
            entity.motion.y += strength * entity.weight

    def apply_motion(self, entity):
        entity.pos += entity.motion * self.dt
        entity.hitbox.topleft = (int(entity.pos.x - entity.radius), int(entity.pos.y - entity.radius))

    def check_bounds(self, entity, screen_width=800, screen_height=600, bounciness=0.75):
        if entity.weight == 0:
            return

        if entity.pos.x - entity.radius < 0:
            entity.pos.x = entity.radius
            entity.motion.x = -entity.motion.x * bounciness
        elif entity.pos.x + entity.radius > screen_width:
            entity.pos.x = screen_width - entity.radius
            entity.motion.x = -entity.motion.x * bounciness

        if entity.pos.y - entity.radius < 0:
            entity.pos.y = entity.radius
            entity.motion.y = -entity.motion.y * bounciness
        elif entity.pos.y + entity.radius > screen_height:
            entity.pos.y = screen_height - entity.radius
            entity.motion.y = -entity.motion.y * bounciness

    def handle_rect_collision(self, item1, item2, bounciness=1.0):
        if item1.weight == 0 or item2.weight == 0:
            return

        item1.hitbox.topleft = (int(item1.pos.x - item1.radius), int(item1.pos.y - item1.radius))
        item2.hitbox.topleft = (int(item2.pos.x - item2.radius), int(item2.pos.y - item2.radius))

        if item1.hitbox.colliderect(item2.hitbox):
            overlap_left = item1.hitbox.right - item2.hitbox.left
            overlap_right = item2.hitbox.right - item1.hitbox.left
            overlap_top = item1.hitbox.bottom - item2.hitbox.top
            overlap_bottom = item2.hitbox.bottom - item1.hitbox.top

            min_overlap = min(overlap_left, overlap_right, overlap_top, overlap_bottom)
            total_weight = item1.weight + item2.weight

            if min_overlap == overlap_left:
                item1.pos.x -= overlap_left * 0.5
                item2.pos.x += overlap_left * 0.5
                if item1.motion.x > item2.motion.x:
                    v1 = item1.motion.x
                    v2 = item2.motion.x
                    item1.motion.x = ((item1.weight - item2.weight) * v1 + 2 * item2.weight * v2) / total_weight * bounciness
                    item2.motion.x = ((item2.weight - item1.weight) * v2 + 2 * item1.weight * v1) / total_weight * bounciness

            elif min_overlap == overlap_right:
                item1.pos.x += overlap_right * 0.5
                item2.pos.x -= overlap_right * 0.5
                if item1.motion.x < item2.motion.x:
                    v1 = item1.motion.x
                    v2 = item2.motion.x
                    item1.motion.x = ((item1.weight - item2.weight) * v1 + 2 * item2.weight * v2) / total_weight * bounciness
                    item2.motion.x = ((item2.weight - item1.weight) * v2 + 2 * item1.weight * v1) / total_weight * bounciness

            elif min_overlap == overlap_top:
                item1.pos.y -= overlap_top * 0.5
                item2.pos.y += overlap_top * 0.5
                if item1.motion.y > item2.motion.y:
                    v1 = item1.motion.y
                    v2 = item2.motion.y
                    item1.motion.y = ((item1.weight - item2.weight) * v1 + 2 * item2.weight * v2) / total_weight * bounciness
                    item2.motion.y = ((item2.weight - item1.weight) * v2 + 2 * item1.weight * v1) / total_weight * bounciness

            elif min_overlap == overlap_bottom:
                item1.pos.y += overlap_bottom * 0.5
                item2.pos.y -= overlap_bottom * 0.5
                if item1.motion.y < item2.motion.y:
                    v1 = item1.motion.y
                    v2 = item2.motion.y
                    item1.motion.y = ((item1.weight - item2.weight) * v1 + 2 * item2.weight * v2) / total_weight * bounciness
                    item2.motion.y = ((item2.weight - item1.weight) * v2 + 2 * item1.weight * v1) / total_weight * bounciness

    def all_collision_checks(self, bounciness):
        for item1, item2 in itertools.combinations(self.renderList, 2):
            self.handle_rect_collision(item1, item2, bounciness)

    def apply_all_motion(self):
        for entity in self.renderList:
            self.check_bounds(entity)
            self.apply_motion(entity)


class ExtraEntity():
    def __init__(self, game, weight):
        self.pos = pygame.Vector2(random.randint(15, 785), random.randint(15, 585))
        self.motion = pygame.Vector2(random.randint(0, 20), random.randint(0, 20))
        self.colour = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.radius = 15
        self.weight = weight
        self.hitbox = pygame.Rect(int(self.pos.x - self.radius), int(self.pos.y - self.radius), self.radius * 2, self.radius * 2)
        game.renderList.append(self)


class Player:
    def __init__(self, game, weight):
        self.colour = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.pos = pygame.Vector2(400, 300)
        self.motion = pygame.Vector2(0, 0)
        self.radius = 15
        self.weight = weight
        self.hitbox = pygame.Rect(int(self.pos.x - self.radius), int(self.pos.y - self.radius), self.radius * 2, self.radius * 2)
        game.renderList.append(self)

    def move(self, speed):
        keys = pygame.key.get_pressed()
        move_vector = pygame.Vector2(0, 0)
        if keys[pygame.K_w]:
            move_vector.y -= speed
        if keys[pygame.K_s]:
            move_vector.y += speed
        if keys[pygame.K_a]:
            move_vector.x -= speed
        if keys[pygame.K_d]:
            move_vector.x += speed

        self.motion += move_vector


class Button:
    def __init__(self, game):
        self.colour = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.pos = pygame.Vector2(15, 15)
        self.motion = pygame.Vector2(0, 0)
        self.radius = 15
        self.weight = 0
        self.hitbox = pygame.Rect(int(self.pos.x - self.radius), int(self.pos.y - self.radius), self.radius * 2, self.radius * 2)
        game.renderList.append(self)

    def pressed(self, game):
        ExtraEntity(game, random.randint(1,10))


game = Game()
player = Player(game, -1)
button = Button(game)

while game.game:
    game.checks(button)
    player.move(2)
    game.apply_gravity(1.5)
    game.all_collision_checks(0.75)
    game.apply_all_motion()
    game.render()
    ms = game.clock.tick(60)
    game.dt = min(ms / 1000.0, 0.1)

pygame.quit()