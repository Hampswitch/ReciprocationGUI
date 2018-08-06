"""
This script exists to explore the effect of noise on the performance of teaching strategies and learning strategies
"""

import reciprocation.teachingstrategies as ts
import reciprocation.UCB as UCB
import reciprocation.genetic_alg as ga

greedy=ts.simpleteacher(.951,-.4,0)
fair=ts.simpleteacher(.7,0,0)
generous=ts.simpleteacher(.5,0,0)

opplist=[greedy,fair,generous]
oppnames=["greedy","fair","generous"]

for opp in range(len(opplist)):
    lfile=open(oppnames[opp]+"learner.csv","w")
    tfile=open(oppnames[opp]+"teacher.csv","w")
    lfile.write(",.5,.25,.125,.0625,.03125,0\n")
    tfile.write(",.5,.25,.125,.0625,.03125,0\n")
    for exploration in [1.0,.5,.25,.125,.0625,.03125]:
        learner = UCB.BucketUCB(8, 1, 1, .001, exploration=exploration)
        tline=str(exploration)
        lline=str(exploration)
        for noise in [.5,.25,.125,.0625,.03125,0]:
            print (exploration,noise)
            result=ga.evaluate(opplist[opp],learner,1000,.99,100,0.0,noise)
            tline=tline+","+str(result[0])
            lline=lline+","+str(result[2])
        lfile.write(lline+"\n")
        tfile.write(tline+"\n")
    lfile.close()
    tfile.close()