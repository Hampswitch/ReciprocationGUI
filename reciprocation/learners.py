import Tkinter as tk
import math

class Static(tk.Frame):
    def __init__(self,parent):
        tk.Frame.__init__(self,parent)
        self.inputcanvas=tk.Canvas(self,width=110,height=210,borderwidth=1,background="white",relief=tk.RAISED)
        self.inputcanvas.pack(side=tk.TOP)
        self.inputcanvas.create_arc(-95,5,105,205,style=tk.ARC,start=270,extent=180)
        self.inputcanvas.bind("<Button-1>", self.__inputcanvasmouseclick)
        self.displaymove=tk.Label(self,text="Current move: 0")
        self.displaymove.pack(side=tk.TOP)
        tk.Label(self,width=30).pack(side=tk.TOP)
        self.move=0

    def __inputcanvasmouseclick(self,event):
        x=event.x
        y=event.y
        if x<5:
            x=5
        if x>105:
            x=105
        if y<5:
            y=5
        if y>205:
            y=205
        xc=(x-5)/100.0
        yc=(105-y)/100.0
        r=math.sqrt(xc**2+yc**2)
        self.move=yc/r
        x=5+100*xc/r
        y=105-100*yc/r
        self.inputcanvas.delete("dot")
        self.inputcanvas.create_oval(x-2,y-2,x+2,y+2,tags="dot",fill="black")
        self.displaymove["text"]="Current move: %f"%self.move

    def getResponse(self,move):
        return self.move


class AdHoc(tk.Frame):
    def __init__(self,parent):
        tk.Frame.__init__(self,parent)
        tk.Label(self, width=30).pack(side=tk.TOP)
        self.displabel=tk.Label(self,text="Current Range: (%.4f,%.4f)"%(0,1))
        self.displabel.pack(side=tk.TOP)
        self.threshhold=1.0
        self.nonthreshhold=0.0
        self.lastmove=None
        
    def getResponse(self,move):
        if self.lastmove==None:
            self.lastmove=0
            return 0
        else:
            if abs(move-math.sqrt(1-self.lastmove**2))<.01:
                self.threshhold=self.lastmove
            else:
                self.nonthreshhold=self.lastmove
                if math.sqrt(1-self.lastmove**2)+move>2*math.sqrt(1-self.threshhold**2):
                    self.threshhold=math.sqrt(1-((move+math.sqrt(1-self.lastmove**2))/2)**2)
            self.displabel['text']="Current Range: (%.4f,%.4f)"%(self.nonthreshhold,self.threshhold)
            self.lastmove=(self.threshhold+self.nonthreshhold)/2
            return self.lastmove
