#include <Arduino.h>

int tiltServo = 10;    // control pin for servo motor
int panServo = 11;
int minPulse = 600;  // minimum servo position
int maxPulse = 2400; // maximum servo position
int refreshTime = 20;   // time (ms) between pulses (50Hz)

// tiltServo setup
int centerPan;         // center servo position
int pulseWidthPan;          // servo pulse width
int servoPositionPan;       // commanded servo position, 0-180 degrees
int pulseRangePan;          // max pulse - min pulse
long lastPulsePan = 0;    // recorded time (ms) of the last pulse

// panServo setup
int centerTilt;         // center servo position
int pulseWidthTilt;          // servo pulse width
int servoPositionTilt;       // commanded servo position, 0-180 degrees
int pulseRangeTilt;          // max pulse - min pulse
long lastPulseTilt = 0;    // recorded time (ms) of the last pulse

void setup() {

    pinMode(panServo, OUTPUT);  // Set servo pin as an output pin
    pulseRangePan = maxPulse - minPulse;
    centerPan = maxPulse - ((pulseRangePan) / 2);
    pulseWidth = centerPan;   // Give the servo a starting point (or it floats)

    pinMode(tiltServo, OUTPUT);  // Set servo pin as an output pin
    pulseRangeTilt = maxPulse - minPulse;
    centerTilt = maxPulse - ((pulseRange) / 2);
    pulseWidthTilt = centerTilt;   // Give the servo a starting point (or it floats)

    Serial.begin(9600);
}

void loop() {
    // wait for serial input
    if (Serial.available() > 0) {
        // read the incoming byte:
        servoPosition = Serial.read();

        // compute pulseWidth from servoPosition
        pulseWidth = minPulse + (servoPosition * (pulseRange / 180));

        // stop servo pulse at min and max
        if (pulseWidth > maxPulse) { pulseWidth = maxPulse; }
        if (pulseWidth < minPulse) { pulseWidth = minPulse; }

        // debug
        //Serial.println(servoPosition);
    }

    // pulse the servo every 20 ms (refreshTime) with current pulseWidth
    // this will hold the servo's position if unchanged, or move it if changed
    if (millis() - lastPulse >= refreshTime) {
        digitalWrite(servoPin, HIGH);   // start the pulse
        delayMicroseconds(pulseWidth);  // pulse width
        digitalWrite(servoPin, LOW);    // stop the pulse
        lastPulse = millis();           // save the time of the last pulse
    }
}
