#ifndef IMU_QUEUE_DEFINE
#define IMU_QUEUE_DEFINE

#include "imu.h"

#define IMU_QUEUE_SIZE 400

namespace imu_queue {

extern imu::imuData queue[];
extern int front;
extern int rear;

int enqueue(imu::imuData data);
int dequeue(imu::imuData& data);
int count();
int calcEnqueueRear();
int calcDequeueFront();

}

#endif