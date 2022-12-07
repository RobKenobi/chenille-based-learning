#include<Arduino_NineAxesMotion.h>
#include<Wire.h>
#include<Servo.h>

NineAxesMotion motionSensor;

void setup(){
  motionSensor.begin(0x28);
}

void loop(){
  
}