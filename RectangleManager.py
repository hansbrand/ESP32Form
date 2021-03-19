import math
import DataContainer as DC
from DataPoint import DataPoint as DP

VList = list()
HList = list()
VstartList = list()
HstartList = list()
targetheight = 0
targetwidth = 0
MINDEG = 11.0

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

def isMinRange(deg1,deg2):
    global MINDEG
    if ((deg2-deg1) < MINDEG ):
        return True
    else:
        return False

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
        if ret >= 7: ret = 7
        elif ret >= 5: ret = 5
        elif ret >= 3: ret = 3
        elif ret >= 1: ret = 1
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
                if (v[1] < point[1]) and (point[1] < v[3] ) and (deg1 <= v[0])  and (deg2 >= v[0]):
                    ret = (v[0], point[1])               
                    return True, False, ret

        if line is HList:
            first = next(filter(lambda p:  point[0] == p.hnewdeg and point[1] == p.vnewdeg, HstartList), None)

            if first:
                return True,True,(point[0],point[1])
            for h in HList:
                if (h[0] < point[0]) and (point[0] < h[2] ) and (deg1 <= h[1])  and (deg2 >= h[1]):
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
    if abs((stop.vnewdeg - start.vnewdeg)) < 0.5:
        return pset
    delta = float(stop.vnewdeg - start.vnewdeg) / float(div + 1)
    pset.update([(start.hnewdeg, start.vnewdeg)])
    pset.update([(stop.hnewdeg, stop.vnewdeg)])

    deg = start.vnewdeg + delta
    olddeg = float(start.vnewdeg)
    count = 1
    while deg < stop.vnewdeg:
        if (deg < 0 or deg > 193):
            #print (deg)
            olddeg = deg
            deg += delta

            continue
        deg = adjust(deg)

        #pset.update([(start.hnewdeg, t[1])])
        pset.update([(start.hnewdeg,deg)])
        pset.update([(stop.hnewdeg,stop.vnewdeg)])
        VstartList.append(stop)
        pset.update([(start.hnewdeg, deg)])

        olddeg = deg
        count += 1
        deg += delta
    xset = set(pset)
    for p in pset:
        xs = p[0]
        ys = p[1]
        ss = xs
        for i  in range(0,count + 1):

            xset.update([(adjust(ss) % 400,ys)])
            ss = ss + delta

    pset = xset
    return pset


def getHScans(start, stop, div):
    global VList, HList
    global VstartList, HstartList

    pset = set()
    if abs(stop.hnewdeg - start.hnewdeg) < 0.5:
        return pset
    if stop.hnewdeg <  start.hnewdeg:
        stopdeg = stop.hnewdeg + 400.0
    else:
        stopdeg = stop.hnewdeg

    pset.update([(start.hnewdeg, start.vnewdeg)])
    pset.update([(stopdeg % 400, stop.vnewdeg)])

    delta = float(abs(stopdeg - start.hnewdeg)) / float(div + 1)
    deg = (start.hnewdeg + delta) % 400
    olddeg = start.hnewdeg
    HstartList.append(stop)
    count = 1
    deg1 = (start.hnewdeg + delta) % 400
    while deg1 < stopdeg:
        deg = adjust(deg)
        if deg > 400:
            print(deg)
        #pset.update([(t[0], start.vnewdeg)])
        pset.update([(deg, start.vnewdeg)])
        olddeg = deg
        deg = (deg + delta) % 400
        deg1 = deg1 + delta
        count += 1

    xset = set(pset)
    for p in pset:
        xs = p[0]
        ys = p[1]
        ss = ys
        for i  in range(0,count + 1):
            if (ss <= 193.0):
                xset.update([(xs % 400, adjust(ss))])
                ss += delta
    pset = xset

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
            r1 = rows[index + 1]
            isline = False
            if VList:
                isline = checkInLine(VList, point)
            if not isline:
                tlist = []
                for p in rows[index + 1:]:
                    if (get3Ddist(p,point) < targetheight) and isMinRange(point.vnewdeg, p.vnewdeg):
                        tlist.append(p)
                        HstartList.append(p)
                    else:
                        break

                if tlist:
                    createVLine(point,tlist[-1])
                    VstartList.append(tlist[-1])
                    if point in VstartList:
                            VstartList.remove(point)
                    HstartList.append(tlist[-1])
                    
                elif isMinRange(point.vnewdeg,r1.vnewdeg):
                    createVLine(point,r1)
                    VstartList.append(r1)
                    HstartList.append(r1)
                    l = len(rows)
                    div = getDivisor(point,r1,targetheight, 
                                     abs(point.vAngle - rows[(index + 1) % l].vAngle))
                    if div > 0:
                        pointset.update(getVScans(point,rows[(index + 1) % l],div))

                #remove from startlist
                if point in VstartList:
                    VstartList.remove(point)
            # for p in pointset:
            #     if (p[0] > 400):
            #         print(p)

            if point in HstartList:
                rvnewdeg = point.vnewdeg
                if rvnewdeg in mrows.keys():
                    srow = mrows[rvnewdeg]
                    if len(srow) < 3:
                        if point in HstartList:
                            HstartList.remove(point)
                        continue
                    colindex = srow.index(point,0) 
                    l = len(mrows[rvnewdeg])
                    pnext = srow[(colindex + 1) % l]
                    stopdeg = pnext.hnewdeg
                    if point.hnewdeg > pnext.hnewdeg:
                        stopdeg = pnext.hnewdeg + 400
                        #print(point.hnewdeg)
                    if get3Ddist(point,pnext) > targetwidth and  isMinRange(point.hnewdeg,stopdeg):
                        div = getDivisor(point,pnext,targetwidth, 
                                     abs(point.hAngle - pnext.hAngle))
                        if div > 0:
                            pointset.update(getHScans(point,pnext,div))
                            # for p in pointset:
                            #     if p[0] > 400:
                            #         print(p)
                            #         getHScans(point,pnext,div)
                            
                        createHLine(point,pnext)
                        VstartList.append(pnext)
                        HstartList.append(pnext)
                    elif isMinRange(point.hnewdeg, stopdeg):
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

def makeLeftVpoints(mrows, mcols, point):
    global VList, HList
    global VstartList, HstartList,targetheight
    try:
        np = None
        pset = set()
        deg = point.hnewdeg
        index = mcols[deg].index(point,0)
        np = mcols[deg][index + 1]
        if get3Ddist(np ,point) > targetheight and isMinRange(point.vnewdeg,np.vnewdeg):
            div = getDivisor(point,np,targetheight, 
                                abs(point.vAngle - np.vAngle))
            if div > 0:
                delta = abs(np.vnewdeg - point.vnewdeg) / float(div +1)
                n = point.vnewdeg + delta 
                pset.update([(point.hnewdeg,n)])
        else:
            np = None
        return pset, np
    except Exception as exc:
        print(exc)
        return pset, np

def makeLeftHpoints(mrows, mcols, point):
    global VList, HList
    global VstartList, HstartList
    try:
        pset = set()
        deg = point.vnewdeg
        l = len(mrows[deg])
        np = None
        if (l < 3):
            return pset, np

        index = mrows[deg].index(point,0)
        pn = mrows[deg][index]
        np = mrows[deg][(index + 1) % l]
        stopdeg =  np.hnewdeg
        hstopdeg = np.hAngle
        if ( np.hnewdeg < pn.hnewdeg):
            stopdeg = np.hnewdeg + 400.0
            hstopdeg = np.hAngle + 180.0

        if get3Ddist(np ,point) > targetwidth and isMinRange(point.hnewdeg, stopdeg):
            div = getDivisor(point,np,targetwidth, 
                                abs(point.hAngle - hstopdeg))
            if div > 0:
                if not np in HstartList:
                    retpoint = np
                delta = abs(stopdeg - point.hnewdeg) / float(div +1)
                n = adjust((point.vnewdeg + delta) % 400)
                pset.update([(n, point.vnewdeg)])
        else:
            np = None                
        return pset, np
    except Exception as exc:
        print(exc)
        return pset, np

    pass

def purifyErrors(mrows,mcols):
    try:
        errorlist,_,_,_ = DC.getAllData()
        pset = set()
        for err in errorlist:
            hdeg = err.hnewdeg
            vdeg = err.vnewdeg

            if hdeg in mcols.keys():
                #culomns
                col = mcols[hdeg]
                if vdeg >= col[0].vnewdeg and vdeg <= col[-1].vnewdeg:
                    first = next(filter(lambda p:  (vdeg <= p.vnewdeg), col), None)
                    if first:
                        colindex = col.index(first,0) 
                        nextpoint = col[colindex]
                        previndex = (colindex - 1) if (colindex - 1) > 0 else len(col) -1
                        prevpoint = col[previndex]
                        if (isMinRange(prevpoint.vnewdeg, err.vnewdeg)):
                            div = getDivisor(prevpoint,err,targetheight,abs(prevpoint.vnewdeg - err.vnewdeg))
                            div = max(div,1)
                            pset.update(getVScans(prevpoint,err,div))
                        if (isMinRange(err.vnewdeg, nextpoint.vnewdeg)):
                            div = getDivisor(err,nextpoint,targetheight,abs(err.vnewdeg - nextpoint.vnewdeg))
                            div = max(div,1)
                            pset.update(getVScans(err,nextpoint,div))

            if vdeg in mrows.keys():
                row = mrows[vdeg]
                if hdeg >= row[0].hnewdeg and hdeg <= row[-1].hnewdeg:
                    first = next(filter(lambda p:  (hdeg <= p.hnewdeg), row), None)
                    if first:
                        rowindex = row.index(first,0) 
                        nextpoint = row[rowindex]
                        previndex = (rowindex - 1) 
                        stopdeg = err.hnewdeg
                        if (rowindex - 1) < 0:
                            previndex = len(row) - 1
                            stopdeg = err.hnewdeg + 400
                        prevpoint = row[previndex]
                        if (isMinRange(prevpoint.hnewdeg, stopdeg)):
                            div = getDivisor(prevpoint,err,targetwidth,abs(prevpoint.hnewdeg - stopdeg))
                            div = max(div,1)
                            pset.update(getHScans(prevpoint,err,div))
                        
                        l = len(row)
                        stopdeg = err.hnewdeg
                        if ((rowindex + 1) % l)  == 0:
                            stopdeg = nextpoint.hnewdeg + 400
                        if (isMinRange(err.hnewdeg, stopdeg)):
                            div = getDivisor(err,nextpoint,targetwidth,abs(err.hnewdeg - stopdeg))
                            div = max(div,1)
                            pset.update(getHScans(err,nextpoint,div))
        
        return pset          
    except Exception as exc:
        print(exc) 




def solveStartpoints(mrows,mcols):
    global VList, HList
    global VstartList, HstartList

    try:
        ret = True
        pset = set()
        horlist = list(HstartList)
        verlist = list(VstartList)
        l1 = len(horlist)
        l2 = len(verlist)
        for p in VstartList:
            hdeg = p.hnewdeg
            if not hdeg in mcols.keys():
                verlist.remove(p)
                continue

            if not p in mcols[hdeg]:
                verlist.remove(p)
                continue
            if p == mcols[hdeg][-1]:
                verlist.remove(p)
                continue

            xset, newpoint = makeLeftVpoints(mrows, mcols,p)
            if len(xset) > 0:
                pset.update(xset)
            if (p in verlist):
                verlist.remove(p)
            if (newpoint != None) and (not newpoint in verlist) and not checkInLine(HList, newpoint):
                verlist.append(newpoint)

        for p in HstartList:
            vdeg = p.vnewdeg
            if not vdeg in mrows.keys():
                horlist.remove(p)
                continue
            if not p in mrows[vdeg]:
                horlist.remove(p)
                continue
            if p == mrows[vdeg][-1]:
                horlist.remove(p)
                continue
            xset, newpoint = makeLeftHpoints(mrows, mcols,p)
            if len(xset) > 0:
                pset.update(xset)
            if (p in horlist):
                horlist.remove(p)
            if (newpoint != None) and (not newpoint in horlist):
                horlist.append(newpoint)


        l1 = len(horlist)
        l2 = len(verlist)
        HstartList = horlist
        VstartList = verlist
        #TODO
        return (l1 + l2 == 0),pset
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
        done, solveset = solveStartpoints(mrows,mcols)
        while not done:
             pset.update(solveset)
             done, solveset = solveStartpoints(mrows,mcols)
        pset.update(solveset)
        pset.update(purifyErrors(mrows,mcols))
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
    k = list(mrows.keys())
    HstartList.append(mrows[k[0]][0])
    targetheight = th
    targetwidth = tw
    pset = searchRectangles(mrows,mcols)    

    # purify
    x = set(pset)
    for p in pset:
        if tuple([int(p[0] * 10.0),int(p[1]*10.0)]) in DC.pointDone:                    
            x.remove(p)
    pset = x

    l = len(pset)
    return pset
