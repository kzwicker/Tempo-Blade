#include <LiquidCrystal.h>
#include "notes.h"
const int rs = 7;
const int e  = 8;
const int d4 = 9;
const int d5 = 10;
const int d6 = 11;
const int d7 = 12;

const int columns = 16;
const int rows = 2;
unsigned long lastMicros = 0;

enum directions {
    UPD = 0,
    DOWND,
    LEFTD,
    RIGHTD,
    UPLEFTD,
    UPRIGHTD,
    DOWNLEFTD,
    DOWNRIGHTD
};

#define C3  131
#define Db3 139
#define D3  147
#define D3  147

byte arrows[8][8] = {{
  ~0b00000,
  ~0b00100,
  ~0b01000,
  ~0b11111,
  ~0b01000,
  ~0b00100,
  ~0b00000,
  ~0b00000,
},
{
  ~0b00000,
  ~0b00100,
  ~0b00010,
  ~0b11111,
  ~0b00010,
  ~0b00100,
  ~0b00000,
  ~0b00000,
},
{
  ~0b00000,
  ~0b00100,
  ~0b00100,
  ~0b10101,
  ~0b01110,
  ~0b00100,
  ~0b00000,
  ~0b00000,
},
{
  ~0b00000,
  ~0b00100,
  ~0b01110,
  ~0b10101,
  ~0b00100,
  ~0b00100,
  ~0b00000,
  ~0b00000,
},
{
  ~0b00000,
  ~0b00000,
  ~0b10010,
  ~0b10100,
  ~0b11000,
  ~0b11110,
  ~0b00000,
  ~0b00000,
},
{
  ~0b00000,
  ~0b11110,
  ~0b11000,
  ~0b10100,
  ~0b10010,
  ~0b00000,
  ~0b00000,
  ~0b00000,
},
{
  ~0b00000,
  ~0b00000,
  ~0b01001,
  ~0b00101,
  ~0b00011,
  ~0b01111,
  ~0b00000,
  ~0b00000,
},
{
  ~0b00000,
  ~0b01111,
  ~0b00011,
  ~0b00101,
  ~0b01001,
  ~0b00000,
  ~0b00000,
  ~0b00000,
}};

LiquidCrystal lcd(rs, e, d4, d5, d6, d7);

void setup() {
  // put your setup code here, to run once:
  for(int i = 0; i < 8; i++) {
    lcd.createChar(i, arrows[i]);
  }
  lcd.begin(columns, rows);

  pinMode(5, OUTPUT);
  pinMode(6, OUTPUT);
  Serial.begin(115200);
}
// good wrong buzzer sound: 4ms high, 4ms low
void loop() {
/*
  static int pitches[] = {E3, 0, E3, 0, 0, E3, 0, 0, C3, 0, E3, 0, 0, G3, 0, 0, G2, 0, C3, 0, 0, G2, 0, 0, E2, 0, 0, A2, 0, B2, 0, Bb2, 0, A2, 0, G2, 0, E3, 0, G3, 0, A3, F3, G3, E3, C3, D3, B2, C3, G2, E2, A2, B2, Bb2, A2, G2, E3, G3, A3, F3, G3, E3, C3, D3, B2, G3, Gb3, F3, D3, E3, G2, A2, C3, A2, C3, D3, G3, Gb3, F3, D3, E3, C4, C4, C4, G3, Gb3, F3, D3, E3, G2, A2, C3, A2, C3, D3, Eb3, D3, C3, C3, C3, C3, C3, D3, E3, C3, A2, G2, C3, C3, C3, C3, D3, E3, C3, C3, C3, C3, D3, E3, C3, A2, G2, E3, E3, E3, C3, E3, G3, G2, C3, G2, E2, A2, B2, Bb2, A2, G2, E3, G3, A3, F3, G3, E3, C3, D3, B2, C3, G2, E2, A2, B2, Bb2, A2, G2, E3, G3, A3, F3, G3, E3, C3, D3, B2, E3, C3, G2, G2, A2, F3, F3, A2, B2, A3, A3, A3, G3, F3, E3, C3, A2, G2, E3, C3, G2, G2, A2, F3, F3, A2, B2, F3, F3, F3, E3, D3, C3, G2, E3, C2, C3, G2, E2, A2, B2, A2, Ab4, Bb2, Ab4, G2, Gb4, G2};
  static int pitch;

  if(millis() < sizeof(pitches)/sizeof(int) * 200) {
    pitch = pitches[millis() / 125];
  } else {
    pitch = 0;
  }
  tone(6, pitch, 1000);
*/

  while(Serial.available() > 0) {
    int c = Serial.read();
    switch(c) {
      case '\n':
        lcd.setCursor(0,1);
        break;
      case '\f':
        lcd.setCursor(0,0);
        break;
      case ' ':
        lcd.write(0xFF);
        break;
      case 8:
        lcd.write('X');
        break;
      default:
        lcd.write((char)c);
    }
  }


/*

  for(unsigned long i = 0; i < 50000; i++){
    tone(6, i);
    delay(10);
  }
  */
}
