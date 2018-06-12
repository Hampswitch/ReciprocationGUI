"""
This file contains a class to allow inputing a dictionary into a tkinter interface
"""

import Tkinter as tk

class tkdict(tk.Frame):
    def __init__(self,master,initdict={}):
        tk.Frame.__init__(self,master)
        self.keyvars=[]
        self.valvars=[]
        self.frames=[]
        tk.Button(self,text="Add Item",command=self.additem).pack(side=tk.TOP)
        tk.Button(self,text="Clear Items",command=self.clear).pack(side=tk.TOP)

    def get(self):
        result={}
        for k,v in zip(self.keyvars,self.valvars):
            key=k.get()
            val=v.get()
            try:
                val=float(val)
            except ValueError:
                pass
            result[key]=val
        return result

    def additem(self):
        self.frames.append(tk.Frame(self))
        self.keyvars.append(tk.StringVar())
        self.valvars.append(tk.StringVar())
        self.frames[-1].pack(side=tk.TOP)
        tk.Entry(self.frames[-1],textvariable=self.keyvars[-1]).pack(side=tk.LEFT)
        tk.Entry(self.frames[-1],textvariable=self.valvars[-1]).pack(side=tk.LEFT)

    def clear(self):
        for f in self.frames:
            f.pack_forget()
        self.frames=[]
        self.keyvars=[]
        self.valvars=[]