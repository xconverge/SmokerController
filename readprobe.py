
import datetime
import time
import math
# Import SPI library (for hardware SPI) and MCP3008 library.
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008

# Software SPI configuration:
CLK  = 11
MISO = 9
MOSI = 10
CS   = 8
mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)

# Steinhart-Hart equation with coefficients for probe
def ohm_to_fahrenheit(x):
    A = 0.4213e-3
    B = 2.09538489e-4
    C = 2.134190749e-7

    tempInCelsius = ((1.0 / (A + (B*math.log(x)) + (C * math.pow(math.log(x),3)))) - 273.15)
    return ((tempInCelsius * 9 / 5) + 32.)

def printReading():
    numSamples = 10
    sampleDelay = 10
    a2dval = 0.0

    # Read a2d channel 1 with multiple samples
    for i in range(0,10):
        a2dval += mcp.read_adc(0)
        time.sleep(sampleDelay / 1000)

    average = a2dval/numSamples
    # print "avg a2d in mv: ", average

    # Convert a2d value to resistance (10k resistor used for voltage divider)
    average = (math.pow(2, 10) / average - 1) * 10000

    # print "resistance: ", average

    # Convert value to fahrenheit
    tempInF = ohm_to_fahrenheit(average)
    print datetime.datetime.now(), tempInF

    return tempInF

printReading()
