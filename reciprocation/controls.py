import Tkinter as tk
import math
import teachingstrategies
import ScrolledText
import scipy.stats
import numpy

"""
Controls for the game simulator found in gui
"""

def display_x(val):
    return 5 + 100 * (val + 2)


def display_y(val):
    return 5 + 100 * (2 - val)


def input_x(val):
    return 105 + 100 * (val + 1)


def input_y(val):
    return 5 + 100 * (1 - val)

preset_strats={
    "greedystrat":[(-1,-1),(0,-1),(99.0/101,20.0/101),(1,20.0/101)],
    "generousstrat":[(-1,0),(0,0),(20.0/101,99.0/101),(math.sqrt(2)/2,math.sqrt(2)/2),(1,math.sqrt(2)/2)],
    "fairstrat":[(-1,-1),(math.sqrt(2)/2,math.sqrt(2)/2),(1,math.sqrt(2)/2)],
    "limitsolo":[(0,0),(math.sqrt(.75),.5)],
    "acceptsolo":[(0,0),(.5,math.sqrt(.75))],
    "s1":[(-1, -0.7794639575615129), (-0.8446552157500906, -0.9896224573935959), (-0.04203693688186024, -0.9170200514502815), (0.3510608848208704, -0.8159345253619382), (1, 0.7048261170971563)],
    "s2":[(-1, -0.820658850873681), (-0.9388296377056126, -0.9475976296106516), (0.39143535047383404, -0.8419787806513155), (0.8514087018229608, 0.48877226280432395), (1, 0.4515249795430891)],
    "s3":[(-1, -0.9134345719749818), (0.4236175836682907, -0.8845488376033471), (0.8153289047375804, 0.3626214924362167), (0.8369542361652093, 0.45564112596765494), (1, 0.4648647308904554)],
    "s4":[(-1, 0.04101252498194046), (-0.9920970530580304, -0.9641914753664058), (0.37030288569952624, -0.9146097201275217), (0.9062984897655945, 0.5660902361348822), (1, 0.4421778147539235)],
    "s5":[(-1, -0.9761349715775307), (-1, 0.21923177138019725), (-0.9797380734730485, -0.9321715037263696), (0.3241511270453441, -0.9186960314771592), (1, 0.709389210142102)],
    "s6":[(-1, -0.9047392502040277), (0.3525119702543211, -0.9181975671072078), (0.6985114441189911, -0.10327305598856962), (0.8178454560344496, 0.46275687119636416), (1, 0.3310036970940886)],
    "s7":[(-1, -0.8584055212210779), (-0.6585442602967201, -0.9768594500573419), (0.36302843670396673, -0.8518667778347204), (1, 0.6996845288050685), (1, 0.8219028705047451)],
    "s8":[(-1, -1), (-1, -0.2767464783899173), (-0.9955157381714942, -0.9246701029640717), (0.309194893708672, -0.9249738025093096), (1, 0.7129284207038739)],
    "s9":[(-1, -0.9148413563693988), (-0.967102262946209, -0.9760318823830801), (0.3069104761628629, -0.9122988313592347), (1, 0.6990700452520512), (1, 0.9404837736925028)],
    "s0":[(-1, -0.9414330936956736), (-0.11795087245717331, -0.9600000247048686), (0.32690024189074407, -0.823531271290028), (1, 0.701988006876726), (1, 0.9893988199875637)]
}

class ReciprocalStrategySelector(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.displaycanvas = tk.Canvas(self, width=410, height=410, borderwidth=1, relief=tk.RAISED, background="white")
        self.displaycanvas.pack(side=tk.TOP)
        self.displaycanvas.create_line(0, 205, 410, 205)
        self.displaycanvas.create_line(205, 0, 205, 410)
        self.displaycanvas.create_line(0, 105, 410, 105, fill="darkgrey")
        self.displaycanvas.create_line(0, 305, 410, 305, fill="darkgrey")
        self.displaycanvas.create_line(105, 0, 105, 410, fill="darkgrey")
        self.displaycanvas.create_line(305, 0, 305, 410, fill="darkgrey")
        self.displaycanvas.create_oval(5, 5, 405, 405)
        self.displaycanvas.create_oval(105, 105, 305, 305)
        self.inputcanvas = tk.Canvas(self, width=310, height=310, borderwidth=1, relief=tk.RAISED, background="white")
        self.inputcanvas.pack(side=tk.TOP)
        self.inputcanvas.create_arc(-95, 5, 105, 205, style=tk.ARC, start=270, extent=180)
        self.inputcanvas.create_arc(105, 205, 305, 405, style=tk.ARC, start=0, extent=180)
        self.inputcanvas.create_line(105, 5, 105, 205)
        self.inputcanvas.create_line(105, 5, 305, 5)
        self.inputcanvas.create_line(105, 205, 305, 205)
        self.inputcanvas.create_line(305, 5, 305, 205)
        self.inputcanvas.create_line(205, 5, 205, 205)
        self.inputcanvas.create_line(105, 105, 305, 105)
        self.inputcanvas.create_line(105, 205, 305, 5)
        self.inputcanvas.create_arc(105, 5, 305, 205, style=tk.ARC, start=0, extent=90)
        self.inputcanvas.bind("<Button-1>", self.__inputcanvasmouseclick)
        buttonpanel = tk.Frame(self)
        buttonpanel.pack(side=tk.TOP)
        tk.Button(buttonpanel, text="Clear", command=self.__clear).pack(side=tk.LEFT)
        self.stratlist = []
        self.bias=None
        for s in preset_strats.keys():
            tk.Button(buttonpanel, text=s,command=(lambda x: lambda: self.loadstrat(x,"preset"))(s)).pack(side=tk.LEFT)
        self.initmove=0

    def __clear(self):
        self.displaycanvas.delete("dots")
        self.inputcanvas.delete("dots")
        self.inputcanvas.delete("filldots")
        self.stratlist = []

    def loadstrat(self,name,strattype):
        self.__clear()
        if strattype=="preset":
            points=preset_strats[name]
        for (x,y) in points:
            print (x,y)
            self.addpoint(x,y)

    def add_display_dot(self, x, y, **kwargs):
        self.displaycanvas.create_oval(display_x(x) - 1, display_y(y) - 1, display_x(x) + 1, display_y(y) + 1, **kwargs)

    def add_input_dot(self, x, y, **kwargs):
        self.inputcanvas.create_oval(input_x(x) - 1, input_y(y) - 1, input_x(x) + 1, input_y(y) + 1, **kwargs)

    def __inputcanvasmouseclick(self, event):
        x = event.x
        y = event.y
        if x < 105:
            x = 105
        if x > 305:
            x = 305
        if y < 5:
            y = 5
        if y > 205:
            y = 205
        xc = (x - 205) / 100.0
        yc = (105 - y) / 100.0
        print(xc, yc)
        self.addpoint(xc,yc)

    def addpoint(self,xc,yc):
        brange=[x/100.0 for x in range(1,100)]
        self.add_input_dot(xc,yc,tags="dots",fill="blue")
        self.stratlist.append((xc, yc))
        self.stratlist.sort()
        self.displaycanvas.delete("dots")
        self.inputcanvas.delete("filldots")
        # Dots which describe the strategy on the display
        for xp, yo in self.stratlist:
            self.add_display_dot(xp + math.sqrt(1 - yo * yo), math.sqrt(1 - xp * xp) + yo, tags="dots", fill="blue")
        # Dots interpolating the strategy on the display and input
        for first, second in zip(self.stratlist[:-1], self.stratlist[1:]):
            for b in brange:
                xp = b * first[0] + (1 - b) * second[0]
                if self.bias is None:
                    yo=b*first[1]+(1-b)*second[1]
                elif self.bias==0:
                    yo = teachingstrategies.interpolate(first, second, b * first[0] + (1 - b) * second[0])
                else:
                    yo = teachingstrategies.biasedinterpolate(first, second, b * first[0] + (1 - b) * second[0], self.bias)
                self.add_display_dot(xp + math.sqrt(1 - yo * yo), math.sqrt(1 - xp * xp) + yo, tags="dots", fill="blue")
                self.add_input_dot(xp,yo,tags="filldots")
        # Add suffix dots to describe the strategy after the last dot
        self.suffixstrat = []
        for b in brange:
            xp = self.stratlist[-1][0] * (1 - b) + b
            self.add_display_dot(2 * xp, 2 * math.sqrt(1 - xp * xp), tags="dots", fill="red")
            self.add_input_dot(xp, math.sqrt(1 - xp * xp), tags="filldots", fill="red")
            self.suffixstrat.append((xp, math.sqrt(1 - xp * xp)))
        # Add prefix dots to describe the strategy before the first dot
        self.prefixstrat = []
        for b in [x for x in [(y - 10.0) / 10 for y in range(21)] if x < self.stratlist[0][0]]:
            xp = b
            yo = min(self.stratlist[0][1],
                     self.stratlist[0][1] + math.sqrt(1 - self.stratlist[0][0] ** 2) - math.sqrt(1 - b ** 2))
            self.add_display_dot(xp + math.sqrt(1 - yo * yo), math.sqrt(1 - xp * xp) + yo, tags="dots", fill="red")
            self.add_input_dot(xp, yo, tags="filldots", fill="red")
            self.prefixstrat.append((xp, yo))
        # Add achievableset polygon to the display
        if self.stratlist[0][0]==-1 and self.stratlist[-1][0]==1:
            recip=teachingstrategies.reciprocal(self.stratlist)
            achieveset=recip.getachievableset(360)
            achieveset=[(display_x(p[0]),display_y(p[1])) for p in achieveset]
            self.displaycanvas.create_polygon(achieveset, fill="green", tags="dots", width=1, outline="black")

    def getstrat(self):
        return self.prefixstrat + self.stratlist + self.suffixstrat

    def getResponse(self,move):
        if move is None:
            return self.initmove
        strat=teachingstrategies.reciprocal(self.stratlist, self.bias).respond(move)
        return strat

def plotpoint(x,y,canvas,size,xmin=-1.0,xmax=1.0,ymin=-1.0,ymax=1.0,dotsize=1,**kwargs):
    x=min(x,xmax)
    x=max(x,xmin)
    y=min(y,ymax)
    y=max(y,ymin)
    xcoord=5+size*(x-xmin)/(xmax-xmin)
    ycoord=5+size*(ymax-y)/(ymax-ymin)
    canvas.create_oval(xcoord - dotsize, ycoord - dotsize, xcoord + dotsize,
                                   ycoord + dotsize, **kwargs)

class Histogram(tk.Frame):
    def __init__(self,parent,minval,maxval,bucketcount):
        tk.Frame.__init__(self,parent)
        self.valuedict={}
        self.bucketcount=bucketcount
        self.display=tk.Canvas(self,width=210,height=210,borderwidth=1,relief=tk.RAISED,background="white")
        self.display.pack(side=tk.TOP)
        self.keyfunc=lambda x: int(math.floor(bucketcount*(min(maxval,max(minval,x))-minval)/float(maxval-minval)))

    def addvalue(self,value):
        k=self.keyfunc(value)
        self.valuedict[k]=self.valuedict.get(k,0)+1
        maxcount=max(self.valuedict.values())
        self.display.delete(tk.ALL)
        for i in range(self.bucketcount):
            xfrom=5+i*200.0/self.bucketcount
            xto=5+(i+1)*200.0/self.bucketcount
            yfrom=205
            yto=205-200.0*self.valuedict.get(i,0)/maxcount
            self.display.create_rectangle(xfrom,yfrom,xto,yto)

class StratEstimatorControl(tk.Frame):
    def __init__(self,parent):
        tk.Frame.__init__(self,parent)
        tk.Label(self,text="Teacher Model").pack(side=tk.TOP)
        self.teacherdisplay=tk.Canvas(self,width=210,height=210,borderwidth=1,relief=tk.RAISED,background="white")
        self.teacherdisplay.pack(side=tk.TOP)
        tk.Label(self,text="Learner Model").pack(side=tk.TOP)
        self.learnerdisplay=Histogram(self,-2,2,100)
        self.learnerdisplay.pack(side=tk.TOP)
        self.lastplayermove=None
        self.lastopponentmove=None
        self.skewlabel=tk.Label(self,text="Skew Measure: ")
        self.varlabel=tk.Label(self,text="Var Measure: ")
        self.skewlabel.pack(side=tk.TOP)
        self.varlabel.pack(side=tk.TOP)
        self.payofflist=[]
        self.responselist=[]

    def addplayermove(self,value):
        self.lastplayermove=value
        if self.lastopponentmove is not None:
            plotpoint(self.lastopponentmove,self.lastplayermove,self.teacherdisplay,200)
            self.responselist.append((self.lastopponentmove,value))
            if len(self.responselist)>1:
                self.varlabel.config(text="Var Measure: "+str(numpy.cov(zip(*self.responselist))))

    def addopponentmove(self,value):
        self.lastopponentmove=value
        if self.lastplayermove is not None:
            payoff=self.lastopponentmove+math.sqrt(1-self.lastplayermove**2)
            self.learnerdisplay.addvalue(payoff)
            self.payofflist.append(payoff)
            if len(self.responselist)>1:
                skew=scipy.stats.skew(self.payofflist)
                pmin=min(self.payofflist)
                prange=max(self.payofflist)-pmin
                normskew=scipy.stats.skew([(p-pmin)/prange for p in self.payofflist])
                self.skewlabel.config(text="Skew Measure: {:.4} ({:.4})".format(skew,normskew))

class GameDisplay(tk.Frame):
    def __init__(self, parent,discount=None):
        self.discountfactor=1.0 if discount is None else 1.0-discount
        self.curdiscount=1.0
        tk.Frame.__init__(self, parent)
        displayframe=tk.Frame(self)
        displayframe.pack(side=tk.TOP)
        self.leftestimator=StratEstimatorControl(displayframe)
        self.leftestimator.pack(side=tk.LEFT)
        self.displaycanvas = tk.Canvas(displayframe, width=410, height=410, borderwidth=1, relief=tk.RAISED, background="white")
        self.displaycanvas.pack(side=tk.LEFT)
        self.displaycanvas.create_line(0, 205, 410, 205)
        self.displaycanvas.create_line(205, 0, 205, 410)
        self.displaycanvas.create_line(0, 105, 410, 105, fill="darkgrey")
        self.displaycanvas.create_line(0, 305, 410, 305, fill="darkgrey")
        self.displaycanvas.create_line(105, 0, 105, 410, fill="darkgrey")
        self.displaycanvas.create_line(305, 0, 305, 410, fill="darkgrey")
        self.displaycanvas.create_oval(5, 5, 405, 405)
        self.displaycanvas.create_oval(105, 105, 305, 305)
        self.displaycanvas.create_polygon(5,380,30,355,30,405,tags="player",fill="black")
        self.rightestimator=StratEstimatorControl(displayframe)
        self.rightestimator.pack(side=tk.LEFT)
        self.x=[0,0]
        self.dx=[0,0]
        self.y=[0,0]
        self.dy=[0,0]
        self.n=[0,0]
        self.dn=[0,0]
        self.moves=[[],[]]
        self.curplayer=0
        self.add_display_dot(0, 0, tags="avg", fill="red")
        tk.Label(self,text="<- X Player                                                                      Y Player ->").pack(side=tk.TOP)
        self.label1=tk.Label(self,text="Totals: x(0) y(0) n(0)")
        self.label1.pack(side=tk.TOP)
        self.label2=tk.Label(self,text="Average: x(0) y(0)")
        self.label2.pack(side=tk.TOP)
        tk.Label(self,text="Discount Factor: "+str(self.discountfactor)).pack(side=tk.TOP)
        self.label3=tk.Label(self,text="Discounted Totals: x(0) y(0)")
        self.label3.pack(side=tk.TOP)
        self.label4=tk.Label(self,text="Discounted Average: x(0) y(0)")
        self.label4.pack(side=tk.TOP)
        self.debug=ScrolledText.ScrolledText(self,width=50,height=10)
        self.debug.pack(side=tk.TOP)
        self.p0=0
        self.p1=0

    def addmove(self, x, y, player):
        self.debug.insert(tk.END,"Player %d: (self: %.3f, opponent: %.3f)\n"%(player,[x,y][player],[y,x][player]))
        self.debug.insert(tk.END, "   Last Pair: ({:.3},{:.3})\n".format(self.p0 + x, self.p1 + y))
        self.p0=x
        self.p1=y
        self.debug.see(tk.END)
        if player!=self.curplayer:
            raise ValueError("Wrong player sent move")
        [self.leftestimator,self.rightestimator][player].addplayermove([y,x][player])
        [self.leftestimator, self.rightestimator][1-player].addopponentmove([y, x][player])
        self.x[player]=self.x[player]+x
        self.y[player]=self.y[player]+y
        self.n[player]=self.n[player]+1
        self.dx[player]=self.dx[player]+self.curdiscount*x
        self.dy[player]=self.dy[player]+self.curdiscount*y
        self.dn[player]=self.dn[player]+self.curdiscount
        self.moves[player].append((x,y))
        self.curdiscount=self.curdiscount*self.discountfactor
        self.add_display_dot(x,y,fill=["blue","green"][player])
        #update total payoffs
        self.displaycanvas.delete("total")
        self.add_display_dot(sum(self.x)/sum(self.n),sum(self.y)/sum(self.n),dotsize=2,tags="total",fill="red")
        #update player average payoffs
        self.displaycanvas.delete("total"+str(player))
        self.add_display_dot(self.x[player]/self.n[player],self.y[player]/self.n[player],dotsize=2,tags="total"+str(player),fill=["blue","green"][player])
        self.label1['text']="Totals: x(%f) y(%f) n(%f)"%(sum(self.x),sum(self.y),sum(self.n))
        self.label2['text']="Average: x(%f) y(%f)"%(sum(self.x)/sum(self.n),sum(self.y)/sum(self.n))
        self.label3['text']="Discounted Totals: x(%f) y(%f) n(%f)"%(sum(self.dx),sum(self.dy),sum(self.dn))
        self.label4['text']="Discounted Average: x(%f) y(%f)"%(sum(self.dx)/sum(self.dn),sum(self.dy)/sum(self.dn))
        self.curplayer=1-self.curplayer
        self.displaycanvas.delete("player")
        if self.curplayer==0:
            self.displaycanvas.create_polygon(5, 380, 30, 355, 30, 405, tags="player", fill="black")
        else:
            self.displaycanvas.create_polygon(405, 380, 380, 355, 380, 405, tags="player", fill="black")

    def add_display_dot(self, x, y, dotsize=1, **kwargs):
        self.displaycanvas.create_oval(display_x(x) - dotsize, display_y(y) - dotsize, display_x(x) + dotsize, display_y(y) + dotsize, **kwargs)

class textlearner(tk.Frame):
    def __init__(self,parent,strat):
        tk.Frame.__init__(self,parent)
        self.strat=strat
        tk.Label(self,text=strat.__class__.__name__).pack(side=tk.TOP)
        self.description=ScrolledText.ScrolledText(self,width=40,height=10)
        self.description.pack(side=tk.TOP)
        self.description.insert(tk.END,self.strat.getDescription())
        self.log = ScrolledText.ScrolledText(self, width=40, height=10)
        self.log.pack(side=tk.TOP)

    def getResponse(self,move):
        response=self.strat.respond(move)
        if move is not None:
            self.log.insert(tk.END, "Received %.3f, responded with %.3f\n" % (move, response))
        else:
            self.log.insert(tk.END, "Played initial move %.3f\n" % response)
        self.log.insert(tk.END, "Status: \n" + self.strat.getStatus()+"\n")
        self.log.see(tk.END)
        self.description.delete(1.0,tk.END)
        self.description.insert(tk.END,self.strat.getDescription())
        return response

class thresholdfunctioncontrol(tk.Frame):
    def __init__(self,master,pointlist=None,command=None,xmin=0,xmax=20,ymin=0,ymax=1,width=210,height=110,verbose=True):
        tk.Frame.__init__(self,master)
        (self.xmin,self.xmax,self.ymin,self.ymax,self.width,self.height)=(xmin,xmax,ymin,ymax,width,height)
        self.displaycanvas=tk.Canvas(self, width=self.width, height=self.height, borderwidth=1, relief=tk.RAISED, background="white")
        self.displaycanvas.pack(side=tk.TOP)
        self.displaycanvas.bind("<Button-1>", self.__mousedown)
        self.displaycanvas.bind("<ButtonRelease-1>", self.__mouseup)
        self.displaycanvas.bind("<Control-Button-1>", self.__ctrlmouseclick)
        self.displaycanvas.bind("<B1-Motion>",self.__mousemove)
        self.displaycanvas.create_line(5,5,self.width-5,5,fill="grey")
        self.displaycanvas.create_line(self.width-5,5,self.width-5,self.height-5,fill="grey")
        self.displaycanvas.create_line(self.width-5,self.height-5,5,self.height-5,fill="grey")
        self.displaycanvas.create_line(5,self.height-5,5,5,fill="grey")
        self.pointlist=pointlist
        if self.pointlist is None:
            self.pointlist=[(xmin,ymax-.001),(xmax,ymin)]
        self.__drawpointlist(self.pointlist)
        self.dragging=False

    def coord2value(self,c):
        result=(self.xmin+(self.xmax-self.xmin)*max(min((c[0]-5.0)/(self.width-10.0),1.0),0.0),
                self.ymin+(self.ymax-self.ymin)*max(min((self.height-5.0-c[1])/(self.height-10.0),1.0),0.0))
        return result

    def value2coord(self,v):
        result=(5+(self.width-10.0)*(v[0]-self.xmin)/(self.xmax-self.xmin),
                5+(self.height-10.0)*(self.ymax-v[1])/(self.ymax-self.ymin))
        return result

    def setpoints(self,pl):
        self.pointlist=pl
        self.__drawpointlist(pl)

    def __mousedown(self,event):
        (x,y)=self.coord2value((event.x,event.y))
        for p in self.pointlist:
            if (x-p[0])**2+(y-p[1])**2<.01:
                self.dragging=True
                self.pointlist.remove(p)

    def __mousemove(self,event):
        if self.dragging:
            pl=[x for x in self.pointlist]+[self.coord2value((event.x,event.y))]
            pl.sort()
            self.__drawpointlist(pl)

    def __mouseup(self,event):
        if self.dragging:
            (x,y)=self.coord2value((event.x,event.y))
            self.pointlist.append((x,y))
            self.pointlist.sort()
            self.dragging=False
            self.__drawpointlist(self.pointlist)

    def __ctrlmouseclick(self,event):
        (x,y)=self.coord2value((event.x,event.y))
        print("{},{}  maps to {},{}".format(event.x,event.y,x,y))
        deleted=False
        for p in self.pointlist:
            if (x-p[0])**2+(y-p[1])**2<.01:
                deleted=True
                self.pointlist.remove(p)
        if not deleted:
            self.pointlist.append((x,y))
            self.pointlist.sort()
        self.__drawpointlist(self.pointlist)

    def __drawpointlist(self,pointlist):
        self.displaycanvas.delete("lines")
        for p1,p2 in zip(pointlist[:1]+pointlist,pointlist+pointlist[-1:]):
            (x1,y1)=self.value2coord((p1[0],p1[1]))
            (x2,y2)=self.value2coord((p2[0],p2[1]))
            self.displaycanvas.create_line(x1,y1,x2,y2,tags="lines")
        for p in pointlist:
            (x,y)=self.value2coord((p[0],p[1]))
            self.displaycanvas.create_oval(x-1,y-1,x+1,y+1,tags="lines")
