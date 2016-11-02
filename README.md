What is oPiUS
=============
opius is all about fast peak calculations. Opius is a lightweight CLI that can also be imported as a python module to get exact peak concurrent event counts over a range of time. Opius has a small memory footprint, and a small code base. It's very good at one thing, finding counts over a time interval for records with a start and end-time where each record occurred at that instance in time, otherwise known as a peak calculation. It's very fast, as it relies on sqlite's in-memory datastore, with a single index on the start and end time of the event or record.  

oPiUS (Peaks Using SQLite)
==========================
Getting peak concurrent event counts, a.k.a peak usage,
peak seats, etc. is a fairly common use case. Coming from an IVR-type background I see a large number of people who actually want to be billed this way.
Getting peaks is easy, but getting accurate peaks, quickly is not. For even modest data sizes of ~50,000 records, getting a days worth of peaks really requires looping through each second of the day (86,400) seconds. As you can see this can spiral out of control quickly. The common quick-access data structure, the dictionary, or hash is really inefficient. You could have a solution that runs in hours or days. My purpose for writing this is multi-fold:

1. To provide an off-the-shelf calculator that is fast, accurate, and memory efficient.

2. To provide this solution in such a way that it reaches the maximum number of developers. This is why I chose python even though the Perl solution to this I've written before seems faster. This is a pretty fast solution. I have to say, I've seen three different algorithms to solve this, and this is the fastest.

3. To illustrate an interesting concept, which is that SQLite can be used in memory as a drop-in replacement for a data structure. Properly indexed, and setup, it can be lightning fast. It's especially useful for ranged index searches.


How to use this module in shell
===============================
1. You can either pipe input to it, which is the default, or you can set it up to take an input_file. The input file must be delimited. The default delimiter is ',', but you can set this to some other value using --input_delim=.

    Available options are:
    * --infile= - a file relative or absolute
    * --outfile= - a file relative or absolute
    * --output_type= - csv or json
    * --input_delim= - , | ^ etc.
    * --output_delim= - , | ^ etc.
    * --start_colno= - the column of the start time of the event, indexed from 1 on
    * --end_colno= - the column of the end time of the event, indexed from 1 on

    The output step is one second. You will always get the concurrent count of records for each second from the record minimum start time to the record maximum end time. It's up to you, the developer to get less granular maxes from that.

How to use this module in python
===============================
1. import it: ``import oPiUS``
2. create an object:
    ```
    opius = oPiUS(in_h, ide, ode, sc, ec, ot, o_h)
    ```
3. call load, find_peaks, and close
    ```
    opius.load()
    ```
    loads the sqlite memory structure
    ```
    opius.find_peaks()
    ```
    get each peak into opius.peaks, a dict
    ```
    opius.close()
    ```
    closes the sqlite object, frees the memory

Installation
============

The best thing to do would be to clone the repository and add a symlink called opius to /usr/local/bin pointing at oPiUS/opius.py

```
$> git clone https://github.com/aadel112/oPiUS.git #clone
$> cd oPiUS #get in project directory
$> sudo su #become root, stay in same directory
$> make all #install requirements, run tests
$> ln -s oPiUS/opius.py /usr/local/bin/opius #create symlink
$> exit #switch back to non-super user
```

Examples
========
Here I have a CSV with 4 columns, non-epoch formatted times, etc.

```
$> cat examples/ex6
dummy, person, 2016-10-31 00:00:00, 2016-10-31 00:00:10
dummy, person2, 2016-10-31 00:00:01, 2016-10-31 00:00:11
dummy, person3, 2016-10-31 00:00:10, 2016-10-31 00:00:10
dummy, person4, 2016-10-31 00:00:09, 2016-10-31 00:00:11

$> time opius --infile=examples/ex6 --start_colno=3 --end_colno=4 | head -2
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

Contributing
============
Find something you want to add or fix? Fix it, and I'll look it over as soon as possible. Have any comments, or find any bugs? Please contact me or open an issue. Suggestions for improvement? Let them be known.

Special Thanks
==============
Special thanks, all contributors.

* @m3talstorm
