import os
import USBCommunicator
import ESPDevices
import FormCommand
import FileManager
import USBCommunicator
import ESP32Form

checkButtonval = None

class FormCallbacks(object):
    """description of class"""
    def __init__(self):
        pass

    @classmethod
    def cbdefault(self , button):
        print("cbdefault  ")

    @classmethod
    def callbackINIT(self,button):
        print("callbackINIT")
        #ESPDevices.initDevices()
        #ESPDevices.genSimpleCommands(False)
        USBCommunicator.startserverThread()
        USBCommunicator.addCommand(ESPDevices.calibrateCommand() )
        USBCommunicator.addCommand(ESPDevices.Sensor1.openCommand())
        USBCommunicator.addCommand(ESPDevices.Sensor2.openCommand())


    @classmethod
    def callbackCALIBRATE(self , button):
        print("callbackCALIBRATE")
        USBCommunicator.addCommand(ESPDevices.calibrateCommand() )

    @classmethod
    def callbackADJUST(self , button):
        print("callbackADJUST")
        USBCommunicator.addCommand(ESPDevices.adjustCommand() )



    @classmethod
    def callbackSTOP(self , button):
        print("callbackSTOP")

    @classmethod
    def callbackRESUME(self , button):
        print("callbackRESUME")

    @classmethod
    def callbackFULLSCAN(self , button):
        print("callbackFULLSCAN")
        clist = ESPDevices.genSimpleCommands(True)
        USBCommunicator.current2send = len(clist)
        USBCommunicator.alreadysent = 0

        for s in clist:
            USBCommunicator.addCommand(s)


    @classmethod
    def callbackSAVE_FILE(self , button):
        print("callbackSAVE_FILE")
        FileManager.saveCSVlist(USBCommunicator.receiveList, "RAW")
        USBCommunicator.receiveList = []

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
        ESP32Form.Application.cleanup()
        #button.master.master.master.destroy()
        os._exit( 0 )

    @classmethod
    def callbackSCAN(self , button):
        print("callbackSCAN")
        hfrom = float(FormCommand.FormCommand.getWidgetByName("HSTART").get())
        hto = float(FormCommand.FormCommand.getWidgetByName("HEND").get())
        vfrom = float(FormCommand.FormCommand.getWidgetByName("VSTART").get())
        vto = float(FormCommand.FormCommand.getWidgetByName("VEND").get())
        hdelta = float(FormCommand.FormCommand.getWidgetByName("HSCALE").get())
        vdelta = float(FormCommand.FormCommand.getWidgetByName("VSCALE").get())
        
        clist = ESPDevices.genSimpleCommands(True, hfrom, hto, vfrom, vto, hdelta, vdelta)
        USBCommunicator.current2send = len(clist)
        USBCommunicator.alreadysent = 0
        for s in clist:
            USBCommunicator.addCommand(s)



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


