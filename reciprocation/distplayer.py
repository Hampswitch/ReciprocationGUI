
import numpy.random

class distplayer:
    def __init__(self,playerlist,weights):
        self.playerlist=playerlist
        self.weights=weights
        self.reset()

    def __str__(self):
        return "Distributed Strat "+str(self.weights)+str([str(x) for x in self.playerlist])

    def __repr__(self):
        return str(self)

    def getDescription(self):
        return str(self)

    def getStatus(self):
        return str(self)

    def reset(self):
        self.curplayer=numpy.random.choice(self.playerlist,1,p=self.weights)[0]
        self.curplayer.reset()

    def respond(self,move):
        return self.curplayer.respond(move)
