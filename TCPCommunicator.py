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
from FileManager import saveCSVlist
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
socketfd=[]
tcpconnection = None

queuelock = threading.RLock() 
commandlock = threading.RLock() 

MAXBUFFERSIZE = 10
current2send = 1
alreadysent = 1
scanstarttime = 0

port = 7165
isScanning = False

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



class TCPCommunicator(StoppableThread):
    """USB Communication"""
    

    def __init__(self):
      """
      """

      StoppableThread.__init__(self)
      print( "thread init", file=sys.stderr )
      self.current_message=""
      #self.qlaser = qlaser
      #isError=False
      #acceptmessages = False

    def appendReceived(self,mess):
        global receiveList
        global receiveCounter
        global currentCommands
        global commandlock
        global isConnected
        global isScanning
        try:
            parts = mess.split('\n');
            for message in parts:
                ident = message[0:2]
                if ident in ESPDevices.deviceList:
                    #print("Device found :" + message)
                    receiveList += [message + "\n"]
                    if (ESPDevices.isSensor(message)):
                        dp = DataPoint(message)
                        addPoint(dp)

                    commandlock.acquire()
                    key = ESPDevices.getMessageID(message)
                    if key in currentCommands.keys():
                        print("currentcom :" + str(currentCommands))
                        del currentCommands[key]
                        if isScanning:
                            isScanning = len(currentCommands) > 0
                    commandlock.release()
                    receiveCounter += 1
        except Exception as exc:
            print (exc)


    def run(self,c):
          global startme

          try:
            currentbuffer = ""
            while startme:
                ch = c.recv(2048) 
                #ch = c.readline()
                if not ch: 
                    print('Bye') 
                    # lock released on exit 
                    break

                #print(ch)
                ch = ch.decode("utf-8")
                currentbuffer += ch
                #ch.strip()
                recm = ""
                for chr in currentbuffer:
                    recm += chr
                    currentbuffer = currentbuffer[1:]
                    if chr == "\n":
                        self.appendReceived(recm)
                        recm = ""
                        if ("\n" in currentbuffer):
                            continue
                        else: 
                            break

                    #time.sleep(0.2);
          except Exception as inst:
                print(inst)
                isConnected = False

          pass


    @staticmethod
    def getCOMPortList():
        global COMPortList
        return COMPortList

    #def serial_ports(self):
    #    """ Lists serial port names

    #        :raises EnvironmentError:
    #            On unsupported or unknown platforms
    #        :returns:
    #            A list of the serial ports available on the system
    #    """
    #    if sys.platform.startswith('win'):
    #        ports = ['COM%s' % (i + 1) for i in range(256)]
    #    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
    #        # this excludes your current terminal "/dev/tty"
    #        ports = glob.glob('/dev/tty[A-Za-z]*')
    #    elif sys.platform.startswith('darwin'):
    #        ports = glob.glob('/dev/tty.*')
    #    else:
    #        raise EnvironmentError('Unsupported platform')

    #    result = []
    #    for port in ports:
    #        try:
    #            s = serial.Serial(port)
    #            s.close()
    #            result.append(port)
    #        except (OSError, serial.SerialException):
    #            pass
    #    return result

    def __init__(self):

        StoppableThread.__init__(self)
        print( "thread init", file=sys.stderr )
        self.current_message=""
        #print(list(serial.tools.list_ports.comports()))
        #ls = list(serial.tools.list_ports.comports())[0]
        #TCPCommunicator.COMPortList = self.serial_ports()
        #print(TCPCommunicator.COMPortList)

        #with serial.Serial(com, 115200, timeout=1) as ser:
        #    s = ser.read(10) 
        #print(s)
        
def sendSingleCommand(command):
    global tcpconnection
    global sendCounter
    global currentCommands
    global commandlock
    global isConnected
    global scanstarttime


    try:
        command += str(sendCounter)+"\n"
        print("send : " + command)
        commandlock.acquire()
        # if ("C1" in command ):
        #     print(command)
        # else:
        #     currentCommands[sendCounter] = command
        currentCommands[sendCounter] = command
        if (str(ESPDevices.C_GETSTATS) in command):
            del currentCommands[sendCounter]
        if (str(ESPDevices.C_STARTTIMER) in command):
            scanstarttime = time.time()
            del currentCommands[sendCounter]


        commandlock.release()

        if (isConnected == False):
            return
        for c in command:
            tcpconnection.send(c.encode('ascii'))
        sendCounter += 1
        if (str(ESPDevices.C_STEPPERCALIBRATE) in command):
            sendCounter += 2
    except Exception as inst:
                print(inst)
                isConnected = False

    pass

def emergeny():
    global tcpconnection
    global sendCounter
    global currentCommands
    global commandlock
    global isConnected
    global sendList
    global bufferList
    global queuelock

    sendSingleCommand(ESPDevices.emergencyCommand());
    
    time.sleep(5)
    commandlock.acquire()
    queuelock.acquire()
    tcpconnection.close()
    sendCounter = 0
    currentCommands=[]
    isConnected = False
    sendList = []
    bufferList = []
    queuelock.release()
    commandlock.release()


def updateSend():
    global queuelock
    global bufferList
    global MAXBUFFERSIZE
    global currentCommands
    global commandlock
    global alreadysent
    global current2send
    global isConnected
    global scanstarttime

    try:
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
            print(str(alreadysent) + " / " + str (current2send))
            pbar = FormCommand.FormCommand.getWidgetByName("PROGRESSBAR")
            pbar["value"]=int(alreadysent / current2send * 100.0)
            st = time.time() - scanstarttime
            tdone = float(st)
            if  (alreadysent != 0):
                single = st / float(alreadysent)
                diff = float(current2send - alreadysent) * single
                tfield = FormCommand.FormCommand.getWidgetByName("TIME")

                tfield["text"] = str(int(st / 60.0)) + " / " + str(int(diff / 60.0))

            if (alreadysent == (current2send - 1) ):
                saveCSVlist(receiveList, "RAW")

            pbar.update();
            
            if (isConnected):
                print("sendlist" + str(sendList))
                sendSingleCommand(s)

        queuelock.release()
    except Exception as exc:
        print(exc)

def addCommand(message,toInsert = False):
    global queuelock
    global bufferList
    global current2send
    #print("Scan List");

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

def tcpClear():
    queuelock.acquire()

    bufferList.clear()
    sendlist.clear()
    queuelock.release()

def TCP_close():
    #socketfd.close()
    tcpconnection.close()

def startServer(): 

    host = "" 
    global myip
    global sth2
    global socketfd
    global tcpconnection
    global isConnected
    host = ""

    try:
        host_name = socket.gethostname() 
        myip = socket.gethostbyname(host_name) 



        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM ) 
        # Get the old state of the SO_REUSEADDR option
        old_state = s.getsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR )
        print ("Old sock state: %s" %old_state)

        # Enable the SO_REUSEADDR option
        s.setsockopt( socket.SOL_SOCKET, socket.SO_REUSEADDR, 1 )
        new_state = s.getsockopt( socket.SOL_SOCKET, socket.SO_REUSEADDR )
        print ("New sock state: %s" %new_state)

        s.bind((host, port)) 

        listen2tcp=TCPCommunicator()
        s.listen(5) 
        print("socket is listening") 
        print("Please start client...")


        while not startme:
            time.sleep(1)

        c = None
        while startme: 
  
            # establish connection with client 
            c, addr = s.accept() 
            tcpconnection = c
            # lock acquired by client 
            print('Connected to :', addr[0], ':', addr[1]) 
            # Start a new thread and return its identifier 
            sth2 = Thread(target=listen2tcp.run,  args=(c,), daemon=True)
            #sth2 = Thread(target=listen2tcp.run,  args=(c,))
            socketfd.append(c)
            sth2.start()
            isConnected = True
        s.close() 

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
    host = "" 
    global port

    status = FormCommand.FormCommand.getWidgetByName("CLIENTLABEL")

    try: 
        startme=True
        #com = FormCommand.FormCommand.getWidgetByName("COMPortList").get()
        #print(com)
        

        sth = Thread(target=startServer)
        sth.start()
        print("Server thread started")
        status["text"] = "Connected"
        status["bg"] = "green"
        
    except Exception as inst:
        status["text"] = "ERROR"
        status["bg"] = "red"
        print(inst)
    #start_new_thread(startServer) 

#if __name__ == '__main__': 
#    Main() 

  



