//Direction and Power for Motors and Actuators
const int DIR1 = 23;  //DIR 1 on MDD10A, controls Base Motor Direction
const int PWM1 = 9;   //PWM 1 on MDD10A, controls Base Motor Power/Duty
const int DIR2 = 22;  //DIR 2 on MDD10A, controls Link 2 Motor Direction
const int PWM2 = 10;  //PWM 2 on MDD10A, controls Link 2 Motor Power/Duty
const int DIR = 24;   //DIR on MDD10C, controls Link 1 Motor Direction
const int PWM = 8;    //PWM on MDD10C, controls Link 1 Motor Power/Duty
const int M1 = 26;    //M1 on L298N, controls End Effector Claw Motor Direction
const int E1 = 7;     //E1 on L298N, controls End Effector Claw Motor Power/Duty
const int M2 = 25;    //M2 on L298N, controls Wrist Motor Direction
const int E2 = 6;     //E2 on L298N, controls Wrist Motor Power/Duty
const int IN1 = 29;   //IN1 on Relay Module, controls Linear Actuator Direction
const int IN2 = 30;   //IN2 on Relay Module, controls Linear Actuator Direction

//Switches and Sensors
const int Pressure_Sensor = 9;
const int Proximity_Sensor_Link1 = 28;
const int Proximity_Sensor_Link2 = 27;
int Potentiometer_Claw = 8;
const int Potentiometer_Knob = 7;
const int SWT_Base_FWD = 31;
const int SWT_Base_REV = 32; 
const int SWT_ACTU_FWD = 33;
const int SWT_ACTU_REV = 34;
const int SWT_M1_FWD = 35;
const int SWT_M1_REV = 36;
const int SWT_M2_FWD = 37;
const int SWT_M2_REV = 38;
//const int SWT_Wrist_FWD = 39;
const int SWT_Wrist_FWD = 50;
const int SWT_Wrist_REV = 40;
//const int SWT_Claw_FWD = 41;
const int SWT_Claw_FWD = 51;
const int SWT_Claw_REV = 42;

//Potentiometer_Knob Variables
int Pot_Value_Knob;

//Pressure Sensor Variables
int Pressure_Sensor_Value;

//Potentiometer_Claw Variables
int Pot_Value_Claw;

//Lock Flags
bool SWT_M1_FWD_Lock;
bool SWT_M1_REV_Lock;
bool SWT_M2_FWD_Lock;
bool SWT_M2_REV_Lock;

//Duty
int duty;

//Proximity Sensor Flag
bool Enable_Proximity_Sensors = 1;

void Query_Pot_Knob()
{
  static int prev_duty = 0;
  Pot_Value_Knob = analogRead(Potentiometer_Knob);
  duty = Pot_Value_Knob * (255.00/1023.00);
  duty = duty -(duty%21); 
  if (prev_duty != duty) 
  {
    Serial.print("Duty: ");
    Serial.println(duty);
    prev_duty = duty;
  }
}

void Query_Claw_Position()
{
  Pot_Value_Claw = analogRead(Potentiometer_Claw);
  //Serial.print("Claw Position: ");
  Serial.println(Pot_Value_Claw); 
}

void Query_Pressure_Sensors()
{
  Pressure_Sensor_Value = analogRead(Pressure_Sensor);
  //if (Pressure_Sensor_Value > 950) Serial.println("High Pressure Detected");
  //Serial.println(Pressure_Sensor_Value);
  if (Pressure_Sensor_Value < 900) Serial.println("High Pressure Detected");
}

void setup()
{
  //OUTPUT Pins
  //MDD10A
  pinMode(DIR1,OUTPUT);
  pinMode(PWM1,OUTPUT);
  pinMode(DIR2,OUTPUT);
  pinMode(PWM2,OUTPUT);
  //MDD10C
  pinMode(DIR,OUTPUT);
  pinMode(PWM,OUTPUT);
  //L298N
  pinMode(M1,OUTPUT);
  pinMode(E1,OUTPUT);
  pinMode(M2,OUTPUT);
  pinMode(E2,OUTPUT);
  //Relay Module
  pinMode(IN1,OUTPUT);
  pinMode(IN2,OUTPUT);

  //INPUT Pins
  pinMode(Proximity_Sensor_Link1,INPUT);
  pinMode(Proximity_Sensor_Link2,INPUT);
  pinMode(SWT_Base_FWD,INPUT_PULLUP);
  pinMode(SWT_Base_REV,INPUT_PULLUP);
  pinMode(SWT_ACTU_FWD,INPUT_PULLUP);
  pinMode(SWT_ACTU_REV,INPUT_PULLUP);
  pinMode(SWT_M1_FWD,INPUT_PULLUP);
  pinMode(SWT_M1_REV,INPUT_PULLUP);
  pinMode(SWT_M2_FWD,INPUT_PULLUP);
  pinMode(SWT_M2_REV,INPUT_PULLUP);
  pinMode(SWT_Wrist_FWD,INPUT_PULLUP);
  pinMode(SWT_Wrist_REV,INPUT_PULLUP);
  pinMode(SWT_Claw_FWD,INPUT_PULLUP);
  pinMode(SWT_Claw_REV,INPUT_PULLUP);

  //Initialize Duty
  Pot_Value_Knob = analogRead(Potentiometer_Knob);
  duty = Pot_Value_Knob * (255.00/1023.00);
  duty = duty -(duty%21); 

  //Initialize locks to 0
  SWT_M1_FWD_Lock = 0;
  SWT_M1_REV_Lock = 0;
  SWT_M2_FWD_Lock = 0;
  SWT_M2_REV_Lock = 0;
  
  Serial.begin(9600);
}

void loop()
{
//Turns off all motors until a while loop is active
  analogWrite(PWM1,0); //PWM digital pins need to use analogWrite, PWM is a technique for getting analog results with digital means.
  analogWrite(PWM2,0);
  analogWrite(PWM,0);
  analogWrite(E1,0);
  analogWrite(E2,0);
  digitalWrite(IN1,1); //Relay Module for actuator uses digitalWrite
  digitalWrite(IN2,1);

//Read Speed Knob
Query_Pot_Knob();  

//Switch while loops
//Base Motor
  while(!digitalRead(SWT_Base_FWD))
  {
    Serial.println("SWT_Base_FWD"); 
    Query_Pot_Knob();
    analogWrite(PWM1,duty);
    digitalWrite(DIR1,1);
  }
  
  while(digitalRead(SWT_Base_REV))//"Fixed"
  {
    Serial.println("SWT_Base_REV"); 
    Query_Pot_Knob();
    analogWrite(PWM1,duty);
    digitalWrite(DIR1,0);
  }

//Link 2
  while(!digitalRead(SWT_M2_FWD) && !SWT_M2_FWD_Lock) //FWD
  {
    Serial.println("SWT_M2_FWD"); 
    if(SWT_M2_REV_Lock && !digitalRead(Proximity_Sensor_Link2))
    {
      while(!digitalRead(SWT_M2_FWD))
      {
        if(digitalRead(Proximity_Sensor_Link2)) break;
        Query_Pot_Knob();
        analogWrite(PWM2,duty);
        digitalWrite(DIR2,0);
      }
        break;
    }
    SWT_M2_REV_Lock = 0; //Unlock REV
    if(!digitalRead(Proximity_Sensor_Link2) && Enable_Proximity_Sensors)
    {
      SWT_M2_FWD_Lock = 1;
    }
    Query_Pot_Knob();
    analogWrite(PWM2,duty);
    digitalWrite(DIR2,0);
  }
  
  while(digitalRead(SWT_M2_REV) && !SWT_M2_REV_Lock) //REV //"Fixed"
  {
    Serial.println("SWT_M2_REV");
    if(SWT_M2_FWD_Lock && !digitalRead(Proximity_Sensor_Link2))
    {
       while(digitalRead(SWT_M2_REV))
      {
       if(digitalRead(Proximity_Sensor_Link2)) break;
       Query_Pot_Knob();
       analogWrite(PWM2,duty);
       digitalWrite(DIR2,1);
      }
      break;
    }
    SWT_M2_FWD_Lock = 0; //Unlock FWD
    if(!digitalRead(Proximity_Sensor_Link2) && Enable_Proximity_Sensors)
    {
      SWT_M2_REV_Lock = 1;
    }
    Query_Pot_Knob();
    analogWrite(PWM2,duty);
    digitalWrite(DIR2,1);
  }
  

//Link 1
  while(!digitalRead(SWT_M1_FWD) && !SWT_M1_FWD_Lock)
  {
    Serial.println("SWT_M1_FWD");
    if(SWT_M1_REV_Lock && !digitalRead(Proximity_Sensor_Link1))//"Fixed"
    {
      while(!digitalRead(SWT_M1_FWD))
      {
        if(digitalRead(Proximity_Sensor_Link1)) break;
        Query_Pot_Knob();
        analogWrite(PWM,duty);
        digitalWrite(DIR,1);
      }
      break;
    }
    SWT_M1_REV_Lock = 0;
    if(!digitalRead(Proximity_Sensor_Link1) && Enable_Proximity_Sensors)
    {
      SWT_M1_FWD_Lock = 1;
    }
    Query_Pot_Knob();
    analogWrite(PWM,duty);
    digitalWrite(DIR,1);
  }
  
  while(!digitalRead(SWT_M1_REV) && !SWT_M1_REV_Lock)
  {
    Serial.println("SWT_M1_REV");
    if(SWT_M1_FWD_Lock && !digitalRead(Proximity_Sensor_Link1))//"Fixed"
    {
       while(!digitalRead(SWT_M1_REV))
       {
          if(digitalRead(Proximity_Sensor_Link1)) break;
          Query_Pot_Knob();
          analogWrite(PWM,duty);
          digitalWrite(DIR,0);
       }
       break;
    }
    SWT_M1_FWD_Lock = 0;
    if(!digitalRead(Proximity_Sensor_Link1) && Enable_Proximity_Sensors)
    {
      SWT_M1_REV_Lock = 1;
    }
    Query_Pot_Knob();
    analogWrite(PWM,duty);
    digitalWrite(DIR,0);
  }
  
//End Effector Claw Motor
  while(!digitalRead(SWT_Claw_FWD) && Pot_Value_Claw < 700)
  //while(!digitalRead(SWT_Claw_FWD))
  {
    Serial.print("SWT_Claw_FWD, Position: ");
    Query_Claw_Position();
    Query_Pressure_Sensors();
    Query_Pot_Knob();
    analogWrite(E1,duty);
    digitalWrite(M1,1);
  }
  while(digitalRead(SWT_Claw_REV))//"Fixed"
  {
    Serial.print("SWT_Claw_REV, Position: ");
    Query_Claw_Position();
    Query_Pressure_Sensors();
    Query_Pot_Knob();
    analogWrite(E1,duty);
    digitalWrite(M1,0);
  }

//Wrist Motor
  while(!digitalRead(SWT_Wrist_FWD))//"Fixed"
  {
    Serial.println("SWT_Wrist_FWD");
    Query_Pot_Knob();
    analogWrite(E2,duty);
    digitalWrite(M2,1);
  }
  while(digitalRead(SWT_Wrist_REV))//"Fixed"
  {
    Serial.println("SWT_Wrist_REV");
    Query_Pot_Knob();
    analogWrite(E2,duty);
    digitalWrite(M2,0);
  }

//Linear Actuator
  while(!digitalRead(SWT_ACTU_FWD))
  {
    Serial.println("SWT_ACTU_FWD");
    Query_Pot_Knob();
    digitalWrite(IN2,0);
  }
  while(digitalRead(SWT_ACTU_REV))//"Fixed"
  {
    Serial.println("SWT_ACTU_REV");
    Query_Pot_Knob();
    digitalWrite(IN1,0);
  }
}


