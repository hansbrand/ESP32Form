import threading 
import Calculator


PointCloud = None
PointDict = None
ErrorList = None
ComputedPoints = None
StatusList = None
xarr = []
yarr = []
zarr = []
marr = []
limits3D = None
mrows = None
mcols = None
lastS1 = None
lastS2 = None
pointDone = set()



# REDLIMIT = 3.0REDLIMIT
# BLUEVALUE = 6.0
# GREENLIMIT = 0.5

REDLIMIT = 0.3
BLUEVALUE = 1.0
GREENLIMIT = 0.01


errorcount = 0



from operator import itemgetter
savelock = threading.RLock() 


def getMarkerColor(val,limits = None):
    global REDLIMIT, GREENLIMIT,BLUEVALUE

    if val == -30000:
        return ("black")

    if (limits != None):
        BLUEVALUE = max(limits["zmax"],-limits["zmin"])
        REDLIMIT = BLUEVALUE * 0.3
        GREENLIMIT = BLUEVALUE * 0.05

    if val > BLUEVALUE: 
        return("blue")

    if val < GREENLIMIT: 
        return("green")            


    if val < REDLIMIT:
        refval = (REDLIMIT - float(val))  
        delta = float(REDLIMIT - GREENLIMIT)  
        refquot = refval / delta
        if (refquot > 1):
            refquot = 1
        return((1 - refquot, refquot, 0.0))
    else:
        refval =  (float(val) - REDLIMIT) 
        delta =  (BLUEVALUE - REDLIMIT) 
        refquot = refval / delta
        if (refquot > 1):
            refquot = 1
        return((1 - refquot , 0, refquot))





def initDataContainer():
    global PointCloud,pointDone
    global PointDict
    global ErrorList
    global StatusList
    global xarr
    global yarr
    global zarr
    global marr
    global limits3D
    global mrows
    global mcols
    global errorcount, ComputedPoints

    PointCloud = []
    PointDict = []
    ErrorList = []
    StatusList = []
    ComputedPoints = []
    xarr = []
    yarr = []
    zarr = []   
    marr = []
    limits3D = None
    mrows =  {}
    mcols =  {}
    pointDone = set()

def addArr(dp):
    global xarr
    global yarr
    global zarr
    global marr
    
    if (dp.state == "VALID"):
        xarr.append(dp.x)
        yarr.append(dp.y)
        zarr.append(dp.z)
        #marr.append(getMarkerColor((dp.meter)))
        #marr.append(getMarkerColor((abs(dp.z))))
        marr.append(getMarkerColor(abs(dp.z), getlimits3D()))



def addLimits(dp):
    global limits3D
    if (dp.state != "VALID"):
        return
    try:
        if (limits3D == None):
            limits3D = {}
            limits3D["xmin"] = dp.x 

            limits3D["xmax"] = dp.x
            limits3D["ymin"] = dp.y
            limits3D["ymax"] = dp.y
            limits3D["zmin"] = dp.z
            limits3D["zmax"] = dp.z    
            limits3D["hmax"] = dp.hnewdeg
            limits3D["vmax"] = dp.vnewdeg
        else:
            limits3D["xmin"] = limits3D["xmin"] if (limits3D["xmin"] < dp.x) else dp.x
            limits3D["xmax"] = limits3D["xmax"] if (limits3D["xmax"] > dp.x) else dp.x
            limits3D["ymin"] = limits3D["ymin"] if (limits3D["ymin"] < dp.y) else dp.y
            limits3D["ymax"] = limits3D["ymax"] if (limits3D["ymax"] > dp.y) else dp.y
            limits3D["zmin"] = limits3D["zmin"] if (limits3D["zmin"] < dp.z) else dp.z
            limits3D["zmax"] = limits3D["zmax"] if (limits3D["zmax"] > dp.z) else dp.z
            limits3D["hmax"] = limits3D["hmax"] if (limits3D["hmax"] > dp.hnewdeg) else dp.hnewdeg
            limits3D["vmax"] = limits3D["vmax"] if (limits3D["vmax"] > dp.vnewdeg) else dp.vnewdeg
    except Exception as exc:
        print(exc)
        return
        
def addRows(dp):
    global mrows
    global mcols

    if (dp.vnewdeg in mrows.keys()):
        mrows[dp.vnewdeg].append(dp)
    else:
        mrows[dp.vnewdeg] = [dp]

    if (dp.hnewdeg in mcols.keys()):
        mcols[dp.hnewdeg].append(dp)
    else:
        mcols[dp.hnewdeg] = [dp]


def addPoint(dp):
    global PointCloud,lastS1,lastS2
    global PointDict
    global savelock
    global errorcount
    global ErrorList

    try:
        PointCloud.append(dp)
        if (dp.hnewdeg < 200):
            lastS1 = dp
        else:
            lastS2 = dp
        savelock.acquire()
        pointDone.update([(dp.x,dp.y)])
        addArr(dp)
        addLimits(dp)
        addRows(dp)
        if (dp.state != "VALID"):
            ErrorList.append(dp)
            errorcount += 1
            #print("Errors : " + str(errorcount) + "/"+ str(len(PointCloud)))
        savelock.release()
        
        return

    except Exception as exc:
        print(exc)
        return
    #PointDict = sorted(PointCloud, key=lambda d: (d['hAngle'], d['vAngle']))
    pass

def getPointData():
    global xarr
    global yarr
    global zarr
    global marr
    global savelock


    savelock.acquire()
    #print(str(len(xarr)) + " / " + str(len(yarr)) + " / " + str(len(zarr)) + " / " + str(len(marr)))
    xl = list(xarr)
    yl = list(yarr)
    zl = list(zarr)
    ml = list(marr)

    savelock.release()
    return xl,yl,zl,ml

def getlimits3D():
    global limits3D
    savelock.acquire()
    if (limits3D != None):
        d= dict(limits3D)
    else: 
        d = None
    savelock.release()
    return d

    pass

def getAllData():
    global ErrorList,mrows, mcols,ComputedPoints

    return ErrorList, ComputedPoints,mrows,mcols

def addComputedPoints(plist,clist,mr,mc):
    global ComputedPoints,mrows,mcols,ErrorList
    savelock.acquire()
    ComputedPoints = plist
    ErrorList = clist
    for p in plist:
        xarr.append(p.x)
        yarr.append(p.y)
        zarr.append(p.z)
        marr.append("black")
    mrows = mr
    mcols = mc


    savelock.release()
