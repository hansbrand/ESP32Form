PointCloud = None
PointDict = None
ErrorList = None
StatusList = None

from operator import itemgetter

def initDataContainer():
    global PointCloud
    global PointDict
    global ErrorList
    global StatusList

    PointCloud = []
    PointDict = []
    ErrorList = []
    StatusList = []

def addPoint(dp):
    global PointCloud
    global PointDict

    PointCloud.append(dp);
    PointDict = sorted(PointCloud, key=lambda d: (d['hAngle'], d['vAngle']))
    pass




