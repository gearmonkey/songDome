#!/usr/bin/env python
# encoding: utf-8
"""
tests.py

Created by Benjamin Fields on 2011-01-23.
Copyright (c) 2011 Goldsmith University of London. All rights reserved.
"""

import sys
import os, os.path
import unittest
import nose

from songDome import *

TEST_AUDIO_A = "AC_Slater_Play_the_Record_Again_Mastered.mp3"
TEST_AUDIO_B = "KeSha - Tik Tok (Grayskull Remix).mp3"

TEST_URL_A = ""
TEST_URL_B = ""

class LocalTest(unittest.TestCase):
	def setUp(self):
		pass
	def zippingLocalTest(self):
		#this is a shitty test
		songA = audio.LocalAudioFile(TEST_AUDIO_A)
		songB = audio.LocalAudioFile(TEST_AUDIO_B)
		zipSongs(songA, songB, 'test.mp3')
		assert os.path.exists('test.mp3')
		#should I just test existance? seems weak...
		os.remove('test.mp3')
	
	def randomizedLocalTest(self):
		songA = audio.LocalAudioFile(TEST_AUDIO_A)
		songB = audio.LocalAudioFile(TEST_AUDIO_B)
		zipSongs(songA, songB, 'test.mp3', random_order=True)
		assert os.path.exists('test.mp3')
		os.remove('test.mp3')
	
	def varLengthLocalTest(self):
		songA = audio.LocalAudioFile(TEST_AUDIO_A)
		songB = audio.LocalAudioFile(TEST_AUDIO_B)
		zipSongs(songA, songB, 'test.mp3', battle_length=4)
		assert os.path.exists('test.mp3')
		os.remove('test.mp3')

if __name__ == '__main__':
	unittest.main()