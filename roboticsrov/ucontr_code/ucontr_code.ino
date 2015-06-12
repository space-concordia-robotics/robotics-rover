//
//void setup()
//{
////  pinMode(3, OUTPUT);
////  pinMode(5, OUTPUT);
//  
//  Serial.begin(9600);
//  
// /*
//  noInterrupts();
//  TCNT1 = 0;
//  TCCR1A = 0;
//  TCCR1B = 0;
//  
//  TCCR1A |= (1<<WGM11) | (0<<WGM10);
//  TCCR1B |= (1<<WGM13) | (1<<WGM12) | (0<<CS12) | (1<<CS11) | (1<<CS10);
//  
//  ICR1 = 8000;
//  OCR1A = 4000;
////  OCR1B = 256;
//  
//  TIMSK1 |= (1<<OCIE1A);// | (1<<TOIE1);
//  interrupts();
//  */
//
//}
///*
//ISR(TIMER1_COMPA_vect)
//{
//  digitalWrite(13, LOW);
//}
//
//
//ISR(TIMER1_OVF_vect)
//{
//  digitalWrite(13, HIGH);
//}
//*/
//
//void loop()
//{
////  digitalWrite(3, HIGH);
////  digitalWrite(5, HIGH);
//  
////  analogWrite(3, pwmVal);
////  analogWrite(5, pwmVal);
//
////  unsigned char pwmVal = Serial.read();
//  
////  if(pwmVal >= 0 || pwmVal <= 255)
////  {
////    Serial.write(pwmVal);
//    analogWrite(A0, 64);
////  }
//  
//  delay(500);
//
//  
//
//}
//



int LED_PIN = 13;


void setup()
{                
  // initialize the digital pin as an output.
  pinMode(LED_PIN, OUTPUT);  
  

  Serial.begin(9600);  
//  Serial1.begin(9600); 
}

void loop()
{
  //read port 0 (computer)
  //write port 1 (motor driver)
  if (Serial.available() > 0)
  {
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
    
    
    unsigned char command = Serial.read();
    
    Serial.print(command);
    
 //   Serial1.write(command);
  }
  
}
  
