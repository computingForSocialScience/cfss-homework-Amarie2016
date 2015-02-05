import csv
import sys

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


if __name__ == "__main__":
	lines = readCSV(sys.argv[1])
	#print len(lines[1]) #output- 131 lines
	#line = lines[1]
	#print line[130]
	avgLoc = get_avg_latlng(lines)
	print avgLoc