import pandas
import Tkinter as tk


import reciprocation.meshutils as meshutils

class meshdisplay(tk.Frame):
    def __init__(self,master):
        tk.Frame.__init__(self,master)
        self.filename=tk.StringVar()
        tk.Entry(self,textvariable=self.filename).pack(side=tk.TOP)
        tk.Button(self,text="Show Mesh",command=self.showMesh).pack(side=tk.TOP)

    def showMesh(self):
        data=pandas.read_csv(self.filename.get(),index_col=0)
        data.index=[float(x) for x in data.index]
        data.columns=[float(x) for x in data.columns]
        meshutils.plotmesh(data,xlabel="exploration",ylabel="noise",title=self.filename.get())

if __name__=="__main__":
    master=tk.Tk()
    meshdisplay(master).pack(side=tk.TOP)
    tk.mainloop()