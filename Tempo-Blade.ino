#include <LiquidCrystal.h>
#include "I2Cdev.h"
#include "MPU6050_6Axis_MotionApps20.h"
#include "Wire.h"

#include "notes.h"
#include "arrows.h"

#define dip return

const int rs = 7;
const int e  = 8;
const int d4 = 9;
const int d5 = 10;
const int d6 = 11;
const int d7 = 12;

const int columns = 16;
const int rows = 2;

const int mpu1 = 0x68;
const int accelReg = 0x3B;
const int pwrReg = 0x6B;

const int threshold = 10000;
const int g = 17300;

const int mpuReadPeriod = 100;

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

byte arrows[8][8] = ARROWS;
LiquidCrystal lcd(rs, e, d4, d5, d6, d7);
MPU6050 mpu;

bool ready = false;


void setup() {
  // put your setup code here, to run once:
  for(int i = 0; i < 8; i++) {
    lcd.createChar(i, arrows[i]);
  }
  lcd.begin(columns, rows);

  pinMode(5, OUTPUT);
  pinMode(6, OUTPUT);
  Serial.begin(115200);

  Wire.begin();

  mpu.initialize();
  Serial.println(mpu.testConnection() ? F("MPU6050 connection successful") : F("MPU6050 connection failed"));

  byte status = mpu.dmpInitialize();

  mpu.setZAccelOffset(g);

  if(status != 0) {
    Serial.println("Something has gone awfully wrong.");
    dip;
  }

  mpu.CalibrateAccel(6);
  mpu.CalibrateGyro(6);
  mpu.PrintActiveOffsets();

  mpu.setDMPEnabled(true);

  ready = true;
}
// good wrong buzzer sound: 4ms high, 4ms low
void loop() {
  if(!ready) {
    dip;
  }
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

  static byte dmpBuf[64];
  static Quaternion q;
  static VectorInt16 accel;
  static VectorInt16 realAccel;
  static VectorInt16 worldAccel;
  static VectorFloat grabity;

  static int mpuTime = 0;

  if(millis() >= mpuTime){
  if(mpu.dmpGetCurrentFIFOPacket(dmpBuf)) {
    mpu.dmpGetQuaternion(&q, dmpBuf);
    mpu.dmpGetAccel(&accel, dmpBuf);
    mpu.dmpGetGravity(&grabity, &q);
    mpu.dmpGetLinearAccel(&realAccel, &accel, &grabity);
    mpu.dmpGetLinearAccelInWorld(&worldAccel, &realAccel, &q);

    Serial.print(worldAccel.x);
    Serial.print(", ");
    Serial.print(worldAccel.y);
    Serial.print(", ");
    Serial.println(worldAccel.z);
  }
  mpuTime += mpuReadPeriod;
  }

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
