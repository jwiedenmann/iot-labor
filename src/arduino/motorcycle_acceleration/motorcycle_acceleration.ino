#include "led.h"
#include "wifi.h"
#include "imu.h"
#include "imu_queue.h"
#include "mqtt.h"

int connectToWifi(int attempts = 5, int delayTime = 0);
int connectToMqtt(int attempts = 5, int delayTime = 0);

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
}

bool wasWifiDisconnected = false;
bool hasMqttConnection = false;

imu::imuData read_data;
imu::imuData push_data;

unsigned long lastDataCollection = 0;
int dataCollectionIntervall = 100;  // 100ms

unsigned short lastUploadSpeed = 0;  // Time for the last data push in ms

void loop() {
  // ensure wifi connection
  // reconnect if wifi connection is lost
  if (wifi::status() != WL_CONNECTED) {
    wasWifiDisconnected = true;
    connectToWifi(10, 1000);
    connectToMqtt(5, 1000);
    return;
  }

  // emtpty the queue if wifi was disconnected
  if (wasWifiDisconnected) {

    while (imu_queue::count() > 0 && hasMqttConnection == 1) {
      imu_queue::dequeue(push_data);
      hasMqttConnection = mqtt::send(push_data);
    }

    // retry if mqtt push was not successful
    wasWifiDisconnected = !hasMqttConnection;
    return;
  }

  // correct abnormal upload speed measurement
  lastUploadSpeed = lastUploadSpeed > 90 ? 0 : lastUploadSpeed;

  // wifi is connected
  // mqtt may not be connected

  // collect data
  unsigned long currentTime = millis();
  if (currentTime - lastDataCollection >= dataCollectionIntervall) {
    imu::read(read_data);
    imu_queue::enqueue(read_data);
    led::gradientRedGreen(imu_queue::count(), IMU_QUEUE_SIZE);
    lastDataCollection = currentTime;
  }

  // try to send data
  // push data if elapsed time plus time for push is smaller than the time left (minus a buffer)
  currentTime = millis();
  if ((imu_queue::count() > 0 || !hasMqttConnection)
      && currentTime - lastDataCollection + lastUploadSpeed < dataCollectionIntervall - 2) {

    // only dequeue if the last element was pushed
    if (hasMqttConnection) {
      imu_queue::dequeue(push_data);
    } else {
      connectToMqtt(1, 0);
    }

    hasMqttConnection = mqtt::send(push_data);
    lastUploadSpeed = millis() - currentTime;

    // delay to not stress mqtt
    int delayTime = 10 - lastUploadSpeed;
    if (delayTime > 0) {
      delay(delayTime);
    }
  }

  // adjust data collection speed based on upload speed and connection status
  if (!hasMqttConnection) {
    dataCollectionIntervall = 100;
  } else if (lastUploadSpeed < 10) {
    dataCollectionIntervall = 25;
  } else if (lastUploadSpeed < 20) {
    dataCollectionIntervall = 50;
  } else {
    dataCollectionIntervall = 100;
  }
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