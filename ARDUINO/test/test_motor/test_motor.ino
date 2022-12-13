#include<Servo.h>

#define PWM_MIN 1300
#define PWM_MAX 1700
#define ZERO 1500

byte pin_motor = 6; // motor left : 5; motor right : 6

Servo motor;
void setup() {
  Serial.begin(117200);
  motor.attach(pin_motor,PWM_MIN, PWM_MAX);
}

void loop() {
  motor.writeMicroseconds(PWM_MIN);
  Serial.println("Minimum");
  delay(1000);
  motor.writeMicroseconds(ZERO);
  Serial.println("Zero");
  delay(1000);
  motor.writeMicroseconds(PWM_MAX);
  Serial.println("Maximum");
  delay(1000);
}
