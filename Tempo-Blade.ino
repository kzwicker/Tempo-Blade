#include <LiquidCrystal.h>

const int rs = 7;
const int e  = 8;
const int d4 = 9;
const int d5 = 10;
const int d6 = 11;
const int d7 = 12;

const int columns = 16;
const int rows = 2;

byte uarrow[8] = {
  0b00000,
  0b00100,
  0b01000,
  0b11111,
  0b01000,
  0b00100,
  0b00000,
  0b00000,
};
byte darrow[8] = {
  0b00000,
  0b00100,
  0b00010,
  0b11111,
  0b00010,
  0b00100,
  0b00000,
  0b00000,
};
byte larrow[8] = {
  0b00000,
  0b00100,
  0b00100,
  0b10101,
  0b01110,
  0b00100,
  0b00000,
  0b00000,
};
byte rarrow[8] = {
  0b00000,
  0b00100,
  0b01110,
  0b10101,
  0b00100,
  0b00100,
  0b00000,
  0b00000,
};
byte uarrowline[8] = {
  0b00100,
  0b00100,
  0b01100,
  0b11111,
  0b01100,
  0b00100,
  0b00100,
  0b00000,
};
byte darrowline[8] = {
  0b00100,
  0b00100,
  0b00110,
  0b11111,
  0b00110,
  0b00100,
  0b00100,
  0b00000,
};
byte larrowline[8] = {
  0b00100,
  0b00100,
  0b00100,
  0b10101,
  0b01110,
  0b00100,
  0b00100,
  0b00000,
};
byte rarrowline[8] = {
  0b00100,
  0b00100,
  0b01110,
  0b10101,
  0b00100,
  0b00100,
  0b00100,
  0b00000,
};

LiquidCrystal lcd(rs, e, d4, d5, d6, d7);

void setup() {
  // put your setup code here, to run once:
  lcd.createChar(0, uarrow);
  lcd.createChar(1, darrow);
  lcd.createChar(2, larrow);
  lcd.createChar(3, rarrow);
  lcd.createChar(4, uarrowline);
  lcd.createChar(5, darrowline);
  lcd.createChar(6, larrowline);
  lcd.createChar(7, rarrowline);
  lcd.begin(columns, rows);
  byte screen[] = {0,1,' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','|',' ',
                   ' ',' ',' ',' ',3,' ',' ',' ',' ',' ',' ',' ',' ',' ',5,' '};
  for(int i = 0; i < 16; i++) {
    lcd.write(screen[i]);
  }
  lcd.setCursor(0,1);
  for(int i = 0; i < 16; i++) {
    lcd.write(screen[i+16]);
  }

  pinMode(4, OUTPUT);
  pinMode(3, OUTPUT);
  Serial.begin(115200);
}

// good wrong buzzer sound: 4ms high, 4ms low
void loop() {
  static long int lastMicros = 0;
  int pitch = 5000;

  // put your main code here, to run repeatedly:
  if(micros() - lastMicros % (1000000/pitch) < 500000/pitch) {
    digitalWrite(4, HIGH);
    digitalWrite(3, LOW);
  } else {
    digitalWrite(4, LOW);
    digitalWrite(3, HIGH);
  }
  if(micros() - lastMicros == 1000000/pitch) {
    lastMicros = micros();
  }
}
