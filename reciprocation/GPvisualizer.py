
import Tkinter as tk
import ScrolledText
import numpy as np
import matplotlib as mpl
import matplotlib.backends.tkagg as tkagg
from matplotlib.backends.backend_agg import FigureCanvasAgg
import sklearn.gaussian_process as skgp
import evaluatorGUI as eg
import matplotlib.pyplot as plt
import scipy.optimize
import time

def draw_figure(canvas, figure, loc=(0, 0)):
    """ Draw a matplotlib figure onto a Tk canvas
    from https://matplotlib.org/gallery/user_interfaces/embedding_in_tk_canvas_sgskip.html

    loc: location of top-left corner of figure on canvas in pixels.
    Inspired by matplotlib source: lib/matplotlib/backends/backend_tkagg.py
    """
    figure_canvas_agg = FigureCanvasAgg(figure)
    figure_canvas_agg.draw()
    figure_x, figure_y, figure_w, figure_h = figure.bbox.bounds
    figure_w, figure_h = int(figure_w), int(figure_h)
    photo = tk.PhotoImage(master=canvas, width=figure_w, height=figure_h)

    # Position: convert from top-left anchor to center anchor
    canvas.create_image(loc[0] + figure_w/2, loc[1] + figure_h/2, image=photo)

    # Unfortunately, there's no accessor for the pointer to the native renderer
    tkagg.blit(photo, figure_canvas_agg.get_renderer()._renderer, colormode=2)

    # Return a handle which contains a reference to the photo object
    # which must be kept live or else the picture disappears
    return photo

class PointSelector(tk.Frame):
    def __init__(self,master):
        tk.Frame.__init__(self,master)
        self.changepoints=lambda x,y:None
        self.inputcanvas=tk.Canvas(self,width=410,height=410,borderwidth=1,relief=tk.RAISED,background="white")
        self.inputcanvas.bind("<Button-1>", self.__inputcanvasmouseclick)
        self.xlist=[]
        self.ylist=[]
        self.inputcanvas.pack(side=tk.TOP)

    def __inputcanvasmouseclick(self, event):
        x = event.x
        y = event.y
        if x < 5:
            x = 5
        if x > 405:
            x = 405
        if y < 5:
            y = 5
        if y > 405:
            y = 405
        xc = (x - 205) / 200.0
        yc = (205 - y) / 200.0
        self.xlist.append(xc)
        self.ylist.append(yc)
        self.inputcanvas.create_oval(x-1,y-1,x+1,y+1)
        self.changepoints(self.xlist,self.ylist)

class GPdisplay(tk.Frame):
    def __init__(self,master):
        tk.Frame.__init__(self,master)
        self.dispcanvas=tk.Canvas(self,width=410,height=410,borderwidth=1, relief=tk.RAISED, background="white")
        self.dispcanvas.pack(side=tk.TOP)
        self.x=[]
        self.y=[]
        self.gp=None
        self.log = ScrolledText.ScrolledText(self, width=50, height=15)
        self.log.pack(side=tk.TOP)

    def updatePoints(self,x,y):
        self.x=x
        self.y=y
        self.updateDisplay()

    def updateGP(self,gp):
        self.gp=gp
        self.updateDisplay()

    def updateDisplay(self):
        self.log.delete(1.0,tk.END)
        if len(self.x)>0 and self.gp is not None:
            self.dispcanvas.delete("all")
            start=time.time()
            self.gp.fit(np.array(self.x).reshape(-1,1),np.array(self.y).reshape(-1,1))
            stop=time.time()
            self.log.insert(tk.END,"log marginal likelihood: "+str(self.gp.log_marginal_likelihood())+"\nparams: \n  "+"\n  ".join([param+" : "+str(val) for param,val in self.gp.get_params(True).items()]))
            self.log.insert(tk.END,"\ntime: "+str(stop-start))
            self.log.insert(tk.END,"\nfinal params:"+"\n  ".join([param+" : "+str(val) for param,val in self.gp.kernel_.get_params(True).items()]))
            mean, std = self.gp.predict(np.arange(-1, 1, .01).reshape(-1, 1), return_std=True)
            fig=mpl.figure.Figure(figsize=(4, 3))
            ax=fig.add_axes([0, 0, 1, 1])
            ax.plot(np.arange(-1, 1, .01), mean)
            ax.fill_between(np.arange(-1, 1, .01), np.squeeze(mean) - std, np.squeeze(mean) + std, alpha=.1)
            ax.scatter(self.x, self.y, c="red", s=50)
            ax.set_xlim([-1,1])
            ax.set_ylim([-1,1])
            fig_x, fig_y = 0, 0
            self.fig_photo = draw_figure(self.dispcanvas, fig, loc=(fig_x, fig_y))
            fig_w, fig_h = self.fig_photo.width(), self.fig_photo.height()

    def dispGP(self):
        self.gp.fit(np.array(self.x).reshape(-1, 1), np.array(self.y).reshape(-1, 1))
        mean,std=self.gp.predict(np.arange(-1,1,.01).reshape(-1,1),return_std=True)
        plt.figure(figsize=(16,9))
        plt.plot(np.arange(-1,1,.01),mean)
        plt.fill_between(np.arange(-1,1,.01),np.squeeze(mean)-std,np.squeeze(mean)+std,alpha=.1)
        plt.scatter(self.x,self.y,c="red",s=50)
        plt.xlim(-1,1)
        plt.ylim(-2,2)
        plt.show()



class GPselector(tk.Frame):
    def __init__(self,master):
        tk.Frame.__init__(self,master)
        self.changeGP=lambda x:None
        buttonpanel = tk.Frame(self)
        buttonpanel.pack(side=tk.LEFT)
        updateButton=tk.Button(buttonpanel,text="Update",command=self.updateGP)
        updateButton.pack(side=tk.TOP)
        self.generalparamselect=eg.ParameterPanel(self,[("alpha: ",tk.DoubleVar,.0000001),("restarts: ",tk.IntVar,25),("optimize: ",tk.BooleanVar,True)])
        self.generalparamselect.pack(side=tk.LEFT)
        buttonpanel=tk.Frame(self)
        buttonpanel.pack(side=tk.LEFT)
        tk.Button(buttonpanel, text="Matern", command=self.setMatern).pack(side=tk.TOP)
        tk.Button(buttonpanel, text="RBF", command=self.setRBF).pack(side=tk.TOP)
        tk.Button(buttonpanel, text="RBFnoise", command=self.setRBFnoise).pack(side=tk.TOP)
        self.paramselect=eg.ParameterPanel(self,[("nu: ",tk.DoubleVar,1.5),("length_scale: ",tk.DoubleVar,1.0),("length_scale_min",tk.DoubleVar,1e-5),("length_scale_max",tk.DoubleVar,1e5)])
        self.paramselect.pack(side=tk.LEFT)
        self.kerneltype="Matern"

    def updateGP(self):
        generalparams=self.generalparamselect.getparameters()
        params=self.paramselect.getparameters()
        if self.kerneltype=="Matern":
            kernel=skgp.kernels.Matern(nu=params[0],length_scale=params[1],length_scale_bounds=(params[2],params[3]))
        elif self.kerneltype=="RBF":
            kernel=skgp.kernels.RBF(length_scale=params[0],length_scale_bounds=(params[1],params[2]))
        elif self.kerneltype=="RBFnoise":
            kernel=skgp.kernels.RBF(length_scale=params[0],length_scale_bounds=(params[3],params[4]))+params[2]*skgp.kernels.WhiteKernel(noise_level=params[1])
        else:
            raise ValueError("Unrecognized kernel type: "+str(self.kerneltype))
        gp=skgp.GaussianProcessRegressor(kernel=kernel,n_restarts_optimizer=generalparams[1],alpha=generalparams[0],optimizer="fmin_l_bfgs_b" if generalparams[2] else None)
        self.changeGP(gp)

    def setMatern(self):
        self.paramselect.pack_forget()
        self.paramselect=eg.ParameterPanel(self,[("nu: ",tk.DoubleVar,1.5),("length_scale: ",tk.DoubleVar,1.0),("length_scale_min",tk.DoubleVar,1e-5),("length_scale_max",tk.DoubleVar,1e5)])
        self.paramselect.pack(side=tk.LEFT)
        self.kerneltype="Matern"

    def setRBF(self):
        self.paramselect.pack_forget()
        self.paramselect=eg.ParameterPanel(self,[("length_scale: ",tk.DoubleVar,1.0),("length_scale_min",tk.DoubleVar,1e-5),("length_scale_max",tk.DoubleVar,1e5)])
        self.paramselect.pack(side=tk.LEFT)
        self.kerneltype="RBF"

    def setRBFnoise(self):
        self.paramselect.pack_forget()
        self.paramselect=eg.ParameterPanel(self,[("length_scale: ",tk.DoubleVar,1.5),("noise_level: ",tk.DoubleVar,1.0),("noise weight",tk.DoubleVar,1.0),("length_scale_min",tk.DoubleVar,1e-5),("length_scale_max",tk.DoubleVar,1e5)])
        self.paramselect.pack(side=tk.LEFT)
        self.kerneltype="RBFnoise"

class GPvisualizer(tk.Frame):
    def __init__(self,master):
        tk.Frame.__init__(self,master)
        pointselector=PointSelector(self)
        pointselector.pack(side=tk.LEFT)
        gpdisp=GPdisplay(self)
        gpdisp.pack(side=tk.LEFT)
        gpselect=GPselector(self)
        gpselect.pack(side=tk.LEFT)
        pointselector.changepoints=gpdisp.updatePoints
        gpselect.changeGP=gpdisp.updateGP

if __name__=="__main__":
    master = tk.Tk()
    GPvisualizer(master).pack(side=tk.TOP)
    tk.mainloop()