import DataContainer as DC
import DataPoint as DP
import math

def get3Ddist(m1,m2):
    mx = (m1.x -m2.x) ** 2
    my = (m1.y -m2.y) ** 2
    mz = (m1.z -m2.z) ** 2
    return(math.sqrt(mx + my + mz))

# m1 is closer
def Hcalchpoint (err,m1,m2):
            if ((m1.state == "VALID") and (m2.state == "VALID")):
                dx = m1.x - m2.x
                dy = m1.y - m2.y
                dz = m1.z - m2.z
                d1 = m1.hnewdeg - m2.hnewdeg
                d2 = err.hnewdeg - m1.hnewdeg
                if (d1 == 0): 
                    return "INVALID"
                k = d2 / d1

                err.x = m1.x + dx * k
                err.y = m1.y + dy * k
                err.z = m1.z + dz
                return "VALID"

# m1 is closer
def Vcalcvpoint (err,m1,m2):
            if ((m1.state == "VALID") and (m2.state == "VALID")):
                dx = m1.x - m2.x
                dy = m1.y - m2.y
                dz = m1.z - m2.z
                d1 = m1.vnewdeg - m2.vnewdeg
                d2 = err.vnewdeg - m1.vnewdeg
                if (d1 == 0): 
                    return "INVALID"
                k = d2 / d1

                err.x = m1.x + dx 
                err.y = m1.y + dy 
                err.z = m1.z + dz * k
                return "VALID"


def Hestimate(err, m):
    if (m.state in ["COMPUTED","VALID"]):
        err.x += m.x
        err.y += m.y
        err.z += m.z
        err.state = "COMPUTED"
        return "VALID"
    return "INVALID"

def estimate(err, mrows, mcols):
    rindex = mrows.index(err)
    vindex = mcols.index(err)
    validcounter = 0
    estcounter = 0

    err.x = 0
    err.y = 0
    err.z = 0

    m1 = mrows[rindex - 1 ]
    if (Hestimate(err,m1) == "VALID"):
        validcounter += 1;

    l = len(mrows)
    m1 = mrows[(rindex + 1) % l ]
    if (Hestimate(err,m1) == "VALID"):
        validcounter += 1;

    if (vindex > 0):
        m1 = mcols[vindex - 1 ]
        if (Hestimate(err,m1) == "VALID"):
            validcounter += 1;

    if (vindex < (len(mcols) - 1)):
        m1 = mcols[vindex + 1 ]
        if (Hestimate(err,m1) == "VALID"):
            validcounter += 1;

    if (validcounter == 0):
        return("INVALID")
    
    err.x = err.x / float(validcounter)
    err.y = err.y / float(validcounter)
    err.z = err.z / float(validcounter)
    err.state = "COMPUTED"
    return("COMPUTED")






def interpolate(err, mrows, mcols):
    rindex = mrows.index(err)
    vindex = mcols.index(err)
    validcounter = 0
    estcounter = 0

    err.x = 0
    err.y = 0
    err.z = 0
    
    m1 = mrows[rindex - 1 ]
    m2 = mrows[rindex - 2 ]
    if (Hcalchpoint(err,m1,m2) == "VALID"):
          validcounter += 1;

    l = len(mrows)
    m1 = mrows[(rindex + 1) % l ]
    m2 = mrows[(rindex + 2) % l ]
    if (Hcalchpoint(err,m1,m2) == "VALID"):
            validcounter += 1;
            
    if (vindex > 1):
        m1 = mcols[vindex - 1 ]
        m2 = mcols[vindex - 2 ]
        if (Vcalcvpoint(err,m1,m2) == "VALID"):
            validcounter += 1;

    
    if (vindex < (len(mcols) - 2)):
        m1 = mcols[vindex + 1 ]
        m2 = mcols[vindex + 2 ]
        if (Vcalcvpoint(err,m1,m2) == "VALID"):
            validcounter += 1;

    if (validcounter == 0):
        return("INVALID")
    
    err.x = err.x / float(validcounter)
    err.y = err.y / float(validcounter)
    err.z = err.z / float(validcounter)
    err.state = "COMPUTED"
    return("COMPUTED")
        







def printall(plist):
    for i in range(0,20):
        print (str(plist[i].hnewdeg) + "--" + str(plist[i].vnewdeg))

def recomputeErrors():
    try:
        resultlist = []
        el,cp,mrows,mcols = DC.getAllData()
        for k in mrows.keys():
            #printall(mrows[k])
            mrows[k] = sorted(mrows[k],key=lambda d: (d['hnewdeg']) )
            #printall(mrows[k])
        for k in mcols.keys():     
                #printall(mcols[k])
                mcols[k] = sorted(mcols[k],key=lambda d: (d['vnewdeg']) )
                #printall(mcols[k])

    
        for err in cp:
            col = mcols.get(err.hkey)
            row = mrows.get(err.vkey)
            if (interpolate(err, row, col) == "COMPUTED"):
                resultlist.append(err)
                el.remove(err)
            else:
                print(err)
                pass



        for err in el:
            col = mcols.get(err.hkey)
            row = mrows.get(err.vkey)
            if (interpolate(err, row, col) == "COMPUTED"):
                resultlist.append(err)
                el.remove(err)
            else:
                #print(err)
                pass



        for err in el:
            col = mcols.get(err.hkey)
            row = mrows.get(err.vkey)
            if (estimate(err, row, col) == "COMPUTED"):
                resultlist.append(err)
                el.remove(err)
            else:
                #print(err)
                pass


        DC.addComputedPoints(resultlist)
    except Exception as pexc:
                       print("3D Error: ", pexc)

    pass