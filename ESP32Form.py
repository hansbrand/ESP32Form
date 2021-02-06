
import tkinter as tk
import ctypes
import random
import time
import math
import sys
import threading
from sys import exit
import atexit
import os

import FormBuild
import FormCallbacks
import FormCommand
import USBCommunicator
import TCPCommunicator
from DataContainer  import initDataContainer 
import ESPDevices
import EMailer
import FormMobile
from Graph3D import Graph3D
import FileManager as FM
import Calculator


progressbar = None
graph3D = None
currentframe = None
SMALLSCREEN = True
ISLINUXOS = False
communicator = None
changeEvent = False
show3Dwindow = False



class Application(tk.Frame):
    master = None
    fb = None
    timedelta = 0
    communicator = None
    newwin = None
    canvas_width = None
    canvas_height = None
    isRunning = False
    isLoading  = False
    drawtime = 10

    @classmethod
    def cleanup(self):
        global ISLINUXOS

        print("exit")
        TCPCommunicator.emergeny()
        time.sleep(10)

        TCPCommunicator.TCP_close()
        if (ISLINUXOS):
            os.system("sudo poweroff")
        time.sleep(10)


    def createNewWindow(self):
        global currentCanvas

        if (tk.Toplevel.winfo_exists(self.newwin) == False):
            self.newwin = tk.Toplevel(self.master, 
                width=self.canvas_width ,
                height=self.canvas_height)
            self.newwin.config(bg='#202020')

        graph3D = Graph3D(self.newwin)



    def initCanvas(self,master):
        global graph3D
        global currentframe

        self.master = master
        self.screen_width = self.master.winfo_screenwidth()
        self.screen_height = self.master.winfo_screenheight()

        self.canvas_width = int((self.screen_width * 7.0) / 8.0)
        #self.canvas_width =  master.winfo_width() 
        self.canvas_height = int((self.screen_height * 7.0) / 8.0)
        self.colmax = self.canvas_width

        self.newwin = tk.Toplevel(master, 
           width  =self.canvas_width,
           height =self.canvas_height)
        #self.newwin.geometry(str(self.canvas_width) + "x" + str(self.canvas_height))
        #cwindow = self.newwin
        #self.clientlabel.grid(row=6,column = 1)
        self.newwin.update()
        graph3D = Graph3D(self.newwin)
    
        #graph3D = Graph3D.Graph3D(self.newwin)

        
        #currentframe = graph3D

        #self.newwin.iconify()

    def show3D(self):
            if tk.Toplevel.winfo_exists(self.newwin):
                self.newwin.deiconify()
            else:
                self.createNewWindow()
 
    @classmethod
    def setshow3D(self):
        show3Dwindow = True
    

    def eventloop(self):
        #print("eventloop")
        global show3Dwindow

        deltatime = 20
        skip = self.timeman > 0

        self.timedelta = time.time()

        self.timedelta = time.time() - self.timedelta
        self.timeman = max(0,(self.timeman + self.timedelta - deltatime))

        #USBCommunicator.updateSend()
        TCPCommunicator.updateSend()

        self.timedelta = time.time() - self.timedelta
        self.timeman = max(0,(self.timeman + self.timedelta - deltatime))
        #print(show3Dwindow)
        if (show3Dwindow):
            show3Dwindow = False
            self.show3D()

        if FM.isScanning:
            self.isLoading = True            
        if self.isLoading:
            if not FM.isScanning:
                self.isLoading = False 
                #Calculator.recomputeErrors()
                pass

        if TCPCommunicator.isScanning:
            self.isRunning = True            
        if self.isRunning:
            if not TCPCommunicator.isScanning:
                self.isRunning = False 
                #Calculator.recomputeErrors()

                pass

        if ((time.time() - self.lastStatus) > self.drawtime):
            self.lastStatus = time.time()
            #print(self.lastStatus)
            if graph3D.Is2Draw():
                graph3D.drawDia(True)
                self.drawtime = max(self.drawtime - 1.0, 2.0)
            else:
                self.drawtime += 5.0

            #self.newwin.update()

#            USBCommunicator.addCommand(ESPDevices.Sensor1.statusCommand(),True)
#           USBCommunicator.addCommand(ESPDevices.Sensor2.statusCommand(),True)
            # TCPCommunicator.addCommand(ESPDevices.Sensor1.statusCommand(),True)
            # TCPCommunicator.addCommand(ESPDevices.Sensor2.statusCommand(),True)

        self.master.after(300,self.eventloop)


    def __init__(self, master=None):
        global SMALLSCREEN
        global ISLINUXOS
        global graph3D

        global communicator
        super().__init__(master)
        #master.attributes('-fullscreen', True)
        #master.update()


        self.master = master
        self.screen_width = self.master.winfo_screenwidth()
        self.screen_height = self.master.winfo_screenheight()

        self.master.title( "ESP32 Controller");
        self.timeman = 0

        #communicator =  USBCommunicator.USBCommunicator()
        tcpc =  TCPCommunicator.TCPCommunicator()

        fc = FormCallbacks.FormCallbacks("TCPCommunicator")

        if (SMALLSCREEN):
            fb = FormMobile.FormMobile(master)

        else:
            fb = FormBuild.FormBuild(master)
        fb.genCallBacks()

        TCPCommunicator.startserverThread()
        time.sleep(2)


        initDataContainer()
        ESPDevices.initDevices()
        self.lastStatus = 0

        self.initCanvas(master)
        initDataContainer()
        atexit.register(self.cleanup)
        #sender = EMailer.Emailer()
        #sendTo = 'fdeitzer@gmail.com'
        #emailSubject = "Hello World"
        #emailContent = "This is a test mail : " 
        #sender.sendmail(sendTo, emailSubject, emailContent)  

        self.master.after(0,self.eventloop)

        #self.pack()
        #initDataPool()
        #self.filelabel=None
        #self.create_widgets(master)
        #ParamMan.initParams(master,self.buttonheight,self.buttonwidth, self.scalelength)
        #self.valueindex=0
        #self.diamax=0
        #self.lastmessage=""
        #self.tupellist =[]
        #DC.init()
        #self.datareset = False

        #self.timeman = 0

        #self.timedelta = 0
        #setPause(False)
        #self.fileloaded = False




def Main():
    global ISLINUXOS

    root = tk.Tk()
    if sys.platform.startswith('win'):
        ISLINUXOS = False
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ISLINUXOS = True
    else:
        raise environmenterror('unsupported platform')

    #tcpserver.initServer()
    app = Application(master=root)
    app.mainloop()

if __name__== "__main__":
    Main()