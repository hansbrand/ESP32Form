import math
import DataContainer as DC
from DataPoint import DataPoint as DP

VList = list()
HList = list()
VstartList = list()
HstartList = list()
targetheight = 0
targetwidth = 0

def adjust(deg):
    f,g = math.modf(deg)
    d = int(f * 100.0)

    if ( d % 25   == 0):
        return( float (g) + (float(d) / 100.0))
    q = int(d / 25.0)
    less = q * 25
    more = (q + 1) * 25
    if (abs(d-less) < abs(more - d)):
        return( float (g) + (float(less) / 100.0))
    else:
        return( float (g) + (float(more) / 100.0))


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
        if ret >= 2: ret = 2
        if ret >= 4: ret = 4
        if ret >= 8: ret = 8
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
    HList.append(tuple([p1.hnewdeg,p1.vnewdeg,p2.hnewdeg,p2.vnewdeg]))
    pass

def checkInLine(line, point):
    global HList,VList
    global VstartList, HstartList

    isline = None
    
    if line is VList:
        if point in VstartList:
            return False
        for v in VList:
            if (v[1] <= point.vnewdeg) and (point.vnewdeg <= v[3] ) and (v[0] == point.hnewdeg):
                return True

    if line is HList:
        if point in HstartList:
            return False
        for h in HList:
            if (h[0] <= point.hnewdeg) and (point.hnewdeg <= h[2] ) and (h[1] == point.vnewdeg):
                return True
    return isline

def checkCrossLine(line, point, deg1, deg2):
    global HList,VList
    global VstartList, HstartList

    try:
        isline = None
        ret = None
        if line is VList:
            first = next(filter(lambda p:  point[0] == p.hnewdeg and point[1] == p.vnewdeg, VstartList), None)
            if first:
                return True,True,(point[0],point[1])
            for v in VList:
                if (v[1] <= point[1]) and (point[1] <= v[3] ) and (deg1 <= v[0])  and (deg2 >= v[0]):
                    ret = (v[0], point[1])               
                    return True, False, ret

        if line is HList:
            first = next(filter(lambda p:  point[0] == p.hnewdeg and point[1] == p.vnewdeg, HstartList), None)

            if first:
                return True,True,(point[0],point[1])
            for h in HList:
                if (h[0] <= point[0]) and (point[0] <= h[2] ) and (deg1 <= h[1])  and (deg2 >= h[1]):
                    ret = ( point[0], h[1])               
                    return True,False,ret
        return False,None,None
    except Exception as exc:
        print(exc)
        return False,None,None






def getVScans(start, stop, div):
    global VList, HList
    global VstartList, HstartList

    pset = set()
    if (stop.vnewdeg - start.vnewdeg) < 0.5:
        return pset
    delta = float(stop.vnewdeg - start.vnewdeg) / float(div + 1)
    deg = start.vnewdeg + delta
    olddeg = float(start.vnewdeg)
    while deg < stop.vnewdeg:
        if (deg < 0 or deg > 193):
            print (deg)
            olddeg = deg
            deg += delta

            continue
        deg = adjust(deg)

        isok,isstart,t = checkCrossLine(HList,(start.hnewdeg, deg), olddeg, deg)
        if isok:
            if isstart:
                break
            else:
                pset.update([(start.hnewdeg, t[1])])
                VstartList.append(stop)
                if (t[1] < 0 or t[1] > 193):
                    print (deg)
                    olddeg = deg
                    deg += delta

                    continue
                break
        else:
                pset.update([(start.hnewdeg, deg)])

        olddeg = deg
        deg += delta
    return pset


def getHScans(start, stop, div):
    global VList, HList
    global VstartList, HstartList

    pset = set()
    if (stop.hnewdeg - start.hnewdeg) < 0.5:
        return pset
    delta = float(stop.hnewdeg - start.hnewdeg) / float(div + 1)
    deg = start.hnewdeg + delta
    olddeg = start.hnewdeg
    while deg < stop.hnewdeg:

        deg = adjust(deg)
        isok,isstart,t = checkCrossLine(VList,(deg, start.vnewdeg), olddeg, deg)
        if isok:
            if isstart:
                break
            else:
                pset.update([(t[0], start.vnewdeg)])
                HstartList.append(stop)
                break
        else:
                pset.update([(deg, start.vnewdeg)])
        olddeg = deg
        deg += delta
    return pset


def createLines(rows,mrows):
    global VList, HList
    global VstartList, HstartList, targetheight,targetwidth
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
                        HstartList.append(p)
                        pindex += 1
                    else:
                        break
                else:
                    pass

                if tlist:
                    createVLine(point,tlist[-1])
                    VstartList.append(tlist[-1])
                    if point in VstartList:
                            VstartList.remove(point)
                    #HstartList.append(tlist[-1])
                    
                else:
                    createVLine(point,rows[index + 1])
                    VstartList.append(rows[index + 1])
                    HstartList.append(rows[index + 1])
                    div = getDivisor(point,rows[index + 1],targetheight, 
                                     abs(point.vAngle - rows[index + 1].vAngle))
                    if div > 0:
                        pointset.update(getVScans(point,rows[index + 1],div))
                #remove from startlist
                if point in VstartList:
                    VstartList.remove(point)
            if point in HstartList:
                rvnewdeg = point.vnewdeg
                if rvnewdeg in mrows.keys():
                    srow = mrows[rvnewdeg]
                    colindex = srow.index(point,0) 
                    l = len(mrows[rvnewdeg])
                    pnext = srow[(colindex + 1) % l]
                    if get3Ddist(point,pnext) > targetwidth:
                        div = getDivisor(point,pnext,targetwidth, 
                                     abs(point.hAngle - pnext.hAngle))
                        if div > 0:
                            pointset.update(getHScans(point,pnext,div))
                        createHLine(point,pnext)
                        VstartList.append(pnext)
                        HstartList.append(pnext)
                    else:
                        createHLine(point,pnext)
                        VstartList.append(pnext)
                        HstartList.append(pnext)
                if point in HstartList:
                    HstartList.remove(point)
            
            index += 1
        return pointset
    except Exception as exc:
        print(exc)
        return pointset

def makeHNewStartpoints(mrows, mcols, p):
    global VList, HList

    ret = list()

    return ret

def makeVNewStartpoints(mrows, mcols, p):
    global VList, HList

    ret = list()

    return ret



def solveStartpoints(mrows,mcols):
    global VList, HList
    global VstartList, HstartList

    try:
        ret = True
        pset = set()
        horlist = list(HstartList)
        verlist = list(VstartList)
        for p in VstartList:
            verlist = makeVNewStartpoints(mrows,mcols, p)

        # for p in HstartList:
        #     horlist = makeHNewStartpoints(mrows,mcols, p)
        return ret,pset
    except Exception as exc:
        print(exc)
        return ret, pset

def searchRectangles(mrows,mcols): 
    global VList, HList
    global VstartList, HstartList

    try:
        pset = set()
        solveset = set()
    # initial pass
        for k in mcols.keys():
            pset.update(createLines(mcols[k], mrows))
        # done, solveset = solveStartpoints(mrows,mcols)
        # while not done:
        #     pset.update(solveset)
        #     done, solveset = solveStartpoints(mrows,mcols)
        #     pass
        pset.update(solveset)
        return pset
    except Exception as exc:
        print(exc)
        return pset
    pass

def createRectangles(tw, th):
    global HList, VList,VstartList, HstartList, targetheight, targetwidth

    mrows, mcols = DC.sortIdentRows()
    pset = set()

    VList = list()
    HList = list()
    VstartList = list()
    HstartList = list()
    VstartList.append(mcols[0][0])
    HstartList.append(mrows[0][0])
    targetheight = th
    targetwidth = tw
    pset = searchRectangles(mrows,mcols)    

    # purify
    x = set(pset)
    for p in pset:
        if p in DC.pointDone:
            x.remove(p)
    pset = x

    return pset
