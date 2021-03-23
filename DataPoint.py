import math
from tkinter import PhotoImage
import DataContainer as DC

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
    S1DIFF = 1.5
    S2DIFF = 1.75
    def __init__(self,line = ""):
        try:
            #print(line)
            if ( line == ""):
                self.x = 0
                self.y = 0
                self.z = 0
                self.hnewdeg = 0
                self.vnewdeg = 0
                return 
            xradius =0.096
            ysensordelta =0.017
            parsed = line.split("|")
            measure = parsed[1]

            if (len(measure.split("m,")) < 2):
                self.state = "ERROR"
                self.hAngle = float(parsed[4]) 
                self.vAngle = float(parsed[5]) + self.S1DIFF
                self.hkey = str(self.hAngle)
                self.vkey = str(self.vAngle)
                self.hnewdeg = self.hAngle
                self.vnewdeg =self.vAngle
                self.hAngle *= 0.900000000000001
                self.vAngle *= 0.900000000000001
                self.meter = -30000
                DC.pointDone.update([(int(self.hnewdeg * 10.0),int (self.vnewdeg * 10.0))])

                if self.vnewdeg > 200.0:
                    print(self.vnewdeg)
                return
            measure = measure[2:]
            self.meter = measure.split("m,")[0]

            self.signal = int(measure.split("m,")[1])
            self.hAngle = float(parsed[4])
            self.vAngle = float(parsed[5])

            self.vAngle += self.S1DIFF
            # else:
            #     self.vAngle += self.S2DIFF

            self.hnewdeg = self.hAngle
            self.vnewdeg =self.vAngle
            if self.vnewdeg > 200.0:
                print(self.vnewdeg)

            self.hkey = str(self.hAngle)
            self.vkey = str(self.vAngle)

            self.hAngle *= 0.900000000000001
            self.vAngle *= 0.900000000000001
            
            tx = xradius *    math.cos(math.radians(self.hAngle))
            ty = xradius *    math.sin(math.radians(self.hAngle))
            #print(math.sqrt(tx ** 2 + ty ** 2))
            if ('Er' in self.meter):
                self.state = "ERROR"
                self.meter = -30000

                DC.pointDone.update([(int(self.hnewdeg * 10.0),int (self.vnewdeg * 10.0))])

                return
            try:
                self.meter = float(self.meter)
            except ValueError:
                self.state = "UNKNOWN"
                DC.pointDone.update([(int(self.hnewdeg * 10.0),int (self.vnewdeg * 10.0))])
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
                rho = self.hAngle
                scanned = self.meter + ysensordelta
                zr = math.sqrt((scanned ** 2) + (xradius ** 2))

                x1 = xradius
                y1 = scanned * math.sin(math.radians(phi))
                zr = scanned *  math.cos(math.radians(phi))
                r = math.sqrt((y1 ** 2) + (x1 ** 2) + (zr ** 2))

                x1 = r *  math.cos(math.radians(rho))  *  math.sin(math.radians(phi))
                y1 = r *  math.sin(math.radians(rho))  *  math.sin(math.radians(phi))

                self.x = x1
                self.y = y1

                #zr = math.sqrt((scanned ** 2) + (xradius ** 2))
                self.z = r *  math.cos(math.radians(phi))
                #self.z = zr *  math.cos(math.radians(phi))
             

                # yradius = math.sqrt((scanned ** 2) + (xradius ** 2))
                # #self.y = scanned *  math.cos(math.radians(phi)) * math.sin(math.radians(self.hAngle)) + xradius * math.cos(math.radians(self.hAngle))
                # self.y = scanned  * math.sin(math.radians(self.hAngle)) #+ xradius * math.cos(math.radians(self.hAngle))

            #if (int(self.signal)  < 4000) and (self.meter < 7) and (self.z > -1.5):
            if  (self.meter < 8.0) and (self.z > -1.5):
                self.state = "VALID"
                DC.pointDone.update([(int(self.hnewdeg * 10.0),int (self.vnewdeg * 10.0))])

                # if (abs(self.x) > 6):
                #         print(self.meter)
                #         pass
                # if (abs(self.y) > 6):
                #         print(self.meter)
                #         pass
            else:
                self.state = "INVALID"
                self.meter = -30000
             

           
        except Exception as exc:
            print (exc)
            pass

        pass

    def __getitem__(self, key): 
        if key == "hnewdeg": return self.hnewdeg
        if key == "vnewdeg": return self.vnewdeg
        return None

    

