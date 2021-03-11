import math
import DataContainer as DC

VList = list()
HList = list()
VstartList = list()
HstartList = list()
targetheight = 0
targetwidth = 0

def getDivisor(p1,p2,targetsize,diffangle):
    try:
        ret = 1
        diff = max(p1.meter,p2.meter) 
        # if (diff > 4.0):
        #     print (diff)
        ddangle = diffangle / 0.225
        scale = diff * math.sin(math.radians(0.225))
        nangle = targetsize / scale
        ret = ddangle / nangle
        return int(ret)
    except Exception as exc:
        print(exc)
        return(1)


def get3Ddist(m1,m2):
    mx = (m1.x -m2.x) ** 2
    my = (m1.y -m2.y) ** 2
    mz = (m1.z -m2.z) ** 2
    return(math.sqrt(mx + my + mz))


def createVLine(p1,p2):
    global VList
    if p1.vnewdeg > p2.vnewdeg:
        p1,p2 = p2,p1
    VList.append(tuple([p1.hnewdeg,p1.vnewdeg,p2.hnewdeg,p2.vnewdeg]))
    pass

def createHLine(p1,p2):
    global HList
    if p1.hnewdeg > p2.hnewdeg:
        p1,p2 = p2,p1
    HList.append([p1.hnewdeg,p1.vnewdeg,p2.hnewdeg,p2.vnewdeg])
    pass

def checkInLine(line, point):
    global HList,VList
    isline = None
    if line is VList:
        for v in VList:
            if (v[1] <= point.vnewdeg) and (point.vnewdeg <= v[3] ) and (v[0] == point.hnewdeg):
                return True

    if line is HList:
        for h in HList:
            if (h[0] <= point.hnewdeg) and (point.hnewdeg <= h[2] ) and (h[1] == point.vnewdeg):
                return True
        isline = [p for p in VList 
            if ((p[1] <= point.hnewdeg <= p[2] ) and p[0] == point.vnewdeg)][0]
    return isline

def getVScans(start, stop, div):
    pset = set()
    delta = (stop.vnewdeg - start.vnewdeg) / div
    deg = start.vnewdeg + delta
    while deg < stop.vnewdeg:
        pset.update([(start.hnewdeg, deg)])
        deg += delta
    return pset

# found_bmi_range = [bmi_range for bmi_range
#                    in bmi_ranges
#                    if bmi_ranges[2] <= bmi <= bmi_ranges[3]
#                   ][0]
def createLines(rows):
    global VList, HList
    global VstartList, HstartList
    try:
        # each point in column
        pointset = set()
        index = 0
        for  row in rows[:-1]:
            #search hline
            point = row
            isline = False
            if VList:
                isline = checkInLine(VList, point)
            if not isline:
                pindex = index + 1
                tlist = []
                for p in rows[index + 1:]:
                    if get3Ddist(p,point) < targetheight:
                        tlist.append(p)
                        pindex += 1
                    else:
                        break
                else:
                    pass

                if tlist:
                    createVLine(point,tlist[-1])
                    VstartList.append([tlist[-1]])
                else:
                    div = getDivisor(point,rows[index + 1],targetheight, 
                                     abs(point.vAngle - rows[index + 1].vAngle))
                    if div > 0:
                        pointset.update(getVScans(point,rows[index + 1],div))


                
            index += 1
            return pointset
    except Exception as exc:
        print(exc)
        return pointset
        


def searchRectangles(mrows,mcols):
    try:
        pset = set()
    # initial pass
        for k in mcols.keys():
            pset.update(createLines(mcols[k]))
    except Exception as exc:
        print(exc)
    pass

def createRectangles(tw, th):
    global HList, VList,VstartList, HstartList, targetheight, targetwidth

    mrows, mcols = DC.sortRows()
    pset = set()

    VList = list()
    HList = list()
    VstartList = list()
    HstartList = list()
    targetheight = th
    targetwidth = tw
    pset = searchRectangles(mrows,mcols)    

    for p in pset:
        if p in DC.pointDone:
            pset.remove(p)

    return pset
