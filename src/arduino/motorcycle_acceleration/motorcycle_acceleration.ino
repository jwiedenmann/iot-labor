#include "led.h"
#include "wifi.h"
#include "imu.h"
#include "imu_queue.h"
#include "mqtt.h"

int connectToWifi(int attempts = 5, int delayTime = 0);

long timestamp = 0;

void setup() {
  Serial.begin(9600);
  while (!Serial) {
    ;  // wait for serial port to connect. Needed for native USB port only
  }

  led::setup();
  led::off();

  connectToWifi(5, 1000);
  connectToMqtt(5, 1000);

  imu::setup();
  timestamp = millis();
}

imu::imuData data;
long last_data_collection = 0;

void loop() {
  long currentTime = millis();

  // work to do in a cycle
  // collect data
  // if (currentTime - last_data_collection >= 100) {
  //   imu::read(data);
  //   imu_queue::enqueue(data);
  //   led::gradientRedGreen(imu_queue::count(), IMU_QUEUE_SIZE);
  //   last_data_collection = currentTime;
  // }

  // push data away

  //reconnect if connection is down
}

int connectToWifi(int attempts, int delayTime) {
  int wifiResult = 0;
  int counter = 0;

  while (wifiResult != WL_CONNECTED && counter < attempts) {
    wifiResult = wifi::connect();

    if (wifiResult == WL_CONNECTED) {
      led::green();
    } else {
      led::red();
    }

    counter++;
    delay(delayTime);
    led::off();
  }

  return wifiResult;
}

int connectToMqtt(int attempts, int delayTime) {
  int mqttResult = 0;
  int counter = 0;

  while (!mqttResult && counter < attempts) {
    mqttResult = mqtt::connect();
    
    if (mqttResult) {
      led::green();
    } else {
      led::red();
    }

    counter++;
    delay(delayTime);
    led::off();
  }

  return mqttResult;
}
