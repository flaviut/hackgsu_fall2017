#include <CurieIMU.h>
#include <CurieBLE.h>


BLEPeripheral blePeripheral;       // BLE Peripheral Device (the board you're programming)
BLEService doorService("9c856326-4517-407e-a661-faba175acdfe");

BLECharacteristic doorChar(
  "6f9af486-ee00-43ac-8df6-897e05af1aa6",  // standard 16-bit characteristic UUID
  BLERead | BLENotify, 17);  // remote clients will be able to get notifications if this characteristic changes
                             // the characteristic is 2 bytes long as the first field needs to be "Flags" as per BLE specifications
                             // https://developer.bluetooth.org/gatt/characteristics/Pages/CharacteristicViewer.aspx?u=org.bluetooth.characteristic.heart_rate_measurement.xml

void setup()
{
  pinMode(13, OUTPUT);
  Serial.begin(115000);
  CurieIMU.begin();
  blePeripheral.setLocalName("DoorSensor");
  blePeripheral.setAdvertisedServiceUuid(doorService.uuid());  // add the service UUID
  blePeripheral.addAttribute(doorService);   // Add the BLE door sensor service
  blePeripheral.addAttribute(doorChar); // add the door sensor characteristic

  /* Now activate the BLE device.  It will start continuously transmitting BLE
     advertising packets and will be visible to remote BLE central devices
     until it receives a new connection */
  Serial.println("Beginning work");
  blePeripheral.begin();
}

void write_int_to_array(uint32_t v, unsigned char target[]) {
  target[0] = v >> 24 & 0xFF;
  target[1] = v >> 16 & 0xFF;
  target[2] = v >>  8 & 0xFF;
  target[3] = v >>  0 & 0xFF;
}

int oldHeartRate = 0;  // last heart rate reading from analog input
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
    unsigned char output[17];
    memset(output, 0, sizeof(output));
    
    int val = analogRead(0); // pot. attached to ADC0
    CurieIMU.readAccelerometer(x,y,z);
  
    write_int_to_array((uint32_t)val, &output[1]);
    write_int_to_array((uint32_t)x, &output[5]);
    write_int_to_array((uint32_t)y, &output[9]);
    write_int_to_array((uint32_t)z, &output[13]);
    doorChar.setValue(output, 17);
}

