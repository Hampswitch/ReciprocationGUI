import pandas
import matplotlib.pyplot as plot
import numpy as np
import teachingstrategies as teachers
import mpl_toolkits.mplot3d as mplot3d
import Tkinter as tk

def getmesh(data,threshhold,zero,negone):
    return data[(data["threshhold"]==threshhold) & (data["zero"]==zero) & (data["negone"]==negone)].pivot(index='startmove',columns='response',values='teacher')

def estimateval(data,x,y):
    xval=data.index[len(data.index[data.index<x])-1]
    yval=data.columns[len(data.columns[data.columns<y])-1]
    return data[xval][yval]

def mkmesh(data,threshhold,zero,negone):
    data=getmesh(data,threshhold,zero,negone)
    teacher=teachers.simpleteacher(threshhold,zero,negone)
    responses=[teacher.respond(x) for x in data.index]
    zvals=[estimateval(data,x,y) for x,y in zip(data.index,responses)]
    fig = plot.figure()
    ax = plot.axes(projection='3d')
    ax.plot_wireframe(np.ones((21, 21)) * data.index.values, (np.ones((21, 21)) * data.index.values).transpose(), data.values)
    zs = [1.4263, 1.4274, 1.4269, 1.4258, 1.4242, 1.4210, 1.4174, 1.4135, 1.4080, 1.4026, 1.3790, 1.3709, 1.3639,
          1.3572, 1.3522, 1.3479, 1.3450, 1.3990, 1.3996, 1.3978, 1.3971]
    ax.plot(xs=data.index, ys=responses, zs=zvals, color='red')
    ax.set_xlabel('opponent move')
    ax.set_ylabel('teacher response')
    fig.show()

class Visualizer(tk.Frame):
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
        mkmesh(self.data,self.threshhold.get(),self.zero.get(),self.negone.get())

if __name__=="__main__":
    data=pandas.read_csv("firstmovedata.csv")
    master = tk.Tk()
    Visualizer(master,data).pack(side=tk.TOP)
    tk.mainloop()