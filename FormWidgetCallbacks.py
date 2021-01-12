#from FormCommand import FormCommand
import FormCommand
import Row0Init
from _thread import *
from threading import Thread
import threading 

class FormWidgetCallbacks(object):
    """description of class"""
    param_lock = threading.RLock() 

    def __init__(self):
        pass

    @classmethod
    def cbdefault(self, x):
        print("cbdefault  ", x)

    @classmethod
    def callbackRadiobuttons(self, button):
        print("callbackRadiobuttons  ")
        v = FormCommand.radioMap[button.master]
        print(v.get())
        #v = FormCommand.FormCommand.getWidgetValue(button)



