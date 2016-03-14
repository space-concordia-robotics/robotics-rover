#include <TinyGPS.h>

void read_gps(long lon, long lat)
{
  while (Serial2.available())
  {
    TinyGPS gps;
    int c = Serial2.read();
    if (gps.encode(c))
    {
      unsigned long fix;
      gps.get_position(&lat,&lon,&fix);
    }
  }
}
