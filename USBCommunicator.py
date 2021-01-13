import serial.tools.list_ports
#import usb
#import usb.core
import sys
import serial
from _thread import *
from threading import Thread
import threading 
import time
import datetime
import os
import queue
import FileHandler as fh
import socket 

import FormCommand 
import ESPDevices
from DataPoint import DataPoint 
from DataContainer import addPoint


startme=True
sth=None
sth2=None
COMPortList = []
myip = None
COMSerial = None
sendCounter = 0
receiveCounter = 0
receiveList = []
sendList = []
bufferList = []
currentCommands = {}
isConnected = False

queuelock = threading.RLock() 
commandlock = threading.RLock() 

MAXBUFFERSIZE = 10
current2send = 1
alreadysent = 1

class StoppableThread(threading.Thread):
    """Thread class with a stop() method. The thread itself has to check
    regularly for the stopped() condition."""

    def __init__(self):
        print( "base init", file=sys.stderr )
        super(StoppableThread, self).__init__()
        self._stopper = threading.Event()          # ! must not use _stop

    def stopit(self):                              #  (avoid confusion)
        print( "base stop()", file=sys.stderr )
        self._stopper.set()                        # ! must not use _stop

    def stopped(self):
        return self._stopper.is_set()              # ! must not use _stop



class USBCommunicator(StoppableThread):
    """USB Communication"""
    COMPortList = []

    def __init__(self):
      """
      """

      StoppableThread.__init__(self)
      print( "thread init", file=sys.stderr )
      self.current_message=""
      #self.qlaser = qlaser
      #isError=False
      #acceptmessages = False

    def appendReceived(self,message):
        global receiveList
        global receiveCounter
        global currentCommands
        global commandlock

        ident = message[0:2]
        if ident == 'S1':
            print(message)
        if ident in ESPDevices.deviceList:
            print("Device found :" + message)
            message = message[:-1]
            receiveList += message
            if (ESPDevices.isSensor(message)):
                dp = DataPoint(message)
                #print(dp)
                addPoint(dp)

            commandlock.acquire()
            key = ESPDevices.getMessageID(message)
            if key in currentCommands.keys():
                print("Delete :" + currentCommands[key])
                del currentCommands[key]
            commandlock.release()
            receiveCounter += 1


    def run(self,c):
          #global COMSerial
          try:
            while True:
                ch = c.readline()
                #print(ch)
                try:
                    ch = ch.decode("utf-8")
                except Exception as deco:
                    print(deco)
                    continue
                ch.strip()
                if  ch != '':
                    print("got : >" + ch + "<")
                    self.appendReceived(ch)
                    time.sleep(0.2)
          except Exception as inst:
                print(inst)

          pass


    @staticmethod
    def getCOMPortList():
        global COMPortList
        return COMPortList

    def serial_ports(self):
        """ Lists serial port names

            :raises EnvironmentError:
                On unsupported or unknown platforms
            :returns:
                A list of the serial ports available on the system
        """
        if sys.platform.startswith('win'):
            ports = ['COM%s' % (i + 1) for i in range(256)]
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            # this excludes your current terminal "/dev/tty"
            ports = glob.glob('/dev/tty[A-Za-z]*')
        elif sys.platform.startswith('darwin'):
            ports = glob.glob('/dev/tty.*')
        else:
            raise EnvironmentError('Unsupported platform')

        result = []
        for port in ports:
            try:
                s = serial.Serial(port)
                s.close()
                result.append(port)
            except (OSError, serial.SerialException):
                pass
        return result

    def __init__(self):

        StoppableThread.__init__(self)
        print( "thread init", file=sys.stderr )
        self.current_message=""
        #print(list(serial.tools.list_ports.comports()))
        #ls = list(serial.tools.list_ports.comports())[0]
        USBCommunicator.COMPortList = self.serial_ports()
        print(USBCommunicator.COMPortList)

        #with serial.Serial(com, 115200, timeout=1) as ser:
        #    s = ser.read(10) 
        #print(s)
        
def sendSingleCommand(command):
    global COMSerial
    global sendCounter
    global currentCommands
    global commandlock
    global isConnected


    try:
        command += str(sendCounter)+"\n"
        #print("send : " + command)
        commandlock.acquire()
        currentCommands[sendCounter] = command
        commandlock.release()

        sendCounter += 1
        if (isConnected == False):
            return
        for c in command:
            COMSerial.write(c.encode('ascii'))
    except Exception as inst:
                print(inst)

    pass

def updateSend():
    global queuelock
    global bufferList
    global MAXBUFFERSIZE
    global currentCommands
    global commandlock
    global alreadysent
    global current2send


    queuelock.acquire()
    if (len(bufferList) == 0):
        queuelock.release()
        return
    queuelock.release()


    commandlock.acquire()
    if (len(currentCommands) >=  MAXBUFFERSIZE):
        commandlock.release()
        return
    diff= MAXBUFFERSIZE - len(currentCommands)
    commandlock.release()

    queuelock.acquire()
    sendList = []
    while (len( bufferList ) > 0):
        sendList.append(bufferList.pop(0))
        diff -= 1
        if (diff == 0): break

    for s in sendList:
        alreadysent += 1
        pbar = FormCommand.FormCommand.getWidgetByName("PROGRESSBAR")
        pbar["value"]=int(alreadysent / current2send * 100.0)
        pbar.update();
        sendSingleCommand(s)
    queuelock.release()

def addCommand(message,toInsert = False):
    global queuelock
    global bufferList
    global current2send

    queuelock.acquire()
    if (toInsert):
        if len(bufferList) == 0:
            bufferList.append(message)
        else:
            bufferList.insert(0, message)
        current2send += 1
    else:
        bufferList.append(message)
    queuelock.release()


def startServer(): 

    host = "" 
    global myip
    global sth2
    global COMSerial

    try:
        host_name = socket.gethostname() 
        myip = socket.gethostbyname(host_name) 
        listen2usb=USBCommunicator()
        sth2 = Thread(target=listen2usb.run,  args=(COMSerial,), daemon=True)
        sth2.start()
    except Exception as inst:
                print(inst)
    pass

        
def stopServer():
    global startme
    print("stop server")
    startme = False
    #sth2.stopit()
    if sth2 != None:
        sth2.join()


def startserverThread():
    global startme
    global sth
    global COMSerial
    global isConnected
    status = FormCommand.FormCommand.getWidgetByName("CLIENTLABEL")

    try: 
        startme=True
        #com = FormCommand.FormCommand.getWidgetByName("COMPortList").get()
        #print(com)
        COMSerial = serial.Serial('COM3', 115200, timeout=1)
        sth = Thread(target=startServer)
        sth.start()
        print("Server thread started")
        status["text"] = "Connected"
        status["bg"] = "green"
        isConnected = True
        
    except Exception as inst:
        status["text"] = "ERROR"
        status["bg"] = "red"
        print(inst)
    #start_new_thread(startServer) 

#if __name__ == '__main__': 
#    Main() 

  



