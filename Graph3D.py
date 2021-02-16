import random
import matplotlib
import tkinter as Tk
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import io
from PIL import Image
import DataContainer as DC
import threading

matplotlib.use('TkAgg')

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)

fig = None
canvas = None
ax = None
annot = None
aborder = None
lasthindex = None

class Graph3D(Tk.Frame):
    """description of class"""
    fig = None
    canvas = None
    t,s = None,None
    is2draw = True
    drawlock = threading.RLock() 

    
    def selfdestroy(self):
        global canvas
        global toolbar
        toolbar.destroy()
        canvas.get_tk_widget().destroy()

    def Is2Draw(self):
        b = False
        self.drawlock.acquire()
        b = self.is2draw
        self.drawlock.release()
        return b



    def __init__(self):
        pass

    def __init__(self, parent):
        global fig
        global canvas
        global s_time
        global ax
        global toolbar
        global annot

        #fig = plt.Figure(figsize=(8,6))
        fig = plt.Figure()

        
        parent.title("Graph3D")
        canvas = FigureCanvasTkAgg(fig, parent)
        canvas.get_tk_widget().pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)

        ax=fig.add_subplot(111,projection='3d')
        #fig.tight_layout()
        
        ax.view_init(azim=0, elev=90)
        #ax = Axes3D(fig)

        fig.subplots_adjust(bottom=0.05)#,top=0.98,right = 0.98, left = 0.05)
        #fig.canvas.mpl_connect("motion_notify_event", self.hover)
        #fig.canvas.mpl_connect('pick_event', self.onpick3)
        #fig.canvas.mpl_connect('scroll_event',self.zreset)

        #toolbar = NavigationToolbar2Tk(canvas, parent)
        #toolbar.update()
        canvas._tkcanvas.pack(side=Tk.TOP, fill=Tk.BOTH, expand=True)
        self.scat = None




    def drawDia(self,changed):
        global fig
        global canvas
        global s_time
        global ax
        global ax2
        global annot
        global aborder


        try:
            #is3D = ParamMan.show3D
            self.drawlock.acquire()
            self.is2draw = False
            self.drawlock.release()

            is3D = False
            x1 = []
            z1 = []
            m1 = []
            y1 = []
            x1,y1,z1,m1 = DC.getPointData()
            if (x1 == []) :
                self.drawlock.acquire()
                self.is2draw = True
                self.drawlock.release()

                return
           

            ax.clear()
            ax.set_xlabel("X - Axis")
            ax.set_ylabel("Y - Axis")
            ax.set_zlabel("Z - Axis")
            ax.xaxis.set_major_locator(plt.MaxNLocator(5))
            ax.yaxis.set_major_locator(plt.MaxNLocator(5))
            ax.zaxis.set_major_locator(plt.MaxNLocator(5))

            # if is3D:
            #     m = DC.dc["0"]["polygons"]
            #     ec = DC.dc["0"]["polycolor3D"]
            #     ax.add_collection3d(Poly3DCollection(m,edgecolors= ec, facecolors = (0,0,0,0)))
            # if is3D:
            #     m = DC.dc["180"]["polygons"]
            #     ec = DC.dc["180"]["polycolor3D"]
            #     ax.add_collection3d(Poly3DCollection(m,edgecolors=ec,facecolors = (0,0,0,0))) 
            #fig.tight_layout()
            self.scat = ax.scatter(x1,y1,z1,c=m1,picker=True)
            b=DC.getlimits3D()
            if (b != None):
                ax.set_xlim(b["xmin"],b["xmax"])
                ax.set_ylim(b["ymin"],b["ymax"])
                ax.set_zlim(b["zmin"],b["zmax"])

            # annot = ax.annotate("", xy=(0,0), xytext=(10,10),textcoords="offset points",
            # bbox=dict(boxstyle="round", fc="w"),
            # arrowprops=dict(arrowstyle="->",
            #                 connectionstyle="angle3", lw=2))
            # annot.set_visible(False)

            fig.canvas.draw()
            self.drawlock.acquire()

            self.is2draw = True

            self.drawlock.release()

        except Exception as pexc:
            print("3D Error: ", pexc)


    def zreset(self,event):
        DataPool.resetIndices()














