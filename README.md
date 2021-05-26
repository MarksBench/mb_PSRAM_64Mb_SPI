# mb_PSRAM_64Mb_SPI.py

Very Simple MicroPython module/driver for Espressif/Generic 64Mbit SPI PSRAM
(Adafruit prdoduct ID: 4677 or similar). Works with RP2040, should work with other MicroPython boards that have SPI.

This module is intended to make using the PSRAM as simple as possible.
It only accepts an address (range 0-8388607) and a value (range 0-255).
Values read from the PSRAM are returned as integers.

Author: mark@marksbench.com

Version: 0.1, 2021-05-26

**NOTE(1): There is no guarantee that this software will work in the way you expect (or at all).
**Use at your own risk.

**NOTE(2): Writing and reading 64Mib over SPI is _not_ fast, and will be even slower if using software SPI.
**If you're concerned about whether your program has crashed out over a long read or write loop, set up some sort
** of heartbeat - a periodically flashing LED, print statment, beep, etc.

**NOTE(3): As this is PSRAM and not SRAM, do not exceed the maximum operating frequency
** or use the PSRAM outside its timing parameters as shown in the datasheet, or the
** PSRAM may not have enough time to do an internal refresh, causing a loss of data.

Prerequisites:
- RP2040 silicon (tested with Raspberry Pi Pico), should work with other MicroPython-capable MCUs with SPI
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

