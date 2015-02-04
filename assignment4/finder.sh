#Print number of rows in the data set 
# call with text file as parameter
wc -l $1

#find all rows with the string Hyde Park
grep --ignore-case 'Hyde Park' permits.csv > permits_hydepark.csv