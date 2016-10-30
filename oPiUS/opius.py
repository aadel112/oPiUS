#!/usr/bin/env python
import getopt
import sqlite3
import sys
import csv

class oPiUS:
    conn = None
    curs = None
    input_h = None
    in_delim = None
    out_delim = None
    out_type = None
    output_h = None
    minimum = -1
    maximum = -1
    peaks = {}

    def __init__(self, input_h = sys.stdin, in_delim=',', out_delim=',', start_colno=1, end_colno=2, out_type='csv', output_h=sys.stdout):
        # init the in-memory data store
        self.conn = sqlite3.connect(':memory:')
        self.curs = self.conn.cursor()
        # single threaded no file sync
        self.curs.execute('''PRAGMA synchronous = off''')
        # set all the pragmas for extra juice
        self.curs.execute('''PRAGMA locking_mode = EXCLUSIVE''')
        self.curs.execute('''PRAGMA journal_mode = OFF''')
        self.curs.execute('''PRAGMA read_uncommitted = 1''')
        self.curs.execute('''PRAGMA temp_store = 2''')
        self.curs.execute('''PRAGMA threads = 8''')
        # just need two columns for this
        self.curs.execute('''CREATE TABLE store(start_time int, end_time int)''')

        self.input_h = input_h
        self.in_delim = in_delim
        self.out_delim = out_delim
        self.start_colno = start_colno - 1
        self.end_colno = end_colno - 1
        self.out_type = out_type
        self.output_h = output_h

    def idx_tbl(self):
        self.curs.execute('''CREATE index idx01 ON store(start_time, end_time)''')

        self.curs.execute('''ANALYZE''')

    #load the database
    def load(self):
        data = []
        if self.input_h == sys.stdin:
            rd = csv.reader(sys.stdin, delimiter=self.in_delim)
            for r in rd:
                cl = self.get_column_list(r)
                self.set_min_max(cl)
                data.append(cl)
        else:
            with open(self.input_h, 'rb') as f:
                rd = csv.reader(f, delimiter=self.in_delim)
                for r in rd:
                    cl = self.get_column_list(r)
                    self.set_min_max(cl)
                    data.append(cl)

        self.curs.executemany('INSERT INTO store VALUES(?,?)', data)
        self.idx_tbl()

    def set_min_max(self, cl):
        if cl[0] < self.minimum or self.minimum == -1:
            self.minimum = int(cl[0])
        if cl[1] > self.maximum or self.maximum == -1:
            self.maximum = int(cl[1])

    def get_column_list(self, r):
        e1 = r[self.start_colno].strip()
        e2 = r[self.end_colno].strip()
        try:
            ie1 = int(e1)
            ie2 = int(e2)
            return [ ie1, ie2 ]
        except Exception:
            self.curs.execute('''select strftime('%s', ?, 'localtime')''', (e1,))
            e1 = self.curs.fetchone()[0]
            self.curs.execute('''select strftime('%s', ?, 'localtime')''', (e2,))
            e2 = self.curs.fetchone()[0]

            return [ e1, e2 ]

    def find_peaks(self):

        for i in range(self.minimum, self.maximum):
            self.curs.execute('''select count(*) from store where start_time <= ? and end_time >= ?''', (i, i))
            cnt = self.curs.fetchone()[0]
            self.peaks[i] = cnt

    def output(self):
        if self.output_h == sys.stdout:
            if self.out_type == 'json':
                print self.peaks
            elif self.out_type == 'csv':
                wt = csv.writer(sys.stdout,delimiter=self.out_delim)
                for k in list(self.peaks.keys()):
                    wt.writerow([k,self.peaks[k]])
        else:
            with open(self.output_h, 'wb') as f:
                if self.out_type == 'json':
                    f.write(self.peaks)
                elif self.out_type == 'csv':
                    wt = csv.writer(f,delimiter=self.out_delim)
                    for k in list(self.peaks.keys()):
                        wt.writerow([k,self.peaks[k]])

    # close out of db
    def close(self):
        self.conn.close()

def main():
    try:
	opts, args = getopt.getopt(sys.argv[1:], "", ["infile=", "outfile=", "output_type=", "input_delim=", "output_delim=", "start_colno=", "end_colno="])
    except getopt.GetoptError as err:
	# print help information and exit:
	print str(err)  # will print something like "option -a not recognized"
	sys.exit(2)

    in_h = sys.stdin
    o_h = sys.stdout
    ot = 'csv'
    ide = ','
    ode = ','
    sc = 1
    ec = 2
#     print opts
    for o, a in opts:
	if o == "--infile":
            in_h = a
	if o == "--outfile":
	     o_h = a
	if o == "--output_type":
	     ot = a
	if o == "--input_delim":
	     ide = a
        if o == "--output_delim":
             ode = a
	if o == "--start_colno":
	     sc = a
	if o == "--end_colno":
             ec = a

    opius = oPiUS(in_h, ide, ode, sc, ec, ot, o_h)
    opius.load()
    opius.find_peaks()
    opius.output()
    opius.close()


if __name__ == "__main__":
    main()


