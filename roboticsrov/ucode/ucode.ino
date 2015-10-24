#include <TinyGPS.h>

const int LED_PIN = 13;

static char input[5];

// Declare variables to hold the longitude and latitude readings
long lon, lat;

// Declare an instance gps of type TinyGPS
TinyGPS gps;

// Function to read longitude and latitude from GPS sensor
void read_gps()
{
  while (Serial2.available())
  {
    int c = Serial2.read();
    if (gps.encode(c))
    {
      unsigned long fix;
      gps.get_position(&lat,&lon,&fix);
    }
  }
}


void setup()
{                
  // Initialize the digital pin as an output.
  pinMode(LED_PIN, OUTPUT);   

  // Usart to talk to and from the parent board.
  Serial.begin(9600);  
  // Usart to control the left side of motors
  Serial1.begin(9600);
  
  // Initialize Serial2 to communicate with the GPS sensor
  Serial2.begin(4800);
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
    
    // If we receive 'r' then read the GPS data 
    //otherwise it's a movement value
    if (val == 'r')
    {
      // Read gps Data
      read_gps();
      // Send data to parent board.
      // The first part of the sentence i.e. "lat: " is for debugging
      Serial.print("lat: "); Serial.println(lat);
      Serial.print("lon: "); Serial.println(lon);
    }
    else
    {
    // Write back to serial port for debugging
    Serial.println(val);
    // Write value to motors
    Serial1.write(val);
    } 
  }
}
