import sys
from dxflib import *

if __name__ == "__main__":
    filename = sys.argv[1]
    print "Opening: %s" % filename
    dxf = DXF()  # create DXF class object
    dxf.open(filename)

    for k in dxf.keys():
        print k, len(dxf[k].subSections)
    print
    lines = []
    points = []
    circles = []
    arcs = []
    lwpolylines = []
    for e in xrange(len(dxf.ENTITIES)):
        if dxf.ENTITIES[e][0] == "LINE":
            lines.append(dxf.ENTITIES[e])
        elif dxf.ENTITIES[e][0] == "POINT":
            points.append(dxf.ENTITIES[e])            
        elif dxf.ENTITIES[e][0] == "CIRCLE":
            circles.append(dxf.ENTITIES[e])                        
        elif dxf.ENTITIES[e][0] == "ARC":
            arcs.append(dxf.ENTITIES[e])                                    
        elif dxf.ENTITIES[e][0] == "LWPOLYLINE":
            lwpolylines.append(dxf.ENTITIES[e])                                                

    print "Lines:", len(lines)
    for l in xrange(len(lines)):
        print "Line %i" % l
        print "\tstartPt\t:", lines[l][1].getStart()
        print "\tendPt\t:", lines[l][1].getEnd()
        print "\tlength\t:", lines[l][1].length()
    print "Points:", len(points)    
    for p in xrange(len(points)):
        print "Point %i" % p
        print "\tstartPt\t:", points[p][1].getStart()
    print "Circles:", len(circles)        
    for c in xrange(len(circles)):
        print "Circle %i" % c
        print "\tcenter\t:",circles[c][1].getCenter()
        print "\tradius\t:", circles[c][1].getRadius()
        print "\tstartPt\t:", circles[c][1].getStart()     
        print "\tendPt\t:", circles[c][1].getEnd()
        print "\tstartAngle\t:", circles[c][1].getStartAngle()
        print "\tendAngle\t:", circles[c][1].getEndAngle()        
        print "\tlength\t:", circles[c][1].length()
        print 
    print "Arcs:", len(arcs)        
    for a in xrange(len(arcs)):
        print "Arc %i" % a
        print "\tcenter\t:",arcs[a][1].getCenter()
        print "\tradius\t:", arcs[a][1].getRadius()
        print "\tstartPt\t:", arcs[a][1].getStart()     
        print "\tendPt\t:", arcs[a][1].getEnd()
        print "\tstartAngle\t:", arcs[a][1].getStartAngle()
        print "\tendAngle\t:", arcs[a][1].getEndAngle()        
        print "\tlength\t:", arcs[a][1].length()
        print 
    print "LWPolylines:", len(lwpolylines)
    for p in xrange(len(lwpolylines)):
        print "LWPolyline %i" % p
        print lwpolylines[p][1].verts
        for lw in lwpolylines[p][1].asLinesArcs():
            print "\t", lw



        

