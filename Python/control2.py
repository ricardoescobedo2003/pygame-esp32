import serial
import time
from Xlib import X, display

# Obtén la pantalla
disp = display.Display()
root = disp.screen().root

# Mapea las teclas de flecha
KEY_LEFT = 0xff51
KEY_RIGHT = 0xff53

# Función para enviar una tecla presionada
def press_key(keycode):
    root.keybd_event(keycode, X.KeyPress)

# Configura el puerto serial
ser = serial.Serial('/dev/ttyUSB0', 9600)  # Ajusta el baudrate según lo configurado en tu ESP32

try:
    while True:
        # Lee una línea de datos desde el puerto serial
        line = ser.readline().decode().strip()
        
        # Imprime los datos leídos
        if line == "y4095":
            print("Derecha")
            press_key(KEY_RIGHT)  # Simula la tecla derecha
        elif line == "y0":
            print("Izquierda")
            press_key(KEY_LEFT)  # Simula la tecla izquierda
              
except KeyboardInterrupt:
    # Manejo de interrupción de teclado (Ctrl+C)
    ser.close()
    print("Serial connection closed.")
