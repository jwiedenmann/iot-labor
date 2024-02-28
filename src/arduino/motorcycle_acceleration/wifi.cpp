#include "wifi.h"

namespace wifi {

char ssid[] = "iPhone von Jonas";  // your network SSID (name)
char pass[] = "Jonas1234";         // your network password (use for WPA, or use as key for WEP)

int connect() {
  led::blue();
  int result = WiFi.begin(ssid, pass);
  led::off();
  return result;
}

int status() {
  return WiFi.status();
}

}