import threading 


PointCloud = None
PointDict = None
ErrorList = None
StatusList = None
xarr = []
yarr = []
zarr = []
marr = []
limits3D = None



REDLIMIT = 8.0
YELLOWVALUE = 3.0
GREENLIMIT = 0.5

errorcount = 0



from operator import itemgetter
savelock = threading.RLock() 


def getMarkerColor(val):

    if val > REDLIMIT: 
        return("red")

    if val < GREENLIMIT: 
        return("green")            


    if val < YELLOWVALUE:
        refval = (YELLOWVALUE - float(val))  
        delta = float(YELLOWVALUE - GREENLIMIT)  
        refquot = refval / delta
        if (refquot > 1):
            refquot = 1
        return((1.0 - refquot, refquot, 0.0))
    else:
        refval =  (float(val) - YELLOWVALUE) 
        delta =  (REDLIMIT - YELLOWVALUE) 
        refquot = refval / delta
        if (refquot > 1):
            refquot = 1
        return((1.0 , 1.0 - refquot, 0))





def initDataContainer():
    global PointCloud
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
    global errorcount

    PointCloud = []
    PointDict = []
    ErrorList = []
    StatusList = []
    xarr = []
    yarr = []
    zarr = []   
    marr = []
    limits3D = None
    mrows =  {}
    mcols =  {}

def addArr(dp):
    global xarr
    global yarr
    global zarr
    global marr
    
    xarr.append(dp.x)
    yarr.append(dp.y)
    zarr.append(dp.z)
    marr.append(getMarkerColor(int(dp.meter)))

def addLimits(dp):
    global limits3D
    if (dp.state != "VALID"):
        return
    if (limits3D == None):
        limits3D = {}
        limits3D["xmin"] = dp.x 

        limits3D["xmax"] = dp.x
        limits3D["ymin"] = dp.y
        limits3D["ymax"] = dp.y
        limits3D["zmin"] = dp.z
        limits3D["zmax"] = dp.z    
        limits3D["hmax"] = dp.hAngle
        limits3D["vmax"] = dp.vAngle
    else:
        limits3D["xmin"] = limits3D["xmin"] if (limits3D["xmin"] < dp.x) else dp.x
        limits3D["xmax"] = limits3D["xmax"] if (limits3D["xmax"] > dp.x) else dp.x
        limits3D["ymin"] = limits3D["ymin"] if (limits3D["ymin"] < dp.y) else dp.y
        limits3D["ymax"] = limits3D["ymax"] if (limits3D["ymax"] > dp.y) else dp.y
        limits3D["zmin"] = limits3D["zmin"] if (limits3D["zmin"] < dp.z) else dp.z
        limits3D["zmax"] = limits3D["zmax"] if (limits3D["zmax"] > dp.z) else dp.z
        limits3D["hmax"] = limits3D["hmax"] if (limits3D["hmax"] > dp.hAngle) else dp.hAngle
        limits3D["vmax"] = limits3D["vmax"] if (limits3D["vmax"] > dp.vAngle) else dp.vAngle
        
def addRows(dp):
    global mrows
    global mcols

    if (str(dp.vAngle) in mrows.keys()):
        mrows[str(dp.vAngle)].append(dp)
    else:
        mrows[str(dp.vAngle)] = [dp]

    if (str(dp.hAngle) in mcols.keys()):
        mcols[str(dp.hAngle)].append(dp)
    else:
        mcols[str(dp.hAngle)] = [dp]


def addPoint(dp):
    global PointCloud
    global PointDict
    global savelock
    global errorcount

    PointCloud.append(dp);
    if (dp.state == "VALID"):
        savelock.acquire()
        addArr(dp)
        addLimits(dp)
        addRows(dp)
        savelock.release()
    else:
        errorcount += 1
        #print("Errors : " + str(errorcount) + "/"+ str(len(PointCloud)))
    return
    PointDict = sorted(PointCloud, key=lambda d: (d['hAngle'], d['vAngle']))
    pass

def getPointData():
    global xarr
    global yarr
    global zarr
    global marr
    global savelock


    savelock.acquire()

    xl = list(xarr)
    yl = list(yarr)
    zl = list(zarr)
    ml = list(marr)

    savelock.release()
    return xl,yl,zl,ml

def getlimits3D():
    global limits3D
    savelock.acquire()
    return dict(limits3D)
    savelock.release()
    pass


