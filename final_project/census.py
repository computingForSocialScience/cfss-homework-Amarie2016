import sys
import requests
import pymysql

dbname="census"
host="localhost"
user="root"
passwd="raingirl13"
db=pymysql.connect(db=dbname, host=host, user=user,passwd=passwd, charset='utf8')


"""def getsexWorkHours():
	searchlink = "http://api.censusreporter.org/1.0/table/B23022"
	data = requests.get(searchlink)
	data = data.json()
	#print "keys for the page", data.keys()
	tblTitle = data['table_title']
	denomColId = data["denominator_column_id"]
	columnIds = data['columns'].keys()
	columns = {}
	for colId in columnIds:
		columns[colId] = data['columns'][colId]['column_title']
	print columns"""

Ds = 'B19125'
def getTableInfo(tableID):
	url = 'http://api.censusreporter.org/1.0/table/' +tableID
	r = requests.get(url).json()
	title = r['table_title']
	columns = r['columns']
	#column_IDs = []
	#column_titles = []
	cols = []
	for k,v in columns.items():
		#column_IDs.append(k)
		#print v
		#column_titles.append(v[u'column_title'])
		cols.append((k,v[u'column_title']))
	denominator_column_id = r['denominator_column_id']
	#get table info
	tableInfo = {}
	tableInfo['title'] = str(title)
	tableInfo['tableID'] = str(tableID)
	#tableInfo['column_IDs'] = column_IDs
	#tableInfo['column_titles'] = column_titles
	tableInfo['cols'] = cols
	tableInfo['denomColId'] = str(denominator_column_id)
	#order columns
	colIdOrder = []
	for col in cols:
		colIdOrder.append(col[0])
	print colIdOrder
	return tableInfo, colIdOrder

def info_table(tableTopics):
	#columnInfoTable 
	c = db.cursor()
	columnInfoTable = "CREATE TABLE IF NOT EXISTS columnInfoTable (colID VARCHAR(500), colName VARCHAR(500), tableID VARCHAR(500), tableName VARCHAR(800), denomColId VARCHAR(500)) ENGINE=MyISAM DEFAULT CHARSET=utf8"
	c.execute(columnInfoTable)
	#for each tableID
	for topic in tableTopics:
		#get the column Order
		info, colOrder = getTableInfo(topic)
		#for each column (in order)
		for colID in colOrder:
			#print "colID", colID
			#find matching column name
			for column in info['cols']:
				if column[0] == colID:
					colName = str(column[1])
			row = "INSERT INTO columnInfoTable (colID, colName, tableID, tableName, denomColId) VALUES (%s, %s, %s, %s, %s)"
			c.execute(row, (colID, colName, info['tableID'], info['title'], info['denomColId']))
	db.commit()
	c.close()

def getTableData(tableID):
	FIPS_dict = {"Mississippi": 28, "Oklahoma": 40, "Delaware": 10, "Minnesota": 27, "Illinois": 17, "Arkansas": 5, "New Mexico": 35, "Indiana": 18, "Maryland": 24, "Louisiana": 22, "Idaho": 16, "Wyoming": 56, "Tennessee": 47, "Arizona": 4, "Iowa": 19, "Michigan": 26, "Kansas": 20, "Utah": 49, "Virginia": 51, "Oregon": 41, "Connecticut": 9, "Montana": 30, "California": 6, "Massachusetts": 25, "West Virginia": 54, "South Carolina": 45, "New Hampshire": 33, "Wisconsin": 55, "Vermont": 50, "Georgia": 13, "North Dakota": 38, "Pennsylvania": 42, "Florida": 12, "Alaska": 2, "Kentucky": 21, "Hawaii": 15, "Nebraska": 31, "Missouri": 29, "Ohio": 39, "Alabama": 1, "New York": 36, "South Dakota": 46, "Colorado": 8, "New Jersey": 34, "Washington": 53, "North Carolina": 37, "District of Columbia": 11, "Texas": 48, "Nevada": 32, "Maine": 23, "Rhode Island": 44}
	info, colIdOrder = getTableInfo(tableID)
	allData = []
	
	for region, fips in FIPS_dict.items():
		#get the page for specific tableID and fips in json-- "data" is a dictionary
		searchlink = "http://api.censusreporter.org/1.0/data/show/latest?table_ids=" + tableID +"&geo_ids=04000US" + str(fips) 
		data = requests.get(searchlink)
		data = data.json()
		#get rid of error entries and get info for each row	
		if data.keys()[0] != u'error':
			dataTitle = data['data']
			dataRegion = data['data'][data['data'].keys()[0]]
			
			dataTableID = dataRegion.keys()[0]
			dataTable = dataRegion[dataTableID]['estimate']
			dataTableError = dataRegion[dataTableID]['error']
			
			#make list of tuples of (coolumnId, columnData)
			columns = []
			for colId in colIdOrder:
				columns.append((colId, dataTable[str(colId)]))
			
			fips = str(fips)
			geoID = str(data['geography'].keys()[0])
			allData.append((geoID, fips, columns))
		
	#allData is a list of tuples with lists inside- each row corresponds to a different fips number
	# each row is a tuple: (geoId, fips, columns) where geoID, fips are strings and columns is a list of tuples
	# columns is a list of tuples with each tuple (colId, data)		
	return allData, colIdOrder

	
def data_table(tableID):
	allData, colIdOrder = getTableData("B19019")
	print type(colIdOrder)
	#print type(geoIDs), type(fipslist), type(columnData), type(allData)
	#print geoIDs, fipslist
	c = db.cursor()
	create = "CREATE TABLE IF NOT EXISTS "+str(tableID)+" (geoID VARCHAR(500), fips VARCHAR(300), "+str(colIdOrder[0])+" VARCHAR (300), "+str(colIdOrder[1])+" VARCHAR (300), "+str(colIdOrder[2])+" VARCHAR (300), "+str(colIdOrder[3])+" VARCHAR (300), "+str(colIdOrder[4])+" VARCHAR (300), "+str(colIdOrder[5])+" VARCHAR (300), "+str(colIdOrder[6])+" VARCHAR (300), "+str(colIdOrder[7])+" VARCHAR (300))"
	c.execute(create)
	#print allData[0], allData[1]
	for row in allData:
		insert_data = "INSERT INTO B19019 (geoID, fips, "+str(colIdOrder[0])+", "+str(colIdOrder[1])+", "+str(colIdOrder[2])+", "+str(colIdOrder[3])+", "+str(colIdOrder[4])+", "+str(colIdOrder[5])+", "+str(colIdOrder[6])+", "+str(colIdOrder[7])+") VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"  
		c.execute(insert_data, (row[0], row[1], row[2][0][1], row[2][1][1], row[2][2][1], row[2][3][1], row[2][4][1], row[2][5][1], row[2][6][1], row[2][7][1]))
	db.commit()
	c.close()
	


if __name__ == '__main__':
	#print getsexWorkHours()
	#getTableData()
	#ACSDatabase("B19019")
	data_info('B19019')
	data_table('B19019')
		
	#intoDatabase()