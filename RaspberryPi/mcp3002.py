from __future__ import division
from time import sleep

import spidev

info = """
MCP3002 2-Channel 10 Bit ADC Driver
Adapted From http://raspberry.io/projects/view/reading-from-a-mcp3002-analog-to-digital-converter/
Also appearing at https://classes.engineering.wustl.edu/ese205/core/index.php?title=ADC_(MCP3002)_%2B_Raspberry_Pi_2

Requirements: 
  spi_bcm2708 - sudo modprobe spi_bcm2708
  spidev      - sudo pip install spidev
  spi         - echo spi_bcm2708 | sudo tee -a /etc/modules OR sudo raspi-config

Pinout:
  MCP3002 | Raspberry Pi
  CS      CE0
  DIN     MOSI
  DOUT    MISO
  CLK     SCLK
  VDD     5V
  VSS     GND
  """

def bitstring(n):
    s = bin(n)[2:]
    return '0'*(8-len(s)) + s

class MCP3002:

    def __init__(self, spi_channel=0):
        self.spi = spidev.SpiDev(0, spi_channel)
        self.spi.max_speed_hz = 1200000 # 1.2 MHz
        # self.spi.mode = 0
        
    def read(self, channel):
        cmd = 128
        # cmd = 192 # Start bit + single-ended
        if channel:
            cmd += 32
        
        reply_bytes = self.spi.xfer2([cmd, 0])
        reply_bitstring = ''.join(bitstring(n) for n in reply_bytes)
        reply = reply_bitstring[5:15]
        return int(reply, 2) / 2**10

if __name__ == "__main__":
    print info
    print "\nReads both channels every 5 seconds"

    adc = MCP3002()

    while True:
        print 'Channel 0 - {0}'.format(adc.read(0))
        print 'Channel 1 - {0}'.format(adc.read(1))
        sleep(5)
