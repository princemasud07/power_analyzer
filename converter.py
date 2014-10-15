import sys
import os
import time
import json
import random
import collections


myStrings = tuple(['FREQ_MHZ','TX_POWER_LEVEL','PACKET_TYPE','CURRENT_1_MA','CURRENT_2_MA','CURRENT_3_MA','MEASUREMENT_1','MEASUREMENT_2','POWER_1_MW','POWER_2_MW','VOLTAGE_1_V','VOLTAGE_2_V','VOLTAGE_3_V'])
testCasesDict = {"TpId" : 403, "TpName" : 'Power_Management', "TesterName" : 'Prince',"ProductName" : 'Han Wireless', "SwVersion" : '0.1.21', "HwVersion" : 'DV2',"UniqueId" : str(random.randint(0,99999999))}
testPlanDict = {"TestPlan" : testCasesDict}
rowarray_list=[]

def writeFile(mesg):
	try:
		outputFile = open('C:\outputJsonFile_%d.json' % int(round(time.time())), 'a')
		outputFile.write(json.dumps(mesg, sort_keys=True, indent=4, separators=(',', ': '))+"\n")
		outputFile.close()	
	except:
		print 'ERROR writing in outputFile'

def dict_merge(old, new):
	current = old.copy()
	current.update(new)
	return current

		
def readFile(filename="C:\Users\prince.masud\Desktop\logOutput.txt"):	
	#inputFile = open("C:\LitePoint\IQfact+\CSR BCx 3.2.0.Eng3_Dongle\Bin\Log\power_log.txt", "r") 
	rowarray_list.append(testPlanDict)
	newlist={}
	count=0
	try:
		inputFile = open(filename, "r") 
		for line in inputFile:
			d = collections.OrderedDict()
			newline=line.split()
			if line.startswith(myStrings):
				d[newline[0]] = newline[2]	
				newlist=dict_merge(newlist,d)
				count=count+1
			if (count==len(myStrings)):
				rowarray_list.append(newlist)
				newlist={}
				count=0
		writeFile(rowarray_list)
		inputFile.close()		
	except:
		print 'COULD NOT LOAD:', filename

readFile()