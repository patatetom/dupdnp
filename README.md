# dupdnp
Find duplicate files

Because duplicate files are usually a problem, `dupdnp.py` is  &nbsp;&nbsp;*yet another*&nbsp;&nbsp; Python script to find them.

The difference lies here in the way to eliminate the unique files :

* the first sort is done very logically and as often on the file size,
* the second sort simply rests on the file header (1Kb by default or 4Kb),
* the third sort is based on the [digital fingerprint](https://en.wikipedia.org/w/index.php?title=Message_digest) of the starting fragment (4Mb) of the file,
* the fourth and last sort takes place on the digital fingerprint of the full file.

The digital fingerprint can be computed with [xxhash](https://github.com/Cyan4973/xxHash) (default choice, if present), md5 or sha1 (default choice, in absence of xxhash).



### Full_file_name &RightArrowBar; size

The search for files and their size is outsourced and entrusted here to the command-line utility `find` :

```bash
find /path/to/search/ -type f -not -empty -printf '%p\t%s\n' | ./dupdnp.py
```

`-printf '%p\t%s\n'` print the full file name and its size in bytes, separated by a `[tab]` character.

***This specific input format - `full_file_name` `[tab]` `size_in_bytes` - is the expected one !***



### Metrics

The dupdnp.py metrics listed below are issued from the search of duplicate files on a typical Windows Seven workstation :
```bash
sudo mount /dev/sda2 /cdrom -o ro

find /cdrom/ -type f | wc -l
66465
find /cdrom/ -type f -not -empty | wc -l
66418

function flush { sync && sudo sysctl -q vm.drop_caches=3; }

# find metrics
flush && time ( find /cdrom/ -type f -not -empty -printf '%p\t%s\n' > /dev/null )
real 0m5,089s user 0m0,150s sys 0m0,790s

# dupdnp.py metrics with xxhash
find /cdrom/ -type f -not -empty -printf '%p\t%s\n' | ./dupdnp.py | wc -l
28950
flush && time ( find /cdrom/ -type f -not -empty -printf '%p\t%s\n' | ./dupdnp.py > /dev/null )
real 0m58,295s user 0m4,720s sys 0m7,310s

# dupdnp.py metrics with xxhash and 4k headers
find /cdrom/ -type f -not -empty -printf '%p\t%s\n' | ./dupdnp.py -4 | wc -l
28950
flush && time ( find /cdrom/ -type f -not -empty -printf '%p\t%s\n' | ./dupdnp.py -4 > /dev/null )
real 0m55,900s user 0m4,910s sys 0m6,480s

# dupdnp.py metrics with md5
find /cdrom/ -type f -not -empty -printf '%p\t%s\n' | ./dupdnp.py --md5 | wc -l
28950
flush && time ( find /cdrom/ -type f -not -empty -printf '%p\t%s\n' | ./dupdnp.py --md5 > /dev/null )
real 1m19,165s user 0m23,700s sys 0m6,200s

# dupdnp.py metrics with sha1
find /cdrom/ -type f -not -empty -printf '%p\t%s\n' | ./dupdnp.py --sha1 | wc -l
28950
flush && time ( find /cdrom/ -type f -not -empty -printf '%p\t%s\n' | ./dupdnp.py --sha1 > /dev/null )
real 1m15,267s user 0m18,170s sys 0m6,430s

# dupdnp.py, duff and jdupes results
find /cdrom/ -type f -not -empty -printf '%p\t%s\n' | ./dupdnp.py -4 -a | sed '/^$/d' | sort > dupdnp.found

duff -v
duff 0.5.2
...
duff -raqzf '' /cdrom/ | sort > duff.found

jdupes -v
jdupes 1.8 (2017-01-31) 64-bit
...
jdupes -rqH /cdrom/ | sed '/^$/d' | sort > jdupes.found

wc -l *.found | grep '\.found$'
   49614 duff.found
   49614 dupdnp.found
   49614 jdupes.found

md5sum *.found
86be9d808c1e8821bf52cd96ee581b46  duff.found
86be9d808c1e8821bf52cd96ee581b46  dupdnp.found
86be9d808c1e8821bf52cd96ee581b46  jdupes.found
```



### Cython

The Python script `dupdnp.py` can be compiled into an executable using Cython and Gcc :
```bash
cython3 --embed ./dupdnp.py
gcc $( python3-config --cflags --libs ) ./dupdnp.c -o ./dupdnp
```



### See also

- [Duff](https://github.com/elmindreda/duff)
- [Jdupes](https://github.com/jbruchon/jdupes)
- [Rmlint](https://github.com/sahib/rmlint)
- [Rdfind](https://github.com/pauldreik/rdfind)
