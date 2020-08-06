int threeway = 24;
int twoway_1 = 25;
int twoway_2 = 27;
int twoway_3 = 29;
int twoway_4 = 31;
int twoway_5 = 33;
int twoway_6 = 35;
int twoway_7 = 37;
int twoway_8 = 49;
float Pressure;
float Temperature;
String DataString;
char PrintData[48];
#include <AMS.h>

AMS AMSa(5915, 0x28,-1000,1000 );

void setup() {
  Serial.begin(9600);
  pinMode(threeway, OUTPUT);
  pinMode(twoway_1, OUTPUT);
  pinMode(twoway_2, OUTPUT);
  pinMode(twoway_3, OUTPUT);
  pinMode(twoway_4, OUTPUT);
  pinMode(twoway_5, OUTPUT);
  pinMode(twoway_6, OUTPUT);
  pinMode(twoway_7, OUTPUT);
  pinMode(twoway_8, OUTPUT);
  digitalWrite(twoway_1, LOW);
  digitalWrite(twoway_2, LOW);
  digitalWrite(twoway_3, LOW);
  digitalWrite(twoway_4, LOW);
  digitalWrite(twoway_5, LOW);
  digitalWrite(twoway_6, LOW);
  digitalWrite(twoway_7, LOW);
  digitalWrite(twoway_8, LOW);
  digitalWrite(threeway, LOW);
}

void loop() {
  // put your main code here, to run repeatedly:
  //Option 2: read pressure values only
  if (AMSa.Available() == true) {
  //read AMS 5915's pressure data only
      Pressure = AMSa.readPressure();
      if (isnan(Pressure)) {
        Serial.print("Please check the sensor family name.");
         }
      else {
        DataString = String(Pressure) + " mbar \n";
        DataString.toCharArray(PrintData, 24);
        Serial.print(PrintData);}
        delay(200);
    }
      else {
        Serial.print("The sensor did not answer.");
        delay(400);
    }
      pressure_valves();
       break;
    }

void pressure_valves(){
  //0: initiation set all to atm
  
  digitalWrite(twoway_1, HIGH); 
  digitalWrite(twoway_2, HIGH);
  digitalWrite(twoway_4, HIGH);
  digitalWrite(twoway_5, HIGH);
  digitalWrite(twoway_6, HIGH);
  digitalWrite(twoway_8, HIGH);
  delay(??);
  digitalWrite(twoway_3, LOW);
  digitalWrite(twoway_7, LOW);
  delay(??);

  //1: pump on
  
  //2: fill r2 with plu
  digitalWrite(twoway_1, HIGH);
  delay(5000);
  digitalWrite(twoway_1, LOW); // on valve 1 5 seconds and off
  digitalWrite(twoway_2, HIGH);
  digitalWrite(twoway_4, HIGH);
  digitalWrite(twoway_8, HIGH);
  delay(??);
  digitalWrite(twoway_2, LOW);
  digitalWrite(twoway_4, LOW);
  digitalWrite(twoway_8, LOW);
  delay(10);

  //3: fill channel with plu
  digitalWrite(twoway_1, HIGH);
  delay(5000);
  digitalWrite(twoway_1, LOW);
  digitalWrite(twoway_2, HIGH);
  digitalWrite(twoway_3, HIGH);
  digitalWrite(twoway_8, HIGH);
  delay(??);
  digitalWrite(twoway_2, LOW);
  digitalWrite(twoway_3, LOW);
  digitalWrite(twoway_8, LOW);
  delay(10);

  //4: clear r1 of plu
  digitalWrite(twoway_1, HIGH);
  digitalWrite(threeway, HIGH);
  delay(5000);
  digitalWrite(twoway_1, LOW);
  digitalWrite(twoway_4, HIGH);
  digitalWrite(twoway_8, HIGH);
  delay(??);
  digitalWrite(twoway_4, LOW);
  digitalWrite(twoway_8, LOW);
  digitalWrite(threeway, LOW);
  delay(10);

  //5: fill r1 with pbs
  digitalWrite(twoway_1, HIGH);
  delay(5000);
  digitalWrite(twoway_1, LOW);
  digitalWrite(twoway_5, HIGH);
  digitalWrite(twoway_8, HIGH);
  delay(??);
  digitalWrite(twoway_5, LOW);
  digitalWrite(twoway_8, LOW);
  delay(10);

  //6: repeat 6 and 7 for flushing
  digitalWrite(twoway_1, HIGH);
  digitalWrite(threeway, HIGH);
  delay(5000);
  digitalWrite(twoway_1, LOW);
  digitalWrite(twoway_6, HIGH);
  digitalWrite(twoway_8, HIGH);
  delay(??);
  digitalWrite(twoway_6, LOW);
  digitalWrite(twoway_8, LOW);
  digitalWrite(threeway, LOW);
  delay(10);

  //7: repeat 6 and 7 for flushing
  digitalWrite(twoway_1, HIGH);
  delay(5000);
  digitalWrite(twoway_1, LOW);
  digitalWrite(twoway_5, HIGH);
  digitalWrite(twoway_8, HIGH);
  delay(??);
  digitalWrite(twoway_5, LOW);
  digitalWrite(twoway_8, LOW);
  delay(10);

  //8: clear r1 of pbs
  digitalWrite(twoway_1, HIGH);
  digitalWrite(threeway, HIGH);
  delay(5000);
  digitalWrite(twoway_1, LOW);
  digitalWrite(twoway_6, HIGH);
  digitalWrite(twoway_8, HIGH);
  delay(??);
  digitalWrite(twoway_6, LOW);
  digitalWrite(twoway_8, LOW);
  digitalWrite(threeway, LOW);
  delay(10);

  // 9: preload sample
  digitalWrite(twoway_1, HIGH);
  digitalWrite(threeway, HIGH);
  delay(5000);
  digitalWrite(twoway_1, LOW);
  digitalWrite(twoway_6, HIGH);
  delay(??);
  digitalWrite(twoway_6, LOW);
  digitalWrite(threeway, LOW);
  delay(10);

  //10: load sample
  digitalWrite(twoway_1, HIGH);
  digitalWrite(threeway, HIGH);
  delay(5000);
  digitalWrite(twoway_1, LOW);
  digitalWrite(twoway_7, HIGH);
  delay(??);
  digitalWrite(twoway_7, LOW);
  digitalWrite(threeway, LOW);
  delay(10);

  //11: start test
  digitalWrite(twoway_1, HIGH);
  digitalWrite(threeway, HIGH);
  digitalWrite(twoway_3, HIGH);
  digitalWrite(twoway_8, HIGH);
  delay(????);
  
  //12: pump OFF
  
  //13: end test all to atm
  digitalWrite(twoway_1, HIGH); 
  digitalWrite(twoway_2, HIGH);
  digitalWrite(twoway_4, HIGH);
  digitalWrite(twoway_5, HIGH);
  digitalWrite(twoway_6, HIGH);
  digitalWrite(twoway_8, HIGH);
  delay(??);
  digitalWrite(twoway_3, LOW);
  digitalWrite(twoway_7, LOW);
  delay(??);

  
}
