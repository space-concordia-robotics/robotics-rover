#include <SoftwareSerial.h>
#include <TinyGPS.h>


long lon, lat;
unsigned long fix;

TinyGPS gps;

void setup()
{
  Serial.begin(4800);
  Serial1.begin(4800);
}

void loop()
{
  while (Serial.available())
  {
    int c = Serial.read();
    if (gps.encode(c))
    {
      gps.get_position(&lat,&lon,&fix);
    }
  }
  
  Serial.print("lat: "); Serial.println(lat);
  Serial.print("lon: "); Serial.println(lon);
}
