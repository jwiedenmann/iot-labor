#ifndef WIFI_DEFINE
#define WIFI_DEFINE

#include "led.h"
#include "secrets.h"

#include <WiFiNINA.h>

namespace wifi {

// returns WL_CONNECTED on success
int connect();
int status();

}

#endif