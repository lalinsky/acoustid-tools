#!/usr/bin/env python

import re
import sys
import os
from chromaprint import Fingerprinter, decode_fingerprint
from audiodecoder import AudioDecoder
from PyQt4 import QtGui

def s32tou(x):
    return x % 2**32

def s24tou(x):
    return x % 2**24

#print libchromaprint.chromaprint_get_version()
print "=> Decoding audio data"
decoder = AudioDecoder(sys.argv[1])
length, sample_rate, num_channels, data = decoder.decode(duration=60)
print "=> Length:", length
print "=> Sample rate:", sample_rate
print "=> Number of channels:", num_channels

print "=> Calculating fingerprint"
fpcal = Fingerprinter()
fpcal.start(sample_rate, num_channels)
fpcal.feed(data)
fingerprint = fpcal.finish()

#print fingerprint
fp = decode_fingerprint(fingerprint)[0]

#fp = map(s24tou, fp)
print "FP length", len(fp)
print "FP uniq length", len(set(fp))

image = QtGui.QImage(32, len(fp), QtGui.QImage.Format_Mono)

for y, bits in enumerate([s32tou(x) for x in fp]):
    for x in range(32):
        index = 0
        if bits & (1 << x):
            index = 1
        image.setPixel(x, y, index)
image.save('fp.png')

