# dupdnp
Find duplicate files

Because duplicate files are usually a problem, **dupdnp** is *yet another* Python script to find them.

The difference lies here in the way to eliminate the unique files :
* the first sort is done very logically and as often on the size file,
* the second sort simply rests on the header file, that is, the first kilobyte,
* the third sort is based on the digital fingerprint of the first megabyte of the file,
* the fourth and last sort takes place on the digital fingerprint of the file.

The search for files and their size is outsourced and entrusted here to the command-line utility [find](https://www.gnu.org/software/findutils/manual/html_mono/find.html) :

```bash
find /path/to/search/ -type f -not -empty -printf '%p\t%s\n' | dupdnp.py
```
