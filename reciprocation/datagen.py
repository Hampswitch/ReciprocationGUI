import reciprocation.learningstrategies as learners
import reciprocation.teachingstrategies as strats
import reciprocation.genetic_alg as ga
import math
import numpy
import pandas

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
        return numpy.random.beta(alpha,beta)
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

simplegreedystrat=strats.simpleteacher(99.0/101,-1,-.5)
simplefairstrat=strats.simpleteacher(math.sqrt(2)/2,0,-1)
simplegenerousstrat=strats.simpleteacher(20.0/101,0,0)

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

competitornamelist=["UCT","Greedy","Fair","Generous","UCT-Greedy-Low","UCT-Greedy-Med","UCT-Greedy-High","UCT-Fair-Low","UCT-Fair-Med","UCT-Fair-High",
                    "UCT-Generous-Low","UCT-Generous-Med","UCT-Generous-High"]

competitorlist1=[learners.player("UCT",c=1),simplegreedystrat,simplefairstrat,simplegenerousstrat,
                 learners.player("UCT", c=1, teachingstrat=simplegreedystrat, teachingweight=.125),
                 learners.player("UCT", c=1, teachingstrat=simplegreedystrat, teachingweight=.5),
                 learners.player("UCT", c=1, teachingstrat=simplegreedystrat, teachingweight=2),
                 learners.player("UCT", c=1, teachingstrat=simplefairstrat, teachingweight=.125),
                 learners.player("UCT", c=1, teachingstrat=simplefairstrat, teachingweight=.5),
                 learners.player("UCT", c=1, teachingstrat=simplefairstrat, teachingweight=2),
                 learners.player("UCT", c=1, teachingstrat=simplegenerousstrat, teachingweight=.125),
                 learners.player("UCT", c=1, teachingstrat=simplegenerousstrat, teachingweight=.5),
                 learners.player("UCT", c=1, teachingstrat=simplegenerousstrat, teachingweight=2)]

competitorlist2=[learners.player("UCT",c=1),simplegreedystrat,simplefairstrat,simplegenerousstrat,
                 learners.player("UCT", c=1, teachingstrat=simplegreedystrat, teachingweight=.125),
                 learners.player("UCT", c=1, teachingstrat=simplegreedystrat, teachingweight=.5),
                 learners.player("UCT", c=1, teachingstrat=simplegreedystrat, teachingweight=2),
                 learners.player("UCT", c=1, teachingstrat=simplefairstrat, teachingweight=.125),
                 learners.player("UCT", c=1, teachingstrat=simplefairstrat, teachingweight=.5),
                 learners.player("UCT", c=1, teachingstrat=simplefairstrat, teachingweight=2),
                 learners.player("UCT", c=1, teachingstrat=simplegenerousstrat, teachingweight=.125),
                 learners.player("UCT", c=1, teachingstrat=simplegenerousstrat, teachingweight=.5),
                 learners.player("UCT", c=1, teachingstrat=simplegenerousstrat, teachingweight=2)]

if __name__=="__main__":
    data=pandas.read_csv("TLanneal.csv",index_col=[0,1,2,3,4,5,6,7])
    for row in data.iterrows():
        agent=learners.player("UCT",c=row[1]["agent_c"],teachingstrat=strats.simpleteacher(row[1]["agent_threshhold"],row[1]["agent_zero"],row[1]["agent_negone"]),teachingweight=row[1]["agent_tweight"])
        opponent=learners.player("UCT",c=row[0][1],teachingstrat=strats.simpleteacher(row[0][2],row[0][3],row[0][4]),teachingweight=row[0][5])
        print "\t".join(str(v) for v in ga.evaluate(agent,opponent,1000,.99,100))

if __name__=="calcmeanoutcomes":
    resultdict={}

    for (c1,n1) in zip(competitorlist1,competitornamelist):
        for (c2,n2) in zip(competitorlist2,competitornamelist):
            print n1+"-"+n2
            if "reset" in dir(c1):
                c1.reset()
            if "reset" in dir(c2):
                c2.reset()
            resultdict[(n1,n2)]=ga.evaluate(c1,c2,1000,discountfactor=.99,repetitions=10)

    print resultdict

    meanfile=open("meandataanneal.csv","w")
    stdfile=open("stddataanneal.csv","w")
    meanfile.write(","+",".join(competitornamelist)+"\n")
    stdfile.write(","+",".join(competitornamelist)+"\n")
    for n1 in competitornamelist:
        meanline=n1
        stdline=n1
        for n2 in competitornamelist:
            meanline=meanline+","+str((resultdict[(n1,n2)][0]+resultdict[(n2,n1)][2])/2.0)
            stdline=stdline+","+str(combine_SD(resultdict[(n1,n2)][0],resultdict[(n1,n2)][1],10,resultdict[(n2,n1)][2],resultdict[(n2,n1)][3],10))
        meanfile.write(meanline+"\n")
        stdfile.write(stdline+"\n")

    meanfile.close()
    stdfile.close()

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