import pandas
import matplotlib.pyplot as plot
import numpy as np
import teachingstrategies as teachers
import mpl_toolkits.mplot3d as mplot3d
import Tkinter as tk

def getmesh(data,threshhold,zero,negone):
    return data[(data["threshhold"]==threshhold) & (data["zero"]==zero) & (data["negone"]==negone)].pivot(index='startmove',columns='response',values='teacher')

def estimateval(data,x,y):
    xindex=len(data.index[data.index<x])-1
    if xindex<0:
        xindex=0
    elif xindex<len(data.index)-1 and abs(data.index[xindex+1]-x)<abs(data.index[xindex]-x):
        xindex=xindex+1
    yindex=len(data.columns[data.columns<y])-1
    if yindex<0:
        yindex=0
    elif yindex<len(data.columns)-1 and abs(data.columns[yindex+1]-y)<abs(data.columns[yindex]-y):
        yindex=yindex+1
    xval=data.index[xindex]
    yval=data.columns[yindex]
    return data[xval][yval]

def mkfirstmovemesh(data, threshhold, zero, negone):
    data=getmesh(data,threshhold,zero,negone)
    teacher=teachers.simpleteacher(threshhold,zero,negone)
    responses=[teacher.respond(x) for x in data.index]
    zvals=[estimateval(data,x,y) for x,y in zip(data.index,responses)]
    fig = plot.figure()
    ax = plot.axes(projection='3d')
    ax.plot_wireframe(np.ones((21, 21)) * data.index.values, (np.ones((21, 21)) * data.index.values).transpose(), data.values)
    ax.plot(xs=data.index, ys=responses, zs=zvals, color='red')
    ax.set_xlabel('opponent move')
    ax.set_ylabel('teacher response')
    ax.set_title('Teacher: ('+str(threshhold)+", "+str(zero)+", "+str(negone))
    fig.show()

class FirstMoveVisualizer(tk.Frame):
    def __init__(self,master,data):
        tk.Frame.__init__(self,master)
        self.data=data
        tframe=tk.Frame(self)
        tframe.pack(side=tk.LEFT)
        zframe=tk.Frame(self)
        zframe.pack(side=tk.LEFT)
        nframe=tk.Frame(self)
        nframe.pack(side=tk.LEFT)
        tk.Label(tframe,text="Threshhold").pack(side=tk.TOP)
        tk.Label(zframe,text="Zero Response").pack(side=tk.TOP)
        tk.Label(nframe,text="Negative One Response").pack(side=tk.TOP)
        self.tvals=self.data["threshhold"].unique()
        self.zvals=self.data["zero"].unique()
        self.nvals=self.data["negone"].unique()
        self.threshhold=tk.DoubleVar(master)
        self.threshhold.set(self.tvals[0])
        self.zero=tk.DoubleVar(master)
        self.zero.set(self.zvals[0])
        self.negone=tk.DoubleVar(master)
        self.negone.set(self.nvals[0])
        tk.OptionMenu(tframe, self.threshhold, *self.tvals).pack(side=tk.TOP)
        tk.OptionMenu(zframe, self.zero, *self.zvals).pack(side=tk.TOP)
        tk.OptionMenu(nframe, self.negone, *self.nvals).pack(side=tk.TOP)
        tk.Button(self,text="Make Mesh",command=self.mkmesh).pack(side=tk.LEFT)

    def mkmesh(self):
        mkfirstmovemesh(self.data, self.threshhold.get(), self.zero.get(), self.negone.get())



if __name__=="firstmove__main__":
    data=pandas.read_csv("firstmoveUCTdata.csv")
    master = tk.Tk()
    FirstMoveVisualizer(master, data).pack(side=tk.TOP)
    tk.mainloop()

if __name__=="":
    data=pandas.read_csv("knnsimpledata.csv")