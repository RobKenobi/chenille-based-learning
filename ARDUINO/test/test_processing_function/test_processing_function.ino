
// Definition of the struct containing the information transmitted by the raspberry
struct ParsedInput{
  float heading_error;  // Heading error computed by the raspberry
  float distance_error; // Distance error computed by the raspberry
};


ParsedInput processReceivedData(const String message){
  // This function allows us to process the message received with the Serial communication
  ParsedInput data; // Struct which will contain the information extracted from the message
  int sep = message.indexOf(";"); // This the separator of the data in the message
  data.heading_error = message.substring(0,sep).toFloat(); // Retrieving first information in the message
  data.distance_error = message.substring(sep + 1).toFloat(); // Retrieving second information in the message
  return data;
}


void setup() {
  Serial.begin(115200); // Initialize communication with the computer
  Serial1.begin(115200); // Initialize communication with the raspberry
}

String message;

void loop() {
  if (Serial1.available()){
      message = Serial1.readStringUntil('\n');  // Read the data transmitted until the character RL is found
      message.trim();
      ParsedInput error = processReceivedData(message);
      Serial.println("Received : " + String(error.heading_error) + " ; " + String(error.distance_error));
  delay(1000);
  }
}