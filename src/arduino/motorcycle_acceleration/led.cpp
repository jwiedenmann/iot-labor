#include "led.h"

namespace led {

void setup() {
  WiFiDrv::pinMode(26, OUTPUT);  //define RED LED
  WiFiDrv::pinMode(25, OUTPUT);  //define GREEN LED
  WiFiDrv::pinMode(27, OUTPUT);  //define BLUE LED
}

void write(int r, int g, int b) {
  WiFiDrv::analogWrite(25, r);  //RED
  WiFiDrv::analogWrite(26, g);  //GREEN
  WiFiDrv::analogWrite(27, b);  //BLUE
}

void off() {
  led::write(0, 0, 0);
};

void red() {
  led::write(255, 0, 0);
};

void green() {
  led::write(0, 255, 0);
};

void blue() {
  led::write(0, 0, 255);
};

void gradientRedGreen(int count, int total) {
    if (count < 0) count = 0;
    if (count > total) count = total;
    
    double percentage = static_cast<double>(count) / total;
    int red, green, blue = 0;

    // If percentage is 0.5 or less, blend from green to yellow
    if (percentage <= 0.5) {
        green = 255;
        red = static_cast<int>(2 * percentage * 255); // Increase red component
    }
    // If percentage is more than 0.5, blend from yellow to red
    else {
        red = 255;
        green = static_cast<int>((1.0 - (percentage - 0.5) * 2) * 255); // Decrease green component
    }

    led::write(red, green, blue);
}

}