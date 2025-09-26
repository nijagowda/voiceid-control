int ledSaif[] = {22, 23};   // LEDs for Saif
int ledAisha[] = {24, 25};  // LEDs for Aisha
int buzzerPin = 26;

void setup() {
  Serial.begin(9600);
  for (int i = 0; i < 2; i++) {
    pinMode(ledSaif[i], OUTPUT);
    pinMode(ledAisha[i], OUTPUT);
    digitalWrite(ledSaif[i], LOW);
    digitalWrite(ledAisha[i], LOW);
  }
  pinMode(buzzerPin, OUTPUT);
  digitalWrite(buzzerPin, LOW);
}

void beep() {
  digitalWrite(buzzerPin, HIGH);
  delay(200);
  digitalWrite(buzzerPin, LOW);
}

void loop() {
  if (Serial.available()) {
    String cmd = Serial.readStringUntil('\n');
    cmd.trim();

    if (cmd == "turnon_saif") {
      digitalWrite(ledSaif[0], HIGH);
      digitalWrite(ledSaif[1], HIGH);
      beep();
    } 
    else if (cmd == "turnoff_saif") {
      digitalWrite(ledSaif[0], LOW);
      digitalWrite(ledSaif[1], LOW);
      beep();
    } 
    else if (cmd == "turnon_aisha") {
      digitalWrite(ledAisha[0], HIGH);
      digitalWrite(ledAisha[1], HIGH);
      beep();
    } 
    else if (cmd == "turnoff_aisha") {
      digitalWrite(ledAisha[0], LOW);
      digitalWrite(ledAisha[1], LOW);
      beep();
    }
  }
}
