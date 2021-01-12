
class DataPoint(object):
    """description of class"""
    meter = None
    signal = None
    hAngle = None
    vAngle = None

    def __init__(self,line):
        parsed = line.split("|")
        measure = parsed[1]
        measure = measure[2:]
        if ("Er" in line):
            self.meter = -1
            return
        self.meter = float(measure.split("m,")[0])
        self.signal = int(measure.split("m,")[1])
        self.hAngle = float(parsed[4])
        self.vAngle = float(parsed[5])


        pass

    def __getitem__(self, key): 
        if key == "hAngle": return self.hAngle
        if key == "vAngle": return self.vAngle
        return None



