import os
from time import sleep
import USBCommunicator
import ESPDevices
import FormCommand
import FileManager
import USBCommunicator
import TCPCommunicator
import ESP32Form

checkButtonval = None
CALPOS = 90.0
CALDELTA = .225

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
        print("callbackINIT")
        if (self.classname == "USBCommunicator"):
             self.com =  __import__("USBCommunicator")
        else:
             self.com =  __import__("TCPCommunicator")
        #ESPDevices.initDevices()
        #ESPDevices.genSimpleCommands(False)
        #self.com.startserverThread()
        self.com.addCommand(ESPDevices.calibrateCommand() )
        self.com.addCommand(ESPDevices.Sensor1.openCommand())
        self.com.addCommand(ESPDevices.Sensor2.openCommand())
        self.com.addCommand(ESPDevices.Sensor1.statusCommand())
        self.com.addCommand(ESPDevices.Sensor2.statusCommand())


    @classmethod
    def callbackCALIBRATE(self , button):
        print("callbackCALIBRATE")
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

    @classmethod
    def callbackRESUME(self , button):
        print("callbackRESUME")

    @classmethod
    def callbackTO10(self , button):
        print("callbackTO10")
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
        CALPOS += CALDELTA
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
        if (self.classname == "USBCommunicator"):
             self.com =  __import__("USBCommunicator")
        else:
             self.com =  __import__("TCPCommunicator")
        clist = ESPDevices.genSimpleCommands(False)
        self.com.current2send = len(clist)
        self.com.alreadysent = 0

        for s in clist:
            self.com.addCommand(s)

    @classmethod
    def callbackQUICKSCAN(self , button):
        print("callbackQUICK")
        if (self.classname == "USBCommunicator"):
             self.com =  __import__("USBCommunicator")
        else:
             self.com =  __import__("TCPCommunicator")
        # hd = (180.0 / 45.0) - 0.01
        # vd = (160.0 / 10.0) - 0.01
        hd = 1
        vd = 10
        clist = ESPDevices.genSimpleCommands(True, hdelta=hd,vdelta =vd)
        self.com.current2send = len(clist)
        self.com.alreadysent = 0

        for s in clist:
            self.com.addCommand(s)
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



    @classmethod
    def callbackINTERRUPT(self , button):
        print("callbackINTERRUPT")

    @classmethod
    def callbackRESET(self , button):
        print("callbackRESET")

    @classmethod
    def callbackSHOW(self , button):
        print("callbackSHOW")
        #ESP32Form.Application.showGraph()


