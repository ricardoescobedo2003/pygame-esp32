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
pygame.display.set_caption("Esquiva el Obstáculo")

# Colores
WHITE = (0, 0, 0)
RED = (255, 0, 0)

# Dimensiones del cuadrado
SQUARE_SIZE = 50
square_x = (WINDOW_WIDTH - SQUARE_SIZE) // 2
square_y = (WINDOW_HEIGHT - SQUARE_SIZE) // 2

# Configura el puerto serial
ser = serial.Serial('/dev/ttyUSB0', 9600)  # Ajusta el puerto según tu configuración

# Clase para representar las figuras en movimiento
class Figure:
    def __init__(self):
        self.width = random.randint(20, 50)
        self.height = random.randint(20, 50)
        self.x = random.randint(0, WINDOW_WIDTH - self.width)
        self.y = 0 - self.height
        self.speed = random.randint(1, 3)

    def update(self):
        self.y += self.speed

    def draw(self, surface):
        pygame.draw.rect(surface, RED, (self.x, self.y, self.width, self.height))

# Lista para almacenar las figuras en movimiento
figures = []

try:
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                ser.close()
                pygame.quit()
                sys.exit()

        # Genera nuevas figuras aleatorias
        if random.randint(1, 100) == 1:
            figures.append(Figure())

        # Actualiza la posición del cuadrado según los datos recibidos del puerto serial
        line = ser.readline().decode().strip()
        if line == '4095':  # Mover a la derecha
            square_x += 5
        elif line == '0':    # Mover a la izquierda
            square_x -= 5

        # Limita la posición del cuadrado dentro de la ventana
        square_x = max(0, min(square_x, WINDOW_WIDTH - SQUARE_SIZE))

        # Borra la pantalla
        window.fill(WHITE)

        # Actualiza y dibuja las figuras en movimiento
        for figure in figures:
            figure.update()
            figure.draw(window)

        # Elimina las figuras que han salido de la ventana
        figures = [figure for figure in figures if figure.y < WINDOW_HEIGHT]

        # Dibuja el cuadrado en su posición actual
        pygame.draw.rect(window, RED, (square_x, square_y, SQUARE_SIZE, SQUARE_SIZE))

        # Actualiza la pantalla
        pygame.display.update()
except KeyboardInterrupt:
    # Manejo de interrupción de teclado (Ctrl+C)
    ser.close()
    pygame.quit()
    print("Serial connection closed.")
