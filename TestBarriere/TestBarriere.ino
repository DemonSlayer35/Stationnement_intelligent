#define RED_LIGHT 23
#define GREEN_LIGHT 22
#define GATE_OPEN 18
#define GATE_CLOSE 17
#define AVANT 5
#define APRES 16
#define OUVERTURE 15
#define FERMETURE 4

int c_open = 0;
int c_close = 0;
int c_avant = 0;
int c_apres = 0;



void setup() {
  // put your setup code here, to run once:
  pinMode(4,OUTPUT);
  pinMode(15,OUTPUT);
  pinMode(21, OUTPUT);
  pinMode(22, OUTPUT);
  pinMode(23,OUTPUT);
  pinMode(5, INPUT);
  pinMode(16, INPUT);
  pinMode(17, INPUT);
  pinMode(18, INPUT);
  
  Serial.begin(115200);
  digitalWrite(RED_LIGHT,HIGH);
  digitalWrite(GREEN_LIGHT,LOW);
}

void loop() {
  /*
  Serial.printf("Open : %d\n\r",(int)digitalRead(18));
  Serial.printf("Close  : %d\n\r",(int)digitalRead(17));
  Serial.printf("Capteur avant : %d\n\r",(int)digitalRead(5));
  Serial.printf("Capteur apres : %d\n\r",(int)digitalRead(16));
  */
  
  c_open = digitalRead(GATE_OPEN);
  c_close = digitalRead(GATE_CLOSE);
  c_avant = digitalRead(AVANT);
  c_apres = digitalRead(APRES);
  
  
  
  Serial.printf("Close : %d  Open : %d  apres :%d\n\r",c_close,c_open,c_apres);
  if(c_close == 0 && c_open == 1 && c_avant == 0 )// Si la barriere est fermée
  {
    digitalWrite((int)FERMETURE,LOW);
    digitalWrite((int)OUVERTURE,HIGH);
    while(c_open == 1)
    {
      c_open = digitalRead(GATE_OPEN);
      c_close = digitalRead(GATE_CLOSE);
    }
    digitalWrite(FERMETURE,LOW);
    digitalWrite(OUVERTURE,LOW);
    digitalWrite(RED_LIGHT,LOW);
    digitalWrite(GREEN_LIGHT,HIGH);
  }
  if(c_close == 1 && c_open == 0 && c_apres == 0)// Si la barriere est ouverte
  {
    digitalWrite((int)OUVERTURE,LOW);
    digitalWrite((int)FERMETURE,HIGH);
    while(c_close == 1)
    {
      c_open = digitalRead(GATE_OPEN);
      c_close = digitalRead(GATE_CLOSE);
    }
    digitalWrite(OUVERTURE,LOW);
    digitalWrite(FERMETURE,LOW);
    digitalWrite(RED_LIGHT,HIGH);
    digitalWrite(GREEN_LIGHT,LOW);
  }
  //delay(2000);
}
