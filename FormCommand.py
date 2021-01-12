import tkinter as tk
import FormBuild
from FormCallbacks import FormCallbacks
from FormWidgetCallbacks import FormWidgetCallbacks
#import FormCallbacks
import inspect
from functools import partial


radioMap = {}

class FormCommand(object):
    WidgetTable = {}
    WidgetLookup = {}
    Row0Frame = None
    master = None
    callbacks = {}

    def createCallbacks(self):
   
        for k in self.WidgetTable.keys():
            FCmember = dir(FormCallbacks)
            if isinstance(k, tk.Button):
                cbname = "callback" + self.WidgetTable[k][0]
                method_to_call = None
                if cbname in FCmember:
                    f = "FormCallbacks." + cbname + "()"
                    method_to_call = getattr(FormCallbacks, cbname)
                    action_with_arg = partial(method_to_call, k)
                    #k["command"] = (lambda: method_to_call(k))
                    k["command"] = action_with_arg
                else:
                    f = eval("FormCallbacks.cbdefault()")
                    #k["command"] = lambda: FormCallbacks.cbdefault(k)
                    k["command"] = FormCallbacks.cbdefault
                #print("Button" + self.WidgetTable[k][0])

            if isinstance(k, tk.Radiobutton):
                FCmember = dir(FormWidgetCallbacks)
                cbname = "callbackRadiobuttons"
                method_to_call = None
                if cbname in FCmember:
                    method_to_call = getattr(FormWidgetCallbacks, cbname)
                    action_with_arg = partial(method_to_call, k)
                    #k["command"] = (lambda: method_to_call(k))
                    #k.param1 = self.WidgetTable[k][2]
                    k["command"] = action_with_arg
                #print("Radiobutton" + self.WidgetTable[k][0])

            if isinstance(k, tk.Scale):
                FCmember = dir(FormWidgetCallbacks)
                cbname = "callbackScale"
                method_to_call = None
                if cbname in FCmember:
                    method_to_call = getattr(FormWidgetCallbacks, cbname)
                    action_with_arg = partial(method_to_call, k)
                    #k["command"] = (lambda: method_to_call(k))
                    #k.param1 = self.WidgetTable[k][2]
                    k["command"] = action_with_arg
                #print("Scale" + self.WidgetTable[k][0])

        pass

    def __init__(self, master):
        super().__init__()
        self.master = master
        callbacks = {}
        for s in FormBuild.widget_names:
            callbacks[s] = None

    def addWidget(self,widget,name,value):
        callback = "callback" + name;
        self.WidgetTable[widget] = [name,callback,value]
        self.WidgetLookup[name] = widget
        self.callbacks[name] = callback;

    @classmethod
    def getWidgetByName(self,name):
        widget = self.WidgetLookup[name]
        return widget
        


