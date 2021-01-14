
from tkinter import filedialog
from tkinter import *
import os
import json 
import queue
import time
from FileHandler import filestat 
import ESPDevices
import DataContainer
from DataPoint import DataPoint 

def analyse(line):
    mi = messageInfo()
    mi.currentMessage=line
    try:
        stt = line;

        #print("received")
        #print(mlist)
        
        fd = None
        if (line[0] !=  "{"):
            newstr = line.split(";")
            if newstr[1][0]  == "T":
                mi.mstatus = newstr[1][0]
                mi.raspi=newstr[1]
                #if "Connected" in newstr[1]:
                #    newstr = newstr[1].split(",")
                #    newstr = newstr[0].split(":")
        else:
            x = json.loads(line)
            #print("messagetype : ", x["messagetype"])
            #print("messagetype : ", x["original"])

            if "null" in x["original"]:
                print(x)

            if "Er" in x["original"]:
                x["tag"] = "E"
                mi.hdegree = x["xdegree"]
                mi.vdegree = x["vdegree"]
                mi.quality= 10000
                mi.messagetype = x["messagetype"]


            if x["tag"] in ("D","M","F","S"):
                try:
                    sttag = x["tag"]
                    mi.mstatus=sttag
                    mi.messagetype = x["messagetype"]
                    mi.device = x["name"] + mi.mstatus
                    stt = x["original"]
                    if (sttag != "S"):
                        stt = stt[2:]
                        nlist = stt.split(",")
                        mpos = nlist[0].replace("m","")
                        #newerstr= mpos[2:]
                        newval = str((int((float(mpos)*1000.0))/1000)*1000)
                        mi.distance = newval
                        mi.hdegree = x["xdegree"]
                        mi.vdegree = x["vdegree"]
                        mi.quality= int(nlist[1])

                except Exception as inst:
                    print (inst)
                    
            if x["tag"] == "E":
                mi.mstatus="E"
                mi.device = x["name"] + mi.mstatus
                mi.messagetype = x["messagetype"]

                mi.error = x["original"]
                mi.hdegree = x["xdegree"]
                mi.vdegree = x["vdegree"]

            if x["tag"] in ("O","C"):
                mi.mstatus = x["tag"]
                mi.messagetype = x["messagetype"]
            mi.jsondata=x
            return mi
    except Exception as inst:
        print(type(inst)) 
        print(inst)
        print("analyse")
        return None





def loadfile(filename):
    try:

        qlaser=queue.Queue()

        DataContainer.initDataContainer()
        datafd=open(filename,"rt")
        buffer = datafd.readlines()
        datafd.close()
        for message in buffer:
            ident = message[0:2]
            if ident in ESPDevices.deviceList:
                #print("Device found :" + message)
                if (ESPDevices.isSensor(message)):
                    dp = DataPoint(message)
                    DataContainer.addPoint(dp)
        print(DataContainer.ErrorList)
        print(DataContainer.StatusList)
        return True
    except Exception as pex:
        print("loadfile:",pex)
        return False





def openLoadFile(master):
    filename = filedialog.askopenfilename(initialdir = "./dist",title = "Data File",filetypes = (("CSV files","*.csv"),("Data files","*.txt"),("all files","*.*")))
    print("Filename :", filename)
    if (filename == ''):
        return False
    check= loadfile(filename)


    return check

def saveCSV(x,y,z,ext):

    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, 'dist\\') + "DIST"+time.strftime("%H_%M_%S")+"_" + ext +".csv"
    with open(filename, 'wt+') as f:
        for l in range(0,len(x)):
            line = str(int(x[l])) + ";" + str(int(y[l])) + ";" + str(int(z[l])) + "\n"
            f.write(line)

def saveCSVlist(slist,ext):

    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, 'dist\\') + "DIST"+time.strftime("%H_%M_%S")+"_" + ext +".csv"
    with open(filename, 'wt+') as f:
        for l in slist:
            #line = str(int(x[l])) + ";" + str(int(y[l])) + ";" + str(int(z[l])) + "\n"
            #l = l.replace("|",";")
            f.write(l)
        f.write("\n")

