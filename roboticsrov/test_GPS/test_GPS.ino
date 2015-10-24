#include <TinyGPS.h>

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
  // Initialize Serial2 to communicate with the GPS sensor
  Serial2.begin(4800);
  Serial.begin(4800);
}

void loop()
{
  
  // Read gps Data
  read_gps();
  // Send data to parent board
  Serial.print("lat: "); Serial.println(lat);
  Serial.print("lon: "); Serial.println(lon);
}
