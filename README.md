# dupdnp
Find duplicate files

Because duplicate files are usually a problem, **dupdnp** is *yet another* Python script to find them.

The difference lies here in the way to eliminate the unique files :
* the first sort is done very logically and as often on the size,
* the second sort simply rests on the header, that is, the first kilobyte,
* the third sorting is based on the digital fingerprint of the first megabyte,
* the fourth and last sorting takes place on the digital fingerprint of the file.

The search for files and their size is outsourced
