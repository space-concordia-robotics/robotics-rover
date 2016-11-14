/*
 * Use this website to calculate A,B,C values for 
 * thermistor: http://www.thinksrs.com/downloads/programs/Therm%20Calc/NTCCalibrator/NTCcalculator.htm
 * must have three distinct resistor values for three distinct temperatures (ice bath, room temperature, boiling water)
 * THE CALIBRATION VALUES BELOW THIS LINE
 * R1, R2, R3 = {10625.00, 28015.65 , 690.0}
 * T1, T2, T3 = {23.6, 3.1, 99.8}
 */
 
#include <math.h>
#define THERMISTORPIN A0
int resistor = 10000;
float A=0.001096024709;
float B=0.0002398158831;
float C=0.00000006336295474;
int sizeArr = 10;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
}

void loop() {
  
  float readings[sizeArr];
  float tempRes = 0;
  
  for (int i=0; i<sizeArr; i++) {

      tempRes = getResistance(analogRead(THERMISTORPIN),resistor);
      readings[i] = getTemperature(A, B, C, tempRes);
      //readings[i] = tempRes;
    delay(100);
  }

  Serial.println("Current Temperature: " + String(getAvg(readings, sizeArr)));
 //Serial.println("Current Resistance: " + String(getAvg(readings, sizeArr)));
}

float getResistance(float analogReading, int resistor) {
  float r = 0;
  r = (1023/analogReading)-1;
  r = resistor/r;
  return r;
}

float getTemperature(float A, float B, float C, float reading) {
  float invTemp=0;
  invTemp = A + B*log(reading) + C*pow(log(reading),3);
  invTemp = 1/invTemp - 273.15;
  return invTemp;
}

float getAvg(float res[], int arraySize) {  
  float sum = 0;
  for (int i=0;i<arraySize;i++) {
        sum += res[i];
  }
  return (sum/arraySize);
}

