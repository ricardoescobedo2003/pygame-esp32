import pygame
import sys

# Definir colores
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# Dimensiones de la pantalla
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Dimensiones del jugador (paleta)
PLAYER_WIDTH = 100
PLAYER_HEIGHT = 20

# Dimensiones del ladrillo
BRICK_WIDTH = 80
BRICK_HEIGHT = 30

# Dimensiones de la pelota
BALL_RADIUS = 10

# Velocidad de la pelota
BALL_SPEED = 5

# Inicializar Pygame
pygame.init()

# Configurar la pantalla
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Breakout")

clock = pygame.time.Clock()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = (SCREEN_WIDTH - PLAYER_WIDTH) // 2
        self.rect.y = SCREEN_HEIGHT - PLAYER_HEIGHT - 10

    def update(self):
        # Mover la paleta con las teclas izquierda y derecha
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= 5
        if keys[pygame.K_RIGHT]:
            self.rect.x += 5
        # Limitar el movimiento de la paleta dentro de la pantalla
        self.rect.x = max(0, min(self.rect.x, SCREEN_WIDTH - PLAYER_WIDTH))

class Brick(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((BRICK_WIDTH, BRICK_HEIGHT))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((BALL_RADIUS * 2, BALL_RADIUS * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, WHITE, (BALL_RADIUS, BALL_RADIUS), BALL_RADIUS)
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.speed_x = BALL_SPEED
        self.speed_y = -BALL_SPEED

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        # Rebotar en los bordes de la pantalla
        if self.rect.left <= 0 or self.rect.right >= SCREEN_WIDTH:
            self.speed_x = -self.speed_x
        if self.rect.top <= 0:
            self.speed_y = -self.speed_y

# Crear grupos de sprites
all_sprites = pygame.sprite.Group()
bricks = pygame.sprite.Group()

# Crear jugador
player = Player()
all_sprites.add(player)

# Crear ladrillos
for i in range(10):
    brick = Brick(i * (BRICK_WIDTH + 5) + 50, 50)
    bricks.add(brick)
    all_sprites.add(brick)

# Crear pelota
ball = Ball()
all_sprites.add(ball)

# Loop del juego
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Actualizar
    all_sprites.update()

    # Colisión entre la pelota y los ladrillos
    brick_hits = pygame.sprite.spritecollide(ball, bricks, True)
    if brick_hits:
        ball.speed_y = -ball.speed_y

    # Colisión entre la pelota y el jugador
    if pygame.sprite.collide_rect(ball, player):
        ball.speed_y = -ball.speed_y

    # Dibujar
    screen.fill(WHITE)
    all_sprites.draw(screen)
    pygame.display.flip()

    clock.tick(60)

pygame.quit()
sys.exit()
