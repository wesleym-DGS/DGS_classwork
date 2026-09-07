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

    def render(self, player_pos):
        self.screen.fill((0, 0, 0))
        # Draw player circle (radius 15)
        pygame.draw.circle(self.screen, (0, 128, 255), (int(player_pos.x), int(player_pos.y)), 15)
        pygame.display.flip()

    def count_gravity_strngth(self, pos, p_strength):
        if pos.y == 585:
            return 0.5
        else:
            return self.strength + p_strength

class Player:
    def __init__(self, x, y):
        self.pos = pygame.Vector2(x, y)
        self.speed = 300  # Pixels per second
        self.player_grav = 1

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

    def gravity(self):
        self.pos.y += self.player_grav

game = Game()
player = Player(400, 300)

while game.running:
    game.check_events()
    player.player_grav = game.count_gravity_strngth(player.pos, player.player_grav)
    player.gravity()
    player.move(game.dt)
    game.render(player.pos)

    # Tick clock and safely convert ms to seconds, capping max dt to 0.1s
    ms = game.clock.tick(60)
    game.dt = min(ms / 1000.0, 0.1)

pygame.quit()