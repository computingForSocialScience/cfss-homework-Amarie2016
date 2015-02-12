import sys
from fetchArtist import fetchArtistId, fetchArtistInfo
from fetchAlbums import fetchAlbumIds, fetchAlbumInfo
from csvUtils import writeArtistsTable, writeAlbumsTable
from barChart import plotBarChart

if __name__ == '__main__':
    artist_names = sys.argv[1:]
    print "input artists are ", artist_names
    
    #create list of artist ids
    artist_ids = []
    for name in artist_names:
    	artist_ids.append(fetchArtistId(name))

    #create list of artist info dictionaries
    artist_info = []
    for artID in artist_ids:
    	artist_info.append(fetchArtistInfo(artID))

    #create artists.csv
    writeArtistsTable(artist_info)

    #create list of album ids
    albums = []
    for artist in artist_ids:
    	artists_albums = fetchAlbumIds(artist)
    	for album in artists_albums:
    		albums.append(fetchAlbumInfo(album)) 

    #create albums.csv
    writeAlbumsTable(albums)

    plotBarChart()
