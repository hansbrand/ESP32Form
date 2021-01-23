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

    def __init__(self,line):
        parsed = line.split("|")
        measure = parsed[1]
        measure = measure[2:]
        self.meter = float(measure.split("m,")[0])
        self.signal = int(measure.split("m,")[1])
        self.hAngle = float(parsed[4])
        self.vAngle = float(parsed[5])
        self.x = self.meter *  math.sin(math.radians(self.vAngle)) *  math.cos(math.radians(self.hAngle))
        self.y = self.meter *  math.sin(math.radians(self.vAngle)) *  math.sin(math.radians(self.hAngle))
        self.z = self.meter *  math.cos(math.radians(self.vAngle)) 


        pass

    def __getitem__(self, key): 
        if key == "hAngle": return self.hAngle
        if key == "vAngle": return self.vAngle
        return None



