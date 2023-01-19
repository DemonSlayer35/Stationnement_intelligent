#include <SPI.h>

void setup() 

{

  // Set the Main in Secondary Out as an output

  pinMode(MISO, OUTPUT);

  // turn on SPI as a secondary

  // Set appropriate bit in SPI Control Register

  SPCR |= _BV(SPE);

}

void loop () 

{

  byte in_byte;

  // SPIF indicates transmission complete (byte received)

  if ((SPSR & (1 << SPIF)) != 0)

  {

    in_byte = SPDR;

    

    // Handle the input code here

    // Set return_val to the value you want to return
    float return_val = 5.2 * 10;
    

    SPDR = return_val;

  }
}
