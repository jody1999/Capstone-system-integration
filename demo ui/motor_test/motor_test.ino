// Define pins
#define EN_PIN    12  // LOW: Driver enabled. HIGH: Driver disabled
#define STEP_PIN  4  // Step on rising edge
#define DIR_PIN  5  // Motor direction
#define RX_PIN    2  // SoftwareSerial pins
#define TX_PIN    3  //

// Setup camera
int Stepperspeed = 100; // Change accordingly for rotational speed
String incoming; // signal from Python
#include <SoftwareSerial.h>

// Setup UART connection to control TMC2208
SoftwareSerial mySerial(2, 3); // RX, TX

#include <TMC2208Stepper.h>

// Create driver that uses SoftwareSerial for communication
TMC2208Stepper driver = TMC2208Stepper(RX_PIN, TX_PIN);


void setup() {
  Serial.begin(115200); // for Python communication
  driver.beginSerial(115200);
  // Push at the start of setting up the driver resets the register to default
  driver.push();

  //set pin modes
  pinMode(EN_PIN, OUTPUT);
  digitalWrite(EN_PIN, HIGH); //deactivate driver (LOW active)
  pinMode(DIR_PIN, OUTPUT);
  pinMode(STEP_PIN, OUTPUT);

  digitalWrite(EN_PIN, LOW); //activate driver

  driver.pdn_disable(true);     // Use PDN/UART pin for communication
  driver.I_scale_analog(false); // Use internal voltage reference
  driver.rms_current(700);      // Set driver current = 700mA, 0.5 multiplier for hold current and RSENSE = 0.11.
  driver.toff(2);               // Enable driver in software
  driver.pwm_autoscale(true);   // Needed for stealthChop


}

void loop() {
  while (Serial.available()) { // continuously read any Python signals
    incoming = Serial.readString();
    if (incoming == "S") { // obtain set of contrast values
            delay(10);
            for (int count = 0; count < 6400; count++) { // 1600counts  = 1 revolution
              digitalWrite(DIR_PIN, HIGH); // HIGH - CW and upwards, LOW - CCW and downwards
              digitalWrite(STEP_PIN,HIGH);
              delayMicroseconds(Stepperspeed);  
              digitalWrite(STEP_PIN,LOW);
              delayMicroseconds(Stepperspeed);  // Control motor speed
            }
            for (int count = 0; count < 6400; count++) { // 1600counts  = 1 revolution
              digitalWrite(DIR_PIN, LOW); // HIGH - CW and upwards, LOW - CCW and downwards
              digitalWrite(STEP_PIN,HIGH);
              delayMicroseconds(Stepperspeed);  
              digitalWrite(STEP_PIN,LOW);
              delayMicroseconds(Stepperspeed);  // Control motor speed
          }
          break;
        }
    if (incoming == "R") { // second Python signal to keep moving downwards
      delay(10);
        for (int count = 0; count < 9600; count++) {
          digitalWrite(DIR_PIN, HIGH); 
          digitalWrite(STEP_PIN,HIGH);
          delayMicroseconds(Stepperspeed);  
          digitalWrite(STEP_PIN,LOW);
          delayMicroseconds(Stepperspeed);
          if (Serial.available()) { 
             incoming = Serial.readString();
             if (incoming == "E") { // Third Python signal to stop motor movement and exit loop
              break;
             }
          exit(0);
        }
      }
    }
    break;
   }
}
   
