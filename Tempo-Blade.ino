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

#define C3  131
#define Db3 139
#define D3  147
#define D3  147

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

  pinMode(5, OUTPUT);
  pinMode(6, OUTPUT);
  Serial.begin(115200);
}
// good wrong buzzer sound: 4ms high, 4ms low
void loop() {
  /*
  static int pitches[] = {Gb5,Gb5,Gb5,Gb5,D5 ,D5 ,D5 ,D5 ,
                          B4 ,B4 ,B4 ,B4 ,G4 ,G4 ,G4 ,Bb4,
                          Bb4,Bb4,Bb4,Bb4,0  ,0  ,0  ,0  ,
                          B4 ,B4 ,B4 ,A4 ,A4 ,A4 ,A4 ,A4 ,
                          D5 ,D5 ,D5 ,D5 ,Bb4,Bb4,Bb4,Bb4,
                          G4 ,G4 ,G4 ,G4 ,Eb4,Eb4,Eb4,Gb4,
                          Gb4,Gb4,Gb4,Gb4,0  ,0  ,0  ,0  ,
                          G4 ,G4 ,G4 ,G4 ,F4 ,F4 ,F4 ,Bb4,
                          Bb4,Bb4,Bb4,Bb4,0  ,0  ,0  ,0  ,
                          B4 ,B4 ,B4 ,B4 ,A4 ,A4 ,A4 ,D5 ,
                          D5 ,D5 ,D5 ,D5 ,0  ,0  ,0  ,0  ,
                          Eb5,Eb5,Eb5,0  ,Eb5,Eb5,Eb5,Gb5,
                          Gb5,Gb5,Gb5,Gb5,Gb5,Gb5,Gb5,0  ,
                          G5 ,G5 ,G5 ,0  ,G5 ,G5 ,G5 ,Bb5,
                          Bb5,Bb5,Bb5,Bb5,Bb5,Bb5,Bb5,0  ,
                          Gb5,Gb5,0  ,Gb5,0  ,0  ,0  ,0  ,

                          Gb5,Gb5,Gb5,Gb5,D5 ,D5 ,D5 ,D5 ,
                          B4 ,B4 ,B4 ,B4 ,G4 ,G4 ,G4 ,Bb4,
                          Bb4,Bb4,Bb4,Bb4,0  ,0  ,0  ,0  ,
                          B4 ,B4 ,B4 ,A4 ,A4 ,A4 ,A4 ,A4 ,
                          D5 ,D5 ,D5 ,D5 ,Bb4,Bb4,Bb4,Bb4,
                          G4 ,G4 ,G4 ,G4 ,Eb4,Eb4,Eb4,Gb4,
                          Gb4,Gb4,Gb4,Gb4,0  ,0  ,0  ,0  ,
                          G4 ,G4 ,G4 ,G4 ,F4 ,F4 ,F4 ,Bb4,
                          Bb4,Bb4,Bb4,Bb4,0  ,0  ,0  ,0  ,
                          B4 ,B4 ,B4 ,B4 ,A4 ,A4 ,A4 ,D5 ,
                          D5 ,D5 ,D5 ,D5 ,0  ,0  ,0  ,0  ,
                          Eb5,Eb5,Eb5,0  ,Eb5,Eb5,Eb5,Gb5,
                          Gb5,Gb5,Gb5,Gb5,Gb5,Gb5,Gb5,0  ,
                          G5 ,G5 ,G5 ,0  ,G5 ,G5 ,G5 ,Bb5,
                          Bb5,Bb5,Bb5,Bb5,Bb5,Bb5,Bb5,0  ,
                          Db5,E5 ,Ab5,B5 ,Bb5,Bb5,Bb5,Ab5,
                          
                          Gb5,};*/
  static int pitches[] = {E3, 0, E3, 0, 0, E3, 0, 0, C3, 0, E3, 0, 0, G3, 0, 0, G2, C3, G2, E2, A2, B2, Bb2, A2, G2, E3, G3, A3, F3, G3, E3, C3, D3, B2, C3, G2, E2, A2, B2, Bb2, A2, G2, E3, G3, A3, F3, G3, E3, C3, D3, B2, G3, Gb3, F3, D3, E3, G2, A2, C3, A2, C3, D3, G3, Gb3, F3, D3, E3, C4, C4, C4, G3, Gb3, F3, D3, E3, G2, A2, C3, A2, C3, D3, Eb3, D3, C3, C3, C3, C3, C3, D3, E3, C3, A2, G2, C3, C3, C3, C3, D3, E3, C3, C3, C3, C3, D3, E3, C3, A2, G2, E3, E3, E3, C3, E3, G3, G2, C3, G2, E2, A2, B2, Bb2, A2, G2, E3, G3, A3, F3, G3, E3, C3, D3, B2, C3, G2, E2, A2, B2, Bb2, A2, G2, E3, G3, A3, F3, G3, E3, C3, D3, B2, E3, C3, G2, G2, A2, F3, F3, A2, B2, A3, A3, A3, G3, F3, E3, C3, A2, G2, E3, C3, G2, G2, A2, F3, F3, A2, B2, F3, F3, F3, E3, D3, C3, G2, E3, C2, C3, G2, E2, A2, B2, A2, Ab4, Bb2, Ab4, G2, Gb4, G2
};
  static int pitch;

  if(millis() < sizeof(pitches)/sizeof(int) * 200) {
    pitch = pitches[millis() / 125];
  } else {
    pitch = 0;
  }
  tone(6, pitch, 1000);


/*

  for(unsigned long i = 0; i < 50000; i++){
    tone(6, i);
    delay(10);
  }
  */
}
