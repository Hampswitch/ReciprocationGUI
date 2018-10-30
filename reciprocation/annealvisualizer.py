

from matplotlib import pyplot as plt
import re
import ast
import Tkinter as tk
from evaluatorGUI import ParameterPanel

def dispfunctions(stratlist):
    plt.figure(figsize=(4, 3))
    for strat in stratlist:
        plt.plot([x[0] for x in strat],[x[1] for x in strat])
    plt.xlim(-1,1)
    plt.ylim(-1,1)
    plt.show()

def parseresults(filename):
    result={}
    pat='== Expand: (\d+) == Resolution: (\d+) == Index: (\d+) == Params: (\d+) ==========================================\n'
    f=open(filename,'r')
    l=f.readlines()
    for i in range(len(l)/2):
        key=tuple([int(v) for v in re.match(pat,l[2*i]).groups()])
        value=[]
        for s in l[2*i+1].split("Linear Strat: ")[1:]:
            value.append(ast.literal_eval(s[:-2]))
        result[key]=value
    return result

class annealdisp(tk.Frame):
    def __init__(self,master):
        tk.Frame.__init__(self,master)
        self.params=ParameterPanel(self,[("Filename: ",tk.StringVar,"../results/SAbaseresults.txt"),("Expand",tk.IntVar,4),("Resolution",tk.IntVar,9),("Index",tk.IntVar,-1)])
        self.params.pack(side=tk.TOP)
        tk.Button(self,text="Make Plot",command=self.plotstrat).pack(side=tk.TOP)

    def plotstrat(self):
        filename,expand,resolution,index=self.params.getparameters()
        results=parseresults(filename)
        if index==-1:
            stratlist=[]
            for e,r,i in results.keys():
                if r==resolution and e==expand:
                    stratlist=stratlist+results[(e,r,i)]
        else:
            stratlist=results[(expand,resolution,index)]
        dispfunctions(stratlist)

if __name__=="__main__":
    master = tk.Tk()
    annealdisp(master).pack(side=tk.TOP)
    tk.mainloop()

