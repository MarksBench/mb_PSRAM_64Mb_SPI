"""
mb_PSRAM_64Mb_SPI.py

Very Simple MicroPython module/driver for Espressif 64Mbit SPI PSRAM
(Adafruit prdoduct ID: 4677 or similar)

Author: mark@marksbench.com

Version: 0.1, 2021-05-26

**NOTE(1): There is no guarantee that this software will work in the way you expect (or at all).
**Use at your own risk.

**NOTE(2): Writing and reading 64Mib over SPI is _not_ fast. If you're concerned about
** whether your program has crashed out over a long read or write loop, set up some sort
** of heartbeat - a periodically flashing LED, print statment, etc.

**NOTE(3): As this is PSRAM and not SRAM, do not exceed the maximum operating frequency
** or access the PSRAM outside its timing parameters as shown in the datasheet, or the
** PSRAM may not have enough time to do an internal refresh, causing a loss of data.

Prerequisites:
- RP2040 silicon (tested with Raspberry Pi Pico), should work with other MCUs with SPI
- MicroPython v1.15 on 2021-04-18; Raspberry Pi Pico with RP2040
- PSRAM connected to hardware SPI port0 or port1 pins, should also work with SW SPI
- Dedicated /CS pin (can be any GP pin that's not already being used for SPI). Do not tie /CS to
  GND - the device requires state changes on /CS to function properly.

Usage:
- from machine import Pin, SPI
- import utime
- import mb_PSRAM_64Mb_SPI
- Set up SPI using a hardware SPI port 0 or 1. Polarity and phase are both 0.
- specify /CS pin (can be any GP pin that's not already being used for SPI):
  cs = GP#
- Create constructor:
  thisMemoryChipDeviceName = mb_PSRAM_64Mb_SPI.mb_PSRAM_64Mb(spi, cs)
- To write a single byte to an address:
  thisMemoryChipDeviceName.write_byte(address, value)
- To read a single byte from an address:
  thisMemoryChipDeviceName.read_byte(address)
- See mb_PSRAM_64Mb_SPI_example.py

For more information, consult the Raspberry Pi Pico MicroPython SDK documentation at:
  https://datasheets.raspberrypi.org/pico/raspberry-pi-pico-python-sdk.pdf
  
and the Adafruit 64Mbit PSRAM page and datasheet at:
  https://www.adafruit.com/product/4677

"""

from machine import Pin, SPI
import utime


# Command set for this device. Only using regular speed reads with normal SPI.
_RESET_EN = const(0x66) # Reset enable
_RESET = const(0x99) # Reset
_WRITE = const(0x02) # Write
_READ = const(0x03) # Read

_MAX_ADDRESS = const(8388607) # 8MiB address size for this device (0 to 8388607)



class mb_PSRAM_64Mb_SPI:
    """Driver for generic 64Mib SPI PSRAM module from Adafruit"""
    
    def __init__(self, spi, cs):
        # Init with SPI settings
        self.spi = spi
        
        # Init /CS pin
        self.cs = Pin(cs, Pin.OUT)

        self.cs.value(1) # According to the datasheet, the device needs /CE high first
        utime.sleep_us(200) # Device needs 150us and a user-issued reset operation to complete its self-init
        self.cs.value(0)
        self.spi.write(bytearray([_RESET_EN])) # Reset enable
        self.cs.value(1)
        utime.sleep_us(50)
        self.cs.value(0)
        self.spi.write(bytearray([_RESET])) # With Reset enabled, do a reset
        self.cs.value(1)
        utime.sleep_us(100)
        # Done init, ready to go
        self.address_byte=[0,0,0]
        
        
    def write_byte(self, address, value):
        
        
        # Check to see if the address is valid
        if((address > _MAX_ADDRESS) or (address < 0)):
            raise ValueError("Address is outside of device address range: 0 to",_MAX_ADDRESS)
            return()
        # Now check to make sure the data is within 0 and 255
        if((value > 255) or (value < 0)):
            raise ValueError("You can only pass an 8-bit data value (0-255) to this function")
            return()
        
        # Break the address into three bytes to send (we're using 8-bit SPI)
        self.address_byte[2] = address & 0x0000ff
        self.address_byte[1] = (address & 0x00ff00) >> 8
        self.address_byte[0] = (address >> 16)
        self.cs.value(0)
        self.spi.write(bytearray([_WRITE, self.address_byte[0], self.address_byte[1], self.address_byte[2], value]))
        self.cs.value(1)
        return()
        
        
    
    def read_byte(self, address):
        
        # Check to see if the address is valid
        if((address > _MAX_ADDRESS) or (address < 0)):
            raise ValueError("Address is outside of device address range: 0 to",_MAX_ADDRESS)
            return()
        
        

        # Break the address into three bytes and send read command
        self.address_byte[2] = address & 0x0000ff
        self.address_byte[1] = (address & 0x00ff00) >> 8
        self.address_byte[0] = (address >> 16)

        self.cs.value(0)
        self.spi.write(bytearray([_READ, self.address_byte[0], self.address_byte[1], self.address_byte[2]]))

        self.value_read = self.spi.read(1)
        self.cs.value(1)
        self.value_read = int.from_bytes(self.value_read, "big")
        return(self.value_read)
