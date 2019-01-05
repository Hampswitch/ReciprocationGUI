
import math

def mkstepfunc(L,limit=0):
    return lambda x: ([response for maxval,response in L if maxval>x]+[limit])[0]

class functionnegotiator:
    def __init__(self,func,forgive):
        self.func=func
        self.forgive=forgive
        self.round=4
        self.opponentloss=0.0

    def __str__(self):
        return "functionnegotiator ({},{:.4})".format(self.round,self.opponentloss)

    def __repr__(self):
        return str(self)

    def getDescription(self):
        return str(self)

    def getStatus(self):
        return str(self)

    def reset(self):
        self.round=4
        self.opponentloss=0.0

    def respond(self,move):
        self.round = self.round + 1
        threshold = self.func(self.opponentloss)
        if move is None:
            return math.sqrt(1-threshold**2)
        else:
            forgivenmove = min(move + self.forgive / self.round, threshold)
            if forgivenmove>=threshold:
                result=math.sqrt(1-threshold**2)
            else:
                x=threshold*math.sqrt(1-forgivenmove**2)-forgivenmove*math.sqrt(1-threshold**2)
                result=-threshold*x+math.sqrt(threshold**2*x**2-x**2-threshold**2+1)
            self.opponentloss=self.opponentloss+2*math.sqrt(1-threshold**2)-math.sqrt(1-forgivenmove**2)-result
            return result

class stepannealer:
    def __init__(self,steplist=None,forgive=.1):
        if steplist is not None:
            self.steplist=[x for x in steplist]
            self.backuplist=[x for x in steplist]
        else:
            raise ValueError("Random Generation not implemented")
        self.forgive=forgive
        self.round=4
        self.opponentloss=0.0

    def __str__(self):
        return "functionnegotiator ({},{:.4})".format(self.round,self.opponentloss)

    def __repr__(self):
        return str(self)

    def getDescription(self):
        return str(self)

    def getStatus(self):
        return str(self)

    def reset(self):
        self.round=4
        self.opponentloss=0.0
        self.steplist=[x for x in self.backuplist]

    def respond(self,move):
        self.round = self.round + 1
        threshold = self.steplist[0][0]
        if move is None:
            return math.sqrt(1-threshold**2)
        else:
            forgivenmove = min(move + self.forgive / self.round, threshold)
            if forgivenmove>=threshold:
                result=math.sqrt(1-threshold**2)
            else:
                x=threshold*math.sqrt(1-forgivenmove**2)-forgivenmove*math.sqrt(1-threshold**2)
                result=-threshold*x+math.sqrt(threshold**2*x**2-x**2-threshold**2+1)
            self.opponentloss=self.opponentloss+2*math.sqrt(1-threshold**2)-math.sqrt(1-forgivenmove**2)-result
            while self.opponentloss>self.steplist[0][1] and len(self.steplist)>1:
                self.opponentloss=self.opponentloss-self.steplist[0][1]
                self.steplist=self.steplist[1:]
            return result
