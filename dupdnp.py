#!/usr/bin/python3

# find /path/to/search/ -type f -not -empty -printf '%p\t%s\n' | ./dupdnp.py

from optparse import OptionParser

parser = OptionParser(usage='%prog [--md5|--sha1|--sha256]')
parser.add_option('-m', '--md5', help='use md5 instead of xxhash', action='store_true')
parser.add_option('-s', '--sha1', help='use sha1 instead of md5', action='store_true')
parser.add_option('-S', '--sha256', help='use sha256 instead of md5', action='store_true')
(options, _) = parser.parse_args()

if (options.md5 and options.sha1) or (options.md5 and options.sha256) or (options.sha1 and options.sha256):
    parser.error('md5, sha1 and sha256 are mutually exclusive')

try:
    # pip install xxhash #--user
    from xxhash import xxhash64 as message
except:
    from hashlib import md5 as message
if options.md5: from hashlib import md5 as message
if options.sha1: from hashlib import sha1 as message
if options.sha256: from hashlib import sha256 as message

from collections import defaultdict

# check size :
# fill dict sizes with size as key and list of paths as value
sizes = defaultdict(list)
with open('/dev/stdin', 'r') as lines:
    for line in lines:
        # line is 'path\tsize\n'
        path, size = line.strip('\n').split('\t')
        sizes[int(size)].append(path)
# remove empty files if ever
sizes.get(0) and sizes.pop(0)
# remove single files
sizes = {size: paths for size, paths in sizes.items() if len(paths) > 1}

# check header :
# fill dict headers with (size, header) as key and list of paths as value
headers = defaultdict(list)
headerWidth = 1024 * 4
for size, paths in sizes.items():
    for path in paths:
        with open(path, 'rb') as data:
            header = data.read(headerWidth)
        headers[(size, header)].append(path)
# free memory
del(sizes)
# remove single files
headers = {(size, header): paths for (size, header), paths in headers.items() if len(paths) > 1}

# check hash of fragment :
# fill dict fragments with (size, hash) as key and list of paths as value
fragmentWidth = 1024 * 1024 * 4
# preload files already read (and stored in memory)
fragments = defaultdict(list, {(size, message(header).digest()): paths for (size, header), paths in headers.items() if size < headerWidth + 1})
# remove files already read and header
headers = {(size, header): paths for (size, header), paths in headers.items() if size > headerWidth}
for (size, header), paths in headers.items():
    for path in paths:
        with open(path, 'rb') as data:
            fragment = message(data.read(fragmentWidth)).digest()
        fragments[(size, fragment)].append(path)
# free memory
del(headers)
# remove single files
fragments = {(size, fragment): paths for (size, fragment), paths in fragments.items() if len(paths) > 1}

# check hash of totality :
# fill dict with hash as key and list of paths as value
# preload files already hashed (and stored in memory)
checksums = defaultdict(list, {(size, fragment): paths for (size, fragment), paths in fragments.items() if size < fragmentWidth + 1})
# remove files already hashed and fragment
fragments = {(size, fragment): paths for (size, fragment), paths in fragments.items() if size > fragmentWidth}
for (size, fragment), paths in fragments.items():
    for path in paths:
        with open(path, 'rb') as data:
            checksum = message(data.read()).digest()
        checksums[(size, checksum)].append(path)
# free memory
del(fragments)
# remove single files
checksums = {(size, checksum): paths for (size, checksum), paths in checksums.items() if len(paths) > 1}

# write results without first path in list
for (size, checksum), paths in checksums.items():
    for path in paths[1:]: print(path)

# cython3 --embed ./dupdnp.py
# gcc $( python3-config --cflags --libs ) ./dupdnp.c -o ./dupdnp
