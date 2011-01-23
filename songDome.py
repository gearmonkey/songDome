#!/usr/bin/env python
# encoding: utf-8
"""
songDome.py




Created by Benjamin Fields on 2011-01-23.
Copyright (c) 2011 Goldsmith University of London. All rights reserved.
"""

try:
	import cgitb
	cgitb.enable()
except ImportError:
    sys.stderr = sys.stdout

print "content-type: text/html\n\n"

import sys
import cgi
import urllib2
import random
from os.path import join, exists
from simplejson import loads, dumps

import echonest.audio as audio
from echonest.selection import fall_on_the

from my_key import EN_API_KEY #a file inline that contains an echonest key
from pyechonest import config
config.ECHO_NEST_API_KEY=EN_API_KEY

CACHE_DIR = "./cache/"
DOMAIN_PATH = "http://songdome.benfields.net/"


help_message = '''
The help message goes here.
'''


class Usage(Exception):
	def __init__(self, msg):
		self.msg = msg

def zipSongs(songA, songB, outfile_name, battle_length = 8, random_order = False):
	"""
	alternates between a downbeat from songA and a downbeat from songB for battle_length number of bars from each, then play the remainder from songA.
	
	if random_order is True then songA will still always win but the playorder will be reversed approximately half the time.

	"""
	if random_order == True and random.sample([True, False], 1)[0]:
		firstSong = songB
		secondSong = songA
		flipped = True
	else:
		firstSong = songA
		secondSong = songB
		flipped = False
	onesA = firstSong.analysis.beats.that(fall_on_the(1))
	onesB = secondSong.analysis.beats.that(fall_on_the(1))
		
	lacedUp = audio.AudioData(shape=
		(int(1.2*len(firstSong.data)),2), numChannels=firstSong.numChannels, sampleRate=firstSong.sampleRate)
	for bar_num in xrange(battle_length):
		lacedUp.append(audio.getpieces(firstSong, [onesA[bar_num]]))
		lacedUp.append(audio.getpieces(secondSong, [onesB[bar_num]]))
	if flipped:
		lacedUp.append(audio.getpieces(firstSong, [onesA[5]]))
	lacedUp.append(audio.getpieces(SongA,SongA.analysis.bars[battle_length:]))
	lacedUp.encode(outfile_name)
	return

def getIDFromName(artist, fuzzy_match=False):
	res = urllib2.urlopen(\
		"http://developer.echonest.com/api/v4/artist/search?api_key=%s&format=json&name=%s&fuzzy_match=%s"%\
		(EN_API_KEY,artist.replace(' ','%20'), str(fuzzy_match).lower()))
	out = res.read()
	res.close()
	return loads(out)['response']['artists'][0]['id']

def fetch7DigUrl(artist, sort_order = "song_hotttnesss-desc"):
	artistID = getIDFromName(artist)
	res = urllib2.urlopen("http://developer.echonest.com/api/v4/song/search?api_key=%s&format=json&results=1&artist_id=%s&sort=%s&bucket=id:7digital&limit=true&bucket=tracks"%(EN_API_KEY,artistID, sort_order))
	out = res.read()
	res.close()
	#this should blow up if the track doesn't exist, should handle that in a reasonable way
	return loads(out)['response']['songs'][0]['tracks'][0]['preview_url']

def dlFile2Disk(url,filename):
	req = urllib2.urlopen(url)
	CHUNK = 16 * 1024
	fp = open(filename, 'wb')
	while True:
		chunk = req.read(CHUNK)
		if not chunk: break
		fp.write(chunk)

def grabSongForArtist(artist, emphasis = "song_hotttnesss-desc"):
	"""
	grab the most relevant 7digital clip for a track based on the emphasis call which must be one of the valid values for sort strings as documented at http://developer.echonest.com/docs/v4/song.html#search
	after the song is dl'd (or the cache is found to exist and be sufficiently fresh) it's loaded in as a remix audio object and returned
	"""
	#dirty cache, for now it never expires
	filename = join(CACHE_DIR, artist+emphasis+'.mp3')
	if not exists(filename):
		dlFile2Disk(fetch7DigUrl(artist, emphasis), filename)
	return audio.LocalAudioFile(filename)

def main(argv=None):
	if argv==None:
		form = cgi.FieldStorage()
		artistA = form.getfirst("artist1")
		artistB = form.getfirst("artist2")
		if None in [artistA, artistB]:
			print dumps({'return_code':'error::give two artists.'}) 
			return
		select_track_by = form.getfirst("select", "song_hotttnesss-desc")
		try:
			battle_length = int(form.getfirst("battle_length", "8"))
		except ValueError:
			print dumps({'return_code':'error::battle_length could not be converted to an integer.'})
			return
	outfile = join(CACHE_DIR, "zipped_"+artistA+"_"+artistB+select_track_by+".mp3")
	# dirty cache here as well... no expire
	if not exists(outfile):
		songA = grabSongForArtist(artistA) #returns the echonest audio object for the song
		songB = grabSongForArtist(artistB)
		zipSongs(songA, songB, outfile)
	print dumps({'return_code':'ok','available_as':join(DOMAIN_PATH,file_name.lstrip('./'))})
	return

if __name__ == "__main__":
	sys.exit(main())
