import reciprocation.learningstrategies as learners
import reciprocation.teachingstrategies as teachers
import reciprocation.genetic_alg as ga

import math
import numpy as np
import pandas
import os.path
import time
import itertools
import matplotlib.pyplot as plot
import mpl_toolkits.mplot3d as mplot3d

def betadist(meanval,var):
    """
    This function will produce a beta distribution over values from -1 to 1 with the given mean and variance
    :param mean:
    :param var:
    :return:
    """
    m=(1-meanval)/meanval
    alpha=(m-var*(1+2*m+m**2))/(var*(1+3*m+3*m**2+m**3))
    beta=alpha*m
    if alpha>0 and beta>0:
        return np.random.beta(alpha,beta)
    else:
        raise ValueError("Maximum achievable variance for mean "+str(meanval)+" is "+str(meanval*(1-meanval)))

def combine_SD(m1,s1,n1,m2,s2,n2):
    m=(m1*n1+m2*n2)/(n1+n2)
    d1=m1-m
    d2=m2-m
    return math.sqrt((n1*(s1**2+d1**2)+n2*(s2**2+d2**2))/(n1+n2))

competitornamelist=["teaching-greedy","teaching-generous","teaching-fair","achievableset-greedy","achievableset-generous","achievableset-fair",
                    "achievableavgset-greedy","achievableavgset-generous","achievableavgset-fair",
                    "UCT-rational","UCT-acceptable-greedy","UCT-acceptable-generous","UCT-acceptable-fair","UCT-envy"]

greedystrat=[(-1,-1),(0,-1),(99.0/101,20.0/101),(1,20.0/101)]
generousstrat=[(-1,0),(0,0),(20.0/101,99.0/101),(1,99.0/101)]
fairstrat=[(-1,-1),(math.sqrt(2)/2,math.sqrt(2)/2),(1,math.sqrt(2)/2)]

simplegreedystrat=teachers.simpleteacher(99.0 / 101, -1, -.5)
simplefairstrat=teachers.simpleteacher(math.sqrt(2) / 2, 0, -1)
simplegenerousstrat=teachers.simpleteacher(20.0 / 101, 0, 0)

greedyset=learners.getacceptableset(greedystrat)
generousset=learners.getacceptableset(generousstrat)
fairset=learners.getacceptableset(fairstrat)

"""
competitorlist1=[strats.reciprocal(greedystrat,startmove=.198),strats.reciprocal(generousstrat,startmove=.7),strats.reciprocal(fairstrat,startmove=.7),
                 strats.achievableteacher(greedyset,startmove=.198),strats.achievableteacher(generousset,startmove=.7),strats.achievableteacher(fairset,startmove=.7),
                 strats.achievableteacher(greedyset,average=True,startmove=.198),strats.achievableteacher(generousset,average=True,startmove=.7),strats.achievableteacher(fairset,average=True,startmove=.7),
                 learners.player("UCT",c=1),learners.player("UCT",c=1,acceptableset=greedyset),learners.player("UCT",c=1,acceptableset=generousset),learners.player("UCT",c=1,acceptableset=fairset),learners.player("UCT",c=1,envy=.5,fairness=0)]

competitorlist2=[strats.reciprocal(greedystrat),strats.reciprocal(generousstrat),strats.reciprocal(fairstrat),
                 strats.achievableteacher(greedyset),strats.achievableteacher(generousset),strats.achievableteacher(fairset),
                 strats.achievableteacher(greedyset,average=True),strats.achievableteacher(generousset,average=True),strats.achievableteacher(fairset,average=True),
                 learners.player("UCT",c=1),learners.player("UCT",c=1,acceptableset=greedyset),learners.player("UCT",c=1,acceptableset=generousset),learners.player("UCT",c=1,acceptableset=fairset),learners.player("UCT",c=1,envy=.5,fairness=0)]
"""

"""
competitornamelist=["UCT","Greedy","Fair","Generous","UCT-Greedy-Low","UCT-Greedy-Med","UCT-Greedy-High","UCT-Fair-Low","UCT-Fair-Med","UCT-Fair-High",
                    "UCT-Generous-Low","UCT-Generous-Med","UCT-Generous-High"]

competitorlist1=[learners.player("UCT",c=1),strats.reciprocal(greedystrat),strats.reciprocal(generousstrat),strats.reciprocal(fairstrat),
                 learners.player("UCT", c=1, teachingstrat=strats.reciprocal(greedystrat), teachingweight=.125),
                 learners.player("UCT", c=1, teachingstrat=strats.reciprocal(greedystrat), teachingweight=.5),
                 learners.player("UCT", c=1, teachingstrat=strats.reciprocal(greedystrat), teachingweight=2),
                 learners.player("UCT", c=1, teachingstrat=strats.reciprocal(fairstrat), teachingweight=.125),
                 learners.player("UCT", c=1, teachingstrat=strats.reciprocal(fairstrat), teachingweight=.5),
                 learners.player("UCT", c=1, teachingstrat=strats.reciprocal(fairstrat), teachingweight=2),
                 learners.player("UCT", c=1, teachingstrat=strats.reciprocal(generousstrat), teachingweight=.125),
                 learners.player("UCT", c=1, teachingstrat=strats.reciprocal(generousstrat), teachingweight=.5),
                 learners.player("UCT", c=1, teachingstrat=strats.reciprocal(generousstrat), teachingweight=2)]

competitorlist2=[learners.player("UCT",c=1),strats.reciprocal(greedystrat),strats.reciprocal(generousstrat),strats.reciprocal(fairstrat),
                 learners.player("UCT", c=1, teachingstrat=strats.reciprocal(greedystrat), teachingweight=.125),
                 learners.player("UCT", c=1, teachingstrat=strats.reciprocal(greedystrat), teachingweight=.5),
                 learners.player("UCT", c=1, teachingstrat=strats.reciprocal(greedystrat), teachingweight=2),
                 learners.player("UCT", c=1, teachingstrat=strats.reciprocal(fairstrat), teachingweight=.125),
                 learners.player("UCT", c=1, teachingstrat=strats.reciprocal(fairstrat), teachingweight=.5),
                 learners.player("UCT", c=1, teachingstrat=strats.reciprocal(fairstrat), teachingweight=2),
                 learners.player("UCT", c=1, teachingstrat=strats.reciprocal(generousstrat), teachingweight=.125),
                 learners.player("UCT", c=1, teachingstrat=strats.reciprocal(generousstrat), teachingweight=.5),
                 learners.player("UCT", c=1, teachingstrat=strats.reciprocal(generousstrat), teachingweight=2)]
"""



rvals=[0.0,.156,.309,.454,.588,.707,.809,.891,.951,.988,1.0]

def getvalues(params):
    return [str(p[0]) if isinstance(p,tuple) else str(p) for p in params]

def getargs(params):
    return [p[1] if isinstance(p,tuple) else p for p in params]

def datagen_evaluate(p1class,p1params,p2class,p2params,discountfactors,iterationlengths,filename,headers):
    if headers is None:
        f=open(filename,"a")
    else:
        f=open(filename,"w")
        f.write(",".join(headers)+"\n")
    for discountfactor in discountfactors:
        for iterations in iterationlengths:
            for p1params in itertools.product(p1params):
                for p2params in itertools.product(p2params):
                    p1=p1class(*getargs(p1params))
                    p2=p2class(*getargs(p2params))
                    result=ga.evaluate(p1,p2,iterations,discountfactor)
                    f.write(",".join(getvalues(p1params)+getvalues(p2params)+[str(discountfactor),str(iterations),str(result[0]),str(result[2])])+"\n")
    f.close()

if __name__=="__main__":
    l=[]
    teacher=teachers.simpleteacher(.951,-1.0,-1.0)
    for m in [-x for x in rvals[-1:0:-1]]+rvals:
        l.append((m,teacher.respond(m)))
    l=np.array(l)
    d = pandas.read_csv("firstmove.csv", index_col=[0], header=0)
    fig = plot.figure()
    ax = plot.axes(projection='3d')
    ax.plot_wireframe(np.ones((21, 21)) * d.index.values, (np.ones((21, 21)) * d.index.values).transpose(), d.values)
    zs=[1.4263,1.4274,1.4269,1.4258,1.4242,1.4210,1.4174,1.4135,1.4080,1.4026,1.3790,1.3709,1.3639,1.3572,1.3522,1.3479,1.3450,1.3990,1.3996,1.3978,1.3971]
    ax.plot(xs=l[:,0],ys=l[:,1],zs=zs,color='red')
    ax.set_xlabel('opponent move')
    ax.set_ylabel('teacher response')

    
if __name__=="__main__firstmovemesh":
    for threshhold in [x for x in rvals if x<1]:
        for zero in [-x for x in rvals if 1 - x < 2 * math.sqrt(1 - threshhold * threshhold)]:
            for negone in [-x for x in rvals]:
                for startmove in [-x for x in rvals[-1:0:-1]]+rvals:
                    for initresponse in [-x for x in rvals[-1:0:-1]]+rvals:
                        learner=learners.player(learner=learners.UCTlearner(c=1.0),startmove=startmove)
                        teacher=teachers.simpleteacher(threshhold,zero,negone,override=[initresponse])
                        result=ga.evaluate(learner,teacher,1000,.99,1000)
                        print ", ".join([str(x) for x in [threshhold,zero,negone,startmove,initresponse,result[2]]])


if __name__=="__maain__":
    outfile=open("TLeval.csv","a")
    rvals=[0.0,.156,.309,.454,.588,.707,.809,.891,.951,.988,1.0]
    for discountfactor in[1.0]:
        print "D: "+str(discountfactor)
        for iterations in [1000]:
            print "I: "+str(iterations)
            for p1c in [.0625,.25,1,4]:
                print "p1c: "+str(p1c)
                for p2c in [1.0]: #[.0625,.25,1,4]:
                    print "p2c: "+str(p2c)
                    for p1t in [x for x in rvals if x<1]:
                        print "p1t: "+str(p1t)
                        for p2t in [.588,.809]: #[x for x in rvals if x<1]:
                            print "p2t: "+str(p2t)
                            for p1z in [-x for x in rvals if 1-x < 2*math.sqrt(1-p1t*p1t)]:
                                print "p1z: "+str(p1z)
                                for p2z in [-.588]: #[-x for x in rvals if 1-x < 2*math.sqrt(1-p2t*p2t)]:
                                    print "p2z: "+str(p2z)
                                    for p1n1 in [-x for x in rvals]:
                                        print "p1n1: "+str(p1n1)
                                        for p2n1 in [-.588]: #[-x for x in rvals]:
                                            print "p2n1: "+str(p2n1)
                                            for p1w in [0.0,.5,1.0,2.0,4.0,8.0,16.0]:
                                                for p2w in [2.0]: #[0.0,.5,1.0,2.0,4.0,8.0,16.0]:
                                                    if (discountfactor,iterations,1,p1c,p2c,p1t,p2t,p1z,p2z,p1n1,p2n1,p1w,p2w) not in result.index:
                                                        p1=learners.player("UCT", c=p1c, teachingstrat=teachers.simpleteacher(p1t, p1z, p1n1), teachingweight=p1w)
                                                        p2=learners.player("UCT", c=p2c, teachingstrat=teachers.simpleteacher(p2t, p2z, p2n1), teachingweight=p2w)
                                                        evaluation=ga.evaluate(p1,p2,iterations,discountfactor=discountfactor,repetitions=1)
                                                        print str((discountfactor,iterations,1,p1c,p2c,p1t,p2t,p1z,p2z,p1n1,p2n1,p1w,p2w))
                                                        result.loc[(discountfactor,iterations,1,p1c,p2c,p1t,p2t,p1z,p2z,p1n1,p2n1,p1w,p2w),:]=(evaluation[0],evaluation[2])
                                                        if max(result.index.duplicated()):
                                                            raise ValueError("Index duplicated: "+str((discountfactor,iterations,1,p1c,p2c,p1t,p2t,p1z,p2z,p1n1,p2n1,p1w,p2w)))
                                                    else:
                                                        print "skipped"
                                result.to_csv("TLeval.csv")
if __name__=="tlanneal":
    data=pandas.read_csv("TLanneal.csv",index_col=[0,1,2,3,4,5,6,7])
    for row in data.iterrows():
        agent=learners.player("UCT", c=row[1]["agent_c"], teachingstrat=teachers.simpleteacher(row[1]["agent_threshhold"], row[1]["agent_zero"], row[1]["agent_negone"]), teachingweight=row[1]["agent_tweight"])
        opponent=learners.player("UCT", c=row[0][1], teachingstrat=teachers.simpleteacher(row[0][2], row[0][3], row[0][4]), teachingweight=row[0][5])
        print "\t".join(str(v) for v in ga.evaluate(agent,opponent,1000,.99,100))



if __name__=="noisedata":
    resultfile=open("noisedata.csv","w")
    resultfile.write(",greedy,fair,generous,\n")
    uct=learners.player("UCT",c=1)
    for noise in [0,.1,.2,.3,.4,.5,.6,.7,.8,.9,1]:
        outline=str(noise)+","
        for strat in [simplegreedystrat,simplefairstrat,simplegenerousstrat]:
            strat.noise=noise
            e=ga.evaluate(uct,strat,10000,1,100)
            outline=outline+str(e[2])+","
        resultfile.write(outline+"\n")
    resultfile.close()

"""
tlist=[math.sin(math.pi*r/40.0) for r in range(1,20)]
stratlist=[[(0,-1),(t,math.sqrt(1-t**2))] for t in tlist]+[[(0,0),(t,math.sqrt(1-t**2))] for t in tlist if math.sqrt(1-t**2)>.5]
reciprocalstrats=[strats.reciprocal(r) for r in stratlist]

learnerparams=[.0625,.25,1,4,16]

for discount in [.9,.999,.9999]:
    for l in learnerparams:
        line=""
        for reciprocal in reciprocalstrats:
            uct= reciprocation.learningstrategies.UCTlearner(l)
            curdiscount=1.0
            recipscore=0.0
            uctscore=0.0
            for i in range(1000):
                move=uct.pickmove()
                response=reciprocal.respond(move)
                uctscore=uctscore+curdiscount*(math.sqrt(1-move**2)+response)
                recipscore=recipscore+curdiscount*(move+math.sqrt(1-response**2))
                uct.observe(move,math.sqrt(1-move**2)+response)
                curdiscount=curdiscount*discount
            line=line+"\t"+str(recipscore)
        print line
"""