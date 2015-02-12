import unicodecsv as csv
import matplotlib.pyplot as plt

def getBarChartData():
    #open the csv files for reading, also I switched it from artists to artist because I named my csv file wrong earlier
    f_artists = open('artist.csv')
    f_albums = open('albums.csv')

    #read the csv files, returns an object
    artists_rows = csv.reader(f_artists)
    albums_rows = csv.reader(f_albums)

    #defines as header the first item (obtained by next which simply takes the next item out) 
    artists_header = artists_rows.next()
    albums_header = albums_rows.next()

    #create an empty list to fill
    artist_names = []
    
    #creates a list from 1900 to 2020 by tens
    decades = range(1900,2020, 10)
    #creates an empty dictionary
    decade_dict = {}
    #iterates through each number (element) in decades list, fills dictionary in with the keys as each decade in the decades list and initializes all values to 0
    for decade in decades:
        decade_dict[decade] = 0
    
    #cycles through each row in the data read from the artists.csv file
    for artist_row in artists_rows:
        #if the row is empty, skips over it
        if not artist_row:
            continue
        #if the row is not empty then it assigns each element of the row to a variable
        artist_id,name,followers, popularity = artist_row
        #appends the name of the artist to a list
        artist_names.append(name)

    #cycles through each row in the data read from the albums.csv file
    for album_row  in albums_rows:
        #if the row is empty, skips over it
        if not album_row:
            continue
        #if the row is not empty then it assigns each element of the row to a variable
        print album_row
        artist_id, album_id, album_name, year, popularity = album_row
        #iterates through each element in the decades list
        for decade in decades:
            #if the album year assigned to 'year' above is inbetween the current decade and the next decade
            if (int(year) >= int(decade)) and (int(year) < (int(decade) + 10)):
                #then the dictionary value associated with the key for that decade is updated one count, then you leave the loop of the decades list and go to the next row
                decade_dict[decade] += 1
                break

    #the decades are defined as the x-values, and the y-values are the values (counts) associate with each decade key in the dictionary
    x_values = decades
    y_values = [decade_dict[d] for d in decades]
    #return the x-values, y-values, and artist_names list

    return x_values, y_values, artist_names

def plotBarChart():
    x_vals, y_vals, artist_names = getBarChartData()
    
    fig , ax = plt.subplots(1,1)
    ax.bar(x_vals, y_vals, width=10)
    #sets the label for the x axis as "decades"
    ax.set_xlabel('decades')
    #sets a lable for the y-axis as "number of albums"
    ax.set_ylabel('number of albums')
    #writes a title for the graph, title is "Totals for 'list of aritsts names'" where lists of artists names is the list of artits
    ax.set_title('Totals for ' + ', '.join(artist_names))
    #forces the bar graph to pop up on the screen
    plt.show()

