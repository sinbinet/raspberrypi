#include "mcp3008.h"
#include <stdio.h>
#include <wiringPi.h>

/*
#define ILED 4
#define ECHO 4

#define CLK 18
#define DOUT 23
#define DIN 24
#define CS 25
*/

int main(void)
{
  int value = 0;
  printf("Hello");

  //if (wiringPiSetup() == -1) return 1;

  //pinMode(ILED, OUTPUT);
  //delayMiceoseconds(280);
  //pinMode(ECHO, INPUT);

  //for(;;)
  //{
	pinMode(4, OUTPUT);
	//delayMicroseconds(280);

	//value = mcp3008_value(0, CLK, DIN, DOUT, CS);
	value = mcp3008_value(0, 18, 24, 23, 25);
	printf("%d", value);
    delay(100);
  //}
  return 0;
}
