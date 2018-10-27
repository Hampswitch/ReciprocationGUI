
import math

def getdiscretemoves(resolution):
    return [(math.cos(2*math.pi*i/resolution),math.sin(2*math.pi*i/resolution)) for i in range(resolution)]

def discretize(move,resolutionlist):
    pass

class discreteucb:
    def __init__(self,resolution):
        self.player=player

    def setstartmove(self,move):
        self.player.setstartmove(move)

    def reset(self):
        self.player.reset()

    def __str__(self):
        return str(self.player)

    def __repr__(self):
        return str(self.player)

    def getStatus(self):
        return self.player.getStatus()

    def getDescription(self):
        return self.player.getDescription()

    def respond(self,opponentmove):
        return self.player.respond(opponentmove)

class discreteteacher:
    def __init__(self, player):
        self.player = player

    def setstartmove(self, move):
        self.player.setstartmove(move)

    def reset(self):
        self.player.reset()

    def __str__(self):
        return str(self.player)

    def __repr__(self):
        return str(self.player)

    def getStatus(self):
        return self.player.getStatus()

    def getDescription(self):
        return self.player.getDescription()

    def respond(self, opponentmove):
        return self.player.respond(opponentmove)