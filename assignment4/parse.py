import csv
import sys
import matplotlib.pyplot as plt
import numpy as np

def readCSV(filename):
    '''Reads the CSV file `filename` and returns a list
    with as many items as the CSV has rows. Each list item 
    is a tuple containing the columns in that row as stings.
    Note that if the CSV has a header, it will be the first
    item in the list.'''
    with open(filename,'r') as f:
        rdr = csv.reader(f)
        lines = list(rdr)
    return(lines)

#lines = readCSV('permits.csv')
#print lines[1]
### enter your code below

def get_avg_latlng(lines):
	numEntries = float(len(lines))
	latPos = 128
	lngPos = 129

	#sum lat and lng
	latSum = 0.0
	lngSum = 0.0

	for i in lines:
		if i[latPos] != "":
			lat = float(latPos)
			latSum = latSum + lat
		if i[lngPos] != "":
			lng = float(lngPos)
			lngSum = lngSum + lng

	avgLat = latSum/numEntries
	avgLng = lngSum/numEntries
	return (avgLat, avgLng)

def zip_code_dict(lines):
	#create dict of zips
	zipCounts = {} 
	allZips = [] 
	for line in lines:
		projZipList = []
		zipOrder = 26
		#zip is every 6th, first zip is the 26th
		while zipOrder < 131:
			projZipList.append(line[zipOrder])
			zipOrder = zipOrder + 6
		
		alreadyFound = False

		#go through all of the contracter zip codes on this project (in this line)
		for projZip in projZipList: 
			#compare each of the current project zips to the list of zips already in the dict
			for zipcode in allZips:
				#if you find the project Zip is already in the dictionary, add one to the value of the entry
				if zipcode == projZip:
					zipCounts[zipCode] = zipCounts[zipCode] + 1
					alreadyFound = True
			#if you did not find 
			if alreadyFound == False:
				allZips.append(projZip)
				zipCounts[projZip] = 1
	return zipCounts

def zip_code_barchart(zipRecords):
	#zipRecords = zip_code_dict(lines)
	zipCodes = []
	zipCounts = []

	print zipRecords

	#go through each item in the dictionary and convert int two lists by appending to end (preserve order)
	for code, count in zipRecords.items():
		zipCodes.append(code)
		zipCounts.append(count)

	#build bar chart
	x = np.arange(len(zipCodes))
	
	plt.bar(x, zipCounts)
	plt.xticks(x+0.5, zipCodes, rotation = 90)
	plt.show() #will force plots to come uo
	return 0



if __name__ == "__main__":
	#lines = readCSV(sys.argv[1])
	#print len(lines[1]) #output- 131 lines
	#avgLoc = get_avg_latlng(lines)
	#print avgLoc
	testZips = {"zip0":1, "zip1":4}
	zip_code_barchart(testZips)