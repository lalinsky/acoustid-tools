#!/usr/bin/env python

import re
import sys
import os
from chromaprint import Fingerprinter
from audiodecoder import AudioDecoder

#print libchromaprint.chromaprint_get_version()
print "=> Decoding audio data"
decoder = AudioDecoder(sys.argv[1])
length, sample_rate, num_channels, data = decoder.decode()
print "=> Length:", length
print "=> Sample rate:", sample_rate
print "=> Number of channels:", num_channels

print "=> Calculating fingerprint"
fpcal = Fingerprinter()
fpcal.start(sample_rate, num_channels)
fpcal.feed(data)
fingerprint = fpcal.finish()

import urllib, urllib2
from xml.etree import ElementTree

data = {}
data['client'] = '8XaBELgH'
data['meta'] = '2'
data['length'] = str(length)
data['fingerprint'] = fingerprint
print "=> Looking up fingerprint"
resp = urllib2.urlopen('http://api.acoustid.org/lookup', urllib.urlencode(data))
tree = ElementTree.parse(resp)
#ElementTree.dump(tree)
for result in tree.findall('results/result'):
    print
    print 'Score:', result.find('score').text
    print 'ID:', result.find('id').text
    for track in result.findall('tracks/track'):
        print 'http://musicbrainz.org/track/%s.html' % track.find('id').text



