#ifndef WIFI_DEFINE
#define WIFI_DEFINE

#include "led.h"

#include <WiFiNINA.h>

namespace wifi {

extern char ssid[];  // your network SSID (name)
extern char pass[];  // your network password (use for WPA, or use as key for WEP)

int connect();
int status();

}

#endif