#include <WiFi.h>

#include "user_config.h"
#include "ApiConnector.hpp"

ApiConnector connector;

void setup() {
  pinMode(CONNECTION_LED, OUTPUT);
  Serial.begin(SERIAL_BAUD);
  Serial2.begin(METER_BAUD);

  delay(4000);

  connector.connect();

  digitalWrite(CONNECTION_LED, HIGH);
}

void loop() {
  String data = "";
  String line = "";
  while (line.length() == 0 || line.charAt(0) != '!') {
    line.clear();
    line = Serial2.readStringUntil('\n') + ";;";
    line.replace('\r', ' ');
    data = data + line;
  }
  connector.sendData(data);
}

