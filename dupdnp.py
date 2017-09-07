#!/usr/bin/python3

# find /path/to/search/ -type f -not -empty -printf '%p\t%s\n' | ./dupdnp.py

from hashlib import md5

# check size :
# fill dict with size as key and list of paths as value
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
sizes = {size:paths for size, paths in sizes.items() if len(paths) > 1}

# check header (first 1024 bytes) :
# fill dict with (size, header) as key and list of paths as value
headers = {}
for size, paths in sizes.items():
    for path in paths:
        with open(path, 'rb') as data:
            header = data.read(1024)
        headers.setdefault((size, header), []).append(path)
# free memory
del(sizes)

# check md5 hash of extended header (first mega-byte) :
# fill dict with (size, hash) as key and list of paths as value
hheaders, megabyte = {}, 1024*1024
for (size, header), paths in headers.items():
    if len(paths) > 1:
        for path in paths:
            with open(path, 'rb') as data:
                hheader = md5(data.read(megabyte)).digest()
            hheaders.setdefault((size, hheader), []).append(path)
# free memory
del(headers)

# check md5 hash :
# fill dict with hash as key and list of paths as value
checksums = { hheader:paths for (size, hheader), paths in hheaders.items() if size <= megabyte }
for (size, hheader), paths in hheaders.items():
    if len(paths) > 1 and size > megabyte:
        for path in paths:
            with open(path, 'rb') as data:
                checksum = md5(data.read()).digest()
            checksums.setdefault(checksum, []).append(path)
# free memory
del(hheaders)

# write results
for checksum, paths in checksums.items():
    if len(paths) > 1:
        paths.pop()
        for path in paths: print(path)

# cython3 --embed ./dupdnp.py
# gcc $( python3-config --cflags --libs ) ./dupdnp.c -o ./dupdnp
