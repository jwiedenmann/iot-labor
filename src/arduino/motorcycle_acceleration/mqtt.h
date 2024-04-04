#ifndef MQTT_DEFINE
#define MQTT_DEFINE

#include "led.h"
#include "imu.h"
#include "secrets.h"

#include <ArduinoMqttClient.h>
#include <string>
#include <sstream>
#include <iomanip>

namespace mqtt {

// returns 1 on success
int connect();
// returns 1 on success
int send(const imu::imuData& data);

}

#endif