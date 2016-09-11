import urllib2 
import csv
from datetime import datetime
import logging
import argparse

logging.basicConfig(filename='error.log',level=logging.ERROR) 

parser = argparse.ArgumentParser(description='Download a CSV and process it.')
parser.add_argument('--url', help='Download data from specified URL')

def downloadData(url):
	try:
		csvData = urllib2.urlopen(url)
		return csvData
	except:
		print 'ERROR:Unable to read the given URL: ' + url
		exit()

def processData(data): # data is a response from downloadData
	data = csv.reader(data) 
	data.next() # consume the header
	processed = {}
	for line in data: # loop through the csv and transform into dictionary
	    key = int(line[0])
	    name = line[1]
	    try: # control for malformed data
	    	date = datetime.strptime(line[2], '%d/%m/%Y')
	     	value = tuple((name, date))
	     	processed[key] = value
	    except:
		    logging.error(	'Unable to process line ' \
		    				+ str(key) + ' ... Value: ' \
		    				+ line[2])
	return processed

def displayPerson(idNum, personData):
	person = []
	try:
		person = personData[idNum]
		print	"Person " + str(idNum) + " is " \
				+ person[0]  + " with a birthday of " \
				+ str(person[1])		
	except:
		print 'No user found with that id'

def main():
	args = parser.parse_args()
	url = args.url

	if not url:
		print 'ERROR: No URL provided'
		exit()

	csvData = downloadData(url)
	personData = processData(csvData)

	while True:
		try:
			idNum = int(raw_input('enter the id: '))
		except:
			print 'ERROR: Invalid ID type'
			exit()
		if(idNum < 0):
			exit()
		displayPerson(idNum, personData)

main()