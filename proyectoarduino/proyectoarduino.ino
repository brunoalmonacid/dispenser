#include <Servo.h>

Servo miServo;  // Crea un objeto servo

void setup() {
  Serial.begin(9600);  // Inicia la comunicación serial
  miServo.attach(9);   // Conecta el servomotor al pin 9
  miServo.write(0);    // Posición inicial del servo
}

void loop() {
  if (Serial.available()) { // Verifica si hay datos en el buffer
    char cmd = Serial.read(); // Lee el dato

    if (cmd == '1') { // Si recibe '1', mueve el servo
      miServo.write(90); // Mueve el servo a 90 grados
    } else if (cmd == '0') { // Si recibe '0', regresa el servo
      miServo.write(0); // Mueve el servo a 0 grados
    }
  }
}