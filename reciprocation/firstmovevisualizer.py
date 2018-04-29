import pandas
import matplotlib.pyplot as plot
import numpy as np
import teachingstrategies as teachers
import mpl_toolkits.mplot3d as mplot3d
import Tkinter as tk

def getmesh(data,fixedvalues,xcolumn,ycolumn,value):
    for k,v in fixedvalues.items():
        data=data[data[k]==v]
    result=data.groupby(by=[xcolumn,ycolumn]).mean().reset_index().pivot(index=xcolumn,columns=ycolumn,values=value)
    # remove NAN columns, change NAN to min
    return result.fillna(result.min().min())

def getfirstmovemesh(data, threshhold, zero, negone):
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

def mkmesh(data,xlabel,ylabel,title):
    fig=plot.figure()
    ax=plot.axes(projection='3d')
    xsize=len(data.index)
    ysize=len(data.columns)
    ax.plot_wireframe(np.ones((xsize,ysize))*data.index.values.reshape(-1,1),(np.ones((ysize,xsize))*data.columns.values.reshape(-1,1)).transpose(),data.values)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    fig.show()

def mkfirstmovemesh(data, threshhold, zero, negone):
    data=getfirstmovemesh(data, threshhold, zero, negone)
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
        data=getmesh(self.data,setdict,self.xaxis.get(),self.yaxis.get(),self.zaxis.get())
        mkmesh(data,self.xaxis.get(),self.yaxis.get(),self.zaxis.get())

if __name__=="firstmove__main__":
    data=pandas.read_csv("firstmoveUCTdata.csv")
    master = tk.Tk()
    FirstMoveVisualizer(master, data).pack(side=tk.TOP)
    tk.mainloop()

if __name__=="__main__":
    data=pandas.read_csv("results/knnsimple.csv")
    master=tk.Tk()
    knnsimplevisualizer(master,data).pack(side=tk.TOP)
    tk.mainloop()