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
c = db.cursor()

app = Flask(__name__)


@app.route('/')
def make_index_resp():
    # this function just renders templates/index.html when
    # someone goes to http://127.0.0.1:5000/
    return(render_template('index.html'))


@app.route('/playlists/')
def make_playlists_resp():
    return render_template('playlists.html',playlists=playlists)


@app.route('/playlist/<playlistId>')
def make_playlist_resp(playlistId):
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
        artistName = str(song[0])
        albumName = str(song[1])
        print albumName
        trackName = str(song[2])
        print trackName
        row = 'INSERT INTO songs (playlistId, songOrder, artistName, albumName, trackName) VALUES (%d, %d, %s, %s, %s)' %(playlistId, songOrder, artistName, albumName, trackName)
        c.execute(row)
        songOrder = songOrder + 1

    db.commit()
    c.close()
    db.close()


if __name__ == '__main__':
    #app.debug=True
    #app.run()
    createNewPlaylist("Coldplay")
