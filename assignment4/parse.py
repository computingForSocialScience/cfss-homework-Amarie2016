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

def get_avg_latlng(filename):
	lines = readCSV(filename)
	lines = lines[:10]
	numEntries = 0 #float(len(lines)) - 1.0
	latPos = 128
	lngPos = 129

	#sum lat and lng
	latSum = 0.0
	lngSum = 0.0

	for line in range(1,len(lines)):
		i = lines[line]
		if i[latPos] != "" and i[lngPos] != "":
			numEntries = numEntries + 1
			lat = float(i[latPos])
			latSum = latSum + lat
			lng = float(i[lngPos])
			lngSum = lngSum + lng

	avgLat = latSum/numEntries
	avgLng = lngSum/numEntries
	return (avgLat, avgLng)

def zip_code_dict(lines):
	#create dict of zips
	zipCounts = {} 
	allZips = [] 

	for project in lines:
		projZipList = []
		zipOrder = 28
		#zip is every 6th, first zip is the 28th...
		#get list of all zipcodes listed for project: THIS WORKS
		while zipOrder < 127:
			projZipList.append(project[zipOrder])
			zipOrder = zipOrder + 6
	
		alreadyFound = False

		#go through all of the contracter zip codes on this project (in this line)
		for projZip in projZipList: 
			#make sure it is a real zip code
			if len(projZip) < 5:
					break
			else:
				projZip = projZip[0:5]
			#compare each of the current project zips to the list of zips already in the dict
			for zipcode in allZips:
				#if you find the project Zip is already in the dictionary, add one to the value of the entry
				if zipcode == projZip:
					zipCounts[zipcode] = zipCounts[zipcode] + 1
					alreadyFound = True
			#if you did not find 
			if alreadyFound == False:
				allZips.append(projZip)
				zipCounts[projZip] = 1
	del zipCounts["CONTR"]
	return zipCounts

def zip_code_barchart(name):
	lines = readCSV(name)
	#lines = lines[:500]
	zipRecords = zip_code_dict(lines)
	zipCodes = []
	zipCounts = []

	#go through each item in the dictionary and convert int two lists by appending to end (preserve order)
	for code, count in zipRecords.items():
		zipCodes.append(code)
		zipCounts.append(count)

	#build bar chart
	x = np.arange(len(zipCodes))
	
	plt.bar(x, zipCounts) 
	plt.title("Zipcodes of contracters")
	plt.xlabel('Zipcodes')
	plt.ylabel('Number of Contracters')
	plt.xticks(x+0.5, zipCodes, rotation = 90)
	plt.show() #will force plots to come uo
	return 0



if __name__ == "__main__":
	choice = sys.argv[1]
	fileName = sys.argv[2]
	if choice == "latlong":
		print get_avg_latlng(fileName)
	elif choice == "hist":
		print zip_code_barchart(fileName)
	else:
		print "invalid call, please give the chosen function and data set as arguments"