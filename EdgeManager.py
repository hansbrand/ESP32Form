import numpy as np
import DataContainer as DC


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
    
    delta = 0.5 if (abs(a1-a2) >= 2.0) else 0.25
    

    deg = a1 + delta

    while deg < a2:
        val = tuple([p1.hnewdeg, deg]) if isrow else tuple([deg, p1.vnewdeg])
        ret.update([val])
        deg += delta


    return ret

def getEdgePoint(row):
    p1 = row[0]
    p1 = np.array([p1.x, p1.y, p1.z])
    p2 = row[1]
    p2 = np.array([p2.x, p2.y, p2.z])
    p3 = row[2]
    p3 = np.array([p3.x, p3.y, p3.z])
    p4 = row[3]
    p4 = np.array([p4.x, p4.y, p4.z])
    d1 = p2 - p1
    d2 = p4 - p3

    #t, s = np.linalg.solve(np.array([A[1]-A[0], B[0]-B[1]]).T, B[0]-A[0])
    t, s = np.linalg.solve(np.array([d1, d2]).T, p2[0]-p1[0])
    print((1-t)*p1[0] + t*p1[1])




def vp( points):
    try:
        p1 = points[0]
        p1 = np.array([p1.x,p1.y,p1.z])
        p2 = points[1]
        p2 = np.array([p2.x,p2.y,p2.z])
        p3 = p2 - p1
        A = np.array(p3)

        p1 = points[2]
        p1 = np.array([p1.x,p1.y,p1.z])
        p2 = points[3]
        p2 = np.array([p2.x,p2.y,p2.z])
        p3 = p2 - p1
        B = np.array(p3)
        C = np.dot(A,B)
        print(C)
        return C
    except Exception as exc:
        print(exc)


def getAngleList(plist ,isrow):
    alist = set()
    edges = list()
    l = len(plist)
    if l < 4:
        return
    
    last = l - 3
    if isrow: last = l
    for i in range(0 , last):
        if abs(vp(plist[i:i+4])) < 0.1:
            al = genScanPoints(plist[1],plist[2],isrow)
            cross = getEdgePoint(plist[i:i+4])
            alist.update(al)
            pass
    return alist



def createEdges():
    try:
        result = set()
        edges = list()

        mrows, mcols = DC.sortRows()
        mrows = dict(mrows)
        mcols = dict(mcols)

        for key in mrows.keys():
            result.update(getAngleList(mrows[key],False))
        for key in mcols.keys():
            result.update(getAngleList(mcols[key],True))
        return result
    except Exception as exc:
        print(exc)


