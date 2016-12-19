# SmokerController

This project is to control a 12V fan connected to a bottom vent of my Weber Smokey Mountain smoker. Everything is running on a RaspberryPi which is powered with a 10000mAh mobile battery pack.

When the temperature falls below a threshold, the fan turns on to heat up the charcoal. When it hits another threshold, the fan shuts down. 

There is also a sqlite3 database of all of the past temperatures for plotting using the google chart API

The temperature probe is a Maverick ET-73 replacement probe from [Amazon](https://www.amazon.com/Maverick-Genuine-Replacement-Probe-ET-73/dp/B004W8B3PC/ref=sr_1_1?s=home-garden&ie=UTF8&qid=1342974838&sr=1-1&keywords=et-73+replacement+probe).

Ice water, room temp water, and boiling water was used to find 3 data points of resistance/temp. I then solved the system of equations to model it after the [Steinhart-Hart](https://en.wikipedia.org/wiki/Steinhart%E2%80%93Hart_equation) equation for resistance. The coefficients matched the curve pretty well.

I then used a voltage divider with a 10k ohm fixed resistance to read the probe into the A2D chip. I used a MCP3008 a2d which is a 10 bit 8 channel ADC with SPI.
 
SPI was then used to interface between the a2d and the raspberry pi

![ScreenShot](https://raw.githubusercontent.com/xconverge/SmokerController/master/screenshot.png)
