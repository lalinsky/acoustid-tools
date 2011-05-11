#!/usr/bin/env python

import re
import sys
import time
import os
from chromaprint import Fingerprinter, decode_fingerprint
from audiodecoder import AudioDecoder

#print libchromaprint.chromaprint_get_version()
print "=> Decoding audio data"
decoder = AudioDecoder(sys.argv[1])
length, sample_rate, num_channels, data = decoder.decode(45)
print "=> Length:", length
print "=> Sample rate:", sample_rate
print "=> Number of channels:", num_channels

print "=> Calculating fingerprint"
fpcal = Fingerprinter()
fpcal.start(sample_rate, num_channels)
fpcal.feed(data)
fingerprint = fpcal.finish()

import urllib, urllib2
import json

data = {}
data['client'] = '8XaBELgH'
data['format'] = 'json'
data['meta'] = '2'
data['duration'] = str(length)
data['fingerprint'] = fingerprint
print "=> Looking up fingerprint"
a = time.time()
resp = urllib2.urlopen('http://api.acoustid.org/v2/lookup', urllib.urlencode(data))
tree = json.loads(resp.read())
print "=> Request took %.3fs" % (time.time() - a,)
if tree['results']:
    for result in tree['results']:
        print
        print 'Score:', result['score']
        print 'ID:', result['id']
        for recording in result['recordings']:
            print 'URL: http://musicbrainz.org/track/%s.html' % (recording['id'],)
            for track in recording['tracks']:
                print "Track:", track['title']
                print "Artist:", track['artist']['name']
                print "Release:", track['medium']['release']['title']
else:
    print "No matching fingerprints were found"
