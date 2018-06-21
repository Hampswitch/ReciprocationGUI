

import reciprocation.meshutils as meshutils
import Tkinter as tk
import evaluatorGUI as evg

class MeshGUI(tk.Frame):
    def __init__(self,master):
        tk.Frame.__init__(self,master)
        self.tselector=evg.SimpleTeacherSelector(self)
        self.tselector.pack(side=tk.LEFT)
        self.lselector=evg.UCBSelector(self)
        self.lselector.pack(side=tk.LEFT)
        tk.Button(self,text="Make Mesh",command=self.mkmesh).pack(side=tk.LEFT)

    def mkmesh(self):
        teacher=self.tselector.getPlayer()
        learner=self.lselector.getPlayer()
        mesh= meshutils.createmesh(teacher, learner, None, 1000, .99, 100, poolsize=4)
        meshutils.plotmesh(mesh, "startmove", "response", "score")

if __name__=="__main__":
    master = tk.Tk()
    MeshGUI(master).pack(side=tk.TOP)
    tk.mainloop()