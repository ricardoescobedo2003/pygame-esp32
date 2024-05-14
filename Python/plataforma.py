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
pygame.display.set_caption("Juego de Plataformas")

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Dimensiones del personaje
CHAR_WIDTH = 50
CHAR_HEIGHT = 50
CHAR_SPEED = 5
CHAR_JUMP = -10

# Dimensiones de las plataformas
PLATFORM_WIDTH = 100
PLATFORM_HEIGHT = 20
PLATFORM_SPEED = 3

# Inicializa el personaje
char_x = (WINDOW_WIDTH - CHAR_WIDTH) // 2
char_y = WINDOW_HEIGHT - CHAR_HEIGHT
char_dy = 0
jumping = False

# Inicializa las plataformas
platforms = []
for _ in range(5):
    platform = pygame.Rect(
        random.randint(0, WINDOW_WIDTH - PLATFORM_WIDTH),
        random.randint(0, WINDOW_HEIGHT - CHAR_HEIGHT - PLATFORM_HEIGHT),
        PLATFORM_WIDTH,
        PLATFORM_HEIGHT
    )
    platforms.append(platform)

# Configura el puerto serial
ser = serial.Serial('/dev/ttyUSB0', 9600)  # Ajusta el puerto según tu configuración

# Configura el temporizador
clock = pygame.time.Clock()
time_limit = 30  # segundos
start_time = pygame.time.get_ticks()

try:
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                ser.close()
                pygame.quit()
                sys.exit()

        # Movimiento del personaje
        line = ser.readline().decode().strip()
        if line == '4095':  # Mover a la derecha
            char_x += CHAR_SPEED
        elif line == '0':   # Mover a la izquierda
            char_x -= CHAR_SPEED

        # Limita la posición del personaje dentro de la ventana
        char_x = max(0, min(char_x, WINDOW_WIDTH - CHAR_WIDTH))

        # Salto del personaje
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and not jumping:  # Si se presiona la barra espaciadora y no está saltando
            char_dy = CHAR_JUMP
            jumping = True

        # Aplica la gravedad
        char_dy += 0.5
        char_y += char_dy

        # Verifica colisiones con el suelo
        if char_y >= WINDOW_HEIGHT - CHAR_HEIGHT:
            char_y = WINDOW_HEIGHT - CHAR_HEIGHT
            char_dy = 0
            jumping = False

        # Mueve las plataformas hacia abajo
        for platform in platforms:
            platform.move_ip(0, PLATFORM_SPEED)

        # Genera una nueva plataforma si alguna desaparece por debajo de la ventana
        platforms = [platform for platform in platforms if platform.top < WINDOW_HEIGHT]
        if len(platforms) < 5:
            new_platform = pygame.Rect(
                random.randint(0, WINDOW_WIDTH - PLATFORM_WIDTH),
                -PLATFORM_HEIGHT,
                PLATFORM_WIDTH,
                PLATFORM_HEIGHT
            )
            platforms.append(new_platform)

        # Verifica colisiones del personaje con las plataformas
        for platform in platforms:
            if platform.colliderect(pygame.Rect(char_x, char_y, CHAR_WIDTH, CHAR_HEIGHT)) and char_dy >= 0:
                char_y = platform.top - CHAR_HEIGHT
                char_dy = 0
                jumping = False

        # Dibuja los elementos en pantalla
        window.fill(BLACK)
        pygame.draw.rect(window, RED, (char_x, char_y, CHAR_WIDTH, CHAR_HEIGHT))
        for platform in platforms:
            pygame.draw.rect(window, WHITE, platform)

        # Verifica el tiempo transcurrido
        current_time = pygame.time.get_ticks()
        elapsed_time = (current_time - start_time) // 1000
        time_remaining = max(time_limit - elapsed_time, 0)
        font = pygame.font.Font(None, 36)
        text = font.render(f"Tiempo restante: {time_remaining}", True, WHITE)
        window.blit(text, (10, 10))

        # Actualiza la pantalla
        pygame.display.update()

        # Limita la velocidad de fotogramas
        clock.tick(60)

        # Termina el juego si se acaba el tiempo
        if time_remaining <= 0:
            print("¡Se acabó el tiempo!")
            break

except KeyboardInterrupt:
    # Manejo de interrupción de teclado (Ctrl+C)
    ser.close()
    pygame.quit()
    print("Serial connection closed.")
