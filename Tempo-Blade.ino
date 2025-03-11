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

const int accelReg = 0x3B;
const int pwrReg = 0x6B;

const float threshold = 20.0;
const int waitTime = 25;

const int mpuReadPeriod = 10;

enum directions {
    UPD = 0,
    DOWND,
    LEFTD,
    RIGHTD,
    UPLEFTD,
    UPRIGHTD,
    DOWNLEFTD,
    DOWNRIGHTD,
    ANYD,
    NOD
};

#define C3  131
#define Db3 139
#define D3  147
#define D3  147

byte arrows[8][8] = ARROWS;
LiquidCrystal lcd(rs, e, d4, d5, d6, d7);
MPU6050 mpu1(MPU6050_ADDRESS_AD0_LOW);
MPU6050 mpu2(MPU6050_ADDRESS_AD0_HIGH);

bool ready = false;

#ifdef __arm__
// should use uinstd.h to define sbrk but Due causes a conflict
extern "C" char* sbrk(int incr);
#else  // __ARM__
extern char *__brkval;
#endif  // __arm__

int freeMemory() {
  char top;
#ifdef __arm__
  return &top - reinterpret_cast<char*>(sbrk(0));
#elif defined(CORE_TEENSY) || (ARDUINO > 103 && ARDUINO != 151)
  return &top - __brkval;
#else  // __arm__
  return __brkval ? &top - __brkval : &top - __malloc_heap_start;
#endif  // __arm__
}


template<typename T>
T operator*(const T &vec, const float &coeff) {
  return T(vec.x*coeff, vec.y*coeff, vec.z*coeff);
}

template<typename T>
T operator+(const T &vec1, const T &vec2) {
  return T(vec1.x + vec2.x, vec1.y + vec2.y, vec1.z + vec2.z);
}

template<typename T>
T operator-(const T &vec1, const T &vec2) {
  return T(vec1.x - vec2.x, vec1.y - vec2.y, vec1.z - vec2.z);
}

template<typename T>
T operator+=(T &obj1, const T &obj2) {
  obj1 = obj1 + obj2;
}

void buzz() {
  tone(6, 125, 125);
}

int gameType = 2;

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

  for(int i = 0; i < 2; i++){
    MPU6050 &mpu = i == 0 ? mpu1 : mpu2;
    mpu.initialize();
    Serial.println(mpu.testConnection() ? F("MPU6050 connection successful") : F("MPU6050 connection failed"));

    byte status = mpu.dmpInitialize();


    if(status != 0) {
      Serial.println("Something has gone awfully wrong.");
      dip;
    }

    mpu.CalibrateAccel(6);
    mpu.CalibrateGyro(6);
    mpu.PrintActiveOffsets();
    mpu.setDMPEnabled(true);

    if (Serial.available() > 0) {
      gameType = Serial.read();
    }
  }

  ready = true;
}

void loop() {
  if(!ready) {
    dip;
  }


  


  static VectorFloat mpu1acc;
  static VectorFloat mpu2acc;
  static VectorFloat mpudiffs[2];

  enum swingStates {
    NOSWING,
    SWING,
    LATENTSWING
  };
  static byte states[2] = {NOSWING, NOSWING};
  static float controllerDirections[2] = {0.0, 0.0};

  static unsigned long mpuTime = 0;
  if(millis() >= mpuTime){
    static byte dmpBuf[64];
    static Quaternion q;
    static VectorInt16 accel;
    static VectorInt16 realAccel;
    static VectorInt16 worldAccel;
    static VectorFloat grabity;
    if(mpu1.dmpGetCurrentFIFOPacket(dmpBuf)) {
      mpu1.dmpGetQuaternion(&q, dmpBuf);
      mpu1.dmpGetAccel(&accel, dmpBuf);
      mpu1.dmpGetGravity(&grabity, &q);
      mpu1.dmpGetLinearAccel(&realAccel, &accel, &grabity);
      mpu1.dmpGetLinearAccelInWorld(&worldAccel, &realAccel, &q);

      static VectorFloat accelAvgSum;
      accelAvgSum += VectorFloat(worldAccel) - mpu1acc;
      mpu1acc = accelAvgSum * (1.0/100);

      static VectorFloat lastAccelAvg;
      mpudiffs[0] = mpu1acc - lastAccelAvg;
      lastAccelAvg = mpu1acc;
    }
    
    if(mpu2.dmpGetCurrentFIFOPacket(dmpBuf)) {
      mpu2.dmpGetQuaternion(&q, dmpBuf);
      mpu2.dmpGetAccel(&accel, dmpBuf);
      mpu2.dmpGetGravity(&grabity, &q);
      mpu2.dmpGetLinearAccel(&realAccel, &accel, &grabity);
      mpu1.dmpGetLinearAccelInWorld(&worldAccel, &realAccel, &q);

      static VectorFloat accelAvgSum;
      accelAvgSum += VectorFloat(worldAccel) - mpu2acc;
      mpu2acc = accelAvgSum * (1.0/100);

      static VectorFloat lastAccelAvg;
      mpudiffs[1] = mpu2acc - lastAccelAvg;
      lastAccelAvg = mpu2acc;
    }

    
    static unsigned long timesWhenSwingEnded[2] = {0,0};
    for(int i = 0; i < 2; i++){
      switch(states[i]) {
        case NOSWING:
          if(mpudiffs[i].getMagnitude() > threshold) {
            states[i] = SWING;
            controllerDirections[i] = atan2(mpudiffs[i].z, mpudiffs[i].x);
          }
          break;
        case SWING:
          if(mpudiffs[i].getMagnitude() <= threshold) {
            states[i] = LATENTSWING;
            timesWhenSwingEnded[i] = millis();
          }
          break;
        case LATENTSWING:
          if(mpudiffs[i].getMagnitude() > threshold) {
            states[i] = SWING;
          } else if(millis() > timesWhenSwingEnded[i] + waitTime) {
            states[i] = NOSWING;
          }
          break;
      
      }
    }

    mpuTime += mpuReadPeriod;
  }


  while(Serial.available() > 0) {
    int c = Serial.read();
    switch(c) {
      case 'h':
        for(int i = 0; i < 2; i++){
          bool isSwinging = true;
          bool hit = false;
          if(states[i] == NOSWING) {
            isSwinging = false;
          }

          while(Serial.available() == 0);
          //TODO: DIRECTION CHECKING
          c = Serial.read();
          if(c != ' ' && !isSwinging) {
            buzz();
            continue;
          }
          switch(c) {
            case UPD:
              if(controllerDirections[i] > M_PI/4 && controllerDirections[i] < 3*M_PI/4) {
                hit = true;
              } else {
                buzz();
              }
              break;
            case DOWND:
              if(controllerDirections[i] < -M_PI/4 && controllerDirections[i] > -3*M_PI/4) {
                hit = true;
              } else {
                buzz();
              }
              break;
            case LEFTD:
              if(controllerDirections[i] > 3*M_PI/4 || controllerDirections[i] < -3*M_PI/4) {
                hit = true;
              } else {
                buzz();
              }
              break;
            case RIGHTD:
              if(controllerDirections[i] < M_PI/4 && controllerDirections[i] > -M_PI/4) {
                hit = true;
              } else {
                buzz();
              }
              break;
            case UPLEFTD:
              if(controllerDirections[i] > M_PI/2 && controllerDirections[i] < M_PI) {
                hit = true;
              } else {
                buzz();
              }
              break;
            case UPRIGHTD:
              if(controllerDirections[i] > 0 && controllerDirections[i] < M_PI/2) {
                hit = true;
              } else {
                buzz();
              }
              break;
            case DOWNLEFTD:
              if(controllerDirections[i] < -M_PI/2 && controllerDirections[i] > -M_PI) {
                hit = true;
              } else {
                buzz();
              }
              break;
            case DOWNRIGHTD:
              if(controllerDirections[i] < 0 && controllerDirections[i] > -M_PI/2) {
                hit = true;
              } else {
                buzz();
              }
              break;
          }
          if(hit) {
            Serial.write(100);
          }
        }
        break;
      if (gameType == 2) {
        case '\n':
        lcd.setCursor(0,1);
        break;
      case '\f':
        lcd.setCursor(0,0);
        break;
      case ' ':
        lcd.write(0xFF);
        break;
      case ANYD:
        lcd.write('X');
        break;
      default:
        lcd.write((char)c);
      }
    }
  }


/*

  for(unsigned long i = 0; i < 50000; i++){
    tone(6, i);
    delay(10);
  }
  */
}
