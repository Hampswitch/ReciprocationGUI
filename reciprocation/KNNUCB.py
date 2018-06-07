
import math
import numpy as np
import sortedcontainers
import itertools
import pandas


def findposweights(v,L):
    pos=len(L[L<v])
    if pos==0:
        return [(0,1)]
    if pos==len(L):
        return [(len(L)-1,1)]
    r=L[pos]-L[pos-1]
    return [(pos-1,(v-L[pos-1])/r),(pos,(L[pos]-v)/r)]

class fixedmeshteacher:
    def __init__(self,mesh):
        self.mesh=mesh

    def observe(self,move,oppmove):
        pass

    def evaluatemove(self,oppmove,move):
        xweights=findposweights(move,self.mesh.columns)
        yweights=findposweights(oppmove,self.mesh.index)
        return sum([self.mesh[x[0]][y[0]]*x[1]*y[1] for x,y in itertools.product(xweights,yweights)])

class KNN:
    def __init__(self, k, nwidth, explore):
        self.k=k
        self.nwidth=nwidth
        self.explore=explore
        self.history=sortedcontainers.SortedList()

    def observe(self,move,response):
        self.history.add((move,response))

    def predict(self,move):
        if len(self.history)==0:
            return 0,math.sqrt(self.explore*math.log(2.0/(2*self.nwidth))/1)
        lowindex=self.history.bisect((move,None))
        highindex=self.history.bisect((move,1000))
        neighbors=self.history[max(0,lowindex-self.k):highindex+self.k]
        neighborscores=[x[1] for x in neighbors]
        nval=self.history.bisect((move+self.nwidth,100))-self.history.bisect((move-self.nwidth,None))
        if nval>0:
            return sum(neighborscores)/len(neighborscores),math.sqrt(self.explore*math.log(len(self.history))/nval)
        else:
            return sum(neighborscores)/len(neighborscores),math.sqrt(self.explore*math.log(len(self.history))*2)

    def reset(self):
        self.history=sortedcontainers.SortedList()


class KNNUCBplayer:
    def __init__(self,k,nwidth,explore,firstmove=None,teacher=None):
        self.k=k
        self.nwidth=nwidth
        self.explore=explore
        self.lastmove=None
        self.knn=KNN(k,nwidth,explore)
        self.firstmove=firstmove
        self.teacher=teacher

    def reset(self):
        self.knn.reset()
        self.lastmove=None

    def __str__(self):
        pass

    def __repr__(self):
        pass

    def getStatus(self):
        pass

    def getDescription(self):
        pass

    def respond(self,oppmove):
        if self.teacher is not None:
            self.teacher.observe(self.lastmove,oppmove)
        if self.lastmove is not None:
            self.update(oppmove)
            self.lastmove=self.pickmove(oppmove)
        else:
            self.lastmove=self.firstmove
            if self.lastmove is None:
                self.lastmove=0.0
        return self.lastmove

    def update(self,oppmove):
        if self.lastmove is not None:
            self.knn.observe(self.lastmove,oppmove)

    def pickmove(self,oppmove):
        maxscore=None
        maxmove=None
        for move in np.arange(-1,1,.01):
            mean,explore=self.knn.predict(move)
            if self.teacher is not None:
                score=mean+explore+math.sqrt(1-move**2)+self.teacher.evaluatemove(oppmove,move)
            else:
                score = mean + explore + math.sqrt(1 - move ** 2)
            if maxscore is None or score>maxscore:
                maxmove=move
                maxscore=score
        return maxmove

if __name__=="__main__":
    import reciprocation.meshutils
    data = pandas.read_csv("results/knnsimple.csv")
    d={"K":2,"nwidth":.2,"explore":1.0,"threshhold":data["threshhold"].unique()[4],"zero":0,"negone":0}
    mesh= reciprocation.meshutils.getmesh(data, d, "startmove", "response", "simplescore")