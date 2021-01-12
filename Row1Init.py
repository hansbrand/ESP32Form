import tkinter as tk
import tkinter.ttk as ttk
import FormCommand 
import FormWidgetCallbacks

Row1Frame = None

class Row1Init(tk.Frame):

    master = None
    fc = None
    

    def __init__(self,master,fc):
        global Row1Frame
        super().__init__(master)
        self.fc = fc

        self.screen_width = self.master.winfo_screenwidth()
        self.screen_height = self.master.winfo_screenheight()
        self.scalelength = int(self.screen_height / 5.0 )


        self.canvas_width = self.screen_width / 2
        #self.canvas_width =  master.winfo_width() 
        self.canvas_height = self.screen_height / 2
        self.colmax = self.canvas_width
        self.buttonheight = int(self.screen_height / 500 )
        self.buttonwidth = int(self.screen_width/ 200 )
        self.scalelength = int(self.screen_height / 6 )


        self.master = master
        Row1Frame = tk.Frame(master)
        Row1Frame.grid(row = 3 ,column = 0,sticky=tk.W,columnspan = 4)
        self.createScanFrame()
        self.createParameterFrame()

    def createScanFrame(self):
        global Row1Frame

        bheight = self.buttonheight
        bwidth = self.buttonwidth

        scanframe = tk.LabelFrame(Row1Frame, text="Scan Limits(Degree)", relief = tk.RAISED)
        scanframe.grid(row = 0,column = 0,sticky=tk.N,ipadx = 10, ipady=10,columnspan = 2);

        lbl = tk.Label(scanframe,text="Start")
        lbl.grid(row = 0,column = 1,sticky=tk.W, ipadx = 30, ipady=10)
        lbl = tk.Label(scanframe,text="End")
        lbl.grid(row = 0,column = 2,sticky=tk.W, ipadx = 30, ipady=10)
        lbl = tk.Label(scanframe,text="Hor.:")
        lbl.grid(row = 1,column = 0,sticky=tk.W, ipadx = 30, ipady=10)
        lbl = tk.Label(scanframe,text="Ver.")
        lbl.grid(row = 2,column = 0,sticky=tk.W, ipadx = 30, ipady=10)

        hstartEntry = tk.Entry(scanframe,justify= tk.RIGHT,bd = 3, width = bwidth)  
        hstartEntry.grid(row = 1,column = 1,sticky=tk.W, ipadx = 30, ipady=10)
        #widgetlist['HStart'][0] = hstartEntry 
        hstartEntry.insert(0, "0")
        #hstartEntry.bind("<FocusIn>", QualEntry_Callback)
        self.fc.addWidget(hstartEntry,"HSTART",None)

        hendEntry = tk.Entry(scanframe,justify= tk.RIGHT,bd = 3, width = bwidth)  
        hendEntry.grid(row = 1,column = 2,sticky=tk.E, ipadx = 30, ipady=10)
        #widgetlist['HEnd'][0] = hendEntry 
        hendEntry.insert(0, "0")
        self.fc.addWidget(hendEntry,"HEND",None)

       # hendEntry.bind("<FocusIn>", QualEntry_Callback)

        vstartEntry = tk.Entry(scanframe,justify= tk.RIGHT,bd = 3, width = bwidth)  
        vstartEntry.grid(row = 2,column = 1,sticky=tk.W, ipadx = 30, ipady=10)
        #widgetlist['VStart'][0] = vstartEntry 
        vstartEntry.insert(0, "0")
        #vstartEntry.bind("<FocusIn>", QualEntry_Callback)
        self.fc.addWidget(vstartEntry,"VSTART",None)

        vendEntry = tk.Entry(scanframe,justify= tk.RIGHT,bd = 3, width = bwidth)
        vendEntry.grid(row = 2,column = 2,sticky=tk.E, ipadx = 30, ipady=10)
        #widgetlist['VStart'][0] = vendEntry 
        vendEntry.insert(0, "0")
        #vendEntry.bind("<FocusIn>", QualEntry_Callback)
        self.fc.addWidget(vendEntry,"VEND",None)

        bt=tk.Button(scanframe)
        bt.config(height = bheight,width=bwidth)
        bt["text"]= "SCAN"
        bt["bd"]=5
        #bt["command"] = lambda : Change_Callback(bt,"Scan")
        bt.grid(row = 0,column = 3,sticky=tk.NSEW, ipadx = 10, ipady=10)
        self.fc.addWidget(bt,"SCAN",None)

        bt=tk.Button(scanframe)
        bt.config(height = bheight,width=bwidth)
        bt["text"]= "INTERRUPT"
        bt["bd"]=5
        bt.grid(row = 1,column = 3,sticky=tk.NSEW, ipadx = 10, ipady=10)
        self.fc.addWidget(bt,"INTERRUPT",None)


        bt=tk.Button(scanframe)
        bt.config(height = bheight,width=bwidth)
        bt["text"]= "RESET"
        bt["bd"]=5
        #bt["command"] = lambda : Change_Callback(bt,"Reset")
        bt.grid(row = 2,column = 3,sticky=tk.NSEW, ipadx = 10, ipady=10)
        self.fc.addWidget(bt,"RESET",None)

        
    def createParameterFrame(self):
        global Row1Frame
        qualStates=[
            ("D","D"),
            ("M","M"),
            ("F","F")
        ]


        bheight = self.buttonheight
        bwidth = self.buttonwidth
        labelframe = tk.LabelFrame(Row1Frame, text="Parameter (Degree)", relief = tk.RAISED)

        labelframe.grid(row = 0,column = 2,sticky=tk.S,ipadx = 5, ipady=10,rowspan = 2,pady= 5);
        #nframe.grid(row = 0,column = 3,sticky=tk.S,ipadx = 5, ipady=10,pady= 5);


        lbl = tk.Label(labelframe,text="VSteps : ")
        lbl.grid(row = 0,column = 1,sticky=tk.W, ipadx = 5, ipady=5)

        lbl = tk.Label(labelframe,text="HSteps : ")
        lbl.grid(row = 0,column = 0,sticky=tk.W, ipadx = 5, ipady=5)

        lbl = tk.Label(labelframe,text="Delay : ")
        lbl.grid(row = 0,column = 2,sticky=tk.W, ipadx = 5, ipady=5)

        MINDEGREE = 0.225
        #hentry = tk.Scale(labelframe,   from_=5, to=0,resolution = 0.1,bg = "cyan", length = scalesize , command= lambda w = hentry: modifyScale2(w))
        hentry = tk.Scale(labelframe,   from_=10.1, to=0,resolution = MINDEGREE,bg = "cyan", length =  self.scalelength,digits =  5)
        #hentry["command"] = (lambda w = hentry: callme(w))
        hentry.grid(row = 1,column = 0,sticky=tk.W , ipadx = 2, ipady=2,rowspan = 5)
        self.fc.addWidget(hentry,"HSCALE",1)

        #widgetlist['HSteps'][0] = hentry 
        #hentry.set(1)
        #paramlist['HSteps'] = '1'

        ventry = tk.Scale(labelframe,   from_=10.1, to=0,resolution = MINDEGREE,bg = "brown", length =  self.scalelength ,digits = 5)
        ventry.grid(row = 1,column = 1,sticky=tk.W , ipadx = 2, ipady=2,rowspan = 5)
        self.fc.addWidget(ventry,"VSCALE",1)
        #widgetlist['VSteps'][0] = ventry 
        #ventry.set(0)
        #paramlist['VSteps'] = '0'

        delayEntry = tk.Scale(labelframe,   from_=20, to=0,resolution = 1,bg = "lightblue", length =  self.scalelength )
        delayEntry.grid(row = 1,column = 2,sticky=tk.W , ipadx = 2, ipady=2,rowspan = 5)
        self.fc.addWidget(delayEntry,"TIMESCALE",1)
        labelframe.update()
        #widgetlist['Delay'][0] = delayEntry 
        #delayEntry.set(1)
        #paramlist['Delay'] = '1'

#        delayEntry = None
#qualentry = None


        quframe = tk.LabelFrame(labelframe,text="Scan Quality: ")
        quframe.grid(row = 4,column = 3,sticky=tk.W, ipadx = 5, ipady=5,rowspan = 2)

        quv = tk.StringVar(quframe,"D")
        FormCommand.radioMap[quframe] = quv

        i = 0
        rblist = []
        for val,mode in qualStates :
            rb = tk.Radiobutton(quframe, 
                        text=val,
                        padx = 5, 
                        pady= 3,
                        variable = quv, 
                        #command= lambda : Change_Callback(rb,mode),
                        font = 'helvetica 8',
                        value = mode)
            rb.grid(row = 0,column = i)
            self.fc.addWidget(rb,mode,quv)

            i = i+1
        quframe.update()
        #rblist[0].select()
        #dheight = rbFrame.winfo_height()
        #paramlist['Quality'] = 'D'



        #hentry.bind("<FocusOut>", lambda : Change_Callback(hentry))
        #ventry.bind("<FocusOut>", lambda : Change_Callback(hentry) )

        # checkbuttons
        CheckVarV = tk.IntVar(labelframe,0)
        CheckVarV2 = tk.IntVar(labelframe,0)
        CheckVarV3 = tk.IntVar(labelframe,0)
        CheckVarV4 = tk.IntVar(labelframe,0)

        icbx=tk.Checkbutton(labelframe,text="Use Strategy?",padx = 10,command= lambda : Change_Callback(icbx,"Use Strategy"), onvalue = 1, offvalue = 0,variable = CheckVarV)
        icbx.var = CheckVarV
        icbx.grid(row =0,column = 3,sticky=tk.W)
        #paramlist["Use Strategy"] = '0'

        icbx.deselect()


        scbx=tk.Checkbutton(labelframe,text="Save Data?", padx = 10,command= lambda : Change_Callback(scbx,"Save Data?"), onvalue = 1, offvalue = 0,variable = CheckVarV3)
        #widgetlist['Virtual 3D'][0] = cbx 
        scbx.var = CheckVarV3
        scbx.grid(row =2,column = 3,sticky=tk.W,pady = 10)
        #paramlist["Save Data?"] = '1'
        scbx.select()
        logging = True
        


        nframe = tk.LabelFrame(Row1Frame, text="Signal Quality", relief = tk.RAISED)
        nframe.grid(row = 0,column = 3,sticky=tk.S,ipadx = 5, ipady=10,pady= 5,rowspan = 2);
        gscale = tk.Scale(nframe,   from_=2000, to=0,bg = "green", length = self.scalelength)# , command= modifyScale)
        gscale.grid(row = 0,column = 0,sticky=tk.W , ipadx = 2, ipady=2)
        self.fc.addWidget(gscale,"GREENSCALE",200)
        gscale.update()
        #gscale.set(DataPool.GREENLIMIT)
        yscale = tk.Scale(nframe,   from_=2000, to=0,bg = "yellow", length = self.scalelength)# , command= modifyScale)
        yscale.grid(row = 0,column = 1,sticky=tk.W , ipadx = 2, ipady=2)
        self.fc.addWidget(yscale,"YELLOWSCALE",400)
        yscale.update()
        #yscale.set(DataPool.YELLOWVALUE)
        rscale = tk.Scale(nframe,   from_=2000, to=0,bg = "red", length = self.scalelength)# , command= modifyScale)
        rscale.grid(row = 0,column = 2,sticky=tk.W , ipadx = 2, ipady=2)
        self.fc.addWidget(rscale,"REDSCALE",500)
        #rscale.set(DataPool.REDLIMIT)
        lscale = tk.Scale(nframe,   from_=5000, to=0,bg = "white", length = self.scalelength)# , command= modifyScale)
        lscale.grid(row = 0,column = 3,sticky=tk.W , ipadx = 2, ipady=2)
        self.fc.addWidget(lscale,"WHITESCALE",500)
        #lscale.set(DataPool.IPLIMIT)


        CheckVarC = tk.IntVar(nframe,1)

        #colcbx=tk.Checkbutton(nframe,text="Colored ?",padx = 10,command=lambda : Change_Callback(colcbx,"Colored"), 
        #                      onvalue = 1, offvalue = 0,variable = CheckVarC)
        colcbx=tk.Checkbutton(nframe,text="Colored ?",padx = 10, 
                              onvalue = 1, offvalue = 0,variable = CheckVarC)
        #widgetlist['Ignoresteps'][0] = cbx 
        colcbx.var = CheckVarC
        colcbx.grid(row =0,column = 4,sticky=tk.W)
        #paramlist['Colored'] = 1
        #isColored = True
        colcbx.select()
        nframe.update()

        #setCurrentSteps()

    @classmethod
    def modifyScale2(self, widget):
        global hentry
        global ventry
        global delayEntry

        h=FormCommand.FormCommand.getWidgetByName("HSCALE")
        v=FormCommand.FormCommand.getWidgetByName("VSCALE")
        d=FormCommand.FormCommand.getWidgetByName("TIMESCALE")
        h = hentry.get()
        v = ventry.get()
        d = delayEntry.get()

