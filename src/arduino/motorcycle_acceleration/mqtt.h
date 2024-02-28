#ifndef MQTT_DEFINE
#define MQTT_DEFINE

#include "led.h"
#include "imu.h"

#include <ArduinoMqttClient.h>
#include <string>
#include <sstream>
#include <iomanip>

namespace mqtt {

int connect();
void send(const imu::imuData& data);

}

#endif