# dupdnp
Find duplicate files

Because duplicate files are usually a problem, dupdnp.py is *yet another* [Python](http://python.org/) script to find them.

The difference lies here in the way to eliminate the unique files :
* the first sort is done very logically and as often on the file size,
* the second sort simply rests on the file header,
* the third sort is based on the [digital fingerprint](https://en.wikipedia.org/w/index.php?title=Message_digest) of the starting fragment of the file,
* the fourth and last sort takes place on the digital fingerprint of the full file.



### Full file name [&RightArrowBar;] size

The search for files and their size is outsourced and entrusted here to the command-line utility [find](https://www.gnu.org/software/findutils/manual/html_mono/find.html) :

```bash
find /path/to/search/ -type f -not -empty -printf '%p\t%s\n' | ./dupdnp.py
```
* `find /path/to/search/` to recursively search in `/path/to/search/`,
* `-type f` to look only for files, not symlinks or directories,
* `-not -empty` to consider only non-empty files,
* `-printf '%p\t%s\n'` to print the full file name and its size in bytes, separated by a `[tab]` character.

The results of the recursive search command are communicated (`|` piped) to the script.

***This specific input format - `full_file_name` `[tab]` `size_in_bytes` - is the expected one !***

*(remember to make the script executable with `chmod +x ./dupdnp.py` or pipe to `python3 ./dupdnp.py`)*



### Metrics

The dupdnp.py metrics listed below are issued from the search of duplicate files on a typical Windows Seven workstation :
```bash
# Windows 7 x64
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
real 1m1,500s user 0m4,200s sys 0m6,770s

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

# dupdnp.py metrics with sha256
find /cdrom/ -type f -not -empty -printf '%p\t%s\n' | ./dupdnp.py --sha256 | wc -l
28950
flush && time ( find /cdrom/ -type f -not -empty -printf '%p\t%s\n' | ./dupdnp.py --sha256 > /dev/null )
real 1m30,073s user 0m34,260s sys 0m6,410s
```



### Cython

The Python script `dupdnp.py` can be compiled into an executable using [Cython](http://cython.org/) and [Gcc](https://gcc.gnu.org/) :
```bash
cython3 --embed ./dupdnp.py
gcc $( python3-config --cflags --libs ) ./dupdnp.c -o ./dupdnp
```



### See also

- [Duff](https://github.com/elmindreda/duff)
- [Jdupes](https://github.com/jbruchon/jdupes)
