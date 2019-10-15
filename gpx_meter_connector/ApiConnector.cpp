#include <HTTPClient.h>
#include <WiFi.h>

#include "ApiConnector.hpp"

#include "user_config.h"

ApiConnector::ApiConnector() {

}

void ApiConnector::connect() {
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);

  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.print("Connecting to WiFi ");
    Serial.println(WIFI_SSID);
  }

  Serial.println("Connected to the WiFi network");
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


    Serial.println("data");
    Serial.println(data);
    Serial.println("payload");
    Serial.println(payload);

    int httpResponseCode = http.POST(payload);

    if (httpResponseCode > 0) {

      String response = http.getString();                       //Get the response to the request

      Serial.println(httpResponseCode);   //Print return code
      Serial.println(response);           //Print request answer

    } else {
      Serial.print("Error on sending POST: ");
      Serial.println(httpResponseCode);
      return false;
    }

    http.end();  //Free resources
    return true;
  } else {
    return false;
  }
}
