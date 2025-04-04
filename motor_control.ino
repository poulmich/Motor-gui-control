#include <Servo.h> 
#include <Adafruit_NeoPixel.h> 
int LED_NUM = 320; 
static unsigned int message_pos = 0; 
const unsigned int MAX_MESSAGE_LENGTH = 12; 
static char message [MAX_MESSAGE_LENGTH]; 
Servo ser;
int number; 
bool leds_on = false; 
Adafruit_NeoPixel pixels = Adafruit_NeoPixel(LED_NUM, 2, NEO_GRB + 
NEO_KHZ800); 
void setup () { 
Serial.begin(9600); 
ser.attach(3); 
delay (15); 
ser.write(0); 
pixels.begin(); 
} 
  void loop () { 
   while (Serial.available() > 0) { 
   char inByte = Serial.read(); 
   if (inByte != '\n' && (message_pos < MAX_MESSAGE_LENGTH - 1) && inByte != '%') { 
    message[message_pos] = inByte; 
    message_pos++; 
 } else { 
     message[message_pos] = '\0'; 
     number = atoi(message); 
    if(number==-1&&!leds_on){ 
    for (int i = 0; i < LED_NUM; i++) { 
      pixels.setPixelColor(i, pixels.Color(0, 255, 0)); 
      pixels.show(); 
      leds_on = true; 
   } 
 } 
else{ 
   if (number! =0) { 
     ser.write(number); 
  } 
 else if(number==0) { 
    for (int i = 0; i < LED_NUM; i++) { 
     pixels.setPixelColor(i, pixels.Color(255, 0, 0)); 
     pixels.show(); 
    } 
    ser.write(number); 
    leds_on = false; 
    } 
   } 
   message_pos = 0; 
  } 
 } 
}  
