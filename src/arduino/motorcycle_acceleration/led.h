#ifndef LED_DEFINE
#define LED_DEFINE

#include <WiFiNINA.h>
#include <utility/wifi_drv.h>

namespace led {

void setup();
void write(int r, int g, int b);

void off();
void red();
void green();
void blue();
void gradientRedGreen(int count, int total);

}

#endif