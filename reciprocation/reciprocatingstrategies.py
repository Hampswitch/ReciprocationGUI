import bisect
import math

def interpolate(s1,s2,p):
    """

    :param s1: tuple of (opponents gift to player, player's gift to opponent)
    :param s2:
    :param p: opponent's gift to player
    :return: player's gift to opponent
    """
    x1=s1[0]+math.sqrt(1-s1[1]**2)
    y1=math.sqrt(1-s1[0]**2)+s1[1]
    x2 = s2[0] + math.sqrt(1 - s2[1] ** 2)
    y2 = math.sqrt(1 - s2[0] ** 2) + s2[1]
    try:
        slope=(y2-y1)/(x2-x1)
    except ZeroDivisionError:
        return x2-math.sqrt(1-p**2)
    intercept=y1-slope*x1
    x3=p
    y3=math.sqrt(1-p**2)
    A=slope**2+1
    B=2*(slope*(intercept-y3)-x3)
    C=y3**2-1+x3**2-2*intercept*y3+intercept**2
    try:
        x=(-B+math.sqrt(B**2-4*A*C))/(2*A)
    except ValueError:
        b=(p-s1[0])/(s2[0]-s1[0])
        return (1-b)*s1[1]+b*s2[1]
    y=slope*x+intercept
    return y-y3

def biasedinterpolate(s1,s2,p,b):
    shift=b*(p-s1[0])/(s2[0]-s1[0])
    result=interpolate((s1[0],s1[1]+shift),s2,p)
    return result

class reciprocal:
    def __init__(self,strat,bias=0):
        """
        strat is an ordered list of tuples (amount opp gives me,amount I give opponent)
        :param strat:
        """
        self.strat=strat
        self.bias=bias

    def __str__(self):
        return "Reciprocating: "+str(self.strat)

    def __repr__(self):
        return str(self)

    def respond(self,oppchoice):
        r=bisect.bisect(self.strat,(oppchoice,None))
        if r==len(self.strat):
            return math.sqrt(1-oppchoice**2)
        elif r==0:
            return self.strat[0][1]
        else:
            if self.bias==0:
                return interpolate(self.strat[r-1],self.strat[r],oppchoice)
            elif self.bias is not None:
                return biasedinterpolate(self.strat[r-1],self.strat[r],oppchoice,self.bias)
            else:
                wt=float(oppchoice-self.strat[r-1][0])/(self.strat[r][0]-self.strat[r-1][0])
                return self.strat[r-1][1]*(1-wt)+self.strat[r][1]*wt
