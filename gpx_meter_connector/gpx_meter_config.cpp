#include "user_config.h"
#include "ApiConnector.hpp"

ApiConnector connector;

HardwareSerial& MeterSerial = Serial;
HardwareSerial& DebugSerial = Serial2;

void setup() {
  pinMode(CONNECTION_LED, OUTPUT);
  DebugSerial.begin(DEBUG_BAUD);
  MeterSerial.begin(METER_BAUD);

  delay(4000);

  connector.connect();

  digitalWrite(CONNECTION_LED, HIGH);
}

void loop() {
  String data = "";
  String line = "";
  while (line.length() == 0 || line.charAt(0) != '!') {
    line.clear();
    line = MeterSerial.readStringUntil('\n');
    if(line.length()) {
      line += ";;";
      line.replace('\r', ' ');
      data = data + line;
    }
  }

  DebugSerial.println(data);

  connector.sendData(data);
}

