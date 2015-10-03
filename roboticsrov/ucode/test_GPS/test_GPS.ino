char b;

void setup()
{
  pinMode(13, OUTPUT);
  Serial.begin(4800);
  
  //delay(5000);
  //Serial.print("$PSRF100,1,9600,8,1,0*0<CR><LF>");
}

void loop()
{
  if (Serial.available() > 0)
  {
    digitalWrite(13, HIGH);
  
  b = Serial.read();
  
  Serial.print(b);
  }
}
