import time
from ScanPoint import ScanPoint
from math import modf
from tkinter.constants import CURRENT
import ESPDevices as ED
import Calculator 
import DataContainer as DC
import FileManager as FM
import FormCommand
import operator
from collections import OrderedDict


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

    hdegree = 10
    vdegree = hdegree + hdegree * (targetheight / targetwidth)
    vdegree = adjust(vdegree)

    starttime = time.monotonic()

    clist = ED.genStrategyCommands(True, hdelta = hdegree, vdelta = vdegree)

    connect.current2send = len(clist)
    connect.alreadysent = 0

    for s in clist:
        connect.addCommand(s)
        print(s)
        pass

    difftime = time.monotonic() - starttime
    ds ="{:8.4f}".format(difftime)
    passfield = FormCommand.FormCommand.getWidgetByName("PASS")
    passtext = "PASS " + str(currentturns + 1) + ":" + ds + "/" + str(len(clist))
    passfield["text"] = passtext


    strategyActive = True

def getHorAngles(row):
    global targetwidth
    index = 0
    horset = set()
    l = len(row)
    for index in range(0, l - 1):
        p = row[index]
        if p.state in ["VALID","COMPUTED"]:
            #minimal degree                    
            np =  row[index - 1]
            dh = abs( np.hnewdeg - p.hnewdeg)
            if np.state in ["VALID","COMPUTED"] and (dh > 0.25):
                dist = Calculator.get3Ddist(p,np)
                if dist > targetwidth:
                    #halfit
                    hd = (p.hnewdeg + np.hnewdeg) / 2.0
                    hd = adjust(hd)
                    horset.add(hd)
            #minimal degree                    
            dh = abs( row[index + 1].hnewdeg - p.hnewdeg)
            np = row[(index + 1) % l]
            if np.state in ["VALID","COMPUTED"] and (dh > 0.25):
                dist = Calculator.get3Ddist(p,np)
                if dist > targetwidth:
                    #halfit
                    hd = (p.hnewdeg + np.hnewdeg) / 2.0
                    hd = adjust(hd)
                    horset.add(hd)
    return horset

def getVerAngles(row):
    global targetheight
    index = 1
    verset = set()
    l = len(row)

    for index in range(1, l - 2):
        p = row[index]
        if p.state in ["VALID","COMPUTED"]:
            #minimal degree       
            np =   row[index - 1]           
            dh = abs( np.vnewdeg - p.vnewdeg)
            if np.state in ["VALID","COMPUTED"] and (dh > 0.25):
                dist = Calculator.get3Ddist(p,np)
                if dist > targetheight:
                    #halfit
                    hd = (p.vnewdeg + np.vnewdeg) / 2.0
                    hd = adjust(hd)
                    verset.add(hd)
            #minimal degree                    
            dh = abs( row[index + 1].vnewdeg - p.vnewdeg)
            np = row[index + 1]
            if np.state in ["VALID","COMPUTED"] and (dh > 0.25):
                dist = Calculator.get3Ddist(p,np)
                if dist > targetheight:
                    #halfit
                    hd = (p.vnewdeg +np.vnewdeg) / 2.0
                    hd = adjust(hd)
                    verset.add(hd)
    return verset

def createScanPoints(HorSet,VerSet):
    retlist = []
    hdict = dict()
    vdict = dict()
    for h in HorSet:
        for v in VerSet:
            sp = ScanPoint(h,v)
            retlist.append(sp)
            if (v in hdict.keys()):
                hdict[v].append(sp)
            else:
                hdict[v] = [sp]            
            if (h in vdict.keys()):
                vdict[h].append(sp)
            else:
                vdict[h] = [sp]    
    return retlist, hdict, vdict        

def addScanning(commandList):
  message = "S1:D:" 
  commandList.append(message)
  message = "S2:D:" 
  commandList.append(message)

def createCommandList(scancols,scanrows,S1rev,S2rev):
    commands = []
    message = ""
    commands.append(ED.starttimerCommand())

    for prow in scancols:
        rdir = False
        if prow.hnewdeg < 200:
            S1rev = not S1rev
            rdir = S1rev
        else:
            S2rev = not S2rev
            rdir = S2rev
        if (rdir):
            prow = sorted(prow, key=lambda d: (d['ver_angle']))
        message = "M1:" + str(prow[0].realH) + ":"
        commands.append(message)

        for point in prow:
            if point.hor_angle < 200:
                message = "M2:" + str(point.ver_angle) + ":"
            else:
                message = "M3:" + str(point.ver_angle) + ":"

            commands.append(message)
            addScanning(commands)
    commands.append(ED.getstatsCommand())

        
    return commands

def nextTurn():
    global strategyActive, currentturns,targetwidth
    global targetheight,maxturns,connect,reversescan

    S1reverse = False
    S2reverse = False

    if connect.scanrunning:
        return
    starttime = time.monotonic()
    FM.SaveTurn(connect.receiveList,int(targetwidth *100),int(targetheight*100),currentturns)
    Calculator.recomputeErrors()
    currentturns += 1
    if (currentturns > maxturns):
        strategyActive = False
        return

    S1reverse = DC.lastS1.vnewdeg > abs(DC.lastS1.vnewdeg - 200)
    S2reverse = DC.lastS2.vnewdeg > abs(DC.lastS2.vnewdeg - 200)

    #mrows and mcols already sorted!!!!
    reversescan = not reversescan
    HorSet = set()
    VerSet = set()
    #row by row
    for key  in DC.mrows.keys():
        HorSet.update(getHorAngles(DC.mrows[key]))
    # colums not closed
    for key in DC.mcols.keys():
        VerSet.update(getVerAngles(DC.mcols[key]))
    
    HorSet = sorted(HorSet,reverse=reversescan)
    VerSet = sorted(VerSet,reverse=reversescan)
    # create scanpoints from angle sets
    scanlist,scanrows,scancols = createScanPoints(HorSet,VerSet)

    # sort in horizontal order
    #scancols = {k:v for k,v in sorted(scancols.items(), key = lambda item[1].realH,,reverse = reversescan)}
    #getcommands
    commands = createCommandList(scancols,scanrows,not S1reverse,not S2reverse)
    #print("Computed" + str(time.monotonic() - starttime))
    difftime = time.monotonic() - starttime
    ds ="{:8.4f}".format(difftime)
    passfield = FormCommand.FormCommand.getWidgetByName("PASS")
    passtext = "PASS " + str(currentturns + 1) + ":" + ds + "/" + str(len(commands))
    passfield["text"] = passtext
    return
    

    



