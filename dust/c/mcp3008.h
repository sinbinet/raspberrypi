/*
  COPYRIGHT (c) 2013 Gabriel Perez-Cerezo. <http://gpcf.eu>

 Permission is hereby granted, free of charge, to any person obtaining
 a copy of this software and associated documentation files (the
 "Software"), to deal in the Software without restriction, including
 without limitation the rights to use, copy, modify, merge, publish,
 distribute, sublicense, and/or sell copies of the Software, and to
 permit persons to whom the Software is furnished to do so, subject to
 the following conditions:
 
 The above copyright notice and this permission notice shall be included
 in all copies or substantial portions of the Software.
 
 THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
 EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
 MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
 IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
 CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
 TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
 SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

 */

#include "gpio.h"
#include <stdio.h>
void clocked_write(int clockpin, int out, int value) {
  gpio_write(out, value);
  gpio_write(clockpin, 1);
  gpio_write(clockpin, 0);
}
int clocked_read(int clockpin, int in){
  gpio_write(clockpin, 1);
  gpio_write(clockpin, 0);
  return gpio_read(in);
}
void mcp3008_select_chip(int bin[], int inputnum){
  bin[0] = 1; bin[1] = 1; //the first two bits have to be 1
  int i = 2;
  int o[3];
  for (i=2; i >= 0; i--) { // convers inputnum to a 3-Bit binary number
    o[i] = (inputnum % 2);
    inputnum /= 2;
  }
  int c;
  for (c  = i-1; c>=0; c--) {
    o[c] = 0;
  }
  c = 2;
  for (i = 0; i<3; i++){
    bin[c] = o[i];
    c++;
  }
}
int power_of_2(int exp) {
  int output = 1;
  int i;
  for (i = 1; i<=exp; i++) {
    output *= 2;
  }
  return output;
}

int mcp3008_value(int inputnum, int clock, int in, int out, int cs) {
  int i; // "for-loop-integer"
  int inputarray[5]; // will contain the input number
  int output = 0; // this will be returned
  gpio_init(clock, "out");
  gpio_init(in, "in");
  gpio_init(out, "out");
  gpio_init(cs, "out");
  if (inputnum < 0 || inputnum > 7) {
    return -1; // Those inputs don't exist !
  }
  gpio_write(cs, 1);
  gpio_write(clock, 0);
  gpio_write(cs, 0);

  mcp3008_select_chip(inputarray, inputnum);
  for (i=0; i<5; i++){
    clocked_write(clock, out, inputarray[i]); // selects the input on the chip.
  }

  for (i=12; i>0; i--) {
    if (clocked_read(clock, in)) {
      output += power_of_2(i);
    }
  }
  gpio_write(cs, 1);
  output /=4 ;
  return output;
}


