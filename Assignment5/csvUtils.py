from io import open
from fetchArtist import *
from fetchAlbums import *

def writeArtistsTable(artist_info_list):
    """Given a list of dictionries, each as returned from 
    fetchArtistInfo(), write a csv file 'artists.csv'.

    The csv file should have a header line that looks like this:
    ARTIST_ID,ARTIST_NAME,ARTIST_FOLLOWERS,ARTIST_POPULARITY
    """
    art_file = open("artist.csv", 'w')

    art_file.write(u'ARTIST_ID,ARTIST_NAME,ARTIST_FOLLOWERS,ARTIST_POPULARITY')
    art_file.write(u'\n')

    for i in range(len(artist_info_list)):
        art_file.write(artist_info_list[i]['id'])
        art_file.write(u',')
        art_file.write("%s" %artist_info_list[i]['name'])
        art_file.write(u',')
        art_file.write(unicode(artist_info_list[i]['followers']))
        art_file.write(u',')
        art_file.write(unicode(artist_info_list[i]['popularity']))
        art_file.write(u'\n')

    art_file.close()

      
def writeAlbumsTable(album_info_list):
    """
    Given list of dictionaries, each as returned
    from the function fetchAlbumInfo(), write a csv file
    'albums.csv'.

    The csv file should have a header line that looks like this:
    ARTIST_ID,ALBUM_ID,ALBUM_NAME,ALBUM_YEAR,ALBUM_POPULARITY
    """
    album_file = open("albums.csv", 'w')

    album_file.write(u'ARTIST_ID,ALBUM_ID,ALBUM_NAME,ALBUM_YEAR,ALBUM_POPULARITY')
    album_file.write(u'\n')

    for i in range(len(album_info_list)):
        album = u'%s, %s, "%s", %s, %s' %(album_info_list[i]['artist_id'], album_info_list[i]['album_id'], album_info_list[i]['name'], album_info_list[i]['year'], album_info_list[i]['popularity'])
        album_file.write(album)
        album_file.write(u'\n')

    album_file.close()

if __name__ == '__main__':
    artists = ["annie lennox", "passion pit"]
    artist_ids = [fetchArtistId(x) for x in artists]
    artist_info_list = [fetchArtistInfo(x) for x in artist_ids]
    writeArtistsTable(artist_info_list)

    all_albums = []
    for artist in artist_ids:
        albums_list = fetchAlbumIds(artist)
        for i in range(len(albums_list)):
            all_albums.append(albums_list[i])
    print all_albums
    album_info_list = [fetchAlbumInfo(x) for x in all_albums]
    
    writeArtistsTable(artist_info_list)   
    writeAlbumsTable(album_info_list)

   #writeArtistsTable(artist_info_list)
