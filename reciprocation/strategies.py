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
    except ValueError:
        return (s1[1]+s2[1])/2.0
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

class reciprocal:
    def __init__(self,strat):
        """
        strat is an ordered list of tuples (amount opp gives me,amount I give opponent)
        :param strat:
        """
        self.strat=strat

    def respond(self,oppchoice):
        r=bisect.bisect(self.strat,(oppchoice,None))
        wt=float(oppchoice-self.strat[r-1][0])/(self.strat[r][0]-self.strat[r-1][0])
        result=self.strat[r-1][1]*(1-wt)+self.strat[r][1]*wt
        return result