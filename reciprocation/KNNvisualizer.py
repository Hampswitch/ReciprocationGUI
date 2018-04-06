
import Tkinter as tk
import numpy as np
import time
import ScrolledText
import matplotlib as mpl
import reciprocation.GPvisualizer as gpv
import reciprocation.evaluatorGUI as eg
import reciprocation.KNNUCB as KNNUCB

class LearnerDisplay(tk.Frame):
    def __init__(self,master):
        tk.Frame.__init__(self,master)
        self.dispcanvas = tk.Canvas(self, width=410, height=410, borderwidth=1, relief=tk.RAISED, background="white")
        self.dispcanvas.pack(side=tk.TOP)
        self.log = ScrolledText.ScrolledText(self, width=50, height=15)
        self.log.pack(side=tk.TOP)

    def update(self,history,learner,lastx,lasty):
        self.log.delete(1.0,tk.END)
        self.dispcanvas.delete("all")
        start = time.time()
        learner.observe(history)
        data = [learner.predict(x) for x in np.arange(-1, 1, .01)]
        stop = time.time()
        self.log.insert(tk.END,"Time: "+str(stop-start)+"\n")
        self.log.insert(tk.END,str(learner)+"\n")
        mean=[x[0] for x in data]
        std=[x[1] for x in data]
        fig = mpl.figure.Figure(figsize=(4, 3))
        ax = fig.add_axes([0, 0, 1, 1])
        ax.plot(np.arange(-1, 1, .01), mean)
        ax.fill_between(np.arange(-1, 1, .01), np.squeeze(mean) - std, np.squeeze(mean) + std, alpha=.1)
        ax.scatter(history[0], history[1], c="red", s=50)
        ax.set_xlim([-1, 1])
        ax.set_ylim([-1, 1])
        fig_x, fig_y = 0, 0
        self.fig_photo = gpv.draw_figure(self.dispcanvas, fig, loc=(fig_x, fig_y))
        fig_w, fig_h = self.fig_photo.width(), self.fig_photo.height()
        self.log.insert(tk.END,"Point: "+str(lastx)+"\n")
        p,b=learner.predict(lastx)
        self.log.insert(tk.END,"Predicted: "+str(p)+","+str(b)+"\n")
        self.log.insert(tk.END,"Observed: "+str(lasty)+"\n")


class LearnerSelect(tk.Frame):
    def __init__(self,master):
        tk.Frame.__init__(self,master)
        self.params=eg.ParameterPanel(self,[("K",tk.IntVar,2),("nwidth",tk.DoubleVar,0.1)])
        self.params.pack(side=tk.TOP)

    def getLearner(self):
        paramvals=self.params.getparameters()
        return KNNUCB.KNN(paramvals[0],paramvals[1])


class KNNvisualizer(tk.Frame):
    def __init__(self,master):
        tk.Frame.__init__(self,master)
        self.pointselector=gpv.PointSelector(self)
        self.pointselector.pack(side=tk.LEFT)
        self.learnerdisp=LearnerDisplay(self)
        self.learnerdisp.pack(side=tk.LEFT)
        self.learnerselect=LearnerSelect(self)
        self.learnerselect.pack(side=tk.LEFT)
        self.pointselector.changepoints=lambda x,y:self.dispUpdate()

    def dispUpdate(self):
        x=self.pointselector.xlist
        y=self.pointselector.ylist
        learner=self.learnerselect.getLearner()
        self.learnerdisp.update((x,y),learner,self.pointselector.lastx,self.pointselector.lasty)


if __name__=="__main__":
    master=tk.Tk()
    KNNvisualizer(master).pack(side=tk.TOP)
    tk.mainloop()