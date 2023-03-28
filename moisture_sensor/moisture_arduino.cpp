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
  float adj1 = reading - MAX_WETNESS;                 // Adjust for max_wetness - så en reading på 300 er = 0
  float adj2 = - adj1 + MIN_WETNESS_ADJ;              // Adjust for omvendt skala, så 1000 bliver et lavt tal og 300 bliver et højt tal
  float adj3 = round((adj2 / MIN_WETNESS_ADJ) * 100); // Omregn fra tal til procent
  int percent = adj3;                                 // Omdan til heltal
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
