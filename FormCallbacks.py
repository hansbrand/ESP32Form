import os
from time import sleep
import USBCommunicator
import ESPDevices
import FormCommand
import FileManager
import USBCommunicator
import TCPCommunicator
import ESP32Form
import DataContainer as  DC
import ScanStrategy as SS
from FormMobile import FormMobile 

checkButtonval = None
CALPOS = 170.0
CALDELTA = .2
initpressed = False

class FormCallbacks(object):
    com = None
    classname = ""
    """description of class"""
    def __init__(self, classname):
        self.classname = classname

        pass

    @classmethod
    def cbdefault(self , button):
        print("cbdefault  ")

    @classmethod
    def callbackINIT(self,button):
        global initpressed
        print("callbackINIT")
        #button["bg"] ="green"
        if (self.classname == "USBCommunicator"):
             self.com =  __import__("USBCommunicator")
        else:
             self.com =  __import__("TCPCommunicator")
        #ESPDevices.initDevices()
        #ESPDevices.genSimpleCommands(False)
        #self.com.startserverThread()
        DC.initDataContainer()
        self.com.addCommand(ESPDevices.calibrateCommand() )
        self.com.addCommand(ESPDevices.Sensor1.openCommand())
        self.com.addCommand(ESPDevices.Sensor2.openCommand())
        initpressed = True
        #self.com.addCommand(ESPDevices.Sensor1.statusCommand())
        #self.com.addCommand(ESPDevices.Sensor2.statusCommand())
        
        #self.com.addCommand(ESPDevices.turnCommand("M3",CALPOS) )

    @classmethod
    def callbackCALIBRATE(self , button):
        print("callbackCALIBRATE")
        FormMobile.enableButtons(True,True)

        if (self.classname == "USBCommunicator"):
             self.com =  __import__("USBCommunicator")
        else:
             self.com =  __import__("TCPCommunicator")

        self.com.addCommand(ESPDevices.calibrateCommand() )

    @classmethod
    def callbackADJUST(self , button):
        print("callbackADJUST")
        if (self.classname == "USBCommunicator"):
             self.com =  __import__("USBCommunicator")
        else:
             self.com =  __import__("TCPCommunicator")

        self.com.addCommand(ESPDevices.adjustCommand() )



    @classmethod
    def callbackSTOP(self , button):
        print("callbackSTOP")
        TCPCommunicator.emergeny()
        initpressed = False
        FormMobile.enableButtons(False)


    @classmethod
    def callbackRESUME(self , button):
        print("callbackRESUME")

    @classmethod
    def callbackTO10(self , button):
        print("callbackTO10")
        self.com.addCommand(ESPDevices.turnCommand("M2",10) )
        self.com.addCommand(ESPDevices.turnCommand("M3",10) )


    @classmethod
    def callbackTO2(self , button):
        print("callbackTO2")
        self.com.addCommand(ESPDevices.turnCommand("M2",10) )
        self.com.addCommand(ESPDevices.turnCommand("M3",10) )


    @classmethod
    def callbackMUP(self , button):
        global CALPOS
        global CALDELTA
        print("callbackMUP")
        CALPOS -= CALDELTA
        sbar = FormCommand.FormCommand.getWidgetByName("STATUS1")
        sbar["text"] =str(CALPOS)
        self.com.addCommand(ESPDevices.turnCommand("M2",CALPOS) )
        self.com.addCommand(ESPDevices.turnCommand("M3",CALPOS) )



    @classmethod
    def callbackMDOWN(self , button):
        global CALPOS
        global CALDELTA
        print("callbackMDOWN")
        CALPOS += 1
        print(CALPOS)
        sbar = FormCommand.FormCommand.getWidgetByName("STATUS1")
        sbar["text"] = str(CALPOS)
        self.com.addCommand(ESPDevices.turnCommand("M2",CALPOS) )
        self.com.addCommand(ESPDevices.turnCommand("M3",CALPOS) )

    @classmethod
    def callbackPIEP(self , button):
        print("callbackPIEP")
        self.com.addCommand(ESPDevices.piepCommand("S1") )
        self.com.addCommand(ESPDevices.piepCommand("S2"))

    @classmethod
    def callbackFULLSCAN(self , button):
        print("callbackFULLSCAN")
        FormMobile.enableButtons(False,True)

        if (self.classname == "USBCommunicator"):
             self.com =  __import__("USBCommunicator")
        else:
             self.com =  __import__("TCPCommunicator")
        hd = 2
        vd = 5
        clist = ESPDevices.genSimpleCommands(True, hdelta=hd,vdelta =vd)
        self.com.current2send = len(clist)
        self.com.alreadysent = 0

        for s in clist:
            self.com.addCommand(s)
        FormMobile.enableButtons(True, True)
        
        pass


    @classmethod
    def callbackQUICKSCAN(self , button):
        print("callbackQUICK")
        FormMobile.enableButtons(True,True)

        if (self.classname == "USBCommunicator"):
             self.com =  __import__("USBCommunicator")
        else:
             self.com =  __import__("TCPCommunicator")
        # hd = (180.0 / 45.0) - 0.01
        # vd = (160.0 / 10.0) - 0.01
        hd = 5
        vd = 15
        clist = ESPDevices.genSimpleCommands(True, hdelta=hd,vdelta =vd)
        self.com.current2send = len(clist)
        self.com.alreadysent = 0

        for s in clist:
            self.com.addCommand(s)
        FormMobile.enableButtons(True, True)

        pass

    @classmethod
    def callbackTEST1(self , button):
        print("callbackTEST1")
        if (self.classname == "USBCommunicator"):
             self.com =  __import__("USBCommunicator")
        else:
             self.com =  __import__("TCPCommunicator")
        hd = .25
        vd = .25
        clist = ESPDevices.genTestCommands(False, hdelta=hd,vdelta =vd)
        self.com.current2send = len(clist)
        self.com.alreadysent = 0

        for s in clist:
            self.com.addCommand(s)
            print(s)
        pass

    @classmethod
    def callbackTEST20(self , button):
        print("callbackTEST20")
        if (self.classname == "USBCommunicator"):
             self.com =  __import__("USBCommunicator")
        else:
             self.com =  __import__("TCPCommunicator")
        hd = 5.0
        vd = 5.0
        clist = ESPDevices.genTestCommands(False, hdelta=hd,vdelta =vd)
        self.com.current2send = len(clist)
        self.com.alreadysent = 0

        for s in clist:
            self.com.addCommand(s)
            print(s)
        pass

    @classmethod
    def callbackTEST80(self , button):
        print("callbackTEST80")
        FormMobile.enableButtons(True,True)

        if (self.classname == "USBCommunicator"):
             self.com =  __import__("USBCommunicator")
        else:
             self.com =  __import__("TCPCommunicator")
        hd = 20.0
        vd = 20.0
        clist = ESPDevices.genTestCommands(False, hdelta=hd,vdelta =vd)
        self.com.current2send = len(clist)
        self.com.alreadysent = 0

        for s in clist:
            self.com.addCommand(s)
            print(s)
        pass



    @classmethod
    def callbackHORIZONTAL(self , button):
        print("callbackHORIZONTAL")
        FormMobile.enableButtons(True,True)

        if (self.classname == "USBCommunicator"):
             self.com =  __import__("USBCommunicator")
        else:
             self.com =  __import__("TCPCommunicator")
        hd = 20.0
        vd = 20.0
        clist = ESPDevices.genHorizontalCommands(False, hdelta=hd,vdelta =vd)
        self.com.current2send = len(clist)
        self.com.alreadysent = 0

        for s in clist:
            self.com.addCommand(s)
            print(s)
        pass



    @classmethod
    def callbackTEST200(self , button):
        print("callbackTEST200")
        if (self.classname == "USBCommunicator"):
             self.com =  __import__("USBCommunicator")
        else:
             self.com =  __import__("TCPCommunicator")
        hd = 50.0
        vd = 50.0
        clist = ESPDevices.genTestCommands(True, hdelta=hd,vdelta =vd)
        self.com.current2send = len(clist)
        self.com.alreadysent = 0

        for s in clist:
            self.com.addCommand(s)
            print(s)
        pass




    @classmethod
    def callbackSAVE_FILE(self , button):
        print("callbackSAVE_FILE")
        if (self.classname == "USBCommunicator"):
             self.com =  __import__("USBCommunicator")
        else:
             self.com =  __import__("TCPCommunicator")
        FileManager.saveCSVlist(self.com.receiveList, "RAW")
        self.com.receiveList = []

    @classmethod
    def callbackLOAD_FILE(self , button):
        print("callbackLOAD_FILE")
        DC.initDataContainer()

        FileManager.openLoadFile(self)

    @classmethod
    def callbackCLEAR(self , button):
        print("callbackCLEAR")


    @classmethod
    def callbackQUIT(self , button):
        print("callbackQUIT")

        sleep(2000)
        ESP32Form.Application.cleanup()
        #button.master.master.master.destroy()
        os._exit( 0 )

    @classmethod
    def callbackSCAN(self , button):
        print("callbackSCAN")
        if (self.classname == "USBCommunicator"):
             self.com =  __import__("USBCommunicator")
        else:
             self.com =  __import__("TCPCommunicator")
        hfrom = float(FormCommand.FormCommand.getWidgetByName("HSTART").get())
        hto = float(FormCommand.FormCommand.getWidgetByName("HEND").get())
        vfrom = float(FormCommand.FormCommand.getWidgetByName("VSTART").get())
        vto = float(FormCommand.FormCommand.getWidgetByName("VEND").get())
        hdelta = float(FormCommand.FormCommand.getWidgetByName("HSCALE").get())
        vdelta = float(FormCommand.FormCommand.getWidgetByName("VSCALE").get())
        
        clist = ESPDevices.genSimpleCommands(True, hfrom, hto, vfrom, vto, hdelta, vdelta)
        self.com.current2send = len(clist)
        self.com.alreadysent = 0
        for s in clist:
            self.com.addCommand(s)
        FormMobile.enableButtons(False, True)




    @classmethod
    def callbackINTERRUPT(self , button):
        print("callbackINTERRUPT")

    @classmethod
    def callbackRESET(self , button):
        print("callbackRESET")

    @classmethod
    def callbackSHOW(self , button):
        print("callbackSHOW")
        ESP32Form.Application.setshow3D()


    @classmethod
    def callbackS30x70(self , button):
        print("callbackS30x70")
        FormMobile.enableButtons(True, True)
        if (self.classname == "USBCommunicator"):
             self.com =  __import__("USBCommunicator")
        else:
             self.com =  __import__("TCPCommunicator")
        targetwidth = 0.05
        targetheight = 0.05
        maxturns = 1000
        minwidth = 0.4
        minheight = 0.04
        DC.initDataContainer()

        SS.startScan(targetwidth, targetheight, maxturns, self.com, minwidth, minheight, "DETAIL")
        pass

    @classmethod
    def callbackEDGES(self , button):
        print("callbackEDGES")
        FormMobile.enableButtons(True, True)
        if (self.classname == "USBCommunicator"):
             self.com =  __import__("USBCommunicator")
        else:
             self.com =  __import__("TCPCommunicator")
        targetwidth = 0.05
        targetheight = 0.05
        maxturns = 1000
        minwidth = 0.05
        minheight = 0.05
        DC.initDataContainer()

        SS.startScan(targetwidth, targetheight, maxturns, self.com, minwidth, minheight,'EDGE')
        pass



    @classmethod
    def callbackMESH(self , button):
        print("callbackLOAD_FILE")
        DC.initDataContainer()

        FileManager.openMeshFile(self)

        print("callbackMESH")
        return
