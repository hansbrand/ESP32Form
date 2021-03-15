import numpy as np
import DataContainer as DC
from DataPoint import DataPoint
import math
from intersection import line_intersection
import Calculator as CC

def genScanPoints(p1, p2, isrow):
    ret = set()
    if not isrow:
        a1 = p1.hnewdeg
        a2 = p2.hnewdeg
    else:        
        a1 = p1.vnewdeg
        a2 = p2.vnewdeg
    
    if (a1 > a2) and not isrow:
        a2 += 400
    
    delta = 2.0 
    if (abs(a1-a2) <= 10.0): delta = 1
    if (abs(a1-a2) <= 2.0): delta = 0.25
    if (abs(a1-a2) <= 0.25): 
        return ret
    

    deg = a1 + delta

    while deg < a2:
        val = tuple([p1.hnewdeg, deg]) if isrow else tuple([deg, p1.vnewdeg])
        ret.update([val])
        deg += delta

    return ret

def getEdgePoint(row):
    try:
        x = list()
        p1 = row[0]
        p2 = row[1]
        p3 = row[2]
        p4 = row[3]

        ix = False
        iy = False
        iz = False

        distx = abs(p2.x - p3.x)
        disty = abs(p2.y - p3.y)
        distz = abs(p2.z - p3.z)

        if (distx >= disty) and (distx >= distz): ix = True
        elif (disty >= distx) and (disty >= distz): iy = True
        elif (distz >= disty) and (distz >= distx): iz = True

        p12d = [p1.x,p1.y]
        p22d = [p2.x,p2.y]
        p32d = [p3.x,p3.y]
        p42d = [p4.x,p4.y]

        np1 = np.array([p1.x, p1.y, p1.z])
        np2 = np.array([p2.x, p2.y, p2.z])
        np3 = np.array([p3.x, p3.y, p3.z])
        np4 = np.array([p4.x, p4.y, p4.z])

        d1 = np2 - np1
        d2 = np4 - np3

        # if iz:
        #     rx, ry = line_intersection(([p1.x,p1.y],[p2.x,p2.y]),([p3.x,p3.y], [p4.x,p4.y]))
        #     rz = p2.z + p3.z / 2#+ rx * d1[2]
        # if ix:
        #     ry, rz = line_intersection(([p1.y,p1.z],[p2.y,p2.z]),([p3.y,p3.z], [p4.y,p4.z]))
        #     rx = p2.x + p3.x / 2 #+ rx * d1[2]

        # if iy:
        #     rx, rz = line_intersection(([p1.x,p1.z],[p2.x,p2.z]),([p3.x,p3.z], [p4.x,p4.z]))
        #     ry = p2.y + p3.y / 2 #+ rx * d1[2]

        rx, ry = line_intersection(([p1.x,p1.y],[p2.x,p2.y]),([p3.x,p3.y], [p4.x,p4.y]))
        rz = p2.z + p3.z / 2#+ rx * d1[2]
        if rx == -10000 or rz == -10000 or ry == -10000:
            return x


        dp = DataPoint()
        dp.x = rx
        dp.y = ry
        dp.z = rz
        dp.state = "EDGE"

        dist1 = CC.get3Ddist(dp, p1)
        dist2 = CC.get3Ddist(dp, p2)
        if dist1 < dist2:
            dp = p1
        else:
            dp = p2
        x = list([dp])
        return (x)
    except Exception as exc:
        print(exc)
        return x

    #print((1-t)*p1[0] + t*p1[1])




def vp( points):
    try:

        p1 = points[0]
        p1 = np.array([p1.x,p1.y,p1.z])
        p2 = points[1]
        p2 = np.array([p2.x,p2.y,p2.z])
        p3 = p2 + (-p1)
        A = np.array(p3)

        p1 = points[2]
        p1 = np.array([p1.x,p1.y,p1.z])
        p2 = points[3]
        p2 = np.array([p2.x,p2.y,p2.z])
        p3 = p2 + (-p1)
        B = np.array(p3)

        C = np.dot(A,B)
        #C = A[0] * B[0] + A[1] * B[1] + A[2] * B[2]

        vl1 = math.sqrt(A[0] ** 2 + A[1] ** 2 + A[2] ** 2)
        vl2 = math.sqrt(B[0] ** 2 + B[1] ** 2 + B[2] ** 2)

        if ((vl1 * vl2) != 0):
            cosphi = C / (vl1 * vl2)
        else:
            return 0.0

        phi = np.degrees (np.arccos(cosphi))

        #print( phi )
        return phi
    except Exception as exc:
        print(exc)


def getAngleList(plist ,isrow):
    try:
        alist = set()
        edges = list()
        
        l = len(plist)
        if l < 4:
            return alist, edges
        
        last = l - 3
        if isrow: 
            last = l
        for i in range(0 , last):
            partlist =plist[i:i+4] 
            if (isrow):
                partlist = list()
                for i in range(0,4):
                    partlist.append(plist[i % l])
                    if (plist[i % l].state != "VALID"):
                        print("wrong")
            degree = vp(partlist) % 180
            if degree < 135 and degree > 45:
                cross = getEdgePoint(partlist)
                if (len(cross) > 0):
                    for e in cross:
                        edges.append(e)
                al = genScanPoints(plist[1],plist[2],isrow)
                alist.update(al)
                pass
        return alist, edges
    except Exception as exc:
        print(exc)



def createEdges():
    try:
        result = set()
        edges = list()

        mrows, mcols = DC.sortRows()
        mrows = dict(mrows)
        mcols = dict(mcols)

        for key in mrows.keys():
            points, edge = getAngleList(mrows[key],False)
            result.update(points)
            if (len(edge) > 0):
                for e in edge:
                    if DC.filter(e):
                        edges.append(e)
        for key in mcols.keys():
            points, edge = getAngleList(mcols[key],True)
            result.update(points)
            if (len(edge) > 0):
                for e in edge:
                    if DC.filter(e):
                        edges.append(e)

        x = set(result)
        for p in result:
            if tuple([int(p[0] * 10.0),int(p[1]*10.0)]) in DC.pointDone:                    
                x.remove(p)
        result = x

        DC.setEdgeList(edges)
        return result
    except Exception as exc:
        print(exc)
        return result


