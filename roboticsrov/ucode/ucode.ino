#include <sensors.h>
#include <TinyGPS.h>

const int LED_PIN = 13;

const int t_pin = 1; // temperature sensor pin
const int v_pin = 2; // voltage sensor pin

static char input[5];

// Declare variables to hold the sensors' readings
long lon, lat; // GPS data
int voltage, temperature;

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

--------------------------------------------------------------------------
 recived char | Action
--------------------------------------------------------------------------
 "r"          | read GPS and sensors data and send it to the parent board
 otherwise    | value for movement
-------------------------------------------------------------------------

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
  digitalWrite(LED_PIN, HIGH);
   
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
    // Otherwise it's a movement value
    if (val == 'r')
    {
      // Read sensors' Data
      read_gps(lon, lat); // read GPS
      temperature = read_temperature(t_pin);
      voltage = read_voltage(v_pin);
      
      /* The values of voltage and temperature right now are just
       the output of the ADC. They should be converted to their 
       actual values but thta depends on the range that the sensors
       can read. For example, a temperature reading of 1024 should
       mapped to +100 degrees if the max of the sensor is +100 */
      
      // Send data to parent board.
      // The first part of the sentence i.e. "lat: " is for debugging
      Serial.print("lat: "); Serial.println(lat);
      Serial.print("lon: "); Serial.println(lon);
      Serial.print("temperature: "); Serial.println(temperature);
      Serial.print("voltage:"); Serial.println(voltage);
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
