# include <Arduino_NineAxesMotion.h> // Contains the bridge code between the API and the Arduino Environment
# include <Wire.h>

NineAxesMotion mySensor; // Object that for the sensor
unsigned long lastStreamTime = 0; // To store the last streamed time stamp
const int streamPeriod = 20; // To stream at 50 Hz without using additional timers ( time period (ms) =1000/ frequency (Hz))

float getRobotYaw () {
  if (( millis () - lastStreamTime ) >= streamPeriod ) {
    lastStreamTime = millis () ;
    mySensor . updateEuler () ; // Update the Euler data into the structure of the object
    return mySensor.readEulerHeading();
  }
}

void setup() //This code is executed once
{
  //Peripheral Initialization
  Serial.begin(115200);           //Initialize the Serial Port to view information on the Serial Monitor
  Wire1.begin();                    //Initialize I2C communication to the let the library communicate with the sensor.
  //Sensor Initialization
  mySensor.initSensor();          //The I2C Address can be changed here inside this function in the library
  mySensor.setOperationMode(OPERATION_MODE_NDOF);   //Can be configured to other operation modes as desired
  mySensor.setUpdateMode(MANUAL);  //The default is AUTO. Changing to MANUAL requires calling the relevant update functions prior to calling the read functions
  //Setting to MANUAL requires fewer reads to the sensor
}

void loop() //This code is looped forever
{     
      unsigned long time = millis();
      Serial.println("Time : "+ (String)time + " ms " + "H: " + getRobotYaw() + " deg");
      delay(100);
  }
