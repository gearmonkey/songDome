#!/usr/bin/env python
# encoding: utf-8
"""
songBoxing.py




Created by Benjamin Fields on 2011-01-23.
Copyright (c) 2011 Goldsmith University of London. All rights reserved.
"""

import sys
import cgi





# track selection methods
LASTFM_POP = 0

help_message = '''
The help message goes here.
'''


class Usage(Exception):
	def __init__(self, msg):
		self.msg = msg


def main(argv=None):
	if argv=None:
		argv = sys.argv()
	if not len(argv) in [2,3]:
		raise Usage('not enough args...')
	artistA = argv[0]
	artistB = argv[1]
	if len(argv) == 3:
		select_track_by = argv[2]
	else:
		select_track_by = LASTFM_POP
		
	songA = selectArtistSong(artistA)
	songB = selectArtistSong(artistB)
	fetchAudio()
	grabDownBeatsA()
	grabDownBeatsB()
	laceTrackTogether()
	return track


if __name__ == "__main__":
	sys.exit(main())
