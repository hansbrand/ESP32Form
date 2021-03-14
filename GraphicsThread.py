import tkinter as tk
import threading
from threading import Thread
from Graph3D import Graph3D
from time import sleep
import sys



class StoppableThread(threading.Thread):
    """Thread class with a stop() method. The thread itself has to check
    regularly for the stopped() condition."""

    def __init__(self):
        print( "base init", file=sys.stderr )
        super(StoppableThread, self).__init__()
        self._stopper = threading.Event()          # ! must not use _stop

    def stopit(self):                              #  (avoid confusion)
        print( "base stop()", file=sys.stderr )
        self._stopper.set()                        # ! must not use _stop

    def stopped(self):
        return self._stopper.is_set()              # ! must not use _stop



class GraphicsThread(StoppableThread):
    """GraphicsThread"""
    
    # class GWindow(tk.Frame):
    #     def __init__(self, master=None):
    #         super().__init__(master)
    #         self.screen_width = self.master.winfo_screenwidth()
    #         self.screen_height = self.master.winfo_screenheight()



    def __init__(self):
      StoppableThread.__init__(self)
      print( "thread init", file=sys.stderr )
      self.current_message=""

    def run(self,root,w,h):
        root = tk.Tk()
        root.title("GRAPH3D")

        #newwin = self.GWindow(root)
        # newwin = tk.Toplevel(root, 
        #    width  =w,
        #    height = h)
        #newwin = tk.Frame(root, width=w, height=h, background="bisque")
        #newwin.geometry(str(w) + "x" + str(h))
        newwin = tk.Frame(root)
        #newwin.update()

        graph3D = Graph3D(newwin,w,h)
        newwin.pack()
        #root.mainloop()
        
        newwin.update()
        root.iconify()
        while True:
            if graph3D.Is2Draw():
                #if root.state() == 'normal':
                    graph3D.drawDia(True)
                    newwin.update()
            sleep(15)


        pass


def startGraphics(master,w,h): 


    gthread = GraphicsThread()
    sth2 = Thread(target=gthread.run, args=(None,w,h),daemon=True)
    sth2.start()






