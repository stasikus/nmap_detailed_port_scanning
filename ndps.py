#!/usr/bin/python

import sys
import os
import commands

def fileToArray(fileName):
	return [line.rstrip('\n').rstrip('\r') for line in open(fileName)]

def spliting(fullOutput):
	splitedList = fullOutput[1].split("\n")
	finalListOfPorts = []
	for line in range(len(splitedList)):
		if "/" in splitedList[line]:
			finalListOfPorts.append(splitedList[line].split("/")[0])
	finalListOfPorts = finalListOfPorts[1:]
	returnStr = ''
	for line in range(len(finalListOfPorts)):
		returnStr += finalListOfPorts[line] + ","
	print "Found follwing open ports: " + returnStr[:-1]
	return returnStr
	
def check(array, outHostName, startFrom):
	for line in range(0+int(startFrom),len(array)):
		print str(line+1) + " from " + str(len(array)) + " (" + array[line] + ")"
		print "Starting searching for open ports"
		wholeOutput = commands.getstatusoutput("nmap -PS -p 1-65535 " + array[line])
		enumeratedOpenPorts = spliting(wholeOutput)
		print "Starting -A for open ports"
		os.system("nmap -A -p "+enumeratedOpenPorts+" -T3 --script=ssl-heartbleed " + array[line] + " >> nmap_sv_out/" + outHostName + "_out.txt")
		os.system("echo '\n\n--------------------------------\n' >> nmap_sv_out/" + outHostName + "_out.txt")
		print "All details about ports was written into file"
		print "--------------------------------\n"

def startPost(dataFile, outHostName, startFrom):
	array = fileToArray(dataFile)
	check(array, outHostName, startFrom)

def main():
    if len(sys.argv) != 4:
        print "Not enough arguments"
    else:
        startPost(sys.argv[1], sys.argv[2], sys.argv[3])
	#1 - list of hosts; 2 - name of output; 3 - start from (in case of aborting)

if __name__ == "__main__":
	main()
