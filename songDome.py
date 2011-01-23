#!/usr/bin/env python
# encoding: utf-8
"""
songDome.py




Created by Benjamin Fields on 2011-01-23.
Copyright (c) 2011 Goldsmith University of London. All rights reserved.
"""

import sys
import cgi

import cgitb
cgitb.enable()

import echonest.audio as audio
from echonest.selection import fall_on_the



# track selection methods
LASTFM_POP = 0

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
	if random_order == True:
		raise NotImplemented('no random order yet')
	onesA = songA.analysis.beats.that(fall_on_the(1))
	onesB = songB.analysis.beats.that(fall_on_the(1))
	
	lacedUp = audio.AudioData(shape=
		(int(1.2*len(songA.data)),2), numChannels=2, sampleRate=44100)
	for bar_num in xrange(8):
		#xrange is numoverlaping downbeats
		lacedUp.append(audio.getpieces(songA, [onesA[bar_num]]))
		lacedUp.append(audio.getpieces(songB, [onesB[bar_num]]))
	lacedUp.encode(outfile_name)
	return


def main(argv=None):
	if argv==None:
		argv = sys.argv()
	if not len(argv) in [2,3,4]:
		raise Usage('not enough args...')
	artistA = argv[0]
	artistB = argv[1]
	if len(argv) == 3:
		select_track_by = argv[2]
	else:
		select_track_by = LASTFM_POP

	
	songA = selectArtistSong(artistA) #returns the echonest audio object for the song
	songB = selectArtistSong(artistB)
	
	zipSongs(song)
	return domain_name+file_name #this should actually be lightly json wrapped me thinks


if __name__ == "__main__":
	sys.exit(main())
