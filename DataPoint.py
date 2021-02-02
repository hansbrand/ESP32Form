import math

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

    def __init__(self,line):
        try:
            xsensordelta =0.096
            ysensordelta =0.017
            parsed = line.split("|")
            measure = parsed[1]

            if (len(measure.split("m,")) < 2):
                self.state = "ERROR"
                self.hAngle = float(parsed[4])
                self.vAngle = float(parsed[5])
                self.hAngle *= 0.900000000000001
                self.vAngle *= 0.900000000000001
                return
            measure = measure[2:]
            self.meter = measure.split("m,")[0]

            self.signal = int(measure.split("m,")[1])
            self.hAngle = float(parsed[4])
            self.vAngle = float(parsed[5])

            self.hAngle *= 0.900000000000001
            self.vAngle *= 0.900000000000001
            
            tx = xsensordelta *    math.cos(math.radians(self.hAngle))
            ty = xsensordelta *    math.sin(math.radians(self.hAngle))

            if ('Er' in self.meter):
                self.state = "Error"
                return
            try:
                self.meter = float(self.meter)
            except ValueError:
                self.state = "UNKNOWN"
                return

            self.meter += ysensordelta

            

            if ((self.vAngle == 0.0)):
                self.z = xsensordelta + self.meter
                self.x = tx
                self.y = ty
            elif (self.vAngle == 180.0):
                self.z = -(xsensordelta + self.meter)
                self.x = tx
                self.y = ty
            else:
                self.z = self.meter *  math.cos(math.radians(self.vAngle)) 
                #TODO :umrechnung hier
                print(str(self.meter) + ":" + str(self.z))
                zz = (self.meter ** 2) - (abs(self.z) ** 2)
                if (zz < 0):
                    zz = math.sqrt((abs(self.z) ** 2) - (self.meter ** 2))
                else:
                    zz = math.sqrt(zz)

                
                if (ty != 0):
                    self.x = tx + zz * (tx / ty)
                    self.y = ty + zz * (tx / ty)
                else :
                    self.x = self.meter
                    self.y = ty + self.meter

            if (int(self.signal)  < 150):
                self.state = "VALID"
            else:
                self.state = "INVALID"

        except Exception as exc:
            print (exc)
            pass





        pass

    def __getitem__(self, key): 
        if key == "hAngle": return self.hAngle
        if key == "vAngle": return self.vAngle
        return None



