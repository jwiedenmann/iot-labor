#include "imu_queue.h"

namespace imu_queue {

imu::imuData queue[IMU_QUEUE_SIZE];
int front = -1;
int rear = -1;

int enqueue(imu::imuData data) {
  // queue is empty
  if (front == -1 && rear == -1) {
    queue[0] = data;
    front = 0;
    rear = 0;
    return 0;
  }

  int nextRear = calcEnqueueRear();
  if (nextRear == -1) {
    return 1;
  }

  queue[nextRear] = data;
  rear = nextRear;

  return 0;
}

int dequeue(imu::imuData& data) {
  // queue is empty
  if (front == -1 && rear == -1) {
    return 1;
  }

  // get element
  data = queue[front];

  // queue contains one element
  if (front == rear) {
    front = -1;
    rear = -1;
    return 0;
  }

  int nextFront = calcDequeueFront();
  if (nextFront == -1) {
    return 1;
  }

  front = nextFront;
  return 0;
}

int count() {
  if (front == -1 || rear == -1) return 0;
  else if (rear >= front) return rear - front + 1;
  else return IMU_QUEUE_SIZE - front + rear + 1;
}

int calcEnqueueRear() {
  if (front == -1 && rear == -1) {
    return 0;
  }

  int nextRear = rear + 1 >= IMU_QUEUE_SIZE ? 0 : rear + 1;
  if (nextRear == front) {
    return -1;
  }

  return nextRear;
}

int calcDequeueFront() {
  if (front == -1 && rear == -1) {
    return -1;
  }

  int nextFront = front + 1 >= IMU_QUEUE_SIZE ? 0 : front + 1;
  if (nextFront > rear) {
    return -1;
  }

  return nextFront;
}

}