"""
This file contains teachinglearning classes and functions.  They all need to implement a function which takes
(opponent's last move, proposed move, history) and returns movevalue.
opponent's last move - float
proposed move - float
history - list of tuples of the form (opponent's move, my move) - (since some classes will update their movevalues based on observations)
movevalue - float
"""

import pandas
import meshutils

#TODO - utility to make fixedvalues work (.707000000000000007 problem)
def mkmeshfunc(filename,score_col="simplescore",fixedvalues=None):
    data = pandas.read_csv(filename)
    fixedvalues=meshutils.fixdict(data,fixedvalues)
    mesh = meshutils.getmesh(data,fixedvalues,"startmove","response",score_col)
    return lambda olm,pm:meshutils.meshlookup(mesh,olm,pm)

class meshTLteacher:
    def __init__(self,filename=None,score_col="simplescore",fixedvalues={},mesh=None):
        if filename is not None:
            self.evalfunc=mkmeshfunc(filename,score_col,fixedvalues)
        else:
            self.mesh=mesh
            self.evalfunc=None

    def evalmove(self,move):
        if self.evalfunc is not None:
            return self.evalfunc(self.opplastmove,move)
        else:
            return meshutils.meshlookup(self.mesh,self.opplastmove,move)

    def observeopponent(self,oppmove):
        self.opplastmove=oppmove

    def observeself(self,move):
        pass

    def reset(self):
        pass

if __name__=="__main__":
    foo=mkmeshfunc("results/uctsimple2h.csv",fixedvalues={"threshhold":.707,"zero":0,"negone":0,"c":.125,"bucketcount":2})