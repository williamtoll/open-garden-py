/*
* Willian Toledo
* @williamtoll
* Copyright 2020 
*/

volatile int pulsesCount; 
int litersPerMinute;      
int solenoidPin = 0;   
int flowMeterPin = 1;    
float facConvert = 7.5;    
int incomingByte = 0; 

void rpm ()  {      //function that is executed during the interruption
  pulsesCount++;   //increment the pulses count
} 
 
void setup() {
  
  pinMode(solenoidPin, OUTPUT);   //initialize the pin
  pinMode(flowMeterPin, INPUT);    //initialize the pin
  Serial.begin(9600);       //init the serial port
  attachInterrupt(0, rpm, RISING);  //interrupting when passing from LOW to HIGH)
}
 
void loop() {

 while(Serial.available()) {

  String a= Serial.readString();// read the incoming data as string
  
  Serial.println(a);
  if(a.equals("open")){
    digitalWrite(solenoidPin,HIGH);
  }else if(a.equals("close")){
    digitalWrite(solenoidPin,LOW);
  }
  
 }

//test the solenoid valve
//  digitalWrite(solenoidPin, HIGH);    //Switch Solenoid ON
//  delay(1000);                      //Wait 1 Second
//  digitalWrite(solenoidPin, LOW);     //Switch Solenoid OFF
//  delay(1000);                      //Wait 1 Second


  pulsesCount = 0;           //reset the pulses count
//  Interrupts();               //Habilitamos las interrupciones, equivalente a sei();
  delay (5000);           //just wait 5 secs we can adjust this
  noInterrupts();               //Deshabilitamos las interrupciones, equivalente a cli();
  litersPerMinute = (pulsesCount / facConvert);     //calculate the flow 
  Serial.print (litersPerMinute, DEC);   
  Serial.print (" L/min\r\n");    


}
