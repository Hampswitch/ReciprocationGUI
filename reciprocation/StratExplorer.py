import Tkinter as tk
import math
import bisect
import teachingstrategies
import teachinglearning
import tkdict
import pandas
import meshutils
import linearstrat


def toCanvas(x,y,size=200,scale=2):
    return (size*.5+5+x*size*.25,size*.5+5-y*size*.25)

def fromCanvas(x,y,size=200,scale=2):
    return ((x-size*.5-5)/(size*.25),(size*.5+5-y)/(size*.25))

def checkbounds(p):
    x=min(2,max(p[0],-2))
    y=min(2,max(p[1],-2))
    return (x,y)

class functioncontrol(tk.Frame):
    def __init__(self,master,pointlist=None,command=None,loadbuttons=False):
        tk.Frame.__init__(self,master)
        self.displaycanvas=tk.Canvas(self, width=210, height=210, borderwidth=1, relief=tk.RAISED, background="white")
        self.displaycanvas.pack(side=tk.TOP)
        self.displaycanvas.bind("<Button-1>", self.__mousedown)
        self.displaycanvas.bind("<ButtonRelease-1>", self.__mouseup)
        self.displaycanvas.bind("<Control-Button-1>", self.__ctrlmouseclick)
        self.displaycanvas.bind("<B1-Motion>",self.__mousemove)
        self.displaycanvas.create_line(5,205,205,5,fill="light grey")
        self.displaycanvas.create_line(105,5,105,205,fill="grey")
        self.displaycanvas.create_line(55,5,55,205,fill="light grey")
        self.displaycanvas.create_line(155,5,155,205,fill="light grey")
        self.displaycanvas.create_line(5,55,205,55,fill="light grey")
        self.displaycanvas.create_line(5,105,205,105,fill="grey")
        self.displaycanvas.create_line(5,155,205,155,fill="light grey")
        if loadbuttons==True:
            buttonframe=tk.Frame(self)
            buttonframe.pack(side=tk.TOP)
            tk.Button(buttonframe,text="Mesh",command=self.setcontrolgridfunc).pack(side=tk.LEFT)
            tk.Button(buttonframe,text="Simple",command=self.setcontrolsimple).pack(side=tk.LEFT)
            tk.Button(buttonframe,text="Slope",command=self.setcontrolslopefunc).pack(side=tk.LEFT)
            tk.Button(buttonframe,text="Linear",command=self.setcontrollinearstrat).pack(side=tk.LEFT)
            self.controlframe=tk.Frame(self)
            self.controlframe.pack(side=tk.TOP)
        self.pointlist=pointlist
        if self.pointlist is None:
            self.pointlist=[]
        self.command=command
        self.__drawpointlist(self.pointlist,False)
        self.dragging=False

    def setcontrolsimple(self):
        self.threshholdvar = tk.DoubleVar()
        self.threshholdvar.set(.707)
        self.zerovar = tk.DoubleVar()
        self.negonevar = tk.DoubleVar()
        self.resolutionvar = tk.IntVar()
        self.resolutionvar.set(10)
        for widget in self.controlframe.winfo_children():
            widget.destroy()
        frame = tk.Frame(self.controlframe)
        frame.pack(side=tk.TOP)
        tk.Label(frame, text="Threshhold:").pack(side=tk.LEFT)
        tk.Entry(frame, textvariable=self.threshholdvar).pack(side=tk.LEFT)
        frame = tk.Frame(self.controlframe)
        frame.pack(side=tk.TOP)
        tk.Label(frame, text="Zero Response:").pack(side=tk.LEFT)
        tk.Entry(frame, textvariable=self.zerovar).pack(side=tk.LEFT)
        frame = tk.Frame(self.controlframe)
        frame.pack(side=tk.TOP)
        tk.Label(frame, text="Negative One Response:").pack(side=tk.LEFT)
        tk.Entry(frame, textvariable=self.negonevar).pack(side=tk.LEFT)
        frame = tk.Frame(self.controlframe)
        frame.pack(side=tk.TOP)
        tk.Label(frame, text="Resolution:").pack(side=tk.LEFT)
        tk.Entry(frame, textvariable=self.resolutionvar).pack(side=tk.LEFT)
        tk.Button(self.controlframe, text="Set Strategy", command=self.setpointlist).pack(side=tk.TOP)

    def setcontrolgridfunc(self):
        self.resolutionvar = tk.IntVar()
        self.resolutionvar.set(10)
        self.filenamevar = tk.StringVar()
        self.filenamevar.set("results/griditerator0.csv")
        self.scorevar = tk.StringVar()
        self.scorevar.set("score")
        self.scalevar = tk.DoubleVar()
        self.scalevar.set(.01)
        for widget in self.controlframe.winfo_children():
            widget.destroy()
        frame = tk.Frame(self.controlframe)
        frame.pack(side=tk.TOP)
        tk.Label(frame, text="Resolution:").pack(side=tk.LEFT)
        tk.Entry(frame, textvariable=self.resolutionvar).pack(side=tk.LEFT)
        frame = tk.Frame(self.controlframe)
        frame.pack(side=tk.TOP)
        tk.Label(frame, text="Filename:").pack(side=tk.LEFT)
        tk.Entry(frame, textvariable=self.filenamevar).pack(side=tk.LEFT)
        frame = tk.Frame(self.controlframe)
        frame.pack(side=tk.TOP)
        tk.Label(frame, text="Score:").pack(side=tk.LEFT)
        tk.Entry(frame, textvariable=self.scorevar).pack(side=tk.LEFT)
        frame = tk.Frame(self.controlframe)
        frame.pack(side=tk.TOP)
        tk.Label(frame, text="Correct:").pack(side=tk.LEFT)
        tk.Entry(frame, textvariable=self.scalevar).pack(side=tk.LEFT)
        self.fixedvars = tkdict.tkdict(self)
        self.fixedvars.pack(side=tk.TOP)
        tk.Button(self, text="Set Strategy", command=self.setmesh).pack(side=tk.TOP)

    def setcontrollinearstrat(self):
        pass

    def setcontrolslopefunc(self):
        self.threshholdvar = tk.DoubleVar()
        self.threshholdvar.set(.707)
        self.resolutionvar = tk.IntVar()
        self.resolutionvar.set(10)
        for widget in self.controlframe.winfo_children():
            widget.destroy()
        frame = tk.Frame(self.controlframe)
        frame.pack(side=tk.TOP)
        tk.Label(frame, text="Threshhold:").pack(side=tk.LEFT)
        tk.Entry(frame, textvariable=self.threshholdvar).pack(side=tk.LEFT)
        frame = tk.Frame(self.controlframe)
        frame.pack(side=tk.TOP)
        tk.Label(frame, text="Resolution:").pack(side=tk.LEFT)
        tk.Entry(frame, textvariable=self.resolutionvar).pack(side=tk.LEFT)
        tk.Button(self.controlframe, text="Set Strategy", command=self.setslopestrat).pack(side=tk.TOP)

    def setpointlist(self):
        try:
            strat=teachingstrategies.simpleteacher(self.threshholdvar.get(),self.zerovar.get(),self.negonevar.get())
        except ValueError:
            t=self.threshholdvar.get()
            self.zerovar.set(2*math.sqrt(1-t*t)-1.01)
            strat = teachingstrategies.simpleteacher(self.threshholdvar.get(), self.zerovar.get(), self.negonevar.get())
        resolution=self.resolutionvar.get()
        x=(resolution-1)/2.0
        self.pointlist=[(2*(i-x)/x,2*strat.respond((i-x)/x)) for i in range(resolution)]
        self.__drawpointlist(self.pointlist)

    def setslopestrat(self):
        strat=linearstrat.slopestrat(self.threshholdvar.get())
        resolution=self.resolutionvar.get()
        x=(resolution-1)/2.0
        self.pointlist=[(2*(i-x)/x,2*strat.respond((i-x)/x)) for i in range(resolution)]
        self.__drawpointlist(self.pointlist)

    def setmesh(self):
        resolution=self.resolutionvar.get()
        x = (resolution - 1) / 2.0
        filename=self.filenamevar.get()
        data = pandas.read_csv(filename)
        for k,v in self.fixedvars.get().items():
            if not v in data[k].unique():
                raise ValueError("Value not found in {}: {}".format(k,v))
        fixedvalues = meshutils.fixdict(data, self.fixedvars.get())
        mesh = meshutils.getmesh(data, fixedvalues, "startmove", "response", self.scorevar.get())
        mesh=meshutils.correctmesh(mesh,self.scalevar.get())
        meshutils.plotmesh(mesh,"startmove","response","score")
        meshfunc=teachinglearning.mkmeshfunc(filename,score_col=self.scorevar.get(),fixedvalues=self.fixedvars.get(),scalecorrect=self.scalevar.get())
        grid=[(i-x)/x for i in range(resolution)]
        self.pointlist = [(2 * (i - x) / x, 2 * max([(meshfunc((i-x)/x,g),g) for g in grid])[1]) for i in range(resolution)]
        self.__drawpointlist(self.pointlist)

    def getValue(self, x):
        if x==2 and len(self.pointlist)>0 and self.pointlist[-1][0]==2:
            return self.pointlist[-1][1]
        if x==-2 and len(self.pointlist)>0 and self.pointlist[0][0]==-2:
            return self.pointlist[0][1]
        pos=bisect.bisect([-3]+[y[0] for y in self.pointlist]+[3],x)
        points=([(-2,-2)]+self.pointlist+[(2,2)])[pos-1:pos+1]
        wt=(x-points[0][0])/(points[1][0]-points[0][0])
        return (1-wt)*points[0][1]+wt*points[1][1]

    def __mousedown(self,event):
        (x,y)=fromCanvas(event.x,event.y)
        for p in self.pointlist:
            if (x-p[0])**2+(y-p[1])**2<.01:
                self.dragging=True
                self.pointlist.remove(p)

    def __mousemove(self,event):
        if self.dragging:
            pl=[x for x in self.pointlist]+[checkbounds(fromCanvas(event.x,event.y))]
            pl.sort()
            self.__drawpointlist(pl)

    def __mouseup(self,event):
        if self.dragging:
            (x,y)=checkbounds(fromCanvas(event.x,event.y))
            self.pointlist.append((x,y))
            self.pointlist.sort()
            self.dragging=False
            self.__drawpointlist(self.pointlist)

    def __ctrlmouseclick(self,event):
        (x,y)=checkbounds(fromCanvas(event.x,event.y))
        deleted=False
        for p in self.pointlist:
            if (x-p[0])**2+(y-p[1])**2<.01:
                deleted=True
                self.pointlist.remove(p)
        if not deleted:
            self.pointlist.append((x,y))
            self.pointlist.sort()
        self.__drawpointlist(self.pointlist)

    def __drawpointlist(self,pointlist,updateDisplay=True):
        self.displaycanvas.delete("lines")
        for p1,p2 in zip([(-2,-2)]+pointlist,pointlist+[(2,2)]):
            (x1,y1)=toCanvas(p1[0],p1[1])
            (x2,y2)=toCanvas(p2[0],p2[1])
            self.displaycanvas.create_line(x1,y1,x2,y2,tags="lines")
        for p in pointlist:
            (x,y)=toCanvas(p[0],p[1])
            self.displaycanvas.create_oval(x-1,y-1,x+1,y+1,tags="lines")
        if updateDisplay and self.command is not None:
            backup=self.pointlist
            self.pointlist=pointlist
            self.command()
            self.pointlist=backup

class giftDisplay(tk.Frame):
    def __init__(self,master,command=None):
        tk.Frame.__init__(self,master)
        self.displaycanvas=tk.Canvas(self, width=410, height=410, borderwidth=1, relief=tk.RAISED, background="white")
        self.displaycanvas.create_oval(5,5,405,405,outline="grey")
        self.displaycanvas.create_oval(105,105,305,305,outline="grey")
        self.displaycanvas.create_line(5,205,405,205,fill="grey")
        self.displaycanvas.create_line(5, 105, 405, 105, fill="light grey")
        self.displaycanvas.create_line(5, 305, 405, 305, fill="light grey")
        self.displaycanvas.create_line(205, 5, 205, 405, fill="grey")
        self.displaycanvas.create_line(105, 5, 105, 405, fill="light grey")
        self.displaycanvas.create_line(305, 5, 305, 405, fill="light grey")
        self.displaycanvas.pack(side=tk.TOP)
        tk.Label(self,text="Opponent Move").pack(side=tk.TOP)
        self.oppmove=tk.Scale(self, from_=-1, to=1, resolution=.01,orient=tk.HORIZONTAL,length=200,command=command)
        self.oppmove.pack(side=tk.TOP)
        frame=tk.Frame(self)
        frame.pack(side=tk.TOP)
        tk.Label(self,text="Response Function").pack(side=tk.TOP)
        self.strat=teachingstrategies.simpleteacher(.95,-1,-1)
        self.stratcontrol=functioncontrol(frame,pointlist=[(i/20.0,2*self.strat.respond(i/40.0)) for i in range(-40,42,2)],loadbuttons=True)
        self.stratcontrol.pack(side=tk.LEFT)
        self.funccanvas = tk.Canvas(frame, width=210, height=210, borderwidth=1, relief=tk.RAISED, background="white")
        self.funccanvas.pack(side=tk.LEFT)
        self.funccanvas.create_line(5, 105, 205, 105)
        self.funccanvas.create_line(105, 5, 105, 205)


    def _getstrat(self):
        result=self.stratcontrol.pointlist
        return teachingstrategies.reciprocal([(p[0] / 2, p[1] / 2) for p in result])

    def drawprefs(self,xpref,ypref,xatt,yatt,xoppwt,yoppwt,xenvy,yenvy):
        points=3600
        self.displaycanvas.delete("pref")
        self.funccanvas.delete("pref")
        for a in [2*math.pi*x/points for x in range(points)]:
            xpayoff=2*math.sin(a)
            ypayoff=2*math.cos(a)
            xvalue=xpref.getValue(xpayoff)
            yvalue=ypref.getValue(ypayoff)
            xoppvalue=xatt.getValue(ypayoff)
            yoppvalue=yatt.getValue(xpayoff)
            xenvyvalue=max(0,(ypayoff-xpayoff)*xenvy)
            yenvyvalue=max(0,(xpayoff-ypayoff)*yenvy)
            (x,y)=toCanvas(xvalue*(1-xoppwt)+xoppvalue*xoppwt-xenvyvalue,yvalue*(1-yoppwt)+yoppvalue*yoppwt-yenvyvalue,400)
            self.displaycanvas.create_oval(x-1,y-1,x+1,y+1,tags="pref")
        strat=self._getstrat()
        pcoords=[]
        lcoords=[]
        l2coords=[]
        for a in [2*math.pi*x/points-math.pi/2 for x in range(points)]:
            xpayoff=math.sin(a)
            ypayoff=math.cos(a)
            response=strat.respond(xpayoff)
            xpayoff=xpayoff+math.sqrt(1-response**2)
            ypayoff=ypayoff+response
            xvalue = xpref.getValue(xpayoff)
            yvalue = ypref.getValue(ypayoff)
            xoppvalue = xatt.getValue(ypayoff)
            yoppvalue = yatt.getValue(xpayoff)
            xenvyvalue=max(0,(ypayoff-xpayoff)*xenvy)
            yenvyvalue=max(0,(xpayoff-ypayoff)*yenvy)
            (x, y) = toCanvas(xvalue * (1 - xoppwt) + xoppvalue * xoppwt-xenvyvalue, yvalue * (1 - yoppwt) + yoppvalue * yoppwt-yenvyvalue, 400)
            pcoords.append(x)
            pcoords.append(y)
            if math.cos(a)>=0:
                if math.sin(a)>=0:
                    lcoords.append(x)
                    lcoords.append(y)
                else:
                    l2coords.append(x)
                    l2coords.append(y)
        self.displaycanvas.create_polygon(pcoords,fill="light grey",tags="pref",width=1,outline="black")
        self.displaycanvas.create_line(lcoords,fill="green",width=2,tags="pref")
        self.displaycanvas.create_line(l2coords,fill="red",width=2,tags="pref")
        m=self.oppmove.get()
        r=strat.respond(m)
        (x,y)=toCanvas(m,math.sqrt(1-m**2),400)
        self.displaycanvas.create_oval(x-2,y-2,x+2,y+2,fill="red",tags="pref")
        (x,y)=toCanvas(math.sqrt(1-r**2),r,400)
        self.displaycanvas.create_oval(x - 2, y - 2, x + 2, y + 2, fill="green",tags="pref")
        (x,y)=toCanvas(m+math.sqrt(1-r**2),r+math.sqrt(1-m**2),400)
        self.displaycanvas.create_oval(x - 2, y - 2, x + 2, y + 2, fill="yellow",tags="pref")
        linecoords=[]
        for i in range(201):
            xpayoff=(i-100.0)/100.0
            ypayoff=math.sqrt(1-xpayoff**2)
            response=strat.respond(xpayoff)
            ypayoff=ypayoff+response
            yvalue=ypref.getValue(ypayoff)
            yoppvalue=yatt.getValue(xpayoff)
            yenvyvalue=max(0,(xpayoff-ypayoff)*yenvy)
            linecoords.append(5+(xpayoff+1.0)*100)
            linecoords.append(205-50*(yvalue*(1-yoppwt)+yoppvalue*yoppwt-yenvyvalue+2))
        self.funccanvas.create_line(linecoords,tags="pref")



class stratexplorer(tk.Frame):
    def __init__(self,master):
        tk.Frame.__init__(self, master)
        leftprefs=tk.Frame(self)
        leftprefs.pack(side=tk.LEFT)
        tk.Label(leftprefs,text="X Player Preferences").pack(side=tk.TOP)
        self.xpref=functioncontrol(leftprefs,command=self.__showprefs)
        self.xpref.pack(side=tk.TOP)
        tk.Label(leftprefs, text="Own Payoff Preferences").pack(side=tk.TOP)
        self.xatt=functioncontrol(leftprefs,[(-2,0),(2,0)],command=self.__showprefs)
        self.xatt.pack(side=tk.TOP)
        tk.Label(leftprefs, text="Opponent Payoff Preferences").pack(side=tk.TOP)
        self.xoppwt = tk.Scale(leftprefs, from_=0, to=1, resolution=.01,orient=tk.HORIZONTAL,command=lambda x:self.__showprefs())
        self.xoppwt.set(0)
        self.xoppwt.pack(side=tk.TOP)
        tk.Label(leftprefs, text="Opponent Relative Weight").pack(side=tk.TOP)
        self.xenvy = tk.Scale(leftprefs, from_=0, to=1, resolution=.01, orient=tk.HORIZONTAL,
                              command=lambda x: self.__showprefs())
        self.xenvy.set(0)
        self.xenvy.pack(side=tk.TOP)
        tk.Label(leftprefs, text="Envy").pack(side=tk.TOP)
        self.display=giftDisplay(self,lambda x:self.__showprefs())
        self.display.pack(side=tk.LEFT)
        self.display.stratcontrol.command=self.__showprefs
        rightprefs=tk.Frame(self)
        rightprefs.pack(side=tk.LEFT)
        tk.Label(rightprefs,text="Y Player Preferences").pack(side=tk.TOP)
        self.ypref=functioncontrol(rightprefs,command=self.__showprefs)
        self.ypref.pack(side=tk.TOP)
        tk.Label(rightprefs, text="Own Payoff Preferences").pack(side=tk.TOP)
        self.yatt=functioncontrol(rightprefs,[(-2,0),(2,0)],command=self.__showprefs)
        self.yatt.pack(side=tk.TOP)
        tk.Label(rightprefs, text="Opponent Payoff Preferences").pack(side=tk.TOP)
        self.yoppwt=tk.Scale(rightprefs,from_=0,to=1,resolution=.01,orient=tk.HORIZONTAL,command=lambda x:self.__showprefs())
        self.yoppwt.set(0)
        self.yoppwt.pack(side=tk.TOP)
        tk.Label(rightprefs,text="Opponent Relative Weight").pack(side=tk.TOP)
        self.yenvy=tk.Scale(rightprefs,from_=0,to=1,resolution=.01,orient=tk.HORIZONTAL,command=lambda x:self.__showprefs())
        self.yenvy.set(0)
        self.yenvy.pack(side=tk.TOP)
        tk.Label(rightprefs,text="Envy").pack(side=tk.TOP)

    def __showprefs(self):
        self.display.drawprefs(self.xpref,self.ypref,self.xatt,self.yatt,self.xoppwt.get(),self.yoppwt.get(),self.xenvy.get(),self.yenvy.get())


if __name__=="__main__":
    master = tk.Tk()
    stratexplorer(master).pack(side=tk.TOP)
    tk.mainloop()