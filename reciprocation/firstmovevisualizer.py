import Tkinter as tk

import matplotlib.pyplot as plot
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import pandas

import teachingstrategies as teachers
from reciprocation.meshutils import getmesh, plotmesh, meshlookup


def getfirstmovemesh(data, threshhold, zero, negone):
    return data[(data["threshhold"]==threshhold) & (data["zero"]==zero) & (data["negone"]==negone)].pivot(index='startmove',columns='response',values='teacher')


def mkfirstmovemesh(data, threshhold, zero, negone):
    data=getfirstmovemesh(data, threshhold, zero, negone)
    teacher=teachers.simpleteacher(threshhold,zero,negone)
    responses=[teacher.respond(x) for x in data.index]
    zvals=[meshlookup(data, x, y) for x, y in zip(data.index, responses)]
    fig = plot.figure()
    ax = plot.axes(projection='3d')
    ax.plot_wireframe(np.ones((21, 21)) * data.index.values, (np.ones((21, 21)) * data.index.values).transpose(), data.values)
    ax.plot(xs=data.index, ys=responses, zs=zvals, color='red')
    ax.set_xlabel('opponent move')
    ax.set_ylabel('teacher response')
    ax.set_title('Teacher: ('+str(threshhold)+", "+str(zero)+", "+str(negone))
    fig.show()

def cleantable(data):
    for column in data.columns:
        if column.find("score")>0:
            data[column]=data[column].astype(float)
        else:
            data[column]=data[column].astype(str)
    data=data[(data["startmove"].astype(str)!='None')&(data["response"].astype(str)!='None')]
    return data

class FirstMoveVisualizer(tk.Frame):
    def __init__(self,master,data,defaults={},title="Title",score="simplescore"):
        tk.Frame.__init__(self,master)
        self.score=score
        self.columnvars={}
        self.columnvalues={}
        self.stringvalues={}
        self.data=cleantable(data)
        tk.Label(self,text=title).pack(side=tk.TOP)
        for column in self.data.columns:
            if column.find("score")<0 and column not in ["startmove","response","iteration"]:
                values=list(data[column].unique())
                if len(values)>1:
                    f = tk.Frame(self)
                    f.pack(side=tk.TOP, fill=tk.X)
                    tk.Label(f, text=column).pack(side=tk.LEFT, fill=tk.X)
                    self.columnvars[column] = tk.StringVar()
                    self.columnvalues[column] = values
                    self.stringvalues[column] = [str(x) for x in self.columnvalues[column]]
                    tk.OptionMenu(f, self.columnvars[column], *(self.stringvalues[column])).pack(side=tk.RIGHT)
        tk.Button(self,text="Make Mesh",command=self.mkmesh).pack(side=tk.LEFT)

    def mkmesh(self):
        fixedvalues={}
        for col,var in self.columnvars.items():
            val=var.get()
            fixedvalues[col]=val
        mesh= getmesh(data, fixedvalues, "startmove", "response", self.score, xdiscard=["None"], ydiscard=["None"])
        plotmesh(mesh, "startmove", "response", "score")

class knnsimplevisualizer(tk.Frame):
    def __init__(self,master,data):
        tk.Frame.__init__(self,master)
        self.data=data
        self.columnvars={}
        self.columnvalues={}
        self.stringvalues={}
        columns=["repetitions","discountfactor","startmove","response","K","nwidth","explore","threshhold","zero","negone"]
        tk.Label(self,text="Set values").pack(side=tk.TOP)
        for column in columns:
            f=tk.Frame(self)
            f.pack(side=tk.TOP,fill=tk.X)
            tk.Label(f,text=column).pack(side=tk.LEFT,fill=tk.X)
            self.columnvalues[column]=list(data[column].unique())
            self.stringvalues[column]=[str(x) for x in self.columnvalues[column]]
            self.columnvars[column]=tk.StringVar()
            tk.OptionMenu(f,self.columnvars[column],*(self.stringvalues[column])).pack(side=tk.RIGHT)
        tk.Label(self,text="Axes").pack(side=tk.TOP)
        self.xaxis=tk.StringVar()
        self.yaxis=tk.StringVar()
        self.zaxis=tk.StringVar()
        f=tk.Frame(self)
        f.pack(side=tk.TOP)
        tk.Label(f,text="X-axis").pack(side=tk.LEFT)
        tk.OptionMenu(f,self.xaxis,"startmove","response","K","nwidth","explore","threshhold","zero","negone").pack(side=tk.TOP)
        f = tk.Frame(self)
        f.pack(side=tk.TOP)
        tk.Label(f, text="Y-axis").pack(side=tk.LEFT)
        tk.OptionMenu(f,self.yaxis,"startmove","response","K","nwidth","explore","threshhold","zero","negone").pack(side=tk.TOP)
        f = tk.Frame(self)
        f.pack(side=tk.TOP)
        tk.Label(f, text="Z-axis").pack(side=tk.LEFT)
        tk.OptionMenu(f,self.zaxis,"knnscore","simplescore").pack(side=tk.TOP)
        tk.Button(self,text="Make Mesh",command=self.mkmesh).pack(side=tk.TOP)

    def mkmesh(self):
        setdict={}
        for column,var in self.columnvars.items():
            if column not in [self.xaxis.get(),self.yaxis.get()]:
                v=var.get()
                if v in self.stringvalues[column]:
                    setdict[column]=self.columnvalues[column][self.stringvalues[column].index(v)]
        data= getmesh(self.data, setdict, self.xaxis.get(), self.yaxis.get(), self.zaxis.get())
        plotmesh(data, self.xaxis.get(), self.yaxis.get(), self.zaxis.get())

if __name__=="__main__":
    data=pandas.read_csv("results/ucb_simple_mesh.csv")
    master = tk.Tk()
    FirstMoveVisualizer(master, data,score="simplescore",title="UCB").pack(side=tk.TOP)
    tk.mainloop()

if __name__=="__main__quickmesh":
    data=pandas.read_csv("results/uctsimple.csv")


if __name__=="__main__knn":
    data=pandas.read_csv("results/knnsimple.csv")
    master=tk.Tk()
    knnsimplevisualizer(master,data).pack(side=tk.TOP)
    tk.mainloop()