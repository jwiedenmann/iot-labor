#include "imu.h"

// The value of the last bit of the I2C address.
// On the SparkFun 9DoF IMU breakout the default is 1, and when the ADR jumper is closed the value becomes 0
#define AD0_VAL 1

namespace imu {

ICM_20948_I2C myICM;

void setup() {
  Wire.begin();
  Wire.setClock(400000);

  bool initialized = false;
  while (!initialized) {
    myICM.begin(Wire, AD0_VAL);

    if (myICM.status != ICM_20948_Stat_Ok) {
      delay(500);
    } else {
      initialized = true;
    }
  }

  // Here we are doing a SW reset to make sure the device starts in a known state
  myICM.swReset();
  delay(250);
  // Now wake the sensor up
  myICM.sleep(false);
  myICM.lowPower(false);
  // Set Gyro and Accelerometer to a particular sample mode
  myICM.setSampleMode((ICM_20948_Internal_Acc | ICM_20948_Internal_Gyr), ICM_20948_Sample_Mode_Continuous);
  // myICM.setSampleMode((ICM_20948_Internal_Acc | ICM_20948_Internal_Gyr), ICM_20948_Sample_Mode_Cycled);

  // ICM_20948_smplrt_t mySmplrt;
  // mySmplrt.g = 54;
  // myICM.setSampleRate(ICM_20948_Internal_Gyr, mySmplrt);

  // Set full scale ranges for both acc and gyr
  ICM_20948_fss_t myFSS;
  myFSS.a = gpm2;
  myFSS.g = dps250;
  myICM.setFullScale((ICM_20948_Internal_Acc | ICM_20948_Internal_Gyr), myFSS);

  // Set up Digital Low-Pass Filter configuration
  ICM_20948_dlpcfg_t myDLPcfg;
  myDLPcfg.a = acc_d473bw_n499bw;
  myDLPcfg.g = gyr_d361bw4_n376bw5;
  myICM.setDLPFcfg((ICM_20948_Internal_Acc | ICM_20948_Internal_Gyr), myDLPcfg);

  // Choose whether or not to use DLPF
  ICM_20948_Status_e accDLPEnableStat = myICM.enableDLPF(ICM_20948_Internal_Acc, false);
  ICM_20948_Status_e gyrDLPEnableStat = myICM.enableDLPF(ICM_20948_Internal_Gyr, false);

  // Start the magnetometer
  myICM.startupMagnetometer();
}

int read(imuData& data) {
  if (!myICM.dataReady()) {
    return 1;
  }

  // get the data
  myICM.getAGMT();

  data.millis = millis();

  data.accX = myICM.accX();
  data.accY = myICM.accY();
  data.accZ = myICM.accZ();

  data.gyrX = myICM.gyrX();
  data.gyrY = myICM.gyrY();
  data.gyrZ = myICM.gyrZ();

  data.magX = myICM.magX();
  data.magY = myICM.magY();
  data.magZ = myICM.magZ();

  data.temp = myICM.temp();

  return 0;
}

imuData oversampleData;
int oversampleCount;

int oversample() {
  imuData tempData;
  int result = read(tempData);

  if (result == 1) return 1;

  oversampleData.accX += tempData.accX;
  oversampleData.accY += tempData.accY;
  oversampleData.accZ += tempData.accZ;

  oversampleData.gyrX += tempData.gyrX;
  oversampleData.gyrY += tempData.gyrY;
  oversampleData.gyrZ += tempData.gyrZ;

  oversampleData.magX += tempData.magX;
  oversampleData.magY += tempData.magY;
  oversampleData.magZ += tempData.magZ;

  oversampleData.temp += tempData.temp;
  oversampleCount++;

  return 0;
}

void readOversample(imuData& data) {
  unsigned long time = millis();
  oversample();

  data.millis = time;

  data.accX = oversampleData.accX / oversampleCount;
  data.accY = oversampleData.accY / oversampleCount;
  data.accZ = oversampleData.accZ / oversampleCount;

  data.gyrX = oversampleData.gyrX / oversampleCount;
  data.gyrY = oversampleData.gyrY / oversampleCount;
  data.gyrZ = oversampleData.gyrZ / oversampleCount;

  data.magX = oversampleData.magX / oversampleCount;
  data.magY = oversampleData.magY / oversampleCount;
  data.magZ = oversampleData.magZ / oversampleCount;

  data.temp = oversampleData.temp / oversampleCount;

  imuData defaultImuData;
  oversampleData = defaultImuData;
  oversampleCount = 0;
}

}