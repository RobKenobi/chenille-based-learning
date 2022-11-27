void setup(){
  Serial.begin(115200); // Serial connection with computer
  Serial1.begin(9600); // Serial connection with raspberry
  // Checking whether the raspeberry is connected
  while(!Serial1){
    Serial.println("Waiting for connection with raspberry"); // Printing message on connected computer
    delay(2000); // Waiting 2 seconds
  }
}

void loop(){
  Serial.println("Waiting for message...");
  int message = Serial1.read();
  Serial.println("Message received : " + String(message));
  delay(1000);
}