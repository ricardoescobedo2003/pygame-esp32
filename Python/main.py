import pyautogui

# Define los límites del eje Y
Y_MIN = 0
Y_MAX = 1023

# Define las teclas asociadas a la izquierda y derecha
TECLA_IZQUIERDA = 'left'
TECLA_DERECHA = 'right'

while True:
    # Simula la lectura del eje Y (aquí puedes reemplazar con la lectura real del joystick)
    valor_y = int(input("Ingrese el valor del eje Y (entre 0 y 1023): "))

    # Calcula la posición normalizada del eje Y
    posicion_normalizada = (valor_y - Y_MIN) / (Y_MAX - Y_MIN)

    # Mapea la posición normalizada al rango de -1 a 1
    posicion_mapeada = (posicion_normalizada - 0.5) * 2

    # Si el eje Y está cerca de su valor mínimo, simula la tecla izquierda
    if posicion_mapeada < -0.5:
        pyautogui.keyDown(TECLA_IZQUIERDA)
    elif posicion_mapeada > 0.5:  # Si el eje Y está cerca de su valor máximo, simula la tecla derecha
        pyautogui.keyDown(TECLA_DERECHA)
    else:
        pyautogui.keyUp([TECLA_IZQUIERDA, TECLA_DERECHA])  # Si no, asegúrate de que ninguna tecla esté presionada
