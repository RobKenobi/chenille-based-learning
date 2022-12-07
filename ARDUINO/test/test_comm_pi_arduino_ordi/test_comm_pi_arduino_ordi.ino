void setup(){
  Serial.begin(115200); // Serial connection with computer
  Serial1.begin(115200); // Serial connection with raspberry
  // Checking whether the raspeberry is connected
  while(!Serial1){
    Serial.println("Waiting for connection with raspberry"); // Printing message on connected computer
    delay(2000); // Waiting 2 seconds
  }
}


void loop(){
  String message; // Defining the String variable which will store the received message
  if(Serial1.available()){  // If data are avaible in the Serial buffer
    message =  Serial1.readStringUntil('\n'); // Read the characters until you reach a line break
    Serial.println("Message received : " + message); // Printing the received message
  }
}