import numpy, sys
from dxflib import *

# set following parameters
# filename = sys.argv[1]
filename = "/home/tocs/4gary/play/3dSheetCam/cad/simplepydxflib/NONAME_2.dxf"
safeH = 0.25
straightFeed = 30.0
startDepth = 0.0
endDepth = -0.25
stepDepth = -0.0625


cutDepths = numpy.arange(startDepth, endDepth + stepDepth, stepDepth)
dxf = DXF()
dxf.open(filename)
print "; filename:", dxf.filename


# print initial modal settings and set cut feed rate
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

    for d in cutDepths:
        print "G1 Z %f\t\t\t\t; straight feed start Z " % d
        for linesArcs in e[1].asLinesArcs():
            if linesArcs[0] == "LINE":
                print "G1 X %f Y %f Z %f\t; straight feed" % (linesArcs[2][0], linesArcs[2][1], d)
                print "G1 X %f Y %f Z %f\t; straight feed" % (linesArcs[2][0], linesArcs[2][1], d) # final move

            elif linesArcs[0] == "ARC":
                startPt = numpy.array(linesArcs[1])
                center = numpy.array(linesArcs[3])
                offset = center - startPt
                if linesArcs[4] == 1:
                    direction = "G3"
                elif linesArcs[4] == 1:
                    direction = "G2"
                print "%s X %f Y %f Z %f I %f J %f\t; r =" % (direction, 
                                                              linesArcs[2][0], linesArcs[2][1], d,
offset[0], offset[1])
                #print "%s X %f Y %f Z %f I %f J %f\t; r =" % (direction, linesArcs[2][0], linesArcs[2][1], d) # final move
    print "G1 Z %f" % safeH
    print
print "M2"
