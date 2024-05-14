#include <ezButton.h>

#define VRX_PIN  36 // Pin del ESP32 GPIO36 (ADC0) conectado al pin VRX
#define VRY_PIN  39 // Pin del ESP32 GPIO39 (ADC0) conectado al pin VRY
#define SW_PIN   17 // Pin del ESP32 GPIO17 conectado al pin SW

ezButton button(SW_PIN);

int valueX = 0; // Para almacenar el valor del eje X
int valueY = 0; // Para almacenar el valor del eje Y
int bValue = 0; // Para almacenar el valor del botón

void setup() {
  Serial.begin(9600);
  button.setDebounceTime(50); // Establecer tiempo de rebote a 50 milisegundos
}

void loop() {
  button.loop(); // DEBE llamar primero a la función loop()

  // Leer valores analógicos de X e Y
  valueX = analogRead(VRX_PIN);
  valueY = analogRead(VRY_PIN);

  // Leer el valor del botón
  bValue = button.getState();

  if (button.isPressed()) {
    Serial.println("El botón está presionado");
    // TODO: realizar alguna acción aquí
  }

  if (button.isReleased()) {
    Serial.println("El botón está suelto");
    // TODO: realizar alguna acción aquí
  }

 // Imprimir datos en el Monitor Serie del IDE de Arduino
  Serial.print("x");
  Serial.println(valueX);
  Serial.print("y");
  Serial.println(valueY);


}
