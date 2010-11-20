import sys
import os
import ctypes
import ctypes.util


for name in ('chromaprint', 'libchromaprint'):
    filename = ctypes.util.find_library(name)
    if filename is not None:
        _libchromaprint = ctypes.CDLL(filename)
        break
else:
    raise ImportError("couldn't find libchromaprint")


_libchromaprint.chromaprint_get_version.argtypes = ()
_libchromaprint.chromaprint_get_version.restype = ctypes.c_char_p

_libchromaprint.chromaprint_new.argtypes = (ctypes.c_int,)
_libchromaprint.chromaprint_new.restype = ctypes.c_void_p

_libchromaprint.chromaprint_free.argtypes = (ctypes.c_void_p,)
_libchromaprint.chromaprint_free.restype = None

_libchromaprint.chromaprint_start.argtypes = (ctypes.c_void_p, ctypes.c_int, ctypes.c_int)
_libchromaprint.chromaprint_start.restype = ctypes.c_int

_libchromaprint.chromaprint_feed.argtypes = (ctypes.c_void_p, ctypes.POINTER(ctypes.c_char), ctypes.c_int)
_libchromaprint.chromaprint_feed.restype = ctypes.c_int

_libchromaprint.chromaprint_finish.argtypes = (ctypes.c_void_p,)
_libchromaprint.chromaprint_finish.restype = ctypes.c_int

_libchromaprint.chromaprint_get_fingerprint.argtypes = (ctypes.c_void_p, ctypes.POINTER(ctypes.c_char_p))
_libchromaprint.chromaprint_get_fingerprint.restype = ctypes.c_int


class Fingerprinter(object):

    ALGORITHM_TEST1 = 0
    ALGORITHM_TEST2 = 1
    ALGORITHM_TEST3 = 2
    ALGORITHM_DEFAULT = ALGORITHM_TEST2

    def __init__(self, algorithm=ALGORITHM_DEFAULT):
        self._ctx = _libchromaprint.chromaprint_new(algorithm)

    def __del__(self):
        _libchromaprint.chromaprint_free(self._ctx)
        del self._ctx

    def start(self, sample_rate, num_channels):
        _libchromaprint.chromaprint_start(self._ctx, sample_rate, num_channels)

    def feed(self, data):
        _libchromaprint.chromaprint_feed(self._ctx, data, len(data) / 2)

    def finish(self):
        _libchromaprint.chromaprint_finish(self._ctx)
        fingerprint = ctypes.c_char_p()
        _libchromaprint.chromaprint_get_fingerprint(self._ctx, ctypes.byref(fingerprint))
        return fingerprint.value

