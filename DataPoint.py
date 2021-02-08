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
                self.z = xradius+ self.meter
                self.x = tx
                self.y = ty
            elif (self.vAngle == 180.0):
                self.z = -(xradius + self.meter)
                self.x = tx
                self.y = ty
            else:
                self.z = self.meter *  math.cos(math.radians(self.vAngle)) 
                #TODO :umrechnung hier
                #print(str(self.meter) + ":" + str(self.z))


                self.x = xradius
                ytemp = self.meter *  math.sin(math.radians(self.vAngle))  
                #self.x = tx
                #self.y = ty + self.meter
                r2 = math.sqrt( (xradius ** 2) + (self.meter ** 2))
                # auf z = 0 projezieren
                r1 = math.sqrt(r2 ** 2 - self.z ** 2)
                r3 = math.sqrt(r1 ** 2 - xradius ** 2)
                r4 = math.sqrt(self.meter ** 2 - self.z ** 2)
                

                if (self.hAngle != 0):
                    self.x = r2 *  math.cos(math.radians(self.hAngle)) * math.sin(math.radians(self.vAngle))
                    self.y = r2 *  math.sin(math.radians(self.hAngle)) #* math.sin(math.radians(self.vAngle))
                else:
                    self.x = xradius
                    self.y = ytemp

    

            if (int(self.signal)  < 300) and (self.meter < 9) and (self.z > -1.5):
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



