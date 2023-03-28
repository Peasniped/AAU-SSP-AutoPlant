#define ADC_PIN A0       // Connect to Moisture-module pin A0 to pin A0
#define PWR_PIN 9        // Connect to Moisture-module pin VCC to pin 9
                         // Connect to Moisture-module pin GND to pin GND

#define MAX_WETNESS 300  // The minimum value measurable by the device
#define MIN_WETNESS 1023 // The maximum value measurable by the device

int MIN_WETNESS_ADJ = MIN_WETNESS - MAX_WETNESS;
int counter = 1;

void setup()
{
  Serial.begin(9600);          // Set Serial Monitor window comm speed
  pinMode(PWR_PIN, OUTPUT);    // Set pin used to power sensor as output
  digitalWrite(PWR_PIN, LOW);  // Set to LOW to turn sensor off at start
}

void loop()
{
  print_moisture();
  counter += 1;
  delay(1000);
}

int read_moisture()
{
  digitalWrite(PWR_PIN, HIGH);       // Turn sensor power on
  delay(25);                         // Allow power to settle
  int val_ADC = analogRead(ADC_PIN); // Read analog value from sensor
  digitalWrite(PWR_PIN, LOW);        // Turn sensor power off
  return val_ADC;                    // Return analog moisture value
}

int moisture_percent()
{
  float reading = read_moisture();
  reading = reading - MAX_WETNESS;                    // Adjust for MAX_WETNESS - so a reading of MAX_WETNESS is = 0
  reading = - reading + MIN_WETNESS_ADJ;              // Adjust for reversed skala, so a reading of MIN_WETNESS returns 0 and MAX_WETNESS returns 100
  reading = round((reading / MIN_WETNESS_ADJ) * 100); // Change the returned value to percent
  int percent = reading;                              // Change type to integer
  return percent;
}

void print_moisture()
{
  Serial.print(counter);
  Serial.print(" - moisture value = ");
  Serial.print(read_moisture());
  Serial.print(" - moisture percent = ");  
  Serial.println(moisture_percent());
}
