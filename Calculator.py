import DataContainer as DC
import DataPoint as DP
import math

def get3Ddist(m1,m2):
    mx = (m1.x -m2.x) ** 2
    my = (m1.y -m2.y) ** 2
    mz = (m1.z -m2.z) ** 2
    return(math.sqrt(mx + my + mz))

# m1 is closer
def calcnewpoint (err,m1,m2):
            if ((m1.state == "VALID") and (m2.state == "VALID")):
                dx = m1.x - m2.x
                dy = m1.y - m2.y
                dz = m1.z - m2.z

                err.x = m1.x + dx
                err.y = m1.y + dy
                err.z = m1.z + dz




def interpolate(err, mrows, mcols):
    rindex = mrows.index(err)
    cindex = mcols.index(err)
    validcounter = 0
    estcounter = 0
    validx = 0
    estx = 0
    validy = 0
    esty = 0

    
    if (rindex > 1):
        m1 = mrows[rindex - 1 ]
        m2 = mrows[rindex - 2 ]
        calcnewpoint(err,m1,m2)


def printall(plist):
    for i in range(0,20):
        print (str(plist[i].hnewdeg) + "--" + str(plist[i].vnewdeg))

def recomputeErrors():
    resultlist = []
    el,mrows,mcols = DC.getAllData()
    for k in mrows.keys():
        printall(mrows[k])
        mrows[k] = sorted(mrows[k],key=lambda d: (d['hnewdeg']) )
        printall(mrows[k])
    for k in mcols.keys():     
            printall(mcols[k])
            mcols[k] = sorted(mcols[k],key=lambda d: (d['vnewdeg']) )
            printall(mcols[k])
 
    for err in el:
        col = mcols.get(err.hkey)
        row = mrows.get(err.vkey)
        resultlist.append(interpolate(err, row, col))


    pass