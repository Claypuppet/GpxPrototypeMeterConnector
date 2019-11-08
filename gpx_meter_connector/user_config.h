#ifndef USER_CONFIG_H
#define USER_CONFIG_H

#include <Arduino.h>

#define GPX_METER_CONNECTOR_VERSION "1.0"

/** System config **/

#define DEVICE_ID "1"

#define ENABLE_DEBUG 1
#define DEBUG_BAUD 115200
#define METER_BAUD 115200

extern HardwareSerial &MeterSerial;
extern HardwareSerial &DebugSerial;

#define CONNECTION_LED 2

/** API connector settings **/
#define API_HOST "prototype.gpxconsole01.nl"
#define HEADER_API_CONTENT_TYPE "application/json"
#define HEADER_API_USER_AGENT "gpxMeterConnector/" GPX_METER_CONNECTOR_VERSION
#define API_ENDPOINT "https://" API_HOST ":3000/measurements"

/** Default ESP configurations **/
#define WIFI_SSID ""
#define WIFI_PASSWORD ""

#endif