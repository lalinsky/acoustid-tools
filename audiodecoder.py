
import subprocess
import re
import sys
import os
import tempfile

class AudioDecoderError(Exception):
    pass


class AudioDecoder(object):

    def __init__(self, filename):
        self._filename = filename

    def decode(self):
        format = 's16le' if sys.byteorder == 'little' else 's16be'
        process = subprocess.Popen(["ffmpeg", "-i", self._filename, "-f", format, "-t", "60", "-"], stdin=open(os.devnull), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        data, info = process.communicate()

        if process.returncode != 0:
            raise AudioDecoderError(info.splitlines()[-1])

        m = re.search("Duration: (\d+):(\d+):(\d+)", info)
        if m is None:
            raise AudioDecoderError("unable to determine the audio length")
        hours, minutes, seconds = map(int, m.groups())
        length = seconds + 60 * (minutes + 60 * hours)

        m = re.search("Stream #0\.0: Audio: pcm_s16le, (\d+) Hz, ([^,]+), s16", info)
        if m is None:
            raise AudioDecoderError("unable to determine the audio format")
        sample_rate, stereo = m.groups()

        num_channels = 1
        if stereo == 'stereo':
            num_channels = 2
        else:
            m = re.match('(\d+) channels', stereo)
            if m is not None:
                num_channels = int(m.group(1))

        return length, int(sample_rate), num_channels, data

        #info = ''
        #print 'Reading stderr'
        #while process.poll() is not None:
        #    line = process.stderr.readline()
        #    if line.startswith('Press'):
        #        break
        #    info += line
        #print info
        #print 'Reading stdin'
        #while process.poll() is not None:
        #    buffer = process.stdout.read(1024 * 16)
        #    if not buffer:
        #        break
        #process.wait()
        #print info



