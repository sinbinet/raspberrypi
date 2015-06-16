#include <stdio.h>
#include <stdint.h>
#include <wiringPi.h>
#include <gertboard.h>

// read SPI data from MCP3008 chip, 8 possible adc's (0 thru 7)
int readadc(adcnum)
{
 uint8_t buff[3];
 int adc;
 if ((adcnum > 7) || (adcnum < 0))
   return -1;
 buff[0] = 1;
 buff[1] = (8+adcnum)<<4;
 buff[2] = 0;
 wiringPiSPIDataRW(0, buff, 3);
 adc = ((buff[1]&3) << 8) + buff[2];
 return adc;
}

int main(int argc, char *argv[])
{
 int i, chan;
 uint32_t x1, tot ;
   
 printf ("SPI test program\n") ;
 // initialize the WiringPi API
 if (wiringPiSPISetup (0, 1000000) < 0)
   return -1 ;
			 
 // get the channel to read, default to 0
 if (argc>1)
   chan = atoi(argv[1]);
 else
   chan = 0;
							 
 // run until killed with Ctrl-C
 while (1)
 {
  tot = 0;
  for (i=0; i<100; i++)
  {
    // read data and add to total
    x1 = readadc(chan);
	tot += x1;
	delay(10);
  }
  // display the average value
  printf("chan %d:  %d \n", chan, (tot/100)) ;
 }
				   
 return 0 ;
}
