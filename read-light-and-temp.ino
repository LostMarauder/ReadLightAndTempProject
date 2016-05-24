/*
Reading Temp and LIght
This program reads an analog signal from an LDR, and sends the output to a text file on the computer.
CODE WORKS, BUT NEED TO FIX TO GET CORRECT VALUES
MAYBE SET ANALOG REFERENCE VALUE
*/

//Declare input pin for light dependant resistor
const int ldrPin = A0;
//Declare input pin for TMP36 temperature sensor
const int temperaturePin = A1;

//Setup loop
void setup()
{
  //Setup Serial
  Serial.begin(9600);
  //Set LDR pin as analog input
  pinMode(ldrPin, INPUT);
  //Set temperature pin as analog input
  pinMode(temperaturePin, INPUT);
  
}

//Main loop
void loop()
{
  //Initialize data string
  //String dataString[1] = "";
  
  //Read the analog pin for LDR
  int rate = analogRead(ldrPin);
  
  //Read the analog pin for voltage from TMP36 (when using 5v pin)
  float voltage = 3.3 * analogRead(temperaturePin);
  voltage = voltage / 4095.0;
  //Convert voltage to temperature
  float temperatureC = (voltage - 0.5) * 100;
  
  //Output data to serial separated by tabs
  Serial.print(rate);
  Serial.print(" ");
  Serial.print(temperatureC);
  Serial.println();

  //Wait for 500 miliseconds
  delay(500);
}
