#include <stdio.h>
#include <wiringPi.h>

#define TRIG 5
#define ECHO 4

int main(void)
{
  int distance = 0;
  int pulse = 0;

  if (wiringPiSetup() == -1) return 1;

  pinMode(TRIG, OUTPUT);
  pinMode(ECHO, INPUT);

  for(;;)
  {
    digitalWrite(TRIG, LOW);
    usleep(2);
    digitalWrite(TRIG, HIGH);
    usleep(20);
    digitalWrite(TRIG, LOW);

    while(digitalRead(ECHO) == LOW);
    long startTime = micros();
    while(digitalRead(ECHO) == HIGH);
    long travelTime = micros() - startTime;

    int distance = travelTime / 58;
    printf("Distance:%dcm\n", distance);
    delay(100);
  }
}
