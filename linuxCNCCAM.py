import sys
from dxflib import *

# filename = sys.argv[1]
filename = "/home/tocs/4gary/play/3dSheetCam/cad/simplepydxflib/NONAME_2.dxf"
safeH = 0.25
straightFeed = 10.0



dxf = DXF()
dxf.open(filename)
print "; filename:", dxf.filename

print """; Modal settings
G17	  ;XY plane
G20	  ;inch mode
G40	  ;cancel diameter compensation
G49	  ;cancel length offset
G54	  ;coordinate system 1
G80	  ;cancel motion
G90 F#1	  ;non-incremental motion
G94 F%f	  ;feed/minute mode
""" % straightFeed



print "; ENTITIES:"
for e in dxf.ENTITIES:
    initMove = e[1].verts[0]
    print "G0 Z %f\t\t\t\t; move to safe height" % safeH
    print "G0 X %f Y %f Z %f\t; rapid to start XYZSafe" % (initMove[0], initMove[1], safeH)
    print "G1 Z %f\t\t\t\t; straight feed start Z " % initMove[2]
    print
    for linesArcs in e[1].asLinesArcs()[1:]:
        if linesArcs[0] == "LINE":
            print "G1 X %f Y %f Z %f\t; straight feed" % tuple(linesArcs[1])
    print "G1 X %f Y %f Z %f\t; straight feed" % tuple(linesArcs[2]) # final move
    print "G1 Z %f" % safeH

print "M2"
