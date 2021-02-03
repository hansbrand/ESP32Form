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
    
    def selfdestroy(self):
        global canvas
        global toolbar
        toolbar.destroy()
        canvas.get_tk_widget().destroy()


    def __init__(self):
        pass

    def __init__(self, parent):
        global fig
        global canvas
        global s_time
        global ax
        global toolbar
        global annot



        fig = plt.Figure()

        
        parent.title("Graph3D")
        canvas = FigureCanvasTkAgg(fig, parent)
        canvas.get_tk_widget().pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)

        ax=fig.add_subplot(111,projection='3d')
        #ax = Axes3D(fig)

        fig.subplots_adjust(bottom=0.25)
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
            is3D = False
            x1 = []
            z1 = []
            m1 = []
            y1 = []
            x1,y1,z1,m1 = DC.getPointData()
            if (x1 == []) :
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
        except Exception as pexc:
            print("3D Error: ", pexc)


    def zreset(self,event):
        DataPool.resetIndices()














