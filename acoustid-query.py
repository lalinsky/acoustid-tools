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
print fingerprint
print decode_fingerprint(fingerprint)

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
import pprint
pprint.pprint(tree)
print time.time() - a
#for result in tree.findall('results/result'):
#    print
#    print 'Score:', result.find('score').text
#    print 'ID:', result.find('id').text
#    for track in result.findall('tracks/track'):
#        print 'http://musicbrainz.org/track/%s.html' % track.find('id').text
#        for track in track.findall('recordings'):



