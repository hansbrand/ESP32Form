from math import modf
import ESPDevices as ED

strategyActive = False
currentturns = 0
targetwidth =  10
targetheight = 0
maxturns = 0
connect = None
reversescan = False

def adjust(deg):
    f,g = modf(deg)
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

    

    


def startScan( width, height, turns, connector):
    global strategyActive, currentturns,targetwidth
    global targetheight,maxturns,connect,reversescan

    targetwidth = width
    targetheight = height
    currentturns = 0
    maxturns = turns
    connect = connector
    reversescan = False

    hdegree = 20
    vdegree = hdegree + hdegree * (targetheight / targetwidth)
    vdegree = adjust(vdegree)

    clist = ED.genStrategyCommands(True, hdelta = hdegree, vdelta = vdegree)

    connect.current2send = len(clist)
    connect.alreadysent = 0

    for s in clist:
        connect.addCommand(s)
        print(s)
        pass


    strategyActive = True