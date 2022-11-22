from tkinter import *
from tkinter import messagebox
from tkhtmlview import HTMLLabel as html
from tkinterweb import HtmlFrame
import htmlsource 
import Exec

class App (object):
    def __init__(self):
        self.root=Tk()
        self.root.geometry("900x650")
        self.root.title("JacksonInn")
        self.variable=StringVar()
        self.waiting = 600
        self.i=-1
        self.body = HtmlFrame(self.root)
        output = Exec.initialize()
        self.systems = output
        self.body.load_html(f"{htmlsource.header()}{htmlsource.body(self.i,self.systems)}{htmlsource.end()}")
    def grid(self):
        self.body.pack(fill="both", expand=True) #attach the HtmlFrame widget to the parent window
    def cycle(self):
        self.i=self.i+1
        self.variable.set(str(self.i))
        Exec.ciclo(self.i)
        self.body.load_html(f"{htmlsource.header()}{htmlsource.body(self.i,self.systems)}{htmlsource.end()}")
        if self.i < Exec.clockEnd-1:
            self.root.after(self.waiting,self.cycle)
        else:
            printlogs()
    def run(self):
        self.grid()
        self.root.after(0,self.cycle)
        self.root.mainloop()
def printlogs():
    logfile = ""
    for log in Exec.logs:
        logfile += f"{log}\n"
    print(logfile)
if __name__=='__main__':
    App().run()