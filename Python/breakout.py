import serial
import pygame
import sys
import random

# Inicializa Pygame
pygame.init()

# Configuración de la ventana
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Breakout")

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Dimensiones
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 20
PADDLE_SPEED = 5  # Se reduce la velocidad de la paleta
BALL_SIZE = 20
BRICK_WIDTH = 80
BRICK_HEIGHT = 30
BRICK_ROWS = 5
BRICK_COLS = 10
BRICK_GAP = 2
BRICK_OFFSET_TOP = 50

# Inicializa la paleta
paddle_x = (WINDOW_WIDTH - PADDLE_WIDTH) // 2
paddle_y = WINDOW_HEIGHT - PADDLE_HEIGHT - 10

# Inicializa la pelota
ball_x = WINDOW_WIDTH // 2
ball_y = WINDOW_HEIGHT // 2
ball_dx = 2
ball_dy = -2
ball_started = False  # Indica si la pelota ha comenzado a moverse

# Inicializa los ladrillos y el puntaje
bricks = []
score = 0
for row in range(BRICK_ROWS):
    for col in range(BRICK_COLS):
        brick = pygame.Rect(
            col * (BRICK_WIDTH + BRICK_GAP),
            BRICK_OFFSET_TOP + row * (BRICK_HEIGHT + BRICK_GAP),
            BRICK_WIDTH,
            BRICK_HEIGHT
        )
        bricks.append(brick)

# Configura el puerto serial
ser = serial.Serial('/dev/ttyUSB0', 9600)  # Ajusta el puerto según tu configuración

# Configura la fuente para el puntaje
font = pygame.font.Font(None, 36)

try:
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                ser.close()
                pygame.quit()
                sys.exit()

        # Movimiento de la paleta
        line = ser.readline().decode().strip()
        if line == '4095':  # Mover a la derecha
            paddle_x += PADDLE_SPEED
        elif line == '0':   # Mover a la izquierda
            paddle_x -= PADDLE_SPEED

        # Limita la posición de la paleta dentro de la ventana
        paddle_x = max(0, min(paddle_x, WINDOW_WIDTH - PADDLE_WIDTH))

        # Reinicia el juego si la pelota pasa por debajo de la paleta
        if ball_y > WINDOW_HEIGHT:
            ball_x = WINDOW_WIDTH // 2
            ball_y = WINDOW_HEIGHT // 2
            ball_started = False
            bricks = [
                pygame.Rect(
                    col * (BRICK_WIDTH + BRICK_GAP),
                    BRICK_OFFSET_TOP + row * (BRICK_HEIGHT + BRICK_GAP),
                    BRICK_WIDTH,
                    BRICK_HEIGHT
                )
                for row in range(BRICK_ROWS) for col in range(BRICK_COLS)
            ]
            score = 0  # Reinicia el puntaje

        # Inicia el movimiento de la pelota si se detecta entrada en el puerto serial
        if not ball_started and (line == '4095' or line == '0'):
            ball_started = True

        if ball_started:
            # Movimiento de la pelota
            ball_x += ball_dx
            ball_y += ball_dy

            # Colisión con los bordes
            if ball_x <= 0 or ball_x >= WINDOW_WIDTH - BALL_SIZE:
                ball_dx = -ball_dx
            if ball_y <= 0:
                ball_dy = -ball_dy

            # Colisión con la paleta
            if paddle_x < ball_x < paddle_x + PADDLE_WIDTH and paddle_y < ball_y < paddle_y + PADDLE_HEIGHT:
                ball_dy = -ball_dy

            # Colisión con los ladrillos
            for brick in bricks:
                if brick.colliderect(pygame.Rect(ball_x, ball_y, BALL_SIZE, BALL_SIZE)):
                    bricks.remove(brick)
                    ball_dy = -ball_dy
                    score += 1  # Incrementa el puntaje
                    break

        # Dibuja los elementos en pantalla
        window.fill(BLACK)
        pygame.draw.rect(window, BLUE, (paddle_x, paddle_y, PADDLE_WIDTH, PADDLE_HEIGHT))
        pygame.draw.circle(window, RED, (ball_x, ball_y), BALL_SIZE // 2)

        for brick in bricks:
            pygame.draw.rect(window, WHITE, brick)

        # Renderiza el puntaje en la pantalla
        score_text = font.render("Score: " + str(score), True, WHITE)
        window.blit(score_text, (10, 10))

        # Actualiza la pantalla
        pygame.display.update()

except KeyboardInterrupt:
    # Manejo de interrupción de teclado (Ctrl+C)
    ser.close()
    pygame.quit()
    print("Serial connection closed.")
