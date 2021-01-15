import numpy
import DataContainer


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


def genSimpleCommands(scanning = True, hstart = 0,hend = 360,vstart = 0,vend = 180, hdelta = 1.0 ,vdelta = 5.0):
  global commandList

  message = ""

  counter = 0

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
    if (hindex > 360.0):
        break

    message = "M1:" + str(hindex) + ":" 
    counter +=1
    commandList.append(message)

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
    
  
  message = "C1:" + str(C_STEPPERCALIBRATE) + ":" 
  commandList.append(message)
  #for c in commandList:
    #print(c)

  return commandList

def handleMotor(message):
    pass

def isSensor(message):
    global deviceList
    if (message[0] == 'M'):
       handleMotor(message)
       return False
    #if (message[0] != 'S'):return False
    st = message[0:2]
    if ((st in deviceList) != True): return False
    parts = message.split("|")
    print(parts)
    if ( len (parts) < 3):return False
    if ("Er" in message):
        DataContainer.ErrorList.append(parts[1])
        return False
    if (parts[1][0] == "S"):
        DataContainer.StatusList.append(parts[1])
        return False
    return (parts[1][0] in ['D','F','M'])



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

def getMessageID(message):
    parts = message.split("|")
    if len(parts) < 4:
        return -1
    print( parts)
    if (message.startswith("M")):
        return int(parts[3])
    if (message.startswith("S")):
        return int(parts[2])
    return -1


