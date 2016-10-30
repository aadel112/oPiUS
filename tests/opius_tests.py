from nose.tools import *
from .context import oPiUS
import sys

#     opius = oPiUS(in_h, ide, sc, ec, ot, o_h)
#     opius.load()
#     opius.find_peaks()
#     opius.output()
#     opius.close()

o = oPiUS.opius.oPiUS('examples/ex1')

def setup():
    o.load()
    o.find_peaks()

def teardown():
    o.close()

def test_basic():
    assert o <> None
    assert len(list(o.peaks.keys())) > 0

