#######################################################################
#This is a simple program that sets a voltage, current, over-voltage, #
#and the status of over-current protection. When done, the program    #
#checks for instrument error and gives a message if there is an error.#
#######################################################################

import sys
import os
import telnetlib
import re
from time import sleep
from power_analyzer import AgilentBank
agilent = AgilentBank()
agilent.reset_agilent()
agilent.verify_response("*IDN?",'Agilent Technologies,N6705B,MY53001146,D.01.10')
agilent.enable_channel(1)
#agilent.disable_channel(1)
#agilent.set_voltage(5)
#agilent.set_current(5)
agilent.set_OverVoltageProtection()
#agilent.set_OverCurrentProtection()
#agilent.device_clear()
#agilent.ask("Syst:err?")
#agilent.data_logger(filename,CHANNEL_NUMBER,CHANNEL_NUMBER,TIME_DURATION,SAMPLE_PERIOD_MS)
#agilent.file_clear('test1')

#agilent.pulse_generator(1, 100,1,1,1,1,5)
agilent.data_logger('default',1,20,0.1)


agilent.writeInFile("LitePoint_Data_Format")
print "Current:"
agilent.fetch_avg_current(1)
agilent.fetch_max_current(1)
agilent.fetch_min_current(1)
agilent.fetch_PTPeak_current(1)
agilent.fetch_amp_hours(1)

print ""
print"Voltage:"
agilent.fetch_avg_voltage(1)
agilent.fetch_max_voltage(1)
agilent.fetch_min_voltage(1)
agilent.fetch_PTPeak_voltage(1)
agilent.fetch_watt_hours(1)

agilent.writeInFile("EXE_CHECK=PASS")
#print "*** Hit CTRL+C to stop ***"

## Start loop ## 
#while True:
        ### Show voltage and current ##
#	agilent.get_voltage(1)
#	agilent.get_current(1)
#	sleep(5)
agilent.file_export_internal('prince')
agilent.terminate()




