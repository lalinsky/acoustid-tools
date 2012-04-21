import sys, os

def format_time(secs):
    secs = int(secs)
    return "%d:%02d" % (secs / 60, secs % 60)


def invert(arr):
    """
    Make a dictionary that with the array elements as keys and
    their positions positions as values.

    >>> invert([3, 1, 3, 6])
    {1: [1], 3: [0, 2], 6: [3]}
    """
    map = {}
    for i, a in enumerate(arr):
        map.setdefault(a, []).append(i)
    return map


popcnt_table_8bit = [
    0,1,1,2,1,2,2,3,1,2,2,3,2,3,3,4,1,2,2,3,2,3,3,4,2,3,3,4,3,4,4,5,
    1,2,2,3,2,3,3,4,2,3,3,4,3,4,4,5,2,3,3,4,3,4,4,5,3,4,4,5,4,5,5,6,
    1,2,2,3,2,3,3,4,2,3,3,4,3,4,4,5,2,3,3,4,3,4,4,5,3,4,4,5,4,5,5,6,
    2,3,3,4,3,4,4,5,3,4,4,5,4,5,5,6,3,4,4,5,4,5,5,6,4,5,5,6,5,6,6,7,
    1,2,2,3,2,3,3,4,2,3,3,4,3,4,4,5,2,3,3,4,3,4,4,5,3,4,4,5,4,5,5,6,
    2,3,3,4,3,4,4,5,3,4,4,5,4,5,5,6,3,4,4,5,4,5,5,6,4,5,5,6,5,6,6,7,
    2,3,3,4,3,4,4,5,3,4,4,5,4,5,5,6,3,4,4,5,4,5,5,6,4,5,5,6,5,6,6,7,
    3,4,4,5,4,5,5,6,4,5,5,6,5,6,6,7,4,5,5,6,5,6,6,7,5,6,6,7,6,7,7,8,
]

def popcnt(x):
    """
    Count the number of set bits in the given 32-bit integer.
    """
    return (popcnt_table_8bit[(x >>  0) & 0xFF] +
            popcnt_table_8bit[(x >>  8) & 0xFF] +
            popcnt_table_8bit[(x >> 16) & 0xFF] +
            popcnt_table_8bit[(x >> 24) & 0xFF])


def ber(fp1, fp2, offset):
    """
    Compare the short snippet against the full track at given offset.
    """
    if offset > 0:
        fp1 = fp1[offset:]
    elif offset < 0:
        fp2 = fp2[-offset:]
    errors = 0
    count = 0
    for a, b in zip(fp1, fp2):
        errors += popcnt(a ^ b)
        count += 1
    return max(0.0, 1.0 - 2.0 * errors / (32.0 * count))


class Fingerprint(object):

    def __init__(self, data):
        self.data = data
        self.query = [x >> 10 for x in data]


def load_fp(filename):
    return Fingerprint([int(i.strip()) & 0xFFFFFFFF for i in open(filename).read().split(',')])



def compare_fp(fp1, fp2):
    # check which items are contained in both fingerprints
    common = set(fp1.query) & set(fp2.query)

    # create small inverted indexes
    i_fp1 = invert(fp1.query)
    i_fp2 = invert(fp2.query)

    # check at which offsets do the common items occur
    offsets = {}
    for a in common:
        for i in i_fp1[a]:
            for j in i_fp2[a]:
                o = i - j
                offsets[o] = offsets.get(o, 0) + 1

    # evaluate the fingerprints at the best matching offsets and sort the results by score
    matches = []
    for count, offset in sorted([(v, k) for k, v in offsets.items()], reverse=True)[:20]:
        matches.append((ber(fp1.data, fp2.data, offset), offset))
    matches.sort(reverse=True)

    # print out the results
    for i, (score, offset) in enumerate(matches):
        if score < 0.4:
            break
        secs = int(offset * 0.1238) # each fingerprint item represents 0.1238 seconds
#        print "%d. position %s with score %f" % (i + 1, format_time(secs), score)
        return score, offset
    return None, None


mix = load_fp(sys.argv[1])

songs = {}
for filename in sys.argv[2:]:
    songs[filename] = load_fp(filename)


index = {}
for id, fp in songs.iteritems():
    for x in fp.query:
        index.setdefault(x, []).append(id)


increment = int(5 / 0.1238)
window = int(20 / 0.1238)

for i in range(0, len(mix.data) - window, increment):
    sample = Fingerprint(mix.data[i:i+window])
    candidates = {}
    for x in sample.query:
        for id in index.get(x, []):
            candidates[id] = candidates.get(id, 0) + 1
    found = False
    if candidates:
        for count, id in sorted([(v, k) for k, v in candidates.items()], reverse=True):
            score, offset = compare_fp(songs[id], sample)
            if score:
                print format_time(i * 0.1238), id, score, offset
                found = True
                break
    if not found:
        print format_time(i * 0.1238), "-"

raise SystemExit(0)


