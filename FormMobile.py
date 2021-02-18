import tkinter as tk
from tkinter import font as tkFont
from tkinter.ttk import *
import FormCommand 
import FormCallbacks
RowMobile = None

class FormMobile(tk.Frame):
    """description of class"""

    master = None
    fc = None
    interface = None
    buttonlist = []


    servercommand=(
    "INIT",
    "CALIBRATE",
#    "TO10",
    "PIEP",
    "STOP",
    # "TEST1",
    # "TEST20",
    "TEST80",
    # "TEST200",
    
    "FULLSCAN",
    "QUICKSCAN",
    #"SHOW",
    "SAVE_FILE",
    "LOAD_FILE",
    "S30x70",
    #"ADJUST",
    #"MUP",
    #"MDOWN",
    "MESH",
    "QUIT"
    )

    

    def __init__(self,master):
        global RowMobile

        super().__init__(master)

        self.fc = FormCommand.FormCommand(master)

        self.screen_width = self.master.winfo_screenwidth()
        self.screen_height = self.master.winfo_screenheight()
        self.scalelength = int(self.screen_height / 5.0 )


        self.canvas_width = self.screen_width / 2
        #self.canvas_width =  master.winfo_width() 
        self.canvas_height = self.screen_height / 2
        self.colmax = self.canvas_width
        self.buttonheight = int(self.screen_height / 150 )
        self.buttonwidth = int(self.screen_width/ 60 )
        self.scalelength = int(self.screen_height / 2 )


        self.master = master
        RowMobile = tk.Frame(master)
        RowMobile.grid(row = 0 ,column = 0,sticky=tk.NSEW,columnspan = 12)
        self.createButtons()
        self.createStatusLine()

    def createButtons(self):
            global RowMobile

            counter = 0
            s = self.servercommand
            bheight = self.buttonheight
            bwidth = self.buttonwidth
            labelframe = tk.LabelFrame(RowMobile, text="Commands", relief = tk.RAISED)
            labelframe.grid(row = 0 ,column = 0,sticky=tk.W,columnspan = 5, padx = 10,rowspan = 4,pady = 5)
            #labelframe.pack(fill=tk.BOTH, expand=tk.YES)
            for c in s:
                boldFont = tkFont.Font (size = 12, weight = "bold")
                bt=tk.Button(labelframe,underline=0, font = boldFont)
                if c in ["INIT",  "QUIT","LOAD_FILE"]:#,"S30x70"]:
                    bt["state"] = tk.NORMAL
                    bt["bg"] = "lightgrey"
                else:                    
                    bt["state"] = tk.DISABLED
                bt["text"]=c
                if (c == "INIT"):
                    bt["bg"] = "red"
                bt["bd"]=5
                #bt["command"] = lambda par=c:interpreter(par)
                bt.config(height = bheight, width= bwidth)
                l = len(s) / 3
            
                #if c == "ADJUST":
                 #   bt.bind("<ButtonPress>", on_press)
                    #bt.bind("<ButtonRelease>", on_release)
            

                bt.grid(row=int(counter/l),column=int(counter%l), ipadx = 10, ipady=10, padx = 5, pady=10)
                self.fc.addWidget(bt,c,None)
                self.buttonlist.append(bt)

                counter=counter+1

            # scrollfram = tk.LabelFrame(RowMobile, text="Scale", relief = tk.RAISED)
            # scrollfram.grid(row = 0 ,column = 6,sticky=tk.E,columnspan = 6, padx = 10,rowspan = 4,pady = 5) 
            # lbl = tk.Label(scrollfram,text="VSteps : ")
            # lbl.grid(row = 0,column = 1,sticky=tk.W, ipadx = 5, ipady=5)

            # lbl = tk.Label(scrollfram,text="HSteps : ")
            # lbl.grid(row = 0,column = 0,sticky=tk.W, ipadx = 5, ipady=5)


            # MINDEGREE = 0.225
            # hentry = tk.Scale(scrollfram,   from_=10.1, to=0,resolution = MINDEGREE,bg = "cyan", length =  self.scalelength,digits =  5, width =45)
            # hentry.grid(row = 1,column = 0,sticky=tk.W , ipadx = 2, ipady=2,rowspan = 5)
            # self.fc.addWidget(hentry,"HSCALE",1)


            # ventry = tk.Scale(scrollfram,   from_=10.1, to=0,resolution = MINDEGREE,bg = "brown", length =  self.scalelength ,digits = 5, width =45)
            # ventry.grid(row = 1,column = 1,sticky=tk.W , ipadx = 2, ipady=2,rowspan = 5)
            # self.fc.addWidget(ventry,"VSCALE",1)


    def createStatusLine(self):
            global RowMobile
            
            labelframe = tk.LabelFrame(RowMobile, relief = tk.RAISED)
            labelframe.grid(row = 5 ,column = 0,sticky=tk.NSEW,columnspan = 10, padx = 10,rowspan = 1,pady = 5)
            clientlabel =tk.Label(labelframe,text="Disconnected",font=("Helvetica", 12), width = 18)
            clientlabel["fg"] = "blue"
            clientlabel.grid(row = 0,column = 0,sticky=tk.W,columnspan = 2)
            self.fc.addWidget(clientlabel,"CLIENTLABEL",0)
            progressbar = Progressbar(labelframe, orient = tk.HORIZONTAL, length = 200, mode = 'determinate') 
            self.fc.addWidget(progressbar,"PROGRESSBAR",0)
            progressbar.grid(row=0,column = 3,sticky=tk.E,columnspan = 3,padx =1,ipadx =1)

            clientlabel =tk.Label(labelframe,text="TIME",font=("Helvetica", 12), width = 18)
            clientlabel["fg"] = "blue"
            clientlabel.grid(row = 1,column = 4,sticky=tk.S,columnspan = 2)
            self.fc.addWidget(clientlabel,"TIME",0)

            clientlabel =tk.Label(labelframe,text="PASS",font=("Helvetica", 12), width = 18)
            clientlabel["fg"] = "blue"
            clientlabel.grid(row = 1,column = 0,sticky=tk.S,columnspan = 3)
            self.fc.addWidget(clientlabel,"PASS",0)

            clientlabel =tk.Label(labelframe,text="TOTALTIME",font=("Helvetica", 12), width = 18)
            clientlabel["fg"] = "blue"
            clientlabel.grid(row = 1,column = 7,sticky=tk.S,columnspan = 2)
            self.fc.addWidget(clientlabel,"TOTALTIME",0)


            clientlabel =tk.Label(labelframe,text="STATUS 1",font=("Helvetica", 12), width = 18)
            clientlabel["fg"] = "blue"
            clientlabel["bg"] = "red"
            clientlabel.grid(row = 0,column = 6,sticky=tk.W,columnspan = 1)
            self.fc.addWidget(clientlabel,"STATUS1",0)
            
            clientlabel =tk.Label(labelframe,text="STATUS 2",font=("Helvetica", 12), width = 18)
            clientlabel["fg"] = "blue"
            clientlabel["bg"] = "red"

            clientlabel.grid(row = 0,column = 7,sticky=tk.W,columnspan = 1)
            self.fc.addWidget(clientlabel,"STATUS2",0)

            clientlabel =tk.Label(labelframe,text="MOTOR 1",font=("Helvetica", 12), width = 18)
            clientlabel["fg"] = "blue"
            clientlabel.grid(row = 0,column = 8,sticky=tk.W,columnspan = 1)
            self.fc.addWidget(clientlabel,"MOTOR1",0)
            
            clientlabel =tk.Label(labelframe,text="MOTOR 2",font=("Helvetica", 12), width = 18)
            clientlabel["fg"] = "blue"
            clientlabel.grid(row = 0,column = 9,sticky=tk.W,columnspan = 1)
            self.fc.addWidget(clientlabel,"MOTOR2",0)


            clientlabel =tk.Label(labelframe,text="MOTOR 3",font=("Helvetica", 12), width = 18)
            clientlabel["fg"] = "blue"
            clientlabel.grid(row = 0,column = 10,sticky=tk.W,columnspan = 1)
            self.fc.addWidget(clientlabel,"MOTOR3",0)


        
    def genCallBacks(self):
        self.fc.createCallbacks()

    @classmethod
    def enableButtons(self,toenable,isscanning = False):
        scanset = ["S30x70", "FULLSCAN", "QUICKSCAN","CALIBRATE", "FULLSCAN","TEST80"]
        for bt in self.buttonlist:
                if toenable:
                    bt["state"] = tk.NORMAL
                    bt["bg"] = "lightgrey"
                    if bt["text"] == "INIT":
                        bt["bg"] = "darkgrey"
                        bt["state"] = tk.DISABLED
                    elif (isscanning):
                        if bt["text"] in scanset:
                            bt["state"] = tk.DISABLED
                            bt["bg"] = "darkgrey"
                        else:
                            bt["state"] = tk.NORMAL
                            bt["bg"] = "lightgrey"

                else:
                    if bt["text"] == "INIT":
                        bt["bg"] = "red"
                    if bt["text"] in ["INIT",  "QUIT","LOAD_FILE"]:
                            bt["state"] = tk.NORMAL
                    else:                    
                        bt["state"] = tk.DISABLED






