import random
import matplotlib
import tkinter as Tk
import matplotlib.pyplot as plt
#import DataPool
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
#import DataContainer as DC
#from  PIL import Im
import io
#import buildGUI
from PIL import Image
import time
#import LaserApplication

matplotlib.use('TkAgg')




fig = None
canvas = None
ax = None
ax2 = None
s_time = None
annot = None
norm = None


class tempGraph(Tk.Frame):
    """description of class"""

    limit = None
    anotlist = None
    
    def __init__(self):
        pass

    def selfdestroy(self):
        global canvas
        global toolbar
        global ani
        toolbar.destroy()
        ani = None
        canvas.get_tk_widget().destroy()


    def __init__(self, parent):
        global fig
        global canvas
        global s_time
        global ax
        global ax2
        global toolbar
        global annot
        global currentax
        global norm

        fig = plt.Figure(figsize=(3, 2), dpi=80)

        canvas = FigureCanvasTkAgg(fig, parent)
        canvas.get_tk_widget().pack(side=Tk.BOTTOM, fill=Tk.BOTH, expand=True)
        canvas.draw()

        ax=fig.add_subplot(111,facecolor = "lightgreen",autoscaley_on = True)
        norm = plt.Normalize(1,8)
   
        fig.subplots_adjust(bottom=0)

        canvas._tkcanvas.pack(side=Tk.BOTTOM, fill=Tk.BOTH, expand=True)
        self.sc0 = None

        fig.canvas.mpl_connect("motion_notify_event", self.hover)
        #self.anotlist = None






    def drawDia(self,changed):
        global fig
        global canvas
        global s_time
        global ax
        global annot
        global norm

        try:
            
            sc = DC.dc["0"]["templist"]
            c1 = []
            if sc == []:
                return
            x1 = sc[0]
            y1 = sc[1]

            self.limit = len(x1)
            for x in x1:
                c1 += ["cyan"]
            ax.clear()
            #ax.xaxis.set_major_locator(plt.MaxNLocator(2))
            ax.yaxis.set_major_locator(plt.MaxNLocator(2))
            #ax.axis('off')
            ax.axes.get_xaxis().set_visible(False)
            ax.axes.get_yaxis().set_visible(True)
            ax.plot(x1,y1, linestyle="-.")
            #self.sc0 = ax.scatter(x1,y1,c="blue",norm = norm)

            #annot = ax.annotate("", xy=(0,0), xytext=(0,-20),textcoords="offset points",
            #                    bbox=dict(boxstyle="round", fc="w"),
            #                    arrowprops=dict(arrowstyle="->",
            #                                    connectionstyle="angle3", lw=2))
            #annot.set_visible(False)

            ax.grid(b=False)

            sc = DC.dc["180"]["templist"]
            if sc == []:
                return
            x2 = sc[0]
            y2 = sc[1]
            for x in x2:
                c1 += ["magenta"]

            x1 += x2
            y1 +=y2
            ax.plot(x2,y2, linestyle=":")

            self.anotlist = []
            for e in DC.dc["0"]["templistannotation"]:
                self.anotlist += e 
            for e in DC.dc["180"]["templistannotation"]:
                self.anotlist += e 

            self.sc0 = ax.scatter(x1, y1, c=c1, norm = norm,s=[100])

            annot = ax.annotate("", xy=(-50,0), xytext=(-40,20),textcoords="offset points",
                                bbox=dict(boxstyle="round", fc="w"),
                                arrowprops=dict(arrowstyle="->",
                                                connectionstyle="angle3", lw=2))
            annot.set_visible(False)

            fig.tight_layout()
            fig.canvas.draw()

        except Exception as pexc:
            print("Linegraph Error: ", pexc)





    def update_annot(self,ind):
        global annot
        global currentax

        index = ind["ind"][0]

        

        pointinfo = self.anotlist[index][0]
        pcolor =  self.anotlist[index][1]
        pos = self.sc0.get_offsets()[index]
            
        annot.xy = pos
        #text = "{}, {}".format("".join(pointinfo), 
        #                        "".join(str(pcolor)))
        text = "{}".format("".join(pointinfo))
        annot.set_text(text)
            
        #annot.get_bbox_patch().set_facecolor(cmap(norm(c[ind["ind"][0]])))
        annot.get_bbox_patch().set_facecolor(pcolor)

        annot.get_bbox_patch().set_alpha(0.8)


        return


    def hover(self,event):
        global fig
        global annot
        global annot180

        if (annot == None):     return
        if (self.sc0 == None):  return
        if (self.anotlist == None):  return


        vis = annot.get_visible()
        if event.inaxes == ax:
            cont, ind = self.sc0.contains(event)
            if cont:
                self.update_annot(ind)
                annot.set_visible(True)
                fig.canvas.draw_idle()
            else:
                if vis:
                    annot.set_visible(False)
                    fig.canvas.draw_idle()











    


