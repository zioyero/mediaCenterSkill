import SocketServer
import urlparse
import os
import urllib
from findInLibrary import MediaLibrary
from subprocess import Popen, PIPE
from BaseHTTPServer import BaseHTTPRequestHandler
from apiclient.discovery import build
import random

vlc = Popen(["/Applications/VLC.app/Contents/MacOS/VLC", "-I", "macosx", "--extraintf", "rc"], stdin=PIPE)
youtube = build("youtube", "v3", developerKey = "yourDeveloperKey")
pathPrefix = ["/Volumes/First","/Volumes/Second"]
library = MediaLibrary(pathPrefix)

class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse.urlparse(self.path)
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        self.wfile.write("done")
        args = urlparse.parse_qs(parsed.query)
        print(self.path)

        handleCommand(args)


def handleCommand(args):
    if "youtube" in args:
        playFromYoutube(args["youtube"][0])
    elif "youtubePlaylist" in args:
        playFromYoutube(args["youtubePlaylist"][0], queryType = "playlist")
    elif "stop" in args:
        vlc.stdin.write("pause\n")
    elif "resume" in args:
        vlc.stdin.write("play\n")
    elif "fullscreen" in args:
        vlc.stdin.write("f\n")
    elif "next" in args:
        vlc.stdin.write("next\n")
    elif "prev" in args:
        vlc.stdin.write("prev\n")
    elif "volume" in args:
        vlc.stdin.write("volume %s\n" % args["volume"][0])
    elif "plex" in args:
        showName = args["plex"][0]
        seasonNum = args["seasonNum"][0]
        episodeNum = args["episodeNum"][0]
        playFromLibrary(showName, seasonNum, episodeNum)
    elif "plexShuffle" in args:
        showName = args["plexShuffle"][0]
        shuffleFromLibrary(showName)
    elif "plexLatest" in args:
        playLatest(args["plexLatest"][0])
    elif "movie" in args:
        playMovie(args["movie"][0])
    elif "sec" in args:
        fastForward(args["sec"][0])

def playLatest(showName):
    show = library.find_show(showName)
    episodeList = library.list_episode_paths(show)
    if not len(episodeList) == 0:
        vlc.stdin.write("clear\nrandom off\n")
        for mediaPath in episodeList:
            vlc.stdin.write("add %s\n" % mediaPath)

def playMovie(movieQuery):
    """
    Play a movie from the local library
    :param movieQuery:
    :return: None
    """
    movie = library.find_movie_path(movieQuery)
    if movie is not None:
        vlc.stdin.write("clear\nrandom off\n")
        vlc.stdin.write("add %s\n" % movie)

def fastForward(seconds):
    if seconds is not None:
        vlc.stdin.write("seek %d" % seconds)


def shuffleFromLibrary(showName):
    show = library.find_show(showName)
    episodeList = library.list_episode_paths(show)
    print(episodeList)
    if not len(episodeList) == 0:
        vlc.stdin.write("clear\nrandom on\n")
        random.shuffle(episodeList, random.random)
        for mediaPath in episodeList:
            vlc.stdin.write("add %s\n" % mediaPath)
        

def playFromLibrary(showName, seasonNum, episodeNum):
    show = library.find_show(showName)
    index, episodeList = library.index_search(show, int(seasonNum), int(episodeNum))
    print(index, episodeList)
    if not len(episodeList) == 0:
        vlc.stdin.write("clear \nrandom off\n")
        vlc.stdin.write("add %s\n" % episodeList[index])
        truncatedList = episodeList[index + 1:]
        for mediaPath in truncatedList:
            vlc.stdin.write("enqueue %s\n" % mediaPath)


def playFromYoutube(query, queryType = "video"):
    print(query, queryType)

    response = youtube.search().list(q=urllib.unquote(query), part="id,snippet", maxResults=5, type=queryType).execute()

    results = response.get("items", [])

    if queryType == "video" and not len(results) == 0:
        playYoutubeVideos([results[0]["id"]["videoId"]])
    elif queryType == "playlist" and not len(results) == 0:
        playYoutubePlaylist(results[0]["id"]["playlistId"])


def playYoutubeVideos(videoIds):
    vlc.stdin.write("clear\nrandom off\n")

    if not len(videoIds) == 0:
        videoUrl = "http://youtube.com/watch?v=%s" % videoIds[0]
        vlc.stdin.write("add %s \n" % videoUrl)

    for videoId in videoIds[1:]:
        videoUrl = "http://youtube.com/watch?v=%s" % videoId
        vlc.stdin.write("enqueue %s \n" % videoUrl)

def playYoutubePlaylist(playlistId):
    response = youtube.playlistItems().list(part="id,snippet", playlistId=playlistId, maxResults = 50).execute()

    results = response.get("items", [])

    videoIds = map(lambda result: result["snippet"]["resourceId"]["videoId"], results)

    playYoutubeVideos(videoIds)

port = 1234
httpd = SocketServer.TCPServer(("", port), MyHandler)
httpd.serve_forever()