#include "SevSeg.h"
SevSeg sevseg; 
int counter = 0;
int frames = 0;

void setup(){
  byte numDigits = 3;
  byte digitPins[] = {11, 12, 13};
  byte segmentPins[] = {9, 2, 3, 5, 6, 8, 7, 4};

  bool resistorsOnSegments = true; 
  bool updateWithDelaysIn = true;
  byte hardwareConfig = COMMON_CATHODE; 
  sevseg.begin(hardwareConfig, numDigits, digitPins, segmentPins, resistorsOnSegments);
  sevseg.setBrightness(90);
}

void loop(){
    sevseg.setNumber(counter, 0);
    sevseg.refreshDisplay(); 

    frames++;
    if(frames==2000){
      counter++;
      frames = 0;
    }
    if(counter == 1000){
      counter = 0;
    }
}
