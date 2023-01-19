// ---------------------------------------------------------------- // 
// Arduino Ultrasoninc Sensor HC-SR04 
// Re-writed by Arbi Abdul Jabbaar 
// Using Arduino IDE 1.8.7 
// Using HC-SR04 Module 
// Tested on 17 September 2019 
// ---------------------------------------------------------------- // 

#define echoPin 2 // attach pin D2 Arduino to pin Echo of HC-SR04 
#define trigPin 3

// defines variables
long duration; // variable for the duration of sound wave travel 
float distance; // variable for the distance measurement  

#define sensor A0 // Sharp IR GP2Y0A41SK0F (4-30cm, analog)

void setup() { 
  pinMode(echoPin, INPUT); // Sets the echoPin as an INPUT 
  pinMode(trigPin, OUTPUT);

  Serial.begin(9600); // // Serial Communication is starting with 9600 of baudrate speed 
  Serial.println("Ultrasonic Sensor HC-SR04 Test"); // print some text in Serial Monitor 
  Serial.println("with Arduino zero"); 

} 

void loop() { 
  /*digitalWrite(trigPin, HIGH); //turn off the Trig pin incase it was on before
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW); //turn off the Trig pin incase it was on before
  
  duration = pulseIn(echoPin, HIGH); // duration en µs 

  if(duration != 0)
  {
    // Calculating the distance 
  distance = duration * 0.034 / 2; // Speed of sound wave divided by 2 (go and back) donc minimum 1.7 cm = 100 µs 

  // Displays the distance on the Serial Monitor 
  Serial.print("Distance: "); 
  Serial.print(distance); 
  Serial.println(" cm"); 

  delay(500);*/

  
  // 5v
  float volts = analogRead(sensor)*0.0048828125;  // value from sensor * (5/1024)
  float distance = 29.988 * (float)pow(volts , -1.173);
  delay(1000); // slow down serial port 

  //Serial.println(volts);
  Serial.println(distance);   // print the distance
  }
  
/*
  // 5v
  float volts = analogRead(sensor)*0.0048828125;  // value from sensor * (5/1024)
  float distance = 29.988 * (float)pow(volts , -1.173);
  delay(1000); // slow down serial port 

  //Serial.println(volts);
  Serial.println(distance);   // print the distance
} */
