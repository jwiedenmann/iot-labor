#include "mqtt.h"

namespace mqtt {

std::string imuDataToJson(const imu::imuData& data);

WiFiClient wifiClient;
MqttClient mqttClient(wifiClient);

int connect() {
  led::write(102, 0, 102);
  mqttClient.setUsernamePassword(secrets::mqtt_user, secrets::mqtt_pass);
  int result = mqttClient.connect(secrets::broker, secrets::port);
  led::off();

  return result;
}

int send(const imu::imuData& data) {
  mqttClient.beginMessage(secrets::topic);
  std::string s = imuDataToJson(data);
  mqttClient.print(s.data());
  return mqttClient.endMessage();
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