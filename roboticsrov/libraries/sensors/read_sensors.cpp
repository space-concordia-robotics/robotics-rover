#include <sensors.h>

int read_temperature(int t_pin)
{
   int temperature = analogRead(t_pin);
}

int read_voltage(int v_pin)
{
   int voltage = analogRead(v_pin);
}
