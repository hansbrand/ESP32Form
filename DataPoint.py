import math
from tkinter import PhotoImage

class DataPoint(object):
    """description of class"""
    meter = None
    signal = None
    hAngle = None
    vAngle = None
    x=None
    y=None
    z=None
    state = ""
    hnewdeg = None
    vnewdeg = None
    hkey = ""
    vkey = ""

    def __init__(self,line):
        try:
            #print(line)
            xradius =0.096
            ysensordelta =0.017
            parsed = line.split("|")
            measure = parsed[1]

            if (len(measure.split("m,")) < 2):
                self.state = "ERROR"
                self.hAngle = float(parsed[4])
                self.vAngle = float(parsed[5])
                self.hkey = str(self.hAngle)
                self.vkey = str(self.vAngle)
                self.hnewdeg = self.hAngle
                self.vnewdeg =self.vAngle
                self.hAngle *= 0.900000000000001
                self.vAngle *= 0.900000000000001
                return
            measure = measure[2:]
            self.meter = measure.split("m,")[0]

            self.signal = int(measure.split("m,")[1])
            self.hAngle = float(parsed[4])
            self.vAngle = float(parsed[5])

            self.hnewdeg = self.hAngle
            self.vnewdeg =self.vAngle
            self.hkey = str(self.hAngle)
            self.vkey = str(self.vAngle)


            self.hAngle *= 0.900000000000001
            self.vAngle *= 0.900000000000001
            
            tx = xradius *    math.cos(math.radians(self.hAngle))
            ty = xradius *    math.sin(math.radians(self.hAngle))
            #print(math.sqrt(tx ** 2 + ty ** 2))
            if ('Er' in self.meter):
                self.state = "ERROR"
                return
            try:
                self.meter = float(self.meter)
            except ValueError:
                self.state = "UNKNOWN"
                return

            self.meter += ysensordelta
            # if (self.meter > 7):
            #     print(self.meter)
            #     print(self.signal)
            #     pass

 
            if ((self.vAngle == 0.0)):
                self.z = self.meter
                self.x = tx
                self.y = ty
            elif (self.vAngle == 180.0):
                self.z = -(self.meter)
                self.x = tx
                self.y = ty
            else:
                phi = self.vAngle
                scanned = self.meter
                self.z = self.meter *  math.cos(math.radians(phi))
             
                #TODO :umrechnung hier
                self.x = xradius *  math.cos(math.radians(self.hAngle))# * math.sin(math.radians(phi))
            #exchange x and z axis
            #rotate x degree
                tradius = abs(scanned * math.sin(math.radians(self.hAngle)))
            #start with 45 degree
                yradius = math.sqrt( 2 * (tradius ** 2))
                self.y = yradius * math.cos(math.radians(phi + 45))

                yradius = math.sqrt((scanned ** 2) + (xradius ** 2))
                newh = self.hAngle + 180.0
                if (newh > 360.0):
                    newh -= 180
                self.y = yradius *  math.cos(math.radians(newh)) * math.sin(math.radians(phi - 90.0))

            if (int(self.signal)  < 1000) and (self.meter < 9) and (self.z > -1.5):
                self.state = "VALID"
                # if (abs(self.x) > 6):
                #         print(self.meter)
                #         pass
                # if (abs(self.y) > 6):
                #         print(self.meter)
                #         pass
            else:
                self.state = "INVALID"

           
        except Exception as exc:
            print (exc)
            pass

        pass

    def __getitem__(self, key): 
        if key == "hnewdeg": return self.hnewdeg
        if key == "vnewdeg": return self.vnewdeg
        return None

    

