import pandas
import matplotlib.pyplot as plot
import numpy as np
import teachingstrategies as teachers
import mpl_toolkits.mplot3d as mplot3d
import Tkinter as tk

def getmesh(data,fixedvalues,xcolumn,ycolumn,value,xdiscard=["None"],ydiscard=["None"]):
    for k,v in fixedvalues.items():
        data=data[data[k]==v]
    data=data[~data[xcolumn].isin(xdiscard)]
    data=data[~data[ycolumn].isin(ydiscard)]
    data[xcolumn]=data[xcolumn].astype(float)
    data[ycolumn]=data[ycolumn].astype(float)
    result=data.groupby(by=[xcolumn,ycolumn]).mean().reset_index().pivot(index=xcolumn,columns=ycolumn,values=value)
    # remove NAN columns, change NAN to min
    result=result.fillna(result.min().min())
    result.index=[float(x) for x in result.index]
    result.columns=[float(x) for x in result.columns]
    result=result.reindex(index=sorted(result.index),columns=sorted(result.columns))
    return result

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

def cleantable(data):
    for column in data.columns:
        if column.find("score")>0:
            data[column]=data[column].astype(float)
        else:
            data[column]=data[column].astype(str)
    data=data[(data["startmove"].astype(str)!='None')&(data["response"].astype(str)!='None')]
    return data

class FirstMoveVisualizer(tk.Frame):
    def __init__(self,master,data,defaults={},score="ucbscore"):
        tk.Frame.__init__(self,master)
        self.score=score
        self.columnvars={}
        self.columnvalues={}
        self.stringvalues={}
        self.data=cleantable(data)
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
        mesh=getmesh(data,fixedvalues,"startmove","response",self.score,xdiscard=["None"],ydiscard=["None"])
        mkmesh(mesh,"startmove","response","score")

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

if __name__=="__main__":
    data=pandas.read_csv("results/uctsimple.csv")
    master = tk.Tk()
    FirstMoveVisualizer(master, data,score="uctscore").pack(side=tk.TOP)
    tk.mainloop()

if __name__=="__main__quickmesh":
    data=pandas.read_csv("results/uctsimple.csv")


if __name__=="__main__knn":
    data=pandas.read_csv("results/knnsimple.csv")
    master=tk.Tk()
    knnsimplevisualizer(master,data).pack(side=tk.TOP)
    tk.mainloop()