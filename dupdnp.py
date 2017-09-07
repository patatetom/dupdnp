#!/usr/bin/python3

# find /path/to/search/ -type f -not -empty -printf '%p\t%s\n' | ./dupdnp.py

from hashlib import md5

# check size :
# fill dict sizes with size as key and list of paths as value
sizes = {}
with open('/dev/stdin', 'r') as lines:
    for line in lines:
        # line is 'path\tsize\n'
        path, size = line.strip('\n').split('\t')
        size = int(size)
        sizes.setdefault(size, []).append(path)
# remove empty files if ever
sizes.get(0) and sizes.pop(0)
# remove single files
sizes = {size: paths for size, paths in sizes.items() if len(paths) > 1}

# check header :
# fill dict headers with (size, header) as key and list of paths as value
headers = {}
headerWidth = 1024 * 4
for size, paths in sizes.items():
    for path in paths:
        with open(path, 'rb') as data:
            header = data.read(headerWidth)
        headers.setdefault((size, header), []).append(path)
# free memory
del(sizes)
# remove single files
headers = {(size, header): paths for (size, header), paths in headers.items() if len(paths) > 1}

# check md5 hash of fragment :
# fill dict fragments with (size, hash) as key and list of paths as value
fragmentWidth = 1024 * 1024 * 4
# preload files already read (and stored in memory)
fragments = {(size, md5(header).digest()): paths for (size, header), paths in headers.items() if size < headerWidth + 1}
# remove files already read and header
headers = {size: paths for (size, header), paths in headers.items() if size > headerWidth}
for size, paths in headers.items():
    for path in paths:
        with open(path, 'rb') as data:
            fragment = md5(data.read(fragmentWidth)).digest()
        fragments.setdefault((size, fragment), []).append(path)
# free memory
del(headers)
# remove single files
fragments = {(size, fragment): paths for (size, fragment), paths in fragments.items() if len(paths) > 1}

# check md5 hash :
# fill dict with hash as key and list of paths as value
# preload files already hashed (and stored in memory)
checksums = {fragment: paths for (size, fragment), paths in fragments.items() if size < fragmentWidth + 1}
# remove files already hashed and fragment
fragments = {size: paths for (size, fragment), paths in fragments.items() if size > fragmentWidth}
for size, paths in fragments.items():
    for path in paths:
        with open(path, 'rb') as data:
            checksum = md5(data.read()).digest()
        checksums.setdefault(checksum, []).append(path)
# free memory
del(fragments)
# remove single files
checksums = {checksum: paths for checksum, paths in checksums.items() if len(paths) > 1}

# write results
for checksum, paths in checksums.items():
    for path in paths[1:]: print(path)

# cython3 --embed ./dupdnp.py
# gcc $( python3-config --cflags --libs ) ./dupdnp.c -o ./dupdnp
