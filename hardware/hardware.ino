#include <CurieIMU.h>
#include <CurieBLE.h>


BLEPeripheral blePeripheral;       // BLE Peripheral Device (the board you're programming)
BLEService doorService("9c856326-4517-407e-a661-faba175acdfe");

BLEIntCharacteristic potChar(
  "6f9af486-ee00-43ac-8df6-897e05af1aa6",
  BLERead | BLENotify);
BLEIntCharacteristic xChar(
  "7c38e88a-2724-4aae-96eb-78857589fa3c",
  BLERead | BLENotify);
BLEIntCharacteristic yChar(
  "301d6851-ce6d-4fca-9a43-ffe6535b2715",
  BLERead | BLENotify);
BLEIntCharacteristic zChar(
  "fe1088ce-68ca-4a4d-ae91-797d046db6e7",
  BLERead | BLENotify);
  
void setup()
{
  pinMode(13, OUTPUT);
  Serial.begin(115000);
  CurieIMU.begin();
  blePeripheral.setLocalName("DoorSensor");
  blePeripheral.setAdvertisedServiceUuid(doorService.uuid());  // add the service UUID
  blePeripheral.addAttribute(doorService);   // Add the BLE door sensor service
  blePeripheral.addAttribute(potChar);
  blePeripheral.addAttribute(xChar);
  blePeripheral.addAttribute(yChar);
  blePeripheral.addAttribute(zChar);
  potChar.setValue(0);
  xChar.setValue(0);
  yChar.setValue(0);
  zChar.setValue(0);

  /* Now activate the BLE device.  It will start continuously transmitting BLE
     advertising packets and will be visible to remote BLE central devices
     until it receives a new connection */
  Serial.println("Beginning work");
  blePeripheral.begin();
}

long previousMillis = 0;  // last time the heart rate was checked, in ms

void loop() {
  // listen for BLE peripherals to connect:
  BLECentral central = blePeripheral.central();

  // if a central is connected to peripheral:
  if (central) {
    Serial.print("Connected to central: ");
    // print the central's MAC address:
    Serial.println(central.address());
    // turn on the LED to indicate the connection:
    digitalWrite(13, HIGH);

    // check the heart rate measurement every 200ms
    // as long as the central is still connected:
    while (central.connected()) {
      long currentMillis = millis();
      // if 200ms have passed, check the heart rate measurement:
      if (currentMillis - previousMillis >= 50) {
        previousMillis = currentMillis;
        Serial.println("updating sensors");
        updateSensors();
      }
    }
    // when the central disconnects, turn off the LED:
    digitalWrite(13, LOW);
    Serial.print("Disconnected from central: ");
    Serial.println(central.address());
  }
}

void updateSensors() {
    int x, y, z;
    int val;
    
    val = analogRead(0); // pot. attached to ADC0
    CurieIMU.readAccelerometer(x, y, z);
      
    potChar.setValue(val);
    xChar.setValue(x);
    yChar.setValue(y);
    zChar.setValue(z);
}

