#include "mcp3008.h"
#include <stdio.h>
/* Prints the value of the input "0" of the MCP 3008 
	*/
int main() {
  int value = mcp3008_value(0, 4, 14, 15, 17);
  printf("%d", value);
  return 0;
}
