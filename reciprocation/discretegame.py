
import math
import random

def getdiscretemoves(resolution):
    result=[(math.cos(2*math.pi*i/resolution),math.sin(2*math.pi*i/resolution)) for i in range(resolution)]
    result=[r for r in result if r[0]>-.0000001 or r[1]>-.0000001]
    return result

class discreteucb:
    def __init__(self,moves,player=0,explore=2.0):
        self.player=player  # Player indicates which payoff from moves they want to maximize
        self.moves=moves
        self.moves=[m for m in self.moves if m[player]>-.0000001]
        self.totals= [None] * len(self.moves)
        self.counts=[0]*len(self.moves)
        self.N=0
        self.lastmove=None
        self.explore=explore

    def reset(self):
        self.totals = [None] * len(self.moves)
        self.counts = [0] * len(self.moves)
        self.N=0
        self.lastmove = None

    def __str__(self):
        return "Discrete UCB"

    def __repr__(self):
        return str(self)

    def getStatus(self):
        return str(self)

    def getDescription(self):
        return str(self)

    def respond(self,opponentmove):
        if self.lastmove is not None:
            if self.totals[self.lastmove] is None:
                self.totals[self.lastmove]=opponentmove
            else:
                self.totals[self.lastmove]+=opponentmove
            self.counts[self.lastmove]+=1
            self.N+=1
        if None in self.totals:
            self.lastmove=random.choice([i for i in range(len(self.moves)) if self.totals[i] is None])
        else:
            self.lastmove=max([(self.totals[i]/self.counts[i]+self.moves[i][self.player]+math.sqrt(self.explore*math.log(self.N)/self.counts[i]),i) for i in range(len(self.moves))])[1]
        return self.moves[self.lastmove][1-self.player]

def mkvalues(moves):
    result=[]
    for m in moves:
        if len(result)==0:
            result.append(m[0])
        elif min([abs(m[0]-r) for r in result])>.001:
            result.append(m[0])
    return result

def getvalue(values,v):
    return min([(abs(values[i]-v),i) for i in range(len(values))])[1]

class discreteteacher:
    def __init__(self, moves=None,player=1,strat=None,values=None):
        if moves is not None:
            self.values=mkvalues(moves)
        elif values is not None:
            self.values=values
        else:
            raise ValueError("Neither moves nor values defined for discreteteacher")
        self.player = player
        if strat is None:
            self.strat=[random.randint(0,len(self.values)-1) for i in range(len(self.values))]
        else:
            self.strat=strat

    def reset(self):
        pass

    def __str__(self):
        return "Discrete Teacher: "+str(self.strat)

    def __repr__(self):
        return str(self)

    def getStatus(self):
        return str(self)

    def getDescription(self):
        return str(self)

    def respond(self, opponentmove):
        return self.values[self.strat[getvalue(self.values,opponentmove)]]


    def perturbsmall(self,stepsize,expandfactor):
        result=[]
        for i in range(expandfactor):
            result.append(discreteteacher(values=self.values,player=self.player,strat=[(r+(1 if random.random()<.5 else -1))%len(self.values) if random.random()<stepsize else r for r in self.strat]))
        return result

class randomizingteacher:
    def __init__(self, moves=None,player=1,strat=None,values=None):
        if moves is not None:
            self.values=mkvalues(moves)
            self.values=sorted(self.values)
        elif values is not None:
            self.values=sorted(values)
        else:
            raise ValueError("Neither moves nor values defined for discreteteacher")
        self.player = player
        if strat is None:
            self.strat=[random.random()*(len(self.values)-1) for i in range(len(self.values))]
        else:
            self.strat=strat

    def reset(self):
        pass

    def __str__(self):
        return "Randomizing Teacher: ["+self.getDescription()+"]"+str(self.strat)

    def __repr__(self):
        return str(self)

    def getStatus(self):
        return str(self)

    def getDescription(self):
        return ", ".join(["{:.3f}->{:.3f}".format(v,self.values[int(int(int(math.floor(s))))]+(s-math.floor(s))*((self.values+[1000])[int(math.floor(s)+1)]-self.values[int(math.floor(s))])) for v,s in zip(self.values,self.strat)])

    def respond(self, opponentmove):
        response=self.strat[getvalue(self.values,opponentmove)]
        base=int(math.floor(response))
        if random.random()<response-base:
            base=base+1
        return self.values[base]

    def perturbsmall(self,stepsize,expandfactor):
        result=[]
        for i in range(expandfactor):
            result.append(randomizingteacher(values=self.values,player=self.player,strat=[max(0,min(r+random.normalvariate(0,1),len(self.values)-1)) for r in self.strat]))
        return result