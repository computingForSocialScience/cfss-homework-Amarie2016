"""NOTE: I am still habing some major encoding errors because windows is actually built for a secret sadist to spy on me and laugh at my tears.
I think this works more consistently on not-windows, but only tried on alyssa's mac once or twice.
Thanks for being nice to me."""

from flask import Flask, render_template, request, redirect, url_for
import pymysql

from artistNetworks import *
from analyzeNetworks import *
from fetchArtist import *
from fetchAlbums import *
from makePlaylist import *

dbname="playlists"
host="localhost"
user="root"
passwd="raingirl13"
db=pymysql.connect(db=dbname, host=host, user=user,passwd=passwd, charset='utf8')


app = Flask(__name__)


@app.route('/')
def make_index_resp():
    # this function just renders templates/index.html when
    # someone goes to http://127.0.0.1:5000/
    return(render_template('index.html'))


@app.route('/playlists/')
def make_playlists_resp():
    c = db.cursor()
    c.execute("SELECT * FROM playlists")
    playlists = c.fetchall()
    return render_template('playlists.html',playlists=playlists)


@app.route('/playlist/<listId>')
def make_playlist_resp(listId):
    c = db.cursor()
    #c.execute("SELECT playlistId, songOrder, artistName, albumName, trackName FROM songs WHERE playlistId='playlistId' ORDER BY songOrder")
    #getList = "SELECT * FROM songs WHERE playlistId=%s ORDER BY songOrder"
    #c.execute(getList, (listId))
    c.execute("SELECT * FROM songs WHERE playlistId=1")
    songs = c.fetchall()
    #print songs
    return render_template('playlist.html',songs=songs)


@app.route('/addPlaylist/',methods=['GET','POST'])
def add_playlist():
    if request.method == 'GET':
        # This code executes when someone visits the page.
        return(render_template('addPlaylist.html'))
    elif request.method == 'POST':
        # this code executes when someone fills out the form
        artistName = request.form['artistName']
        # YOUR CODE HERE
        return(redirect("/playlists/"))

def createNewPlaylist(artist):
    c = db.cursor()
    makePlaylists = "CREATE TABLE IF NOT EXISTS playlists (ID INT PRIMARY KEY AUTO_INCREMENT, rootArtist VARCHAR(300)) ENGINE=MyISAM DEFAULT CHARSET=utf8"
    makeSongs = "CREATE TABLE IF NOT EXISTS songs (playlistId INT, songOrder INT, artistName VARCHAR(300), albumName VARCHAR(300), trackName VARCHAR(300)) ENGINE=MyISAM DEFAULT CHARSET=utf8"
    c.execute(makePlaylists)
    c.execute(makeSongs)
    """print 'selecting...'
    sql3 = "select * from playlists"
    c.execute(sql3)
    test = c.fetchall()
    print "return values are: ", test"""

    #add the artist's name to the playlists table"
    addRootPlay = "INSERT INTO playlists (rootArtist) VALUES ('%s')" %artist
    c.execute(addRootPlay)
    #get the playlist id associated with this new row"
    getRootId = "SELECT ID FROM playlists WHERE rootArtist = '%s'" %artist
    c.execute(getRootId)
    rootId = c.fetchall()[0][0]
    print "root id is:", rootId

    #create songs list
    artists = chooseArtists([artist])
    play_list = chooseList(artists)
    print "length of playlist:", len(play_list)

    print play_list[:1]

    #record playlist
    playlistId = rootId
    songOrder = 1
    for song in play_list:
        artistName = song[0]
        albumName = song[1]
        trackName = song[2]
        #print trackName
        row = 'INSERT INTO songs (playlistId, songOrder, artistName, albumName, trackName) VALUES (%d, %d, %s, %s, %s)' # %(playlistId, songOrder, artistName, albumName, trackName)
        c.execute(row,(playlistId, songOrder, artistName, albumName, trackName))
        songOrder = songOrder + 1

    c.execute("SELECT * FROM playlists")
    playlists = c.fetchall()
    print "playlists type", type(playlists)
    print "playlists 1", type(playlists[0]), playlists[0]
    c.execute("SELECT * FROM songs WHERE playlistId=1")
    songs = c.fetchall()
    print "songs type", type(songs)
    print "songs 1", type (songs[0]), songs[0]
    db.commit()
    c.close()
    #db.close()


if __name__ == '__main__':
    #createNewPlaylist("Coldplay")
    #createNewPlaylist("Spoon")
    #createNewPlaylist("Metric")

    app.debug=True
    app.run(port=5001)