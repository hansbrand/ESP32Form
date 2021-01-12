import tkinter as tk
from tkinter.ttk import *
from tempGraph import tempGraph
import FormCommand 
import FormCallbacks
from USBCommunicator import USBCommunicator

Row0Frame = None
progressbar = None
diagVar = None

class Row0Init(tk.Frame):
    canvasStates=[
    ("F5 Error List","F5"),
    ("F6 Lines","F6"),
    ("F7 Radar","F7"),
    ("F8 3D","F8")
    ]

    servercommand=(
    "INIT",
    "CALIBRATE",
    "STOP",
    "RESUME",
    "FULLSCAN",
    "SAVE_FILE",
    "LOAD_FILE",
    "CLEAR",
    "ADJUST",
    "QUIT"
    )

    master = None
    fc = None
    

    def __init__(self,master,fc):
        global Row0Frame
        global progressbar


        super().__init__(master)
        self.fc = fc

        self.screen_width = self.master.winfo_screenwidth()
        self.screen_height = self.master.winfo_screenheight()

        self.canvas_width = self.screen_width / 2
        #self.canvas_width =  master.winfo_width() 
        self.canvas_height = self.screen_height / 2
        self.colmax = self.canvas_width
        self.buttonheight = int(self.screen_height / 500 )
        self.buttonwidth = int(self.screen_width/ 200 )
        self.scalelength = int(self.screen_height / 4 )


        self.master = master
        Row0Frame = tk.Frame(master)
        Row0Frame.grid(row = 0 ,column = 0,sticky=tk.N,ipady = 5,ipadx = 10)
        self.createValLabel()
        self.createLaserStatus()
        self.createConnectionMode()
        self.createCanvasBox()
        self.createButtons()


    def createConnectionMode(self):
        buttonframe = tk.LabelFrame(Row0Frame, text="Connection", relief = tk.RAISED)
        buttonframe.grid(row = 0,column = 2,sticky=tk.N, rowspan = 2,padx=10,pady=5,ipady=10);


        rb = tk.Radiobutton(buttonframe, 
                    text="WLAN",
                    padx = 20, 
                    indicatoron = 1,
                    pady=2,
                    #variable = btn1 if (i == 1) else btn2, 
                    variable = FormCallbacks.checkButtonval,
#                    command= lambda : pm.Change_Callback(rb, val),
                    state = tk.DISABLED,
                    font = 'helvetica 10',
                    value = "WLAN"
                    )

        rb.grid(row = 0,column = 0,sticky=tk.W, ipadx = 10, ipady=10, padx = 5, pady=5)
        
        self.fc.addWidget(rb,"WLAN",0)

        rb = tk.Radiobutton(buttonframe, 
                    text="USB",
                    padx = 20, 
                    indicatoron = 1,
                    pady=2,
                    #variable = btn1 if (i == 1) else btn2, 
                    variable = FormCallbacks.checkButtonval,
#                    command= lambda : pm.Change_Callback(rb, val),
                    font = 'helvetica 10',
                    value = "USB"
                    )
        #rb.set("USB")

        rb.grid(row = 1,column = 0,sticky=tk.W, ipadx = 10, ipady=10, padx = 5, pady=5)
        self.fc.addWidget(rb,"USB",0)

        print(USBCommunicator.COMPortList)
        listbox = tk.Spinbox(buttonframe,values = USBCommunicator.COMPortList,state = "readonly")
        #listbox.insert(0, "a list entry")
        #counter = 0;
        #for item in ["one", "two", "three", "four"]:
        #    counter += 1
        #    listbox.insert(counter, item)
        listbox.grid(row = 1,column = 1,sticky=tk.E, ipadx = 10, ipady=10, padx = 5, pady=5)
        self.fc.addWidget(listbox,"COMPortList",USBCommunicator.COMPortList)

        #listbox1 = tk.Spinbox(buttonframe, from_=0, to=10 )

        ##for item in ["one", "two", "three", "four"]:
        ##    listbox1.insert(tk.END, item)
        #listbox1.grid(row = 0,column = 1,sticky=tk.E, ipadx = 10, ipady=10, padx = 5, pady=5)


    def createValLabel(self):
            global Row0Frame
            global progressbar

            lframe = tk.LabelFrame(Row0Frame, text = "Info", relief = tk.RAISED)
            #lframe.grid(row = 0 ,column = 0,sticky=tk.N,columnspan = 1, rowspan = 1,pady = 5,padx = 5,ipadx = 10, ipady = 10)
            lframe.grid(row = 0 ,column = 0,sticky=tk.NW,ipadx = 1, ipady=1, rowspan = 1,padx=5,columnspan = 2)
            flabel =tk.Label(lframe,text="Client:")
            flabel.grid(row=0,column = 0,sticky=tk.NW, pady = 10)
            clientlabel =tk.Label(lframe,text="Disconnected",font=("Helvetica", 12), width = 18)
            clientlabel["fg"] = "blue"
            clientlabel.grid(row = 0,column = 1,sticky=tk.E)
            self.fc.addWidget(clientlabel,"CLIENTLABEL",0)
            vallabel =tk.Label(lframe,text="Loop Time:")
            vallabel.grid(row=2,column = 0,sticky=tk.NW, padx = 1)
            slabel =tk.Label(lframe,text="MAX \nLoop Time :")
            slabel.grid(row=3,column = 0,sticky=tk.NE, padx = 1)
            mlabel =tk.Label(lframe,text="",fg="red")
            mlabel.grid(row=2,column = 1,sticky=tk.NE, padx = 20)
            maxval=tk.Label(lframe,text="0")
            maxval.grid(row=3,column = 1,sticky=tk.NE, padx = 20)
            flabel =tk.Label(lframe,text="Status:")
            flabel.grid(row=1,column = 0,sticky=tk.NW)
            filelabel =tk.Label(lframe,text="Filestatus",font=("Helvetica", 12))
            filelabel["fg"] = "violet"
            filelabel.grid(row = 1,column = 1, padx = 10,sticky=tk.E)
            #iplabel =tk.Label(master,text=str(tcpserver.myip),font=("Helvetica", 16))
            #iplabel["fg"] = "green"
            xlabel =tk.Label(lframe,text="Progress:")
            xlabel.grid(row=4,column = 1,sticky=tk.NW,columnspan = 4)
            progressbar = Progressbar(lframe, orient = tk.HORIZONTAL, 
                  length = 100, mode = 'determinate') 
            self.fc.addWidget(progressbar,"PROGRESSBAR",0)
            progressbar.grid(row=5,column = 0,sticky=tk.NSEW,columnspan = 4,padx =1,ipadx =1)

            #iplabel.grid(row = 3,column = 4, sticky=tk.E)



    def createLaserStatus(self):
        lsFrame =tk.LabelFrame(Row0Frame,text = "Laser Status", relief = tk.RAISED)   
        lsFrame.grid(row = 0,column = 4,sticky=tk.NE,ipadx = 1, ipady=1,  padx= 10,columnspan = 3,rowspan = 2)

        laser1label = tk.Label(lsFrame,text="Laser 1",font=("Helvetica", 10), fg = "blue")
        laser1label.grid(row=0,column = 0, ipadx = 5, ipady=3,sticky=tk.W)
        laser1message = tk.Label(lsFrame,text="Laser 1",font=("Helvetica", 8))
        laser1message.grid(row=1,column = 0, ipadx = 5, ipady=3,sticky=tk.W)
        laser1time = tk.Label(lsFrame,text="Laser 1",font=("Helvetica", 8))
        laser1time.grid(row=2,column = 0, ipadx = 5, pady=3,sticky=tk.W)


        laser2label = tk.Label(lsFrame,text="Laser 2",font=("Helvetica", 10),fg = "magenta")
        laser2label.grid(row=0,column = 1, ipadx = 5, ipady=5,sticky=tk.W)
        laser2message = tk.Label(lsFrame,text="Laser 2",font=("Helvetica", 8))
        laser2message.grid(row=1,column = 1, ipadx = 10, ipady=10,sticky=tk.W)
        laser2time = tk.Label(lsFrame,text="Laser 2",font=("Helvetica", 8))
        laser2time.grid(row=2,column = 1, ipadx = 10, ipady=3,sticky=tk.W)

        laserhistory = tk.Frame(lsFrame, width=320, height=300, background="lightgreen")
        laserhistory.grid(row = 3 ,column = 0,sticky=tk.S,pady=30,ipady = 20,columnspan = 2)

        tgraph = tempGraph(laserhistory)
        self.fc.addWidget(tgraph,"TEMPGRAPH",0)


    
    def createCanvasBox(self):
            global Row0Frame
            global bif
            global diagVar

            rbFrame =tk.LabelFrame(Row0Frame,text = "Diagramm", relief = tk.RAISED)   
            rbFrame.grid(row = 0,column = 7,sticky=tk.NE,ipadx = 10, ipady=5, rowspan = 3,padx=20)

        
            #s = canvasStates[1][0]
            i = 0
            rblist = []
            diagVar = tk.StringVar()
            FormCommand.radioMap[rbFrame] = diagVar
            diagVar.set("F5")
            for val,mode in self.canvasStates :
                rb = tk.Radiobutton(rbFrame, 
                            text=val,
                            padx = 5, 
                            pady= 10,
                            variable = diagVar, 
                            #command=canvasChoice,
                            font = 'helvetica 10',
                            value = mode)
                #rbFrame.bind("<" + mode + ">",keyChoice)
                #rbFrame.bind(mode,canvasChoice)
                rb.grid(row = int((i % 2)),column = int(i / 2), ipadx = 10, ipady=10)
                self.fc.addWidget(rb,mode,diagVar)

                rblist.append(rb)
                i = i+1
            #ma.bind('<Key>', lambda a : keyChoice(a))
            rbFrame.update()
            dheight = rbFrame.winfo_height()


            #rb1Frame =tk.LabelFrame(Row0Frame, relief = tk.RAISED)   
        
            #rb1Frame.grid(row = 0,column = 0,sticky=tk.NSEW,ipadx = 10, ipady=10, padx = 5, pady=10)

            bif=tk.Button(rbFrame)
            bif["text"]="SHOW"
            bif["bd"]=5
            #bif["command"] = lambda par="SHOW":interpreter(par)
            bif.grid(row=2,column=0, sticky=tk.N,ipadx = 10, ipady=10, padx = 5, pady=10 , columnspan  = 2)

            h = int( dheight * 0.8)
            w= int(h * 4.0/ 3.0)
            buttonheight = int(self.screen_height / 500 )
            buttonwidth = int(self.screen_width/ 200 )


            bif.config(height = buttonheight, width= buttonwidth)
            self.fc.addWidget(bif,'SHOW',None)


    def createButtons(self):
            global Row0Frame

            counter = 0
            s = self.servercommand
            bheight = self.buttonheight
            bwidth = self.buttonwidth
            labelframe = tk.LabelFrame(Row0Frame, text="Commands", relief = tk.RAISED)
            labelframe.grid(row = 1 ,column = 0,sticky=tk.NW,columnspan = 3, padx = 10,rowspan = 1,pady = 5)
            #labelframe.pack(fill=tk.BOTH, expand=tk.YES)

            for c in s:
                bt=tk.Button(labelframe,underline=0)
                bt["text"]=c
                bt["bd"]=5
                #bt["command"] = lambda par=c:interpreter(par)
                bt.config(height = bheight, width= bwidth)
                l = len(s) / 2
            
                #if c == "ADJUST":
                 #   bt.bind("<ButtonPress>", on_press)
                    #bt.bind("<ButtonRelease>", on_release)
            

                bt.grid(row=int(counter/l),column=int(counter%l), ipadx = 10, ipady=10, padx = 5, pady=10)
                self.fc.addWidget(bt,c,None)

                counter=counter+1



