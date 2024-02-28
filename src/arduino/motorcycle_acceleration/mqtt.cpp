#include "mqtt.h"

namespace mqtt {

const char MQTT_USER[] = "wiedenmann";
const char MQTT_PASS[] = "Bcdrf6.x";
const char broker[] = "164.92.190.0";
const int port = 1883;
const char topic[] = "arduino/echo";

std::string imuDataToJson(const imu::imuData& data);

WiFiClient wifiClient;
MqttClient mqttClient(wifiClient);

int connect() {
  led::write(102, 0, 102);
  int result = mqttClient.connect(broker, port);
  led::off();

  return result;
}

void send(const imu::imuData& data) {
  mqttClient.beginMessage(topic);
  std::string s = imuDataToJson(data);
  mqttClient.print(s.data());
  mqttClient.endMessage();
}

std::string imuDataToJson(const imu::imuData& data) {
  std::stringstream ss;
  ss << std::fixed << std::setprecision(4);
  ss << "{"
     << "\"millis\":" << data.millis << ","
     << "\"accX\":" << data.accX << ","
     << "\"accY\":" << data.accY << ","
     << "\"accZ\":" << data.accZ << ","
     << "\"gyrX\":" << data.gyrX << ","
     << "\"gyrY\":" << data.gyrY << ","
     << "\"gyrZ\":" << data.gyrZ << ","
     << "\"magX\":" << data.magX << ","
     << "\"magY\":" << data.magY << ","
     << "\"magZ\":" << data.magZ << ","
     << "\"temp\":" << data.temp
     << "}";
  return ss.str();
}

}