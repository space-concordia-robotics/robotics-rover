**Thermistor INFO**

- The Arduino code returns "Current Temperature: {temp in Celsius}"
- 10K resistor must be placed BEFORE 10K NTC thermistor (in Series: 5v > 10K Resistor > A0 pin > 10K NTC Thermistor > GND)
- Swapping this thermistor with another WILL NOT WORK. Each new thermistor must be recalibrated (and properly)
- Here are the calibration values {Resitance in Ohms} --> {Temperature in Celcius}: {10625.00, 28015.65 , 690.0} --> {23.6, 3.1, 99.8}
- Here are the A, B, C values used in the Steinhart-Hart Equation
	-	A = 0.001096024709
	-	B = 0.0002398158831
	-	C = 0.00000006336295474
- Use this website if recalibration is required --> http://www.thinksrs.com/downloads/programs/Therm%20Calc/NTCCalibrator/NTCcalculator.htm

This was completed by Anthony Andreoli and Tom Serrano