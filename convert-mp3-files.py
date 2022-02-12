import eyed3
import spotipy
import spotipy.util as util
import os
import urllib
import json
from config import *

def getEyeD3Tag(path):
    """"""
    trackInfo = eyed3.load(path)
    tag = trackInfo.tag
    print("Artist: %s" % tag.artist)
    print("Album: %s" % tag.album)
    print("Track: %s" % tag.title)
    return tag

def getSpotifyToken():
    token = util.prompt_for_user_token(USERNAME, scope='playlist-modify-private,playlist-modify-public', client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri='https://localhost:8080')
    if token:
        return token
    else:
        print ("Can't get token for", USERNAME)

def getTracksAndAddToPlaylist(token,tags):
    sp = spotipy.Spotify(auth=token)
    for tag in tags:
        query = "album:%s&artist:%s&track:%s" % (tag.album,tag.artist,tag.title)
        track_results = sp.search(query,limit=2,type='track')
        song_ids = []
        print(track_results['tracks']['items'])
        items = track_results['tracks']['items']
        for item in items:
            song_ids.append(item["id"])
        if(len(song_ids)>0):
            sp.user_playlist_add_tracks(user=USERNAME, playlist_id=PLAYLIST_ID, tracks=song_ids)


def main():
    mp3_files = []
    for i in os.scandir(SOURCE_PATH):
        if i.is_file():
            mp3_files.append(i.path)
    
    tags = []
    for file in mp3_files:
        tag = getEyeD3Tag(file)
        tags.append(tag)

    token = getSpotifyToken()
    getTracksAndAddToPlaylist(token,tags)

if __name__ == '__main__':
    main()
