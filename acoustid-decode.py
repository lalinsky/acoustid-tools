#!/usr/bin/env python

import re
import sys
import os
from chromaprint import Fingerprinter, decode_fingerprint
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

print fingerprint
print decode_fingerprint(fingerprint)
