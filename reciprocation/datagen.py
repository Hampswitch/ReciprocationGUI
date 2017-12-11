import reciprocation.learningstrategies as learners
import reciprocation.teachingstrategies as strats
import reciprocation.genetic_alg as ga
import math
import shapely.geometry as sg

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

greedyset=learners.getacceptableset(greedystrat)
generousset=learners.getacceptableset(generousstrat)
fairset=learners.getacceptableset(fairstrat)

competitorlist1=[strats.reciprocal(greedystrat,startmove=.198),strats.reciprocal(generousstrat,startmove=.7),strats.reciprocal(fairstrat,startmove=.7),
                 strats.achievableteacher(greedyset,startmove=.198),strats.achievableteacher(generousset,startmove=.7),strats.achievableteacher(fairset,startmove=.7),
                 strats.achievableteacher(greedyset,average=True,startmove=.198),strats.achievableteacher(generousset,average=True,startmove=.7),strats.achievableteacher(fairset,average=True,startmove=.7),
                 learners.player("UCT",c=1),learners.player("UCT",c=1,acceptableset=greedyset),learners.player("UCT",c=1,acceptableset=generousset),learners.player("UCT",c=1,acceptableset=fairset),learners.player("UCT",c=1,envy=.5,fairness=0)]

competitorlist2=[strats.reciprocal(greedystrat),strats.reciprocal(generousstrat),strats.reciprocal(fairstrat),
                 strats.achievableteacher(greedyset),strats.achievableteacher(generousset),strats.achievableteacher(fairset),
                 strats.achievableteacher(greedyset,average=True),strats.achievableteacher(generousset,average=True),strats.achievableteacher(fairset,average=True),
                 learners.player("UCT",c=1),learners.player("UCT",c=1,acceptableset=greedyset),learners.player("UCT",c=1,acceptableset=generousset),learners.player("UCT",c=1,acceptableset=fairset),learners.player("UCT",c=1,envy=.5,fairness=0)]

if __name__=="__main__":
    resultdict={}

    for (c1,n1) in zip(competitorlist1,competitornamelist):
        for (c2,n2) in zip(competitorlist2,competitornamelist):
            print n1+"-"+n2
            if "reset" in dir(c1):
                c1.reset()
            if "reset" in dir(c2):
                c2.reset()
            resultdict[(n1,n2)]=ga.evaluate(c1,c2,10000,repetitions=10)

    print resultdict

    meanfile=open("meandata.csv","w")
    stdfile=open("stddata.csv","w")
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