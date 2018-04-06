
import math
import numpy as np
import sortedcontainers


class KNN:
    def __init__(self,k,nwidth,explore):
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
    def __init__(self,k,nwidth,explore,firstmove=None):
        self.k=k
        self.nwidth=nwidth
        self.explore=explore
        self.lastmove=None
        self.knn=KNN(k,nwidth,explore)
        self.firstmove=firstmove

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
        if self.lastmove is not None:
            self.update(oppmove)
            self.lastmove=self.pickmove()
        else:
            self.lastmove=self.firstmove
        return self.lastmove

    def update(self,oppmove):
        if self.lastmove is not None:
            self.knn.observe(self.lastmove,oppmove)

    def pickmove(self):
        maxscore=None
        maxmove=None
        for move in np.arange(-1,1,.01):
            mean,explore=self.knn.predict(move)
            score=mean+explore+math.sqrt(1-move**2)
            if maxscore is None or score>maxscore:
                maxmove=move
                maxscore=score
        return maxmove
