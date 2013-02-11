import numpy, sys

EOF='  0\nEOF\n'
RED = 1
YELLOW = 2
GREEN = 3
CYAN = 4
BLUE = 5
MAGENTA = 6
WHITE = 7


def getDist(pt1, pt2):
    # returns distance between points
    pt1a = numpy.array(pt1)
    pt2a = numpy.array(pt2)
    return(numpy.sqrt(sum(pow(pt2a-pt1a, 2))))

class DXF(dict):
    def __init__(self, dict = None):
        self.data = {}
        if dict is not None: self.update(dict)
        self["HEADER"] = Header()
        self["CLASSES"] = Classes()
        self["TABLES"] = Tables()
        self["BLOCKS"] = Blocks()
        self["ENTITIES"] =Entities()
        self["OBJECTS"] = Objects()

        self.name = "default.dxf"
        self.filename = ""
        
    def update(self):
        for k in self.keys():
                setattr(DXF, k, self[k].subSections)

        
    def open(self, filename = ""):
        """opens a dxf file"""
        if filename != "":
                self.filename = filename
        fi = open(self.filename).readlines()
        self.load(fi)

    def load(self, dxfText):
        """return a dict of sections in the dxf
        dxftxt(dxftxt) => dict list of lines from each section\n(think open(filename, 'r').readlines())
        dxftxt : string, text of dxf file

        dict key: value
        {"header" : list of header lines,
        "classes" : list of classes lines,
        "tables"  : list of tables lines,
        "blocks:  : list of blocks lines,
        "entities": list of entities lines,
        "objects" : list of objects lines}
        """

        currentSection = ""
        for l in xrange(len(dxfText) - 1):

            # find top of section
            if (dxfText[l].rstrip() == "  0") and (dxfText[l + 1].rstrip() == "SECTION"): 
                currentSection = dxfText[l + 3].strip()
                self[currentSection].append(dxfText[l])
            elif (dxfText[l].rstrip() == "  0") and (dxfText[l + 1].rstrip() == "ENDSEC"):
                self[currentSection].append(dxfText[l])
            else:
                self[currentSection].append(dxfText[l])

        for s in self.keys():
                self[s].parse()

        self.update()
        
    def save(self, filename = ""):
        pass

class Sections(list):
    def __init__(self, list = None):
        self.data = []
        if list is not None: self.update(list)
        self.subSections = []
        
    def getSubType(self, p):
        
        typ = p[1].strip()
        return([typ, p])

    def parse(self):
        # parts of section
        currentPart = []
        n = 0
        for l in xrange(4, len(self) - 1):
            # find top of part
            if (self[l].rstrip() == "  0"):
                if currentPart != []:
                    currentPart = self.getSubType(currentPart)
                    self.subSections.append(currentPart)
                currentPart = [self[l]]
            else:
                currentPart.append(self[l])
                #        self.subSections.append(currentPart)


class Header(Sections):
       def __init__(self):
                Sections.__init__(self, list = None)

class Classes(Sections):
       def __init__(self):
                Sections.__init__(self, list = None)

class Tables(Sections):
        def __init__(self):
                Sections.__init__(self, list = None)
                
class Blocks(Sections):
       def __init__(self):
                Sections.__init__(self, list = None)

class Entities(Sections):
    def __init__(self):
        Sections.__init__(self, list = None)
        self.supported = ['LINE', "POINT", "CIRCLE", "ARC", "LWPOLYLINE"]
        
    def getSubType(self, p):
        typ = p[1].strip()
        if self.supported.count(typ) == 1:
            if typ == "LINE":
                ent = LINE()
                ent.fromDXF(p)
            elif typ == "POINT":
                ent = POINT()
                ent.fromDXF(p)
            elif typ == "CIRCLE":
                ent = CIRCLE()
                ent.fromDXF(p)                
            elif typ == "ARC":
                ent = ARC()
                ent.fromDXF(p)                                
            elif typ == "LWPOLYLINE":
                ent = LWPOLYLINE()
                ent.fromDXF(p)                                                
                
        else:
            ent = p
        return([typ, ent])        
            
class Objects(Sections):
       def __init__(self):
                Sections.__init__(self, list = None)


class ENTITIES:
    def __init__(self):
            self.startPt = []           # tags 10, 20, 30
            self.endPt = []             # tags 11, 21, 31
            self.layer =  ""            # tag  8
            self.linetype = "BYLAYER"   # tag  6
            self.color = "BYLAYER"      # tag  62
            self.visable = 0            # 0 : visible, 1 : not visible
            self.center = []

    def length(self):
            return(None)
            
    def getStart(self):
        return(self.startPt)
         
    def putStart(self, pt):
        if len(pt) == 3:
            self.startPt = map(float, pt)
        elif len(pt) == 2:
            pt.append(self.startPt[2])
            self.startPt = map(float, pt)

    def getEnd(self):
        return(self.endPt)
         
    def putEnd(self, pt):
        if len(pt) == 3:
            self.startPt = map(float, pt)
        elif len(pt) == 2:
            pt.append(self.startPt[2])
            self.startPt = map(float, pt)
    def getCenter(self):
        return(self.center)


class ARC(ENTITIES):
        def __init__(self):
                ENTITIES.__init__(self)
                self.radius = 0.0
                self.startAngle = 0.0
                self.endAngle = 0.0
        def getRadius(self):
                return(self.radius)
        def getStartAngle(self):
                return(self.startAngle)
        def getEndAngle(self):
                return(self.endAngle)                
        def length(self):
                return(2 * self.radius * numpy.pi)

        def fromDXF(self, dxfTxt):
                for l in xrange(2, len(dxfTxt)):
                        if dxfTxt[l].rstrip() == " 10":
                                x1 = float(dxfTxt[l + 1])
                        elif dxfTxt[l].rstrip() == " 20":
                                y1 = float(dxfTxt[l + 1])
                        elif dxfTxt[l].rstrip() == " 30":
                                z1 = float(dxfTxt[l + 1])
                        elif dxfTxt[l].rstrip() == " 40":
                                self.radius = float(dxfTxt[l + 1])                                
                        elif dxfTxt[l].rstrip() == " 50":
                                self.startAngle = float(dxfTxt[l + 1])                                
                        elif dxfTxt[l].rstrip() == " 51":
                                self.endAngle = float(dxfTxt[l + 1])                                                                                                
                        elif dxfTxt[l].rstrip() == "  8":
                                self.layer = dxfTxt[l + 1].strip()
                        elif dxfTxt[l].rstrip() == "  6":
                                self.linetype = dxfTxt[l + 1].strip()                                
                        elif dxfTxt[l].rstrip() == " 62":
                                self.color = dxfTxt[l + 1].strip()                                
                        elif dxfTxt[l].rstrip() == "":
                                self.visable = int(dxfTxt[l + 1])
                self.center = [x1, y1, z1]
                self.startPt = [numpy.cos(numpy.radians(self.startAngle)) * self.radius + self.center[0], 
                                numpy.sin(numpy.radians(self.startAngle)) * self.radius + self.center[1], 
                                z1]
                self.endPt = [(numpy.cos(numpy.radians(self.endAngle)) * self.radius) + self.center[0], 
                              (numpy.sin(numpy.radians(self.endAngle)) * self.radius) + self.center[1], 
                              z1]



class CIRCLE(ENTITIES):
        def __init__(self):
                ENTITIES.__init__(self)
                self.radius = 0.0
                self.startAngle = 0.0
                self.endAngle = 0.0
        def getRadius(self):
                return(self.radius)
        def getStartAngle(self):
                return(self.startAngle)
        def getEndAngle(self):
                return(self.endAngle)                
        def length(self):
                return(2 * self.radius * numpy.pi)
        def fromDXF(self, dxfTxt):
                for l in xrange(2, len(dxfTxt)):
                        if dxfTxt[l].rstrip() == " 10":
                                x1 = float(dxfTxt[l + 1])
                        elif dxfTxt[l].rstrip() == " 20":
                                y1 = float(dxfTxt[l + 1])
                        elif dxfTxt[l].rstrip() == " 30":
                                z1 = float(dxfTxt[l + 1])
                        elif dxfTxt[l].rstrip() == " 40":
                                self.radius = float(dxfTxt[l + 1])                                
                        elif dxfTxt[l].rstrip() == " 50":
                                self.startAngle = float(dxfTxt[l + 1])                                
                        elif dxfTxt[l].rstrip() == " 51":
                                self.endAngle = float(dxfTxt[l + 1])                                              
                        elif dxfTxt[l].rstrip() == "  8":
                                self.layer = dxfTxt[l + 1].strip()
                        elif dxfTxt[l].rstrip() == "  6":
                                self.linetype = dxfTxt[l + 1].strip()                                
                        elif dxfTxt[l].rstrip() == " 62":
                                self.color = dxfTxt[l + 1].strip()                                
                        elif dxfTxt[l].rstrip() == "":
                                self.visable = int(dxfTxt[l + 1])
                self.startPt = [x1 + self.radius, y1, z1]
                self.endPt = [x1 + self.radius, y1, z1]
                self.center = [x1, y1, z1]
                         
class LINE(ENTITIES):
        def __init__(self):
                ENTITIES.__init__(self)

        def fromDXF(self, dxfTxt):
                for l in xrange(2, len(dxfTxt)):
                        if dxfTxt[l].rstrip() == " 10":
                                x1 = float(dxfTxt[l + 1])
                        elif dxfTxt[l].rstrip() == " 20":
                                y1 = float(dxfTxt[l + 1])
                        elif dxfTxt[l].rstrip() == " 30":
                                z1 = float(dxfTxt[l + 1])
                        elif dxfTxt[l].rstrip() == " 11":
                                x2 = float(dxfTxt[l + 1])
                        elif dxfTxt[l].rstrip() == " 21":
                                y2 = float(dxfTxt[l + 1])
                        elif dxfTxt[l].rstrip() == " 31":
                                z2 = float(dxfTxt[l + 1])
                        elif dxfTxt[l].rstrip() == "  8":
                                self.layer = dxfTxt[l + 1].strip()
                        elif dxfTxt[l].rstrip() == "  6":
                                self.linetype = dxfTxt[l + 1].strip()                                
                        elif dxfTxt[l].rstrip() == " 62":
                                self.color = dxfTxt[l + 1].strip()                                
                        elif dxfTxt[l].rstrip() == "":
                                self.visable = int(dxfTxt[l + 1])
                self.startPt = [x1, y1, z1]
                self.endPt = [x2, y2, z2]
                self.center = self.startPt
        def length(self):
                return(getDist(self.startPt, self.endPt))
                
class LWPOLYLINE(ENTITIES):
        def __init__(self):
                ENTITIES.__init__(self)
                self.numberOfVerts = 0        # 90
                self.closed = 0               # 70 1 : yes  ,  2 : no
                self.elevation = 0.0            # 38
                self.constantWidth = None     # 43  
                self.startWidth = None        # 40
                self.endWidth = None          # 41
                self.bulge = None             # 42
                self.verts = []

        def asLinesArcs(self):
                """Returns a list of lines and arcs in the polyline
                format:
                ["LINE", [start point xyz], [end point xyz]]
                or 
                ["ARC", [[start point xyz], [end point xyz], [center point xyz]]

                only supports closed polylines for now
                """
                
                ents = []
                for e in xrange(len(self.verts)):
                    # for lines
                    if (self.verts[e][3] == 0.0):
                        nextPoint = (e + 1) % len(self.verts)
                        ents.append(["LINE", 
                                     self.verts[e][0:3],
                                     self.verts[nextPoint][0:3]])
                    else:
                        nextPoint = (e + 1) % len(self.verts)
                        # get center using bulge factor
                        bulge = self.verts[e][3]
                        angle = 4 * numpy.arctan(bulge) # included angle for center and 2 end points
                        startPt = numpy.array(self.verts[e][0:3])
                        endPt = numpy.array(self.verts[nextPoint][0:3])
                        cordCenter = (endPt + startPt) / 2.0
                        sP2cCVector = cordCenter - startPt
                        sP2cCMag = numpy.sqrt(sum(pow(sP2cCVector, 2.0)))
                        cC2CircleCMag = sP2cCMag / numpy.tan(angle / 2.0)
                        cC2CircleCUnitV = numpy.array([-1 * sP2cCVector[1], sP2cCVector[0], 0])  / sP2cCMag
                        center = cordCenter + (cC2CircleCUnitV * cC2CircleCMag)
                        ents.append(["ARC", 
                                     list(startPt),
                                     list(endPt),
                                     list(center)])
                                     

                        
                # got to be better ways to do this
                # get rid of single point at end if last move is an arc 
                if ents[-1][1] == ents[-1][2]:
                    ents.pop(-1)

                return(ents)
                        
        def fromDXF(self, dxfTxt):  
                x1 = None              
                y1 = None
                for l in xrange(2, len(dxfTxt)):
                        if dxfTxt[l].rstrip() == " 10":
                                x1 = float(dxfTxt[l + 1])
                        elif dxfTxt[l].rstrip() == " 20":
                                y1 = float(dxfTxt[l + 1])
                        elif dxfTxt[l].rstrip() == " 38":
                                self.elevation = float(dxfTxt[l + 1])
                        elif dxfTxt[l].rstrip() == " 90":
                                self.numberOfVerts = float(dxfTxt[l + 1])
                        elif dxfTxt[l].rstrip() == " 70":
                                self.closed = float(dxfTxt[l + 1])
                        elif dxfTxt[l].rstrip() == " 43":
                                self.constantWidth = float(dxfTxt[l + 1])
                        elif dxfTxt[l].rstrip() == " 40":
                                self.startWidth = float(dxfTxt[l + 1])
                        elif dxfTxt[l].rstrip() == " 41":
                                self.endWidth = float(dxfTxt[l + 1])
                        elif dxfTxt[l].rstrip() == " 42":
                                self.bulge = float(dxfTxt[l + 1])
                        if (x1 != None) and (y1 != None):
                                pt = [x1, y1, self.elevation]
                                if len(dxfTxt) >= l + 3:
                                        if dxfTxt[l + 2].rstrip() == " 42":
                                                pt.append(float(dxfTxt[l + 3]))
                                        else:
                                                        pt.append(0)
                                else:
                                        pt.append(0)                                                


                                self.verts.append(pt)
                                x1 = None
                                y1 = None


                                        
        def getVerts(self):
                return(self.verts)
                
class POINT(ENTITIES):
        def __init__(self):
                ENTITIES.__init__(self)
                self.endPt = None
                self.getEnd = None
                
        def fromDXF(self, dxfTxt):
                for l in xrange(2, len(dxfTxt)):
                        if dxfTxt[l].rstrip() == " 10":
                                x1 = float(dxfTxt[l + 1])
                        elif dxfTxt[l].rstrip() == " 20":
                                y1 = float(dxfTxt[l + 1])
                        elif dxfTxt[l].rstrip() == " 30":
                                z1 = float(dxfTxt[l + 1])
                        elif dxfTxt[l].rstrip() == "  8":
                                self.layer = dxfTxt[l + 1].strip()
                        elif dxfTxt[l].rstrip() == "  6":
                                self.linetype = dxfTxt[l + 1].strip()                                
                        elif dxfTxt[l].rstrip() == " 62":
                                self.color = dxfTxt[l + 1].strip()                                
                        elif dxfTxt[l].rstrip() == "":
                                self.visable = int(dxfTxt[l + 1])
                self.startPt = [x1, y1, z1]
                self.center = self.startPt 
                

