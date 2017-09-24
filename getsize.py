# https://goshippo.com/blog/measure-real-size-any-python-object/

# this file is not used by dudnp : you can safely delete it

# headers = defaultdict(list)
# from sys import stderr
# from getsize import get_size as getsizeof
# print(getsizeof(headers)/1024./1024, file=stderr)
# ...
# print(getsizeof(headers)/1024./1024, file=stderr)
# headers = {(size, header): paths for (size, header), paths in headers.items() if len(paths) > 1}
# print(getsizeof(headers)/1024./1024, file=stderr)

# find /cdrom/ -type f -not -empty -printf '%p\t%s\n' | ./dupdnp.py -4 > /dev/null
# 0.00023651123046875
# 115.95255661010742
# 81.43520450592041
# find /cdrom/ -type f -not -empty -printf '%p\t%s\n' | ./dupdnp.py > /dev/null
# 0.00023651123046875
# 48.35742473602295
# 31.0556583404541


import sys

def get_size(obj, seen=None):
    """Recursively finds size of objects"""
    size = sys.getsizeof(obj)
    if seen is None:
        seen = set()
    obj_id = id(obj)
    if obj_id in seen:
        return 0
    # Important mark as seen *before* entering recursion to gracefully handle
    # self-referential objects
    seen.add(obj_id)
    if isinstance(obj, dict):
        size += sum([get_size(v, seen) for v in obj.values()])
        size += sum([get_size(k, seen) for k in obj.keys()])
    elif hasattr(obj, '__dict__'):
        size += get_size(obj.__dict__, seen)
    elif hasattr(obj, '__iter__') and not isinstance(obj, (str, bytes, bytearray)):
        size += sum([get_size(i, seen) for i in obj])
    return size
