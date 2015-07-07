const int LED_PIN = 13;

static char input[5];

void setup()
{                
  // Initialize the digital pin as an output.
  pinMode(LED_PIN, OUTPUT);   

  // Usart to talk to and from the parent board.
  Serial.begin(9600);  
  // Usart to control the left side of motors
  Serial1.begin(9600);
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

/*

Protocol for micro <--> uManager ????

"m" + value for movement
"r" + sensor to read sensor data  or have a timed interval to send data to  uManager
...

unsigned long readCommand()
{
  union u_tag
  {
    byte b[4];
    unsigned long ulval;
  } u;
  
  u.b[0] = Serial.read();
  u.b[1] = Serial.read();
  u.b[2] = Serial.read();
  u.b[3] = Serial.read();
  return u.ulval;
}
*/

void loop()
{
 
  if (Serial.available() > 0)
//      Serial1.available() > 0) //&&
 //     Serial2.available() > 0)
  {
    
//    int command = Serial.parseInt();
//    static char c = Serial.read();
//    static char c = Serial.read();
    
//    int command = atoi(&c);
     
     
    // Send command back to parent board.
//    Serial.println(command, DEC);
    // Update command to motors.
//    Serial1.write(command);
//    Serial2.write(command);
  
   
    int val = Serial.read();

    // Write back to serial port for debugging
    Serial.println(val);
    // Write value to motors
    Serial1.write(val); 
    
  }
}
  
