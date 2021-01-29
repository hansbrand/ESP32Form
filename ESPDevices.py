import numpy
import DataContainer
import FormCommand

hStepper = None
vStepper = None
v2Stepper = None
Sensor1 = None
Sensor2 = None

STEPPER = "Stepper"
SENSOR = "Sensor"
C_STEPPERCALIBRATE = 32000
C_SYSTEMINIT       =  32001
C_TURN2ZERO        =   32002
C_STARTTIMER       =  32003
C_GETSTATS        =   32004
C_EMERGENCY        =   32005

commandList = []
deviceList = ["S1","S2","M1","M2","M3","C1"]

class ESPDevices(object):
    """description of class"""
    name = ''
    kind =''


    def __init__(self,name,kind):
        self.name = name
        self.kind = kind

    def turnCommand(self,degree): 
        global STEPPER
        if (self.kind == STEPPER):
            command = self.name + ":" +  str(degree) + ":"
            return command
        else :
            return None


    def openCommand(self): 
        global SENSOR
        if (self.kind == SENSOR):
            command = self.name + ":O:"
            return command
        else :
            return None

    def statusCommand(self): 
        global SENSOR
        if (self.kind == SENSOR):
            command = self.name + ":S:"
            return command
        else :
            return None

    def scanCommand(self,dc):
        global SENSOR
        if (self.kind == SENSOR):
            command = self.name + ":" + dc + ":"
            return command
        else :
            return None

    def closeCommand(self):
        global SENSOR
        if (self.kind == SENSOR):
            command = self.name + ":C:"
            return command
        else :
            return None


    def turnoffCommand(self):
        global SENSOR
        if (self.kind == SENSOR):
            command = self.name + ":X:"
            return command
        else :
            return None

def addScanning(counter):
  global commandList
  message = "S1:D:" 
  commandList.append(message)
  message = "S2:D:" 
  commandList.append(message)


def starttimerCommand():
    global C_STARTTIMER
    command = "C1:" + str(C_STARTTIMER) + ":"
    return command

def getstatsCommand():
    global C_GETSTATS
    command = "C1:" + str(C_GETSTATS) + ":"
    return command


def statusCommand(ind): 
    command = "S" + str(ind) + ":S:"
    return command

def genSimpleCommands(scanning = True, hstart = 0,hend = 200,vstart = 0,vend = 200, hdelta = 2.0 ,vdelta = 10.0):
  global commandList
  round = 0;

  message = ""

  counter = 0
  commandList.append(starttimerCommand())
  hindex = hstart
  while  (hindex < hend):
    if (scanning):
        addScanning(counter)
        counter += 1
    message = "M1:" + str(hindex) + ":" 
    counter +=1
    commandList.append(message)
    vindex = vstart
    while (vindex < vend):
      if (scanning):
        addScanning(counter)
      message = "M2:" + str(vindex) + ":" 
      counter += 1
      commandList.append(message)
      message = "M3:" + str(vindex) + ":" 
      counter += 1
      commandList.append(message)
      vindex += vdelta
    
    hindex += hdelta
    if (hindex > hend):
        break

    message = "M1:" + str(hindex) + ":" 
    counter +=1
    commandList.append(message)
    vindex -= vdelta

    while (vindex >= vstart):
      if (scanning):
        addScanning(counter)
      counter +=1
      message = "M2:" + str(vindex) + ":" 
      commandList.append(message)
      counter +=1
      message = "M3:" + str(vindex) + ":" 
      commandList.append(message)
      vindex -= vdelta
    hindex += hdelta
    round += 1
    if ((round % 3) == 0):
        commandList.append(statusCommand(1))
        commandList.append(statusCommand(2))
  commandList.append(getstatsCommand())

  message = "C1:" + str(C_STEPPERCALIBRATE) + ":" 
  commandList.append(message)

  return commandList



def genTestCommands(scanning = True, hstart = 0,hend = 180,vstart = 0,vend = 180, hdelta = 2.0 ,vdelta = 10.0):
    global commandList
    round = 0;

    message = ""

    counter = 0
    commandList.append(starttimerCommand())
    hindex = hstart
    if (scanning):
        addScanning(counter)
        counter += 1
    message = "M1:" + str(hindex) + ":" 
    counter +=1
    commandList.append(message)
    vindex = vstart
    while (vindex < vend):
        if (scanning):
            addScanning(counter)
        message = "M2:" + str(vindex) + ":" 
        counter += 1
        commandList.append(message)
        message = "M3:" + str(vindex) + ":" 
        counter += 1
        commandList.append(message)
        vindex += vdelta
        message = "M1:" + str(hindex) + ":" 
        counter += 1
        commandList.append(message)
        hindex += hdelta

    while (vindex >= 0):
        if (scanning):
            addScanning(counter)
        counter +=1
        message = "M2:" + str(vindex) + ":" 
        commandList.append(message)
        counter +=1
        message = "M3:" + str(vindex) + ":" 
        commandList.append(message)
        vindex -= vdelta
        counter +=1
        message = "M1:" + str(hindex) + ":" 
        commandList.append(message)
        hindex -= hdelta
    round += 1

    commandList.append(getstatsCommand())


    return commandList





def handleMotor(message):
    if (message[0][1] == '1'):
        sbar = FormCommand.FormCommand.getWidgetByName("MOTOR1")
        sbar["text"] = message[3]
    if (message[0][1] == '2'):
        sbar = FormCommand.FormCommand.getWidgetByName("MOTOR3")
        sbar["text"] = message[3]
    if (message[0][1] == '3'):
        sbar = FormCommand.FormCommand.getWidgetByName("MOTOR3")
        sbar["text"] = message[3]
    pass

def isSensor(message):
    global deviceList
    try:
        if (message[0] == 'M'):
            handleMotor(message)
            return False
        st = message[0:2]
        if ("C1" == st):
            print(message)
            return False
        if (message[0] != 'S'):return False
        if ((st in deviceList) != True): return False
        # TODO
        parts = message.split("|")
        #parts = message.split(":")

        if ( len (parts) < 3):return False
        if ("Er" in parts[1]):
            DataContainer.ErrorList.append(parts[1])
            return False
        if (parts[1][0] == "S"):
            DataContainer.StatusList.append(parts[1])
            if (parts[0][1] == '1'):
                sbar = FormCommand.FormCommand.getWidgetByName("STATUS1")
                sbar["text"] = parts[1]
            if (parts[0][1] == '2'):
                sbar = FormCommand.FormCommand.getWidgetByName("STATUS2")
                sbar["text"] = parts[1]
            return False
        return (parts[1][0] in ['D','F','M'])
    except Exception as exc:
        print(exc)


def initDevices():
    global SENSOR
    global STEPPER
    global hStepper
    global v2Stepper
    global vStepper
    global Sensor1
    global Sensor2

    hStepper = ESPDevices("M1", STEPPER)
    vStepper = ESPDevices("M2", STEPPER)
    v2Stepper = ESPDevices("M3", STEPPER)
    Sensor1 = ESPDevices("S1", SENSOR)
    Sensor2 = ESPDevices("S2", SENSOR)


def calibrateCommand():
    global C_STEPPERCALIBRATE
    command = "C1:" + str(C_STEPPERCALIBRATE) + ":"
    return command


def adjustCommand():
    global C_TURN2ZERO
    command = "C1:" + str(C_TURN2ZERO) + ":"
    return command

def emergencyCommand():
    global C_EMERGENCY
    command = "C1:" + str(C_EMERGENCY) + ":"
    return command

def getMessageID(message):
    try:
        parts = message.split("|")
        #parts = message.split(":")

        print( parts)
        if len(parts) < 3:
            return -1
        #return int(parts[3])
        if (message.startswith("M")):
            return int(parts[3])
        if (message.startswith("S")):
            return int(parts[2])
        return -1
    except Exception as exc:
        print(exc)

def turnCommand(dev,degree): 
            command = dev + ":" +  str(degree) + ":"
            return command

def piepCommand(dev): 
            command = dev + ":D:"
            return command
