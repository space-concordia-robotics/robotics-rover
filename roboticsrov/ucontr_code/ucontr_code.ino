const int LED_PIN = 13;

void setup()
{                
  // Initialize the digital pin as an output.
  pinMode(LED_PIN, OUTPUT);   

  // Usart to talk to and from the parent board.
  Serial.begin(9600);  
  // Usart to control the left side of motors
  Serial1.begin(9600);
  //Usart to control the right side of motors
//  Serial2.begin(9600);
}

/* 
simpified serial motor mode 
switch left to right 011100
(0 = up)

motor 1
1 reverse 
64 stop
127 forward

motor 2
128 reverse
192 stop
255 forward

0 stop all motors
*/
  
void loop()
{
 
  if (Serial.available() > 0 &&
      Serial1.available() > 0) //&&
 //     Serial2.available() > 0)
  {
    unsigned char command = Serial.read();
    
    // Send command back to parent board.
//    int bytesSent = Serial.print(command);
    // Update command to motors.
    int bytesSent = Serial1.print(command);
//    Serial2.write(command);
    
  }
  
}
  
