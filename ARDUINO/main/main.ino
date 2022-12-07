#include<Arduino_NineAxesMotion.h>
#include<Wire.h>
#include<Servo.h>

// PWM range
#define PWM_MIN 1300
#define PWM_MAX 1700

// Motor's pins
#define PIN_MOTOR_L 5
#define PIN_MOTOR_R 6

// Robot parameters
// R --> Wheel radius (mm)
// B --> Wheels distance (mm)
#define R 34
#define B 150

// Gain controller
#define GAIN_D 1
#define GAIN_H 1

// Definition of the struct containing the motor commands
struct MotorCommand{
  int motorL; // Command for left motor
  int motorR; // Command for right motor
};

// Definition of the struct containing the information transmitted by the raspberry
struct ParsedInput{
  float heading_error;  // Heading error computed by the raspberry
  float distance_error; // Distance error computed by the raspberry
};


// Motor initialisation
Servo motor_L, motor_R;

// IMU definition
NineAxesMotion motionSensor;


ParsedInput processReceivedData(const String message){
  // This function allows us to process the message received with the Serial communication
  ParsedInput data; // Struct which will contain the information extracted from the message
  int sep = message.indexOf(";"); // This the separator of the data in the message
  data.heading_error = message.substring(0,sep).toFloat(); // Retrieving first information in the message
  data.distance_error = message.substring(sep + 1).toFloat(); // Retrieving second information in the message
  return data;
}

MotorCommand computeCommand(ParsedInput errors){
  MotorCommand command;
  motorL = errors.distance_error * GAIN_D + errors.heading_error * B * GAIN_H / R; // rd/s
  motorR = errors.distance_error * GAIN_D - errors.heading_error * B * GAIN_H / R; // rd/s
  
  

}


void setup(){
  Serial.begin(117200);
  motionSensor.initSensor();
}

void loop(){
  
}