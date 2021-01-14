
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
import FormCommand
import USBCommunicator
from DataContainer  import initDataContainer 
import ESPDevices
import Graph3D
import EMailer
import FormMobile


progressbar = None
graph3D = None
currentframe = None
SMALLSCREEN = True


class Application(tk.Frame):
    master = None
    fb = None
    timedelta = 0
    communicator = None
    newwin = None
    canvas_width = None
    canvas_height = None

    def cleanup(self):
        print("exit")
        os.system("sudo poweroff")
        time.sleep(10)


    # def createNewWindow(self):
    #     global currentCanvas

    #     if (tk.Toplevel.winfo_exists(self.newwin) == False):
    #         self.newwin = tk.Toplevel(self.master, 
    #             width=self.canvas_width ,
    #             height=self.canvas_height)
    #         self.newwin.config(bg='#202020')

    #     graph3D = Graph3D(self.newwin)



    def initCanvas(self,master):
        global graph3D
        global currentframe

        self.master = master
        self.canvas_width = self.screen_width / 2
        #self.canvas_width =  master.winfo_width() 
        self.canvas_height = self.screen_height / 2
        self.colmax = self.canvas_width

        self.newwin = tk.Toplevel(master, 
           width=self.canvas_width,
           height=self.canvas_height)
        cwindow = self.newwin
        #self.clientlabel.grid(row=6,column = 1)

        self.lwin= tk.Frame(self.newwin, 
           width=self.canvas_width,
           height=self.canvas_height)


        self.lwin.config(bg='#202020')
        graph3D = Graph3D.Graph3D(self.newwin)

        
        currentframe = graph3D

        self.newwin.iconify()




    def eventloop(self):
        #print("eventloop")
        deltatime = 180
        skip = self.timeman > 0
        self.timedelta = time.time()

        self.timedelta = time.time() - self.timedelta
        self.timeman = max(0,(self.timeman + self.timedelta - deltatime))
        USBCommunicator.updateSend()

        self.timedelta = time.time() - self.timedelta
        self.timeman = max(0,(self.timeman + self.timedelta - deltatime))
        if ((time.time() - self.lastStatus) > 60.0):
            self.lastStatus = time.time()
            USBCommunicator.addCommand(ESPDevices.Sensor1.statusCommand(),True)
            USBCommunicator.addCommand(ESPDevices.Sensor2.statusCommand(),True)

        self.master.after(1000,self.eventloop)


    def __init__(self, master=None):
        global SMALLSCREEN
        super().__init__(master)
        #master.attributes('-fullscreen', True)
        #master.update()
        self.master = master
        self.screen_width = self.master.winfo_screenwidth()
        self.screen_height = self.master.winfo_screenheight()

        self.master.title( "ESP32 Controller")
        self.timeman = 0
        communicator =  USBCommunicator.USBCommunicator()

        if (SMALLSCREEN):
            fb = FormMobile.FormMobile(master)

        else:
            fb = FormBuild.FormBuild(master)
        fb.genCallBacks()

        initDataContainer()
        ESPDevices.initDevices()
        self.lastStatus = 0

        #self.initCanvas(master)
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
    root = tk.Tk()
#tcpserver.initServer()
    #tcpserver.startserverThread()
    app = Application(master=root)
    app.mainloop()

if __name__== "__main__":
    Main()