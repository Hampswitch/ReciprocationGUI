
import reciprocation.UCB as ucb
import reciprocation.simanneal as sa
import reciprocation.linearstrat as ls
import sys
import reciprocation.learningstrategies as learn
import reciprocation.KNNUCB as knnucb

# params : stepsize,stepratio,minstep,repetitions
# base : .2,.9,.001,1

# learnertype, explore
opponentparams=[("UCBsplit",1.0),
                ("UCBsplit",.125)]

# discount, iterations, skiprounds
evaluationparams=[(.99,1000,0),
                  (.99,1000,10),
                  (.99,1000,50),
                  (1.0,1000,10),
                  (1.0,1000,50)]

# stepsize,stepratio,minstep,repetitions
annealparams=[(.2,.99,.01,10),
              (.2,.995,.01,10),
              (.2,.99,.01,20),
              (.2,.997,.01,10),
              (.2,.9985,.01,10)]

# perturbfunc,expandfactor,resolution
particleparams=[((10,"regularlinear",33),"fullvertperturb",(8,)),
                ((10, "regularlinear", 17), "fullperturb", (8,)),
                ((10,"regularlinear",65),"fullvertperturb",(8,)),
                ((10,"regularlinear",129),"fullvertperturb",(8,)),
                ((10,"biasedlinear"),"fullvertperturb",(8,))]

# opponent,eval,anneal,particle
combinedparams=[(0,0,0,0),
                (0,0,0,1),
                (0,0,3,3),
                (0,0,4,3),
                (0,0,0,4), # bugged
                (0,4,0,4), # bugged
                (0,1,0,0),
                (0,2,0,0),
                (0,3,0,0),
                (0,4,0,0)]

def getopponent(index):
    if opponentparams[index][0]=="fastlearner":
        return learn.fastlearner()
    elif opponentparams[index][0]=="UCT":
        return learn.player(learner=learn.UCTlearner(c=.35, initdata=None, bucketcount=2), radial=True)
    elif opponentparams[index][0]=="UCBsplit":
        return ucb.TrackBucketUCB(8, opponentparams[index][1], 4, .001, widthexp=1)
    elif opponentparams[index][0]=="UCB":
        return ucb.TrackBucketUCB(8, opponentparams[index][1], 4000, .001, widthexp=1)
    elif opponentparams[index][0]=="KNN":
        return knnucb.KNNUCBplayer(4, .4, .35)
    elif opponentparams[index][0]=="Simple":
        return ucb.TrackBucketUCB(8, 0, 4000, .001, widthexp=1)



def getevalparams(index):
    return evaluationparams[index]

def getannealparams(index):
    return annealparams[index]

def getparticleparams(index):
    """
    returns particlelist,perturbfunc,perturbargs
    :param index:
    :return:
    """
    particle=particleparams[index][0]
    perturbfunc=particleparams[index][1]
    perturbargs=particleparams[index][2]
    if particle[1]=="regularlinear":
        return ([ls.linearstrat.regularlinear(particle[2]) for i in range(particle[0])],perturbfunc,perturbargs)
    elif particle[1]=="biasedlinear":
        return ([ls.linearstrat.biasedlinear() for i in range(particle[0])],perturbfunc,perturbargs)
    else:
        raise ValueError("Unrecognized particle type: "+str(particle[1]))



c=int(sys.argv[1])

o,e,a,p=combinedparams[c]

print (c,opponentparams[o],evaluationparams[e],annealparams[a],particleparams[p])

opponent=getopponent(o)


for dupe in range(10):
    particles,perturbfunc,perturbargs=getparticleparams(p)
    stepsize,stepratio,minstep,repetitions=getannealparams(a)
    discount,iterations,skiprounds=getevalparams(e)
    print sa.anneal(particles,opponent,stepsize,stepratio,minstep,perturbfunc,
                    perturbargs,iterations,discount,repetitions,22,skiprounds=skiprounds,verbose=False)
