#ifndef USER_CONFIG_H
#define USER_CONFIG_H

#define GPX_METER_CONNECTOR_VERSION "1.0"

/** System config **/
#define ENABLE_DEBUG 1
#define SERIAL_BAUD 115200
#define METER_BAUD 9600

/** API connector settings **/
#define API_HOST "192.168.1.104"
#define HEADER_API_CONTENT_TYPE "application/json"
#define HEADER_API_USER_AGENT "gpxMeterConnector/" GPX_METER_CONNECTOR_VERSION
#define API_ENDPOINT "http://" API_HOST ":3000/measurements"

/** Default ESP configurations **/
#define DEVICE_ID             "1"
#define WIFI_SSID             "Kali"
#define WIFI_PASSWORD         "Cheesecake"
#define APIKEY                ""


#endif