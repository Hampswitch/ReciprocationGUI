import Tkinter as tk
import controls
import math
import learners



class gametracker(tk.Frame):
    def __init__(self,master,curplayer=0,curmove=0):
        self.curplayer=curplayer
        self.curmove=curmove
        tk.Frame.__init__(self,master)
        displaypanel = tk.Frame(self)
        displaypanel.pack(side=tk.TOP)
        self.stratselector=[None,None]
        self.stratselector[0] = controls.ReciprocalStrategySelector(displaypanel)
        self.stratselector[0].pack(side=tk.LEFT)

        self.gamedisp = controls.GameDisplay(displaypanel,discount=.2)
        self.gamedisp.pack(side=tk.LEFT)

        #self.stratselector[1] = controls.ReciprocalStrategySelector(displaypanel)
        #self.stratselector[1] = learners.Static(displaypanel)
        self.stratselector[1]=learners.AdHoc(displaypanel)
        self.stratselector[1].pack(side=tk.LEFT)



        controlpanel = tk.Frame(self)
        controlpanel.pack(side=tk.TOP)

        tk.Button(controlpanel, text="Move", command=lambda :self.move()).pack(side=tk.LEFT)
        tk.Button(controlpanel, text="Move 10", command=lambda : self.move10()).pack(side=tk.LEFT)
        tk.Button(controlpanel, text="Move 100", command=lambda: self.move100()).pack(side=tk.LEFT)

    def move(self):
        self.gamedisp.addmove([math.sqrt(1-self.curmove**2),self.curmove][self.curplayer],[self.curmove,math.sqrt(1-self.curmove**2)][self.curplayer],self.curplayer)
        self.curplayer=1-self.curplayer
        self.curmove=self.stratselector[self.curplayer].getResponse(self.curmove)

    def move10(self):
        for i in range(10):
            self.move()

    def move100(self):
        for i in range(100):
            self.move()



master = tk.Tk()
gametracker(master).pack(side=tk.TOP)
tk.mainloop()