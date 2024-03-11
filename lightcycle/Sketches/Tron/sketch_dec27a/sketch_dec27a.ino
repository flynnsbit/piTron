//Tron Lightcycle Wheelie Mod - Flynnsbit 2017

#include <Servo.h>
int button1 = 2; //button pin D2, connect to ground to move servo
int press1 = 0;
int button2 = 7; //button pin D2, connect to ground to move servo
int press2 = 0;

int pos = 0;    // variable to store the servo position
Servo myservo_orange;
Servo myservo_blue;
void setup()
{
 Serial.begin(9600);
 pinMode(button1, INPUT);
// pinMode(button2, INPUT);

 myservo_orange.attach(4);
 myservo_blue.attach(8);

 digitalWrite(2, HIGH); //enable pullups to make pin high Wemos Mini D4
  myservo_orange.write(180); // this is the initial height/position on boot /  80 is higher than 90.  
  myservo_blue.write(180); // this is the initial height/position on boot /  80 is higher than 90.  
}
  press2 = digitalRead(button2);
 if (press2 == LOW)
 {
       for (pos = 90; pos <= 180; pos += 1) { // goes from 0 degrees to 180 degrees
// in steps of 1 degree
myservo_blue.write(pos);              // tell servo to go to position in variable 'pos'
delay(10);                       // waits 15ms for the servo to reach the position
}
   delay(3000);
for (pos = 180; pos >= 90; pos -= 3) { // goes from 180 degrees to 0 degrees
myservo_blue.write(pos);              // tell servo to go to position in variable 'pos'
delay(10);   // waits 15ms for the servo to reach the position
Serial.print(pos);
Serial.print("                    ");


}
  } else {
  }

