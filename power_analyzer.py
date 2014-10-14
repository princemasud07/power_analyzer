import sys
import os
import telnetlib
from time import * 
from threading import Lock


HOST = "192.168.1.105"
DEFAULT_VISA_TIMEOUT = 120
MODEL_NUMBER = "N6705B"
CHANNEL = 1 #channel 1#
overVoltSetting = 7.5 
class AgilentBank:
	LOCK = Lock()

	def __init__(self):
	#Initialize the VISA COM communication#
		print ""	
		print "Setting up power analyzer for testing"
		print ""
		print ""
		try:
			self.power_analyzer = telnetlib.Telnet(HOST, 5024, DEFAULT_VISA_TIMEOUT)
		except:
			self.exc_info=sys.exc_info()
		sleep(3)
			
	def write_cmd(self, query_string):
		"""write function"""
		try:
			self.power_analyzer.read_until('SCPI> ')
		except:
			sleep(2)
			raise Exception("SCPI response not returned") 

		AgilentBank.LOCK.acquire()
		try:
			self.power_analyzer.write(query_string+"\n")
		except:
			sleep(2)
			self.power_analyzer.write(query_string+"\n")
		finally:
			AgilentBank.LOCK.release()
		#print query_string
	
	def writeInFile(self, msg):
		fsock = open("C:\LitePoint\IQfact+\CSR BCx 3.2.0.Eng3_Dongle\Bin\Log\power_log.txt", "a+") 
		try:
			fsock.write(msg+"\n")
		except:
			sleep(2)
			fsock.write(msg+"\n")
		print msg
		fsock.close()
		
	def ask(self, query_string):
		"""A convenience method, performs a write(query) and returns the output
        of read(query).
        
        :param query: The query to send to the instrument
        :type query: str
        @return: The response from read()
        @rtype: str
		"""

		self.write_cmd(query_string)
		sleep(1)
		AgilentBank.LOCK.acquire()
		try:
			res=self.power_analyzer.read_until('\r\n')
		except:
			sleep(2)
			res=self.power_analyzer.read_until('\r\n')
		finally:
			AgilentBank.LOCK.release()
		sleep(1)
		new_res=res.lstrip('SCPI> ')  ###Space must required after SCPI###
		#print new_res
		return new_res
		
	def verify_response(self, query_string, expected_response):
		"""Simple helper method that will query the power_analyzer with 'query' string
		and make sure that the response is equal to 'valueExpected'.  If they
		are not equal, a GPIBpower_analyzerException is raised
		
		:param query: String used to query the power_analyzer (ex. "CALL:BAND?")
        :type query: str
        :param expected_response: String which the result of the query is compared against
        :type expected_response: str
        :raises GPIBpower_analyzerException: If the response is not equal to the expected_response
		"""	
		res=self.ask(query_string)
		new_res=res.rstrip()
		if not (new_res == expected_response):
			raise Exception("response returned '%s', expected '%s' from query '%s'" % (new_res, expected_response, query_string))
		else:
			print "Response Found for %s" %query_string

	def enable_channel(self,CHANNEL_VALUE):
		"""
        Sets the voltage value of the power_analyzer

        :param attenuation_value: the value to set.
        :param type: int

        :raises AgilentException: if power_analyzer_value is not within range.
		"""				
		if(CHANNEL_VALUE>5):
			raise Exception('Channel number out of range 1 to 4')
		try:
			cmd_str = "OUTPut ON,(@%d)" % (int(CHANNEL_VALUE))
			print cmd_str
			self.power_analyzer.write(cmd_str+"\n")
		except:
			raise Exception("Channel is not enabled") 

	def disable_channel(self,CHANNEL_VALUE):
		"""
        Sets the voltage value of the power_analyzer

        :param attenuation_value: the value to set.
        :param type: int

        :raises AgilentException: if power_analyzer_value is not within range.
		"""		
		if(CHANNEL_VALUE>5):
			raise Exception('Channel number out of range 1 to 4')
		try:
			cmd_str = "OUTPut OFF,(@%d)" % (int(CHANNEL_VALUE))
			print cmd_str
			self.power_analyzer.write(cmd_str+"\n")
		except:
			raise Exception("Channel is not disabled") 
			
	def set_voltage(self, VOLTAGE_VALUE):
		"""
        Sets the voltage value of the power_analyzer

        :param attenuation_value: the value to set.
        :param type: int

        :raises AgilentException: if power_analyzer_value is not within range.
		"""		
		if(VOLTAGE_VALUE>5):
			raise Exception('Voltage out of range 0.00 to 5.10')
		try:
			cmd_str = "VOLTage %d,(@%d)" % (int(VOLTAGE_VALUE), CHANNEL)
			print cmd_str
			self.power_analyzer.write(cmd_str+"\n")
		except:
			raise Exception("Voltage could not be set") 

	def set_OverVoltageProtection(self):
		"""
        Sets the Over Voltage Protections for the power_analyzer

        :param attenuation_value: the value to set.
        :param type: int

        :raises AgilentException: if power_analyzer_value is not within range.
		"""		
		try:
			cmd_str = "VOLT:PROT:LEV %f,(@%d)" % (float(overVoltSetting), CHANNEL)
			print cmd_str
			self.power_analyzer.write(cmd_str+"\n")
		except:
			raise Exception("Over Voltage Protection could not be set") 

	def set_current(self, CURRENT_VALUE):
		"""
        Sets the current value of the power_analyzer

        :param attenuation_value: the value to set.
        :param type: int

        :raises AgilentException: if power_analyzer_value is not within range.
		"""		
		if(CURRENT_VALUE>10.2):
			raise Exception('Current out of range 0.00 to 10.2')
		try:
			cmd_str = "CURRent %d,(@%d)" % (int(CURRENT_VALUE), CHANNEL)
			print cmd_str
			self.power_analyzer.write(cmd_str+"\n")
		except:
			raise Exception("Current could not be set") 
			
			
	def set_OverCurrentProtection(self):
		"""
        Sets the Over Current Protections for the power_analyzer

        :param attenuation_value: the value to set.
        :param type: int

        :raises AgilentException: if power_analyzer_value is not within range.
		"""		
		try:
			cmd_str = "CURR:PROT:STAT ON,(@%d)" % CHANNEL
			print cmd_str
			self.power_analyzer.write(cmd_str+"\n")
		except:
			raise Exception("Over Current Protection could not be set") 

	def get_voltage(self,CHANNEL_VALUE):
		"""
        Reads voltage level.

        :returns: float - the value in volt
		"""
		try:
			cmd_str = "*WAI;:MEAS:VOLT? (@%d)" % CHANNEL_VALUE
			print cmd_str
			voltage=self.ask(cmd_str)
		except:
			raise Exception("Voltage couldn't be measured")
		return "Measured Voltage is %f channel %d" %(float(voltage),int(CHANNEL_VALUE))

	def get_current(self,CHANNEL_VALUE):
		"""
        Reads current level.

        :returns: float- the value in current
		"""
		try:
			cmd_str = "*WAI;:MEAS:CURR? (@%d)" % CHANNEL_VALUE
			print cmd_str
			current=self.ask(cmd_str)
		except:
			raise Exception("Current couldn't be measured")
		return "Measured Current is %f channel %d" %(float(current),int(CHANNEL_VALUE))
		
	def reset_agilent(self):
		"""
        Resets the attenuator controller
		"""
		cmd_str = "*RST"
		self.write_cmd(cmd_str)

	def device_clear(self):
		"""
        clear power analyzer.
		"""
		cmd_str = "*CLS"
		self.write_cmd(cmd_str)
	
	def internal_file_delete(self,filename):

		try:
			cmd_str = '*WAI;MMEM:DEL "internal:\%s"' % filename
			print cmd_str
			self.write_cmd(cmd_str)
		except:
			raise Exception("File was not deleted") 
	
	def external_file_delete(self,filename):

		try:
			cmd_str = '*WAI;MMEM:DEL "external:\%s"' % filename
			print cmd_str
			self.write_cmd(cmd_str)
		except:
			raise Exception("File was not deleted") 
			
	def file_export_internal(self,filename):
		print ""	
		print ""
		print "File Exporting to internal memory...."
		print ""
		try:
			cmd_str = '*WAI;MMEM:EXP:DLOG "internal:\%s.csv"' % filename
			print cmd_str
			self.write_cmd(cmd_str)
			print "File Export Completed"
		except:
			raise Exception("File was not exported") 
			
	def file_export_external(self,filename):
		print ""	
		print ""
		print "File Exporting to external memory...."
		print ""
		try:
			cmd_str = '*WAI;MMEM:EXP:DLOG "external:\%s.csv"' % filename
			self.write_cmd(cmd_str)
			print "File Export Completed"
		except:
			raise Exception("File was not exported") 
			
			
	def data_logger(self,filename,CHANNEL_NUMBER,TIME_DURATION,SAMPLE_PERIOD_MS):
			
		print ""	
		print "Running data logger for measurement"
		print ""
		print ""	
	###Set data logger properties, list of commands:
		cmd_str1 = "*WAI;SENS:DLOG:FUNC:CURR ON,(@%d)" %int(CHANNEL_NUMBER)
		cmd_str2 = "*WAI;SENS:DLOG:FUNC:VOLT ON,(@%d)" %int(CHANNEL_NUMBER)
		cmd_str3 = "*WAI;SENS:DLOG:TIME %d" %int(TIME_DURATION)
		cmd_str4 = "*WAI;SENS:DLOG:TINT %s" %SAMPLE_PERIOD_MS
		cmd_str5 = '*WAI;INIT:DLOG "internal:\%s.dlog"' %filename
		cmd_str6 = "*WAI;TRIG:DLOG"
		cmd_str7 = "*WAI;SENS:DLOG:MARK1:POIN 0.5" 
		cmd_str8 = "*WAI;SENS:DLOG:MARK2:POIN %d" %int(TIME_DURATION)
		self.write_cmd(cmd_str1)
		self.write_cmd(cmd_str2)
		self.write_cmd(cmd_str3)
		self.write_cmd(cmd_str4)
		self.write_cmd(cmd_str5)
		self.write_cmd(cmd_str6)
		self.write_cmd(cmd_str7)
		self.write_cmd(cmd_str8)
		sleep(TIME_DURATION+1)
		print ""
		print "Analyzing test results..."
		print ""
		print ""
			#for prince in range(1, 7):
			#	status = self.ask("*OPC?")
			#	while "1" in status:
			#		self.write_cmd("cmd_str"%d) % prince;
			#		status = self.ask("*OPC?")
			#			break;
			
	def pulse_generator(self, CHANNEL_NUMBER, STEP, TIME_0, TIME_1, TIME_2, VOLTAGE_0, VOLTAGE_1):
			
		print ""	
		print "Generating Pulse"
		print ""
		print ""	
	###Set data logger properties, list of commands:
		cmd_str1 = "*WAI;ARB:SEQ:STEP:VOLT:PULS:STAR %d, %d,(@%d)" %(float(VOLTAGE_0), STEP, CHANNEL_NUMBER)
		cmd_str2 = "*WAI;ARB:SEQ:STEP:VOLT:PULS:STAR:TIM %d, %d,(@%d)" %(float(TIME_0), STEP,CHANNEL_NUMBER)
		cmd_str3 = "*WAI;ARB:SEQ:STEP:VOLT:PULS:TOP %d, %d,(@%d)" %(float(VOLTAGE_1), STEP,CHANNEL_NUMBER)
		cmd_str4 = "*WAI;ARB:SEQ:STEP:VOLT:PULS:TOP:TIM %d, %d,(@%d)" %(float(TIME_1), STEP,CHANNEL_NUMBER)
		cmd_str5 = "*WAI;ARB:SEQ:STEP:VOLT:PULS:END:TIM %d, %d,(@%d)" %(float(TIME_2), STEP,CHANNEL_NUMBER)
		self.write_cmd(cmd_str1)
		self.write_cmd(cmd_str2)
		self.write_cmd(cmd_str3)
		self.write_cmd(cmd_str4)
		self.write_cmd(cmd_str5)
		sleep(1)
		print ""
		print "Pulse Generation Complete..."
		print ""
		print ""
	
	#### All voltage output section #####
	def fetch_watt_hours(self,CHANNEL_VALUE):
		try:
			cmd_str = "FETC:DLOG:WHO? (@%d)" % CHANNEL_VALUE
			watt_hours=self.ask(cmd_str)
			temp_watt_hours=float(watt_hours)*1000  ###Convert to milliamps ####
		except:
			raise Exception("Watt-Hours couldn't be measured")

		#self.writeInFile("Measured Watt-Hours is %f channel %d" %(float(watt_hours),int(CHANNEL_VALUE)))
		self.writeInFile("POWER_1_MW = %f" %float(temp_watt_hours))
		
		
	def fetch_avg_voltage(self,CHANNEL_VALUE):	
		try:
			cmd_str = "FETC:DLOG:VOLT? (@%d)" % CHANNEL_VALUE
			#print cmd_str
			avg_voltage=self.ask(cmd_str)
			#print avg_current
		except:
			raise Exception("Avg voltage couldn't be measured")
		
		#self.writeInFile("Measured Avg Voltage is %f channel %d" %(float(avg_voltage),int(CHANNEL_VALUE)))
		self.writeInFile("VOLTAGE_1_V = %f" %float(avg_voltage))
		
	def fetch_max_voltage(self,CHANNEL_VALUE):
		try:
			cmd_str = "FETC:DLOG:VOLT:MAX? (@%d)" % CHANNEL_VALUE
			max_voltage=self.ask(cmd_str)
		except:
			raise Exception("max-voltage couldn't be measured")
		
		#self.writeInFile("Measured max-voltage is %f channel %d" %(float(max_voltage),int(CHANNEL_VALUE)))
		self.writeInFile("VOLTAGE_2_V = %f" %float(max_voltage))
	
	def fetch_min_voltage(self,CHANNEL_VALUE):
		try:
			cmd_str = "FETC:DLOG:VOLT:MIN? (@%d)" % CHANNEL_VALUE
			min_voltage=self.ask(cmd_str)
		except:
			raise Exception("min-voltage couldn't be measured")
		
		#self.writeInFile("Measured min-voltage is %f channel %d" %(float(min_voltage),int(CHANNEL_VALUE)))
		self.writeInFile("VOLTAGE_3_V = %f" %float(min_voltage))
		
	def fetch_PTPeak_voltage(self,CHANNEL_VALUE):
		try:
			cmd_str = "FETC:DLOG:VOLT:PTP? (@%d)" % CHANNEL_VALUE
			ptp_voltage=self.ask(cmd_str)
		except:
			raise Exception("Peak-to-Peak voltage couldn't be measured")
		
		#self.writeInFile("Measured Peak-to-Peak voltage is %f channel %d" %(float(ptp_voltage),int(CHANNEL_VALUE)))
		self.writeInFile("MEASUREMENT_1 = %f" %float(ptp_voltage))
		
	#### All current output section #####
	def fetch_amp_hours(self,CHANNEL_VALUE):
		try:
			cmd_str = "FETC:DLOG:AHO? (@%d)" % CHANNEL_VALUE
			amp_hours=self.ask(cmd_str)
			temp_amp_hours=float(amp_hours)*1000  ###Convert to milliwatts ####
		except:
			raise Exception("Amp-Hours couldn't be measured")
		
		#self.writeInFile("Measured Amp-Hours is %f channel %d" %(float(amp_hours),int(CHANNEL_VALUE)))
		self.writeInFile("POWER_2_MW = %f" %float(temp_amp_hours*1000))
	def fetch_avg_current(self,CHANNEL_VALUE):	
		try:
			cmd_str = "FETC:DLOG:CURR? (@%d)" % CHANNEL_VALUE
			#print cmd_str
			avg_current=self.ask(cmd_str)
			temp_avg_current=float(avg_current)*1000  ###Convert to milliamps ####
			#print avg_current
		except:
			raise Exception("Avg Current couldn't be measured")
		
		#self.writeInFile("Measured Avg current is %f channel %d" %(float(avg_current),int(CHANNEL_VALUE)))
		self.writeInFile("CURRENT_1_MA = %f" % float(temp_avg_current))
		
	def fetch_max_current(self,CHANNEL_VALUE):
		try:
			cmd_str = "FETC:DLOG:CURR:MAX? (@%d)" % CHANNEL_VALUE
			max_current=self.ask(cmd_str)
			temp_max_current=float(max_current)*1000  ###Convert to milliamps ####
		except:
			raise Exception("max-current couldn't be measured")
		
		#self.writeInFile("Measured max-current is %f channel %d" %(float(max_current),int(CHANNEL_VALUE)))
		self.writeInFile("CURRENT_2_MA = %f" %float(temp_max_current))
		
	def fetch_min_current(self,CHANNEL_VALUE):
		try:
			cmd_str = "FETC:DLOG:CURR:MIN? (@%d)" % CHANNEL_VALUE
			min_current=self.ask(cmd_str)
			temp_min_current=float(min_current)*1000  ###Convert to milliamps ####
		except:
			raise Exception("min-current couldn't be measured")
		
		#self.writeInFile("Measured min-current is %f channel %d" %(float(min_current),int(CHANNEL_VALUE)))
		self.writeInFile("CURRENT_3_MA = %f" %float(temp_min_current))
	
	def fetch_PTPeak_current(self,CHANNEL_VALUE):
		try:
			cmd_str = "FETC:DLOG:CURR:PTP? (@%d)" % CHANNEL_VALUE
			ptp_current=self.ask(cmd_str)
			temp_ptp_current=float(ptp_current)*1000  ###Convert to milliamps ####
		except:
			raise Exception("Peak-to-Peak current couldn't be measured")
		
		#self.writeInFile("Measured Peak-to-Peak current is %f channel %d" %(float(ptp_current),int(CHANNEL_VALUE)))
		self.writeInFile("MEASUREMENT_2 = %f" %float(temp_ptp_current))

	def terminate(self):
		self.power_analyzer.close()
		

















