#include <HTTPClient.h>
#include <WiFi.h>

#include "ApiConnector.hpp"

#include "user_config.h"

ApiConnector::ApiConnector() {

}

void ApiConnector::connect() {
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);

  bool led = false;
  while (WiFi.status() != WL_CONNECTED) {
    DebugSerial.println("Connecting to WiFi " WIFI_SSID);
    delay(1000);
    digitalWrite(CONNECTION_LED, led = !led);
  }

  DebugSerial.println("Connected to the WiFi network");
}

bool ApiConnector::sendData(const String& data) {

  if (WiFi.status() == WL_CONNECTED) {   //Check WiFi connection status

    HTTPClient http;

    http.begin(API_ENDPOINT);
    http.addHeader("Content-Type", HEADER_API_CONTENT_TYPE);
    http.addHeader("User-Agent", HEADER_API_USER_AGENT);

    String payload = "{\"id\":" DEVICE_ID ",\"raw\":\"";
    payload += data;
    payload += "\"}";


    DebugSerial.println("data");
    DebugSerial.println(data);
    DebugSerial.println("payload");
    DebugSerial.println(payload);

    int httpResponseCode = http.POST(payload);

    if (httpResponseCode > 0) {

      String response = http.getString();                       //Get the response to the request

      DebugSerial.println(httpResponseCode);   //Print return code
      DebugSerial.println(response);           //Print request answer

    } else {
      DebugSerial.print("Error on sending POST: ");
      DebugSerial.println(httpResponseCode);
      return false;
    }

    http.end();  //Free resources
    return true;
  } else {
    return false;
  }
}
