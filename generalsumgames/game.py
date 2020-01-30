
import numpy


class gamegenerator:
    def __init__(self,n=16):
        self.n=n
        self.p1payoffs=numpy.random.uniform(size=(n,n))
        self.p2payoffs=numpy.random.uniform(size=(n,n))

    def changegame(self):
        self.p1payoffs=numpy.random.uniform(size=(self.n,self.n))
        self.p2payoffs=numpy.random.uniform(size=(self.n,self.n))

    def getresult(self,p1move,p2move,p1dist=None,p2dist=None):
        if p1dist is None:
            return (self.p1payoffs[p1move,p2move],self.p2payoffs[p1move,p2move])
        else:
            pass
            #return (self.p1payoffs[p1move,p2move],self.p2payoffs[p1move,p2move],p1move expected payof vs. p2dist, p2move expected payoff vs p1dist)

def gameseq(game,player1,player2,length):
    """

    :param game:
    :param player1:
    :param player2:
    :param length:
    :return:
    """
    result=[]
    for i in range(length):
        game.changegame()
        p1,p2=(player1.getmove(game,0),player2.getmove(game,1))
        player1.report(game,0,p1,p2)
        player2.report(game,1,p1,p2)
        result.append(game.getresult(p1,p2))
    return result

class player:
    def __init__(self):
        pass

    def getmove(self,game,role):
        pass

    def report(self,game,role,p1move,p2move):
        pass