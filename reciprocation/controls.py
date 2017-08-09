import Tkinter as tk
import math
import strategies
import ScrolledText

def display_x(val):
    return 5 + 100 * (val + 2)


def display_y(val):
    return 5 + 100 * (2 - val)


def input_x(val):
    return 105 + 100 * (val + 1)


def input_y(val):
    return 5 + 100 * (1 - val)

preset_strats={
    "fair":[(-1,-1),(0,0),(math.sqrt(2)/2,math.sqrt(2)/2)],
    "godfather":[(0,-1),(99.0/101,20.0/101)],
    "rational":[(0,0),(20.0/101,99.0/101)]
}

def interpolate(s1,s2,p):
    """

    :param s1: tuple of (opponents gift to player, player's gift to opponent)
    :param s2:
    :param p: opponent's gift to player
    :return: player's gift to opponent
    """
    x1=s1[0]+math.sqrt(1-s1[1]**2)
    y1=math.sqrt(1-s1[0]**2)+s1[1]
    x2 = s2[0] + math.sqrt(1 - s2[1] ** 2)
    y2 = math.sqrt(1 - s2[0] ** 2) + s2[1]
    slope=(y2-y1)/(x2-x1)
    intercept=y1-slope*x1
    x3=p
    y3=math.sqrt(1-p**2)
    A=slope**2+1
    B=2*(slope*(intercept-y3)-x3)
    C=y3**2-1+x3**2-2*intercept*y3+intercept**2
    x=(-B+math.sqrt(B**2-4*A*C))/(2*A)
    y=slope*x+intercept
    return y-y3


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
        for s in preset_strats.keys():
            tk.Button(buttonpanel, text=s,command=(lambda x: lambda: self.loadstrat(x))(s)).pack(side=tk.LEFT)

    def __clear(self):
        self.displaycanvas.delete("dots")
        self.inputcanvas.delete("dots")
        self.inputcanvas.delete("filldots")
        self.stratlist = []

    def loadstrat(self,name):
        self.__clear()
        for (x,y) in preset_strats[name]:
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
        self.add_input_dot(xc,yc,tags="dots",fill="blue")
        self.stratlist.append((xc, yc))
        self.stratlist.sort()
        self.displaycanvas.delete("dots")
        self.inputcanvas.delete("filldots")
        for xp, yo in self.stratlist:
            self.add_display_dot(xp + math.sqrt(1 - yo * yo), math.sqrt(1 - xp * xp) + yo, tags="dots", fill="blue")
        for first, second in zip(self.stratlist[:-1], self.stratlist[1:]):
            for b in [.1, .2, .3, .4, .5, .6, .7, .8, .9]:
                xp = b * first[0] + (1 - b) * second[0]
                yo=strategies.interpolate(first,second,b*first[0]+(1-b)*second[0])
                self.add_display_dot(xp + math.sqrt(1 - yo * yo), math.sqrt(1 - xp * xp) + yo, tags="dots", fill="blue")
        self.suffixstrat = []
        for b in [.1, .2, .3, .4, .5, .6, .7, .8, .9, 1]:
            xp = self.stratlist[-1][0] * (1 - b) + b
            self.add_display_dot(2 * xp, 2 * math.sqrt(1 - xp * xp), tags="dots", fill="red")
            self.add_input_dot(xp, math.sqrt(1 - xp * xp), tags="filldots", fill="red")
            self.suffixstrat.append((xp, math.sqrt(1 - xp * xp)))
        self.prefixstrat = []
        for b in [x for x in [(y - 10.0) / 10 for y in range(21)] if x < self.stratlist[0][0]]:
            xp = b
            yo = min(self.stratlist[0][1],
                     self.stratlist[0][1] + math.sqrt(1 - self.stratlist[0][0] ** 2) - math.sqrt(1 - b ** 2))
            self.add_display_dot(xp + math.sqrt(1 - yo * yo), math.sqrt(1 - xp * xp) + yo, tags="dots", fill="red")
            self.add_input_dot(xp, yo, tags="filldots", fill="red")
            self.prefixstrat.append((xp, yo))

    def getstrat(self):
        return self.prefixstrat + self.stratlist + self.suffixstrat

    def getResponse(self,move):
        strat=strategies.reciprocal(self.getstrat()).respond(move)
        return strat

class GameDisplay(tk.Frame):
    def __init__(self, parent,discount=None):
        self.discountfactor=1.0 if discount is None else 1.0-discount
        self.curdiscount=1.0
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
        self.displaycanvas.create_polygon(5,380,30,355,30,405,tags="player",fill="black")
        self.x=[0,0]
        self.dx=[0,0]
        self.y=[0,0]
        self.dy=[0,0]
        self.n=[0,0]
        self.dn=[0,0]
        self.moves=[[],[]]
        self.curplayer=0
        self.add_display_dot(0, 0, tags="avg", fill="red")
        self.label1=tk.Label(self,text="Totals: x(0) y(0) n(0)")
        self.label1.pack(side=tk.TOP)
        self.label2=tk.Label(self,text="Average: x(0) y(0)")
        self.label2.pack(side=tk.TOP)
        self.label3=tk.Label(self,text="Discounted Totals: x(0) y(0)")
        self.label3.pack(side=tk.TOP)
        self.label4=tk.Label(self,text="Discounted Average: x(0) y(0)")
        self.label4.pack(side=tk.TOP)
        self.debug=ScrolledText.ScrolledText(self,width=40,height=10)
        self.debug.pack(side=tk.TOP)

    def addmove(self, x, y, player):
        self.debug.insert(tk.END,"Player %d: (self: %.3f, opponent: %.3f)\n"%(player,[x,y][player],[y,x][player]))
        self.debug.see(tk.END)
        if player!=self.curplayer:
            raise ValueError("Wrong player sent move")
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



