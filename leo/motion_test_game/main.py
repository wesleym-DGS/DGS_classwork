import random
import pygame

class Game:
    def __init__(self):
        pygame.init()
        self.game = True
        self.screen = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()
        self.dt = 0.016
        self.renderList = []

    def checks(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game = False

    def render(self):
        self.screen.fill((0, 0, 0))
        for item in self.renderList:
            pygame.draw.circle(self.screen, item.colour, (int(item.pos.x), int(item.pos.y)), item.radius)
        pygame.display.flip()

    def handle_rect_collision(self, item1, item2, bounciness=1.0):
        item1.hitbox.topleft = (int(item1.pos.x - item1.radius), int(item1.pos.y - item1.radius))
        item2.hitbox.topleft = (int(item2.pos.x - item2.radius), int(item2.pos.y - item2.radius))

        if item1.hitbox.colliderect(item2.hitbox):
            overlap_left = item1.hitbox.right - item2.hitbox.left
            overlap_right = item2.hitbox.right - item1.hitbox.left
            overlap_top = item1.hitbox.bottom - item2.hitbox.top
            overlap_bottom = item2.hitbox.bottom - item1.hitbox.top

            min_overlap = min(overlap_left, overlap_right, overlap_top, overlap_bottom)

            if min_overlap == overlap_left:
                item1.pos.x -= overlap_left * 0.5
                item2.pos.x += overlap_left * 0.5
                item1.motion.x, item2.motion.x = -item1.motion.x * bounciness, -item2.motion.x * bounciness

            elif min_overlap == overlap_right:
                item1.pos.x += overlap_right * 0.5
                item2.pos.x -= overlap_right * 0.5
                item1.motion.x, item2.motion.x = -item1.motion.x * bounciness, -item2.motion.x * bounciness

            elif min_overlap == overlap_top:
                item1.pos.y -= overlap_top * 0.5
                item2.pos.y += overlap_top * 0.5
                item1.motion.y, item2.motion.y = -item1.motion.y * bounciness, -item2.motion.y * bounciness

            elif min_overlap == overlap_bottom:
                item1.pos.y += overlap_bottom * 0.5
                item2.pos.y -= overlap_bottom * 0.5
                item1.motion.y, item2.motion.y = -item1.motion.y * bounciness, -item2.motion.y * bounciness

class ExtraEntity():
    def __init__(self, game):
        self.pos = pygame.Vector2(random.randint(15,785), random.randint(15,585))
        self.motion = pygame.Vector2(random.randint(0,20), random.randint(0,20))
        self.colour = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.radius = 15
        self.hitbox = pygame.Rect(int(self.pos.x - self.radius), int(self.pos.y - self.radius), self.radius * 2, self.radius * 2)
        game.renderList.append(self)

    def apply_gravity(self, strength):
        self.motion.y += strength

    def check_bounds(self, screen_width=800, screen_height=600, bounciness=1.0):
        if self.pos.x - self.radius < 0:
            self.pos.x = self.radius
            self.motion.x = -self.motion.x * bounciness
        elif self.pos.x + self.radius > screen_width:
            self.pos.x = screen_width - self.radius
            self.motion.x = -self.motion.x * bounciness

        if self.pos.y - self.radius < 0:
            self.pos.y = self.radius
            self.motion.y = -self.motion.y * bounciness
        elif self.pos.y + self.radius > screen_height:
            self.pos.y = screen_height - self.radius
            self.motion.y = -self.motion.y * bounciness

    def apply_motion(self, game):
        self.pos += self.motion * game.dt
        self.hitbox.topleft = (int(self.pos.x - self.radius), int(self.pos.y - self.radius))

class Player:
    def __init__(self, game):
        self.colour = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.pos = pygame.Vector2(400, 300)
        self.motion = pygame.Vector2(0, 0)
        self.radius = 15
        self.hitbox = pygame.Rect(int(self.pos.x - self.radius), int(self.pos.y - self.radius), self.radius * 2, self.radius * 2)
        game.renderList.append(self)

    def apply_motion(self, game):
        self.pos += self.motion * game.dt
        self.hitbox.topleft = (int(self.pos.x - self.radius), int(self.pos.y - self.radius))

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

    def apply_gravity(self, strength):
        self.motion.y += strength

    def check_bounds(self, screen_width=800, screen_height=600, bounciness=0.75):
        if self.pos.x - self.radius < 0:
            self.pos.x = self.radius
            self.motion.x = -self.motion.x * bounciness
        elif self.pos.x + self.radius > screen_width:
            self.pos.x = screen_width - self.radius
            self.motion.x = -self.motion.x * bounciness

        if self.pos.y - self.radius < 0:
            self.pos.y = self.radius
            self.motion.y = -self.motion.y * bounciness
        elif self.pos.y + self.radius > screen_height:
            self.pos.y = screen_height - self.radius
            self.motion.y = -self.motion.y * bounciness

game = Game()
player = Player(game)
extra = ExtraEntity(game)

while game.game:
    game.checks()
    extra.apply_motion(game)
    extra.apply_gravity(1.5)
    extra.check_bounds()
    game.handle_rect_collision(player, extra)
    player.move(2)
    player.apply_gravity(1.5)
    player.apply_motion(game)
    player.check_bounds(800, 600, 0.75)
    game.render()
    ms = game.clock.tick(60)
    game.dt = min(ms / 1000.0, 0.1)

pygame.quit()