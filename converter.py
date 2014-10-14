import sys
import os
import time
import json
import random

myStrings = tuple(['FREQ_MHZ','TX_POWER_LEVEL','PACKET_TYPE','CURRENT_1_MA','CURRENT_2_MA','CURRENT_3_MA','MEASUREMENT_1','MEASUREMENT_2','POWER_1_MW','POWER_2_MW','VOLTAGE_1_V','VOLTAGE_2_V','VOLTAGE_3_V'])
testCasesDict = {"TpId" : 403, "TpName" : 'Power_Management', "TesterName" : 'Prince',"ProductName" : 'Han Wireless', "SwVersion" : '0.1.21', "HwVersion" : 'DV2',"UniqueId" : str(random.randint(0,99999999))}
testPlanDict = {"TestPlan" : testCasesDict}


	#testCase0 = {'TcId' : 0, 'TcName' : 'Setup', 'TcStartTime' : setupStart,'TestSteps' : testSteps0}#



	#testCase1 = {'TcId' : 1, 'TcName' : 'Power Cycling Test', 'TcStartTime' : testStart,'TestSteps' : testSteps1}#



	#testCasesDict["TestCase0"], testCasesDict["TestCase1"] = testCase0, testCase1#

	

def writeFile(mesg):
	try:
		outputFile = open('C:\outputJsonFile_%d.json' % int(round(time.time())), 'a')
		print mesg
		#outputFile.write(mesg)
		outputFile.write(json.dumps(mesg, sort_keys=True, indent=2, skipkeys=True, separators=(',', ': '))+"\n")
		outputFile.close()	
	except:
		print 'ERROR writing in outputFile'
	
def readFile(filename="C:\Users\prince.masud\Desktop\logOutput.txt"):	
	#inputFile = open("C:\LitePoint\IQfact+\CSR BCx 3.2.0.Eng3_Dongle\Bin\Log\power_log.txt", "r") 
	writeFile(testPlanDict)
	try:
		inputFile = open(filename, "r") 
		for line in inputFile:
			if line.startswith(myStrings):
				newline=line.split()
				writeFile(newline[0]+"\""+":"+newline[2])
		inputFile.close()		
	except:
		print 'COULD NOT LOAD:', filename
 
readFile()