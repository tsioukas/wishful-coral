#!/usr/bin/python

import serial
from write2anyPort import writeThis

writeThis('/dev/ttyUSB0', 115200,"TD")
