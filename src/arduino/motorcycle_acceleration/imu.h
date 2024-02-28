#ifndef IMU_DEFINE
#define IMU_DEFINE

#include "ICM_20948.h"

namespace imu {

typedef struct {
  long millis;
  float accX;
  float accY;
  float accZ;
  float gyrX;
  float gyrY;
  float gyrZ;
  float magX;
  float magY;
  float magZ;
  float temp;
} imuData; // 44 bytes (should be 48, but ok)

extern ICM_20948_I2C myICM;

void setup();
int read(imuData& data);

}

#endif