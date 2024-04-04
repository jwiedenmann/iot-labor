#include "wifi.h"

namespace wifi {

int connect() {
  led::blue();
  int result = WiFi.begin(secrets::ssid, secrets::pass);
  led::off();
  return result;
}

int status() {
  return WiFi.status();
}

}