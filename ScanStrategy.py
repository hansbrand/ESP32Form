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
from DataPoint import DataPoint
from FormMobile import FormMobile 
import EMailer

strategyActive = False
currentturns = 0
targetwidth =  10
targetheight = 0
maxturns = 0
connect = None
reversescan = False
MINWIDTH = 0.1
MINHEIGHT = 0.2
totaltime = None

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

    

    


def startScan( width, height, turns, connector, minwidth, minheight):
    global strategyActive, currentturns,targetwidth
    global targetheight,maxturns,connect,reversescan
    global MINWIDTH, MINHEIGHT
    global totaltime

    targetwidth = width
    targetheight = height
    currentturns = 0
    maxturns = turns
    connect = connector
    reversescan = False
    MINWIDTH = minwidth
    MINHEIGHT = minheight

    hdegree = 10
    factor = ((targetheight * 1000.0) / (targetwidth * 1000.0))
    vdegree = hdegree * factor
    vdegree = adjust(vdegree)
    #FM.LoadTurn(int(targetwidth * 100),int(targetheight * 100) , currentturns)
    #time.sleep(1)
    strategyActive   =  True
    starttime = time.monotonic()
    totaltime = time.time()

    clist = ED.genStrategyCommands(True, hdelta = hdegree, vdelta = vdegree)

    connect.current2send = len(clist)
    connect.alreadysent = 0
    FormMobile.enableButtons(True,True)

    for s in clist:
        connect.addCommand(s)
        print(s)
        pass

    difftime = time.monotonic() - starttime
    ds ="{:8.4f}".format(difftime)
    passfield = FormCommand.FormCommand.getWidgetByName("PASS")
    passtext = "PASS " + str(currentturns + 1) + ":" + ds + "/" + str(len(clist))
    passfield["text"] = passtext

    sleep(2)
    strategyActive = True


def getHorPoints( p1, p2, div, upper):
    pset = set()

    delta = abs(upper - p1.hnewdeg)
    #minimize
    for div1 in range(div,0,-1):
        d = delta / (div1 + 1)
        if (d > (0.25 * div1)):
            for i in range(1,div1 + 1):
                nx = adjust(p1.hnewdeg + float(d * i))
                ny = p1.vnewdeg
                if not (nx,ny) in DC.pointDone:                    
                    DC.pointDone.update([(nx,ny)])
                    pset.update([(nx,ny)])


            break
    return (pset)

def getHorAngles(row):
    global targetwidth
    index = 0
    horset = set()
    pointset = set()
    l = len(row)
    for index in range(0, l - 1):
        p = row[index]
        if p.state in ["VALID","COMPUTED"]:
            #minimal degree                    
            np =  row[index - 1]
            upper = p.hnewdeg
            if (upper < np.hnewdeg ):
                upper += 400
            
            dh = abs( np.hnewdeg - upper)
            if np.state in ["VALID","COMPUTED"] and (dh >= 0.5):
                dist = Calculator.get3Ddist(p,np)
                if dist > targetwidth:
                    #halfit

                    div = int(dist / targetwidth)
                    hd = (upper + np.hnewdeg) / 2.0
                    pset = getHorPoints(np,p,div,upper)
                    if len(pset) > 0:
                        pointset.update(pset)
                        hd = adjust(hd)
                        horset.update([hd])


            #minimal degree                    
            np = row[(index + 1) % l]
            dh = abs(np.hnewdeg - p.hnewdeg)
            upper = np.hnewdeg
            if (upper < p.hnewdeg ):
                upper += 400
            if np.state in ["VALID","COMPUTED"] and (dh >= 0.5):
                dist = Calculator.get3Ddist(p,np)
                if dist > targetwidth:
                    div = int(dist / targetwidth)
                    #halfit
                    hd = (upper + p.hnewdeg) / 2.0
                    pset = getHorPoints(p,np,div,upper)
                    if len(pset) > 0:
                        pointset.update(pset)
                        hd = adjust(hd)
                        horset.update([hd])

    return horset,pointset


def getVerPoints( p1, p2, div):
    pset = set()

    delta = abs(p2.vnewdeg - p1.vnewdeg)
    #minimize
    for div1 in range(div,0,-1):
        d = delta / (div1 + 1)
        if (d > (0.25 * div1)):
            for i in range(1,div1 + 1 ):
                ny = adjust(p1.vnewdeg + float(d * i))
                nx = p1.hnewdeg
                if not (nx,ny) in DC.pointDone:                    
                    DC.pointDone.update([(nx,ny)])
                    pset.update([(nx,ny)])
            break
    return (pset)

def getVerAngles(row):
    global targetheight
    index = 1
    verset = set()
    l = len(row)
    pointset = set()

    for index in range(1, l - 2):
        p = row[index]
        if p.state in ["VALID","COMPUTED"]:
            #minimal degree       
            np =   row[index - 1]           
            dh = abs( np.vnewdeg - p.vnewdeg)
            if np.state in ["VALID","COMPUTED"] and (dh >= 0.5):
                dist = Calculator.get3Ddist(p,np)
                if dist > targetheight:
                    #halfit
                    div = int(dist / targetheight)

                    hd = (p.vnewdeg + np.vnewdeg) / 2.0
                    pset = getVerPoints(np,p,div)
                    if len(pset) > 0:
                        pointset.update(pset)
                        hd = adjust(hd)
                        verset.update([hd])

            #minimal degree                    
            dh = abs( row[index + 1].vnewdeg - p.vnewdeg)
            np = row[index + 1]
            if np.state in ["VALID","COMPUTED"] and (dh >= 5):
                dist = Calculator.get3Ddist(p,np)
                if dist > targetheight:
                    #halfit
                    div = int(dist / targetheight)

                    hd = (p.vnewdeg +np.vnewdeg) / 2.0
                    pset = getVerPoints(p,np,div)
                    if len(pset) > 0:
                        pointset.update(pset)
                        hd = adjust(hd)
                        verset.update([hd])
    return verset,pointset

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

def addS1Scanning(commandList):
  message = "S1:D:" 
  commandList.append(message)

def addS2Scanning(commandList):
  message = "S2:D:" 
  commandList.append(message)

def createCommandList(angles, s1dict,s2dict):
    commands = []
    message = ""
    commands.append(ED.starttimerCommand())
    commandcounter = 0

    for a  in angles:
        #horiontal turn
        message = "M1:" + str(a) + ":"
        commands.append(message)
        if (a in s1dict.keys()):
            s1list =  list(s1dict[a])
        else:
            s1list = list()

        if (a in s2dict.keys()):
            s2list =  list(s2dict[a])
        else:
            s2list = list()            

        l1 = len(s1list)
        l2 = len(s2list)

        #generate command  per column
        for index in range(0,max(l1,l2)):
            if len(s1list) > 0:
                vs1point = s1list.pop()
                message = "M2:" + str(vs1point[1]) + ":"
                commands.append(message)
                addS1Scanning(commands)
                commandcounter += 1
            if len(s2list) > 0:
                vs2point = s2list.pop()
                message = "M3:" + str(vs2point[1]) + ":"
                commands.append(message)
                commandcounter += 1
                addS2Scanning(commands)
            #observe sensors
            if (commandcounter > 200):
                commandcounter = 0
                commands.append(ED.statusCommand(1))
                commands.append(ED.statusCommand(2))

    commands.append(ED.getstatsCommand())

        
    return commands

# def getRealh(sp):
#     return(sp[1]['realH'])

def createOpposits(points,scandir):
    horangles = set()
    newpoints = set()
    s1dict = dict()
    s2dict = dict()    
    s3dict = dict()


    #create opposite points and determine hangles
    for p in points:
        horangles.update([p[0]])
        if p[0] < 200:
            pnew = p[0] + 200
            xele = (pnew, p[1])
        else:
            pnew = p[0] - 200
        xele = (pnew, p[1])
        if not xele in DC.pointDone:
            newpoints.update([xele])
            DC.pointDone.update([xele])
            horangles.update([pnew])
    horlist = list(sorted(horangles,reverse = reversescan))
    points.update(newpoints)

    #sort each column
    for h in horlist:
        if (h < 200):
            s1dict[h]  = [t for t in points if t[0] == h]
        else:
            s2dict[h] = [t for t in points if t[0] == h]

    #determine  vertical direction
    S1reverse = DC.lastS1.vnewdeg > abs(DC.lastS1.vnewdeg - 200)
    S2reverse = DC.lastS2.vnewdeg > abs(DC.lastS2.vnewdeg - 200)

    #sort each column by vangle
    for k in s1dict.keys():
        s1 = s1dict[k]
        s1 = sorted(s1,key=lambda tup: tup[1],reverse=S1reverse)
        last = s1[len(s1) -1]
        S1reverse = last[1] > abs(last[1] - 200)
        s1dict[k] = s1

    for k in s2dict.keys():
        s2 = s2dict[k]

        s2 = sorted(s2,key=lambda tup: tup[1],reverse=S2reverse)
        last = s2[len(s2) -1]

        S2reverse = last[1] > abs(last[1] - 200)
        s2dict[k] = s2
    #normalize to hangle
    for k in s2dict.keys():
        s3dict[k - 200] = s2dict[k]
        horlist.remove(k)
    
    
    return points, horlist, s1dict, s3dict

def createRange(PointSet,reversescan, HorSet, VerSet):
        #row by row
    for k  in DC.mrows.keys():
        hset , pset = getHorAngles(DC.mrows[k])
        HorSet.update(hset)
        PointSet.update(pset)
    # colums not closed
    for k in DC.mcols.keys():
        vset , pset = getVerAngles(DC.mcols[k])
        VerSet.update(vset)
        PointSet.update(pset)
    
    # create scanpoints from angle sets
    PointSet, horlist, s1dict, s2dict = createOpposits(PointSet, reversescan)
    #scanlist,scanrows,scancols = createScanPoints(HorSet,VerSet)

    # sort in horizontal order with horpos
    #scancols = sorted(scancols.items(), key = getRealh ,reverse = reversescan)
    # for k in scancols.keys():     
    #     scancols[k] = sorted(scancols[k],key=lambda d: (d['realH'], d['hor_angle']) )


    #getcommands
    commands = createCommandList(horlist, s1dict,s2dict)
    return commands,PointSet

def sendMail():
        datestr = time.strftime("%d.%m.%y")
        timestr = time.strftime("%H:%M:%S")
        sender = EMailer.Emailer()
        sendTo = 'fdeitzer@gmail.com'
        emailSubject = "Hello World"
        emailContent = "Die Messung wurde am " + datestr + " um " + timestr + " abgeschlossen." 
        sender.sendmail(sendTo, emailSubject, emailContent)  



def nextTurn():
    global strategyActive, currentturns,targetwidth
    global targetheight,maxturns,connect,reversescan
    global MINWIDTH, MINHEIGHT,totaltime



    if connect.scanrunning:
        return
    starttime = time.monotonic()
    FM.SaveTurn(connect.receiveList,int(targetwidth *100),int(targetheight*100),currentturns)
    currentturns += 1
    if (currentturns > maxturns):
        strategyActive = False
        #sendMail()
        FormMobile.enableButtons(True,False)

        return
    Calculator.recomputeErrors()

    reversescan = not reversescan
    HorSet = set()
    VerSet = set()
    PointSet = set()

    commands, PointSet =createRange(PointSet, reversescan, HorSet, VerSet)
    if (len(commands) < 100):
        targetwidth = targetwidth / 2.0
        targetheight = targetheight / 2.0
        if (targetwidth >= MINWIDTH) and (targetheight >= MINHEIGHT):
            commands,PointSet =createRange(PointSet, reversescan, HorSet, VerSet)

    for c in commands:
        connect.addCommand(c)
    connect.current2send = len(commands)
    connect.alreadysent = 0

    difftime = time.monotonic() - starttime
    ds ="{:8.4f}".format(difftime)
    passfield = FormCommand.FormCommand.getWidgetByName("PASS")
    passtext = "PASS " + str(currentturns + 1) + "(" + str(maxturns + 1) + "): " + str(len(commands))
    passfield["text"] = passtext

    totaldiff = time.time() - totaltime
    ds ="{:8.4f}".format(totaldiff)
    passfield = FormCommand.FormCommand.getWidgetByName("TOTALTIME")
    passtext = "TOTALTIME " + ds 
    passfield["text"] = passtext
    return

def showTotalTime():
    global totaltime
    totaldiff = time.time() - totaltime
    f,g = modf(totaldiff)
    minutes = int(g / 60)
    seconds = int(g % 60)
    #ds ="{:8.4f}".format(totaldiff)
    ds = str(minutes) + " : " +f'{seconds:02}'
    passfield = FormCommand.FormCommand.getWidgetByName("TOTALTIME")
    passtext = ds 
    passfield["text"] = passtext

    

    



