#include <CurieIMU.h>

void setup() {
  pinMode(13, OUTPUT);
  Serial.begin(115200);
  CurieIMU.begin();
}

void loop() {
  updateSensors();
  delay(50);
}

void updateSensors() {
    int x, y, z;
    int val;

    val = analogRead(0); // pot. attached to ADC0
    CurieIMU.readAccelerometer(x, y, z);

  Serial.print(val);
  Serial.print(" ");
  Serial.print(x);
  Serial.print(" ");
  Serial.print(y);
  Serial.print(" ");
  Serial.println(z);
}

