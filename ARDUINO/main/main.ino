#include<Wire.h>
#include<Servo.h>

// PWM range
#define PWM_MIN 1300
#define PWM_MAX 1700

// Motor's pins
#define PIN_MOTOR_L 5
#define PIN_MOTOR_R 6

// Servo motor pin
#define PIN_SERVO 3

// Robot parameters
// R --> Wheel radius (mm)
// B --> Wheels distance (mm)
#define R 34
#define B 150
// Maximum speed in rd/s (evaluated experimentally)
#define MAX_SPEED 4.0

// Gain controller
#define GAIN_D 1
#define GAIN_H 1


/*
###################
  Global variables
###################
*/

// Definition of the struct containing the motor commands
struct MotorCommand{
  int motorL=1500; // Command for left motor
  int motorR=1500; // Command for right motor
  int servo=90;
};

// Definition of the struct containing the information transmitted by the raspberry
struct ParsedInput{
  float heading_error;  // Heading error computed by the raspberry
  float distance_error; // Distance error computed by the raspberry
  int servo_angle;    // Servo angle to set
};

// Motor initialisation
Servo motorL, motorR, servo;


/*
############
  Functions
############
*/

ParsedInput processReceivedData(const String message){
  // This function allows us to process the message received with the Serial communication
  ParsedInput data; // Struct which will contain the information extracted from the message
  int sep1 = message.indexOf(";"); // This the separator of the data in the message
  int sep2 = message.lastIndexOf(";");
  data.distance_error = message.substring(0,sep1).toFloat(); // Retrieving first information in the message
  data.heading_error = message.substring(sep1 + 1, sep2).toFloat(); // Retrieving second information in the message
  data.servo_angle = message.substring(sep2+1).toInt();
  return data;
}

MotorCommand computeCommand(ParsedInput errors){
  MotorCommand command;
  float motorL = errors.distance_error * GAIN_D + errors.heading_error * B * GAIN_H / R; // rd/s
  float motorR = - errors.distance_error * GAIN_D + errors.heading_error * B * GAIN_H / R; // rd/s

  // Making sure that the speed is between -MAX_SPEED and +MAX_SPEED
  motorL = max(min(MAX_SPEED, motorL), -MAX_SPEED);
  motorR = max(min(MAX_SPEED, motorR), -MAX_SPEED);
  
  // Converting the speed on the PWM scale
  motorL = 200/MAX_SPEED * motorL + 1500;
  motorR = 200/MAX_SPEED * motorR + 1500;

  command.motorL = (int)motorL;
  command.motorR = (int)motorR;
  command.servo = errors.servo_angle + 90;

  return command;
}


/*
############
  Main code
############
*/


void setup(){
  // Communication
  Serial1.begin(117200); // For communication with Raspberry

  // Motor initialization
  motorL.attach(PIN_MOTOR_L, PWM_MIN, PWM_MAX);
  motorR.attach(PIN_MOTOR_R, PWM_MIN, PWM_MAX);

  // Camera servomotor initialization
  servo.attach(PIN_SERVO);
  servo.write(90); // Camera looking forward
}

void loop(){
  MotorCommand commands;
  if (Serial1.available()){
    String message = Serial1.readStringUntil('\n');
    ParsedInput error = processReceivedData(message);
    commands = computeCommand(error);
  }
  motorL.writeMicroseconds(commands.motorL);
  motorR.writeMicroseconds(commands.motorR);
  servo.write(commands.servo);
  delay(1000);
}
