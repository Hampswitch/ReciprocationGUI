import bisect
import math
import random


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
    y=min(max(y1,y2),y)
    result=y-y3
    result=max(min(s1[1],s2[1]),result)
    result=min(max(s1[1],s2[1]),result)
    return result


def biasedinterpolate(s1,s2,p,b):
    shift=b*(p-s1[0])/(s2[0]-s1[0])
    result=interpolate((s1[0],s1[1]+shift),s2,p)
    return result

class bucketnoiseteacher:
    def __init__(self,threshhold,zeroresponse,negoneresponse,buckets,startmove=0,split=False,irrationalopponent=False):
        self.threshhold=threshhold
        self.zeroresponse=zeroresponse
        self.negoneresponse=negoneresponse
        self.buckets=buckets
        self.startmove=startmove
        self.split=split
        self.irrationalopponent=irrationalopponent
        self.lowerbounds=[i*2.0/buckets-1 for i in range(buckets)]

    def __str__(self):
        return "Bucket Noise Simple Teacher: "+str((self.threshhold,self.zeroresponse,self.negoneresponse,self.buckets))

    def __repr__(self):
        return str(self)

    def reset(self):
        self.lowerbounds = [i * 2.0 / self.buckets - 1 for i in range(self.buckets)]

    def clone(self):
        return bucketnoiseteacher(self.threshhold,self.zeroresponse,self.negoneresponse,self.buckets,self.startmove,self.split)

    def respond(self,oppchoice):
        if oppchoice is None:
            result=self.startmove
        elif oppchoice>=self.threshhold:
            if self.irrationalopponent:
                result=math.sqrt(1-oppchoice**2)
            else:
                result=math.sqrt(1-self.threshhold**2)
        elif oppchoice>=0:
            result=interpolate((0,self.zeroresponse),(self.threshhold,math.sqrt(1-self.threshhold**2)),oppchoice)
        else:
            result=interpolate((-1,self.negoneresponse),(0,self.zeroresponse),oppchoice)
        bucket=bisect.bisect(self.lowerbounds,result)-1
        result=self.lowerbounds[bucket]+random.random()*((self.lowerbounds+[1.0])[bucket+1]-self.lowerbounds[bucket])
        if self.split:
            self.lowerbounds[bucket + 1:bucket + 1] = [(self.lowerbounds[bucket] + (self.lowerbounds + [1.0])[bucket + 1]) / 2.0]
        return result

class simpleteacher:
    def __init__(self,threshhold=None,zeroresponse=None,negoneresponse=None,startmove=None,override=[],correctparams=False):
        if threshhold is None:
            self.threshhold=random.random()
            self.zeroresponse=random.uniform(-1,min(0,2*math.sqrt(1-self.threshhold**2)-1))
            self.negoneresponse=random.uniform(-1,1+self.zeroresponse)
        else:
            self.threshhold=threshhold
            self.zeroresponse=zeroresponse
            if 1+zeroresponse+.0001>2*math.sqrt(1-threshhold**2):
                if correctparams:
                    self.zeroresponse=min(0,2*math.sqrt(1-threshhold**2)-1)
                else:
                    raise ValueError("Threshhold not best response for opponent: "+str(threshhold)+", "+str(zeroresponse))
            self.negoneresponse=negoneresponse
            if negoneresponse-.0001>1+self.zeroresponse:
                if correctparams:
                    self.negoneresponse=0
                else:
                    raise ValueError("Opponent motivated to punish")
        if startmove is None:
            self.startmove=math.sqrt(1-self.threshhold**2)
        else:
            self.startmove=startmove
        self.override=[x for x in override]
        self.initoverride=[x for x in override]
        self.irrationalopponent=False
        self.noise=None

    def setstartmove(self,move):
        self.initoverride=[move]
        self.override=[move]

    def __str__(self):
        return "Simple Teacher: "+str((self.threshhold,self.zeroresponse,self.negoneresponse))

    def __repr__(self):
        return str(self)

    def respond(self,oppchoice):
        if oppchoice is None:
            result=self.startmove
        elif len(self.override)>0:
            result=self.override.pop(0)
        elif oppchoice>=self.threshhold:
            if self.irrationalopponent:
                result=math.sqrt(1-oppchoice**2)
            else:
                result=math.sqrt(1-self.threshhold**2)
        elif oppchoice>=0:
            result=interpolate((0,self.zeroresponse),(self.threshhold,math.sqrt(1-self.threshhold**2)),oppchoice)
        else:
            result=interpolate((-1,self.negoneresponse),(0,self.zeroresponse),oppchoice)
        if self.noise is not None:
            if random.random()<self.noise:
                result=random.uniform(-1,1)
        return result

    def perturb(self,mag):
        newthreshhold=max(0,min(1,self.threshhold+random.normalvariate(0,mag)))
        newzeroresponse=max(-1,min(2*math.sqrt(1-newthreshhold**2)-1,self.zeroresponse+random.normalvariate(0,mag)))
        newnegoneresponse=max(-1,min(1,1+newzeroresponse,self.negoneresponse+random.normalvariate(0,mag)))
        return simpleteacher(newthreshhold,newzeroresponse,newnegoneresponse)

    def getDescription(self):
        return "Simple Teacher\n  Threshhold: %.3f\n  Zero Response: %.3f\n  NegOne Response: %.3f\n"%(self.threshhold,self.zeroresponse,self.negoneresponse)

    def getStatus(self):
        return ""

    def reset(self):
        self.override=[x for x in self.initoverride]

    def clone(self):
        return simpleteacher(self.threshhold,self.zeroresponse,self.negoneresponse,self.startmove,self.initoverride)

def stratperturb(val,amt):
    return max(-1,min(1,val+random.normalvariate(0,amt)))

class reciprocal:
    def __init__(self,strat,bias=None,startmove=0,perturb_type="simul"):
        """
        strat is an ordered list of tuples (amount opp gives me,amount I give opponent)
        :param strat:
        """
        self.strat=strat
        self.bias=bias
        self.startmove=startmove
        self.perturb_type=perturb_type

    def __str__(self):
        return "Reciprocating: "+str(self.strat)

    def __repr__(self):
        return str(self)

    def reset(self):
        pass

    def respond(self,oppchoice):
        if oppchoice is None:
            return self.startmove
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

    def perturb(self,mag):
        if self.perturb_type=="simul":
            perturbstrat=[(-1,stratperturb(self.strat[0][1],mag))]+\
                 [(stratperturb(s[0],mag),stratperturb(s[1],mag)) for s in self.strat[1:-1]]+\
                 [(1,stratperturb(self.strat[-1][1],mag))]
        elif self.perturb_type=="single":
            perturbstrat=[x for x in self.strat]
            i=random.randint(0,len(self.strat)-1)
            if i==0 or i==len(self.strat)-1:
                perturbstrat[i]=(perturbstrat[i][0],stratperturb(perturbstrat[i][1],mag))
            else:
                perturbstrat[i]=(stratperturb(perturbstrat[i][0],mag),stratperturb(perturbstrat[i][1],mag))
        else:
            raise ValueError("unrecognized perturb type: "+str(self.perturb_type))
        perturbstrat.sort()
        return reciprocal(perturbstrat,self.bias,self.startmove,self.perturb_type)

    def getachievableset(self,pointcount=100):
        """
        Note: This is the set achieveable by the opponent from the agent's perspective (i.e. my_payoff,opp_payoff)
        :param pointcount:
        :return:
        """
        result=[]
        for i in range(pointcount):
            a=i*2*math.pi/pointcount
            opp_c_opp=math.sin(a)
            opp_c_me=math.cos(a)
            me_c_opp=self.respond(opp_c_me)
            me_c_me=math.sqrt(1-me_c_opp**2)
            result.append((opp_c_me+me_c_me,opp_c_opp+me_c_opp))
        return result

