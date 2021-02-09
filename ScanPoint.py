import math

class ScanPoint(object):
    def __init__(hangle, vangle):
        self.hor_angle = hangle
        self.ver_angle = vangle
        self.realH = hangle
        if (hangle >= 200):
            self.realH -= 200

    
    def __getitem__(self, key): 
        if key == "hor_angle": return self.hor_angle
        if key == "ver_angle": return self.ver_angle
        if key == "realH": return self.realH

        return None