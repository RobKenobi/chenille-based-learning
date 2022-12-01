
// Definition of the struct containing the information transmitted by the raspberry
struct ErrorInput{
  float heading_error;  // Heading error computed by the raspberry
  float distance_error; // Distance error computed by the raspberry
};


ErrorInput processReceivedData(const String message){
  ErrorInput error;
  int sep = message.indexOf(";");
  error.heading_error = message.substring(0,sep);
}

void setup() {
  Serial.begin(115200); // Initialize communication with the computer
}

String message;

void loop() {
  if (Serial1.available()){
      message = Serial.readStringUntil('\n');  // Read the data transmitted until the character RL is found
  }
}
