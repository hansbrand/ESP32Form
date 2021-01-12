import tkinter as tk
from tkinter.ttk import *
import FormCommand 
import FormCallbacks
from USBCommunicator import USBCommunicator
from tempGraph import tempGraph
from Row0Init import Row0Init
from Row1Init import Row1Init
from FormMobile import FormMobile


widget_names = (            
    "INIT",
    "CALIBRATE",
    "STOP",
    "RESUME",
    "FULLSCAN",
    "SAVE_FILE",
    "LOAD_FILE",
    "CLEAR",
    "ADJUST"
    "QUIT",
    "WLAN",
    "USB",
    "HSteps",
    "VSteps",
    "Use Strategy",
    "Virtual 3D",
    "Save Data?",
    "Red",
    "Yellow",
    "Green",
    "Colored",
    "HStart",
    "HEnd",
    "VStart",
    "VEnd",
    "Delay",
    "Quality"
               )

class FormBuild(tk.Frame):
    master = None
    buttonheight = None
    buttonwidth = None
    scalelength  = None
    Row0Frame = None
    Row1Frame = None
    Row2Frame = None
    fc = None


    #graphicWindows = {
    #    "lines":    lineGraph,
    #    "radar":    radarGraph,
    #    "errorlist": errorList,
    #    "3D":       graph3D
    #    }


    def __init__(self, master=None):
        
        super().__init__(master)
        self.master = master
        fc = FormCommand.FormCommand(master)

        self.fc = FormCommand.FormCommand(master)
        self.screen_width = self.master.winfo_screenwidth()
        self.screen_height = self.master.winfo_screenheight()

        self.canvas_width = self.screen_width / 2
        #self.canvas_width =  master.winfo_width() 
        self.canvas_height = self.screen_height / 2
        self.colmax = self.canvas_width
        self.buttonheight = int(self.screen_height / 500 )
        self.buttonwidth = int(self.screen_width/ 200 )
        self.scalelength = int(self.screen_height / 4 )

        self.Row0 = Row0Init(master,fc)
        self.Row1 = Row1Init(master,fc)
        #self.fm =FormMobile(master,fc)
        
    def genCallBacks(self):
        self.fc.createCallbacks()








