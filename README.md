oPiUS (Peaks Using Sqlite)
==========================
Getting peak concurent event counts, a.k.a peak usage,
peak seats, etc. is a fairly common use case. Coming from an IVR-type background I see a large number of people who actually want to be billed this way.
Getting peaks is easy, but getting accurate peaks, quickly is not. For even modest data sizes of ~50,000 records, getting a days worth of peaks really requires looping through each second of the day (86,400) seconds. As you can see this can spiral out of control quickly. The common quick-access data structure, the dictionary, or hash is really inefficient. You could have a solution that runs in hours or days. My purpose for writing this is multi-fold:
    
    1. To provide an off-the-shelf calculator that is fast, accurate, and memory efficient.
    
    2. To provide this solution in such a way that it reaches the maximum number of developers. This is why I chose python even though the perl solution to this I've written before seems faster. This is a pretty fast solution. I have to say, I've seen three different algorithms to solve this, and this is the fastest.
    
    3. To illustrate an interesting concept, which is that sqlite can be used in memory as a drop-in replacement for a data structure. Prpoerly indexed, and setup, it can be lightning fast. It's especially useful for ranged index searches.


How to use this module in shell
===============================
1. You can either pipe input to it, which is the default, or you can set it up to take an input_file. The input file must be delimited. The default delimiter is ',', but you can set this to some other value using --input_delim=.

    Available options are:
    --infile= - a file relative or absolute
    --outfile= - a file realtive or absolute
    --output_type= - csv or json
    --input_delim= - , | ^ etc.
    --output_delim= - , | ^ etc.
    --start_colno= - the column of the start time of the event, indexed from 1 on
    --end_colno= - the columm of the end time of the event, indexed from 1 on

    The output step is one second. You will always get the concurrent count of records for each second from the record minimum start time to the record maximum end time. It's up to you, the developer to get less granular maxes from that.

How to use this module in python
===============================
1. import it: ``import oPiUS``
2. create an object:
    ```python
    opius = oPiUS(in_h, ide, ode, sc, ec, ot, o_h)
    ```
3. call load, find_peaks, and close
    ```python
    opius.load()
    ``` - loads the sqlite memory structure
    ```python
    opius.find_peaks()
    ``` - get each peak into opius.peaks, a dict
    ```python
    opius.close()
    ``` - closes the sqlite object, free the memory

Installation
============
The best thing to do would be to clone the repository, and add a symlink called opius to /usr/local/bin pointing at oPiUS/opius.py

``ln -s oPiUS/opius.py /usr/local/bin/opius``

Examples
========
Here I have a csv with 4 columns, non-epoch formatted times, etc.

```
$> time opius --infile=examples/ex6 --start_colno=3 --end_col=4 | head -2
1477872000,1
1477872001,2

real    0m0.043s
user    0m0.028s
sys     0m0.008s
```

```
$> ./oPiUS/opius.py --infile=examples/ex1 --output_delim='~'
```

```
$> ./oPiUS/opius.py --infile=examples/ex1 --output_type=json
```
