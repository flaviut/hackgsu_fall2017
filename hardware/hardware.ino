#include <CurieIMU.h>
#include <CurieBLE.h>


BLEPeripheral blePeripheral;       // BLE Peripheral Device (the board you're programming)
BLEService doorService("9B9B");

BLECharacteristic doorChar("5BF9",  // standard 16-bit characteristic UUID
    BLERead | BLENotify, 16);  // remote clients will be able to get notifications if this characteristic changes
                              // the characteristic is 2 bytes long as the first field needs to be "Flags" as per BLE specifications
                              // https://developer.bluetooth.org/gatt/characteristics/Pages/CharacteristicViewer.aspx?u=org.bluetooth.characteristic.heart_rate_measurement.xml

void setup()
{
  Serial.begin(115000);
  CurieIMU.begin();
  blePeripheral.setLocalName("DoorSensor");
  blePeripheral.setAdvertisedServiceUuid(doorService.uuid());  // add the service UUID
  blePeripheral.addAttribute(doorService);   // Add the BLE door sensor service
  blePeripheral.addAttribute(doorChar); // add the door sensor characteristic

  /* Now activate the BLE device.  It will start continuously transmitting BLE
     advertising packets and will be visible to remote BLE central devices
     until it receives a new connection */
  blePeripheral.begin();

}

void write_int_to_array(uint32_t v, unsigned char target[]) {
  target[0] = v >> 24 & 0xFF;
  target[1] = v >> 16 & 0xFF;
  target[2] = v >>  8 & 0xFF;
  target[3] = v >>  0 & 0xFF;
}
void loop()
{
  BLECentral central = blePeripheral.central();
  
  while (central && central.connected()) {
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
    delay(50);
  }
}

