import reciprocation.learningstrategies
import reciprocation.reciprocatingstrategies as strats
import reciprocation.guilearners as learners
import math

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