
import reciprocation.UCB as ucb
import reciprocation.simanneal as sa
import reciprocation.linearstrat as ls
import sys
import reciprocation.learningstrategies as learn
import reciprocation.KNNUCB as knnucb
import reciprocation.negotiator as negot
import reciprocation.distplayer as distplayer

# params : stepsize,stepratio,minstep,repetitions
# base : .2,.9,.001,1

# learnertype, explore
opponentparams=[("UCBsplit",1.0),
                ("UCBsplit",.125),
                ("MixedDist1",),
                ("MixedDist2",),
                ("MixedDist3",),
                ("LearnerThresholdMix",1.0,.8,.5), #5
                ("LearnerThresholdMix",1.0,.8,.1),
                ("LearnerThresholdMix",1.0,.8,.9),
                ("LearnerThresholdMix",.125,.8,.5),
                ("LearnerThresholdMix",1.0,.5,.5),
                ("LearnerThresholdMix",1.0,.95,.5),
                ("ThresholdThresholdMix",.9,.5,.5),
                ("ThresholdThresholdMix",.9,.5,.9),
                ("ThresholdThresholdMix",.9,.5,.1),
                ("StubbornMix",.8,.5,.5,5), #14
                ("StubbornMix",.8,.5,.5,2),
                ("StubbornMix",.95,.5,.5,5),
                ("StubbornMix",.6,.5,.5,5),
                ("StubbornMix",.8,.5,.1,5),
                ("StubbornMix",.8,.5,.9,5)]

# discount, iterations, skiprounds
evaluationparams=[(.99,1000,0),
                  (.99,1000,10),
                  (.99,1000,50),
                  (1.0,1000,10),
                  (1.0,1000,50),
                  (1.0,1000,0)]

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
                ((10,"biasedlinear"),"fullvertperturb",(8,)),
                ((10,"seqslope"),"fullpermute",(8,))]

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
                (0,4,0,0),
                (2,5,0,5), # 10
                (3,5,0,5),
                (4,5,0,5),
                (2,0,0,5),
                (3,0,0,5),
                (4,0,0,5),
                (5, 5, 0, 5),
                (6, 5, 0, 5),
                (7, 5, 0, 5),
                (8, 5, 0, 5),
                (9, 5, 0, 5), #20
                (10, 5, 0, 5),
                (11, 5, 0, 5),
                (12, 5, 0, 5),
                (13, 5, 0, 5),
                (14, 5, 0, 5),
                (15, 5, 0, 5),
                (16, 5, 0, 5),
                (17, 5, 0, 5),
                (18, 5, 0, 5),
                (19, 5, 0, 5), #30
                (5,0,0,5),
                (6,0,0,5),
                (7,0,0,5),
                (8,0,0,5),
                (9,0,0,5),
                (10,0,0,5),
                (11,0,0,5),
                (12,0,0,5),
                (13,0,0,5),
                (14,0,0,5), #40
                (15,0,0,5),
                (16,0,0,5),
                (17,0,0,5),
                (18,0,0,5),
                (19,0,0,5)]

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
    elif opponentparams[index][0]=="MixedDist1":
        return  distplayer.distplayer([ucb.TrackBucketUCB(8, 1.0, 4, .001, widthexp=1),ls.slopestrat(.8)],[.5,.5])
    elif opponentparams[index][0]=="MixedDist2":
        return distplayer.distplayer([ls.slopestrat(.9),ls.slopestrat(.5)], [.5, .5])
    elif opponentparams[index][0]=="MixedDist3":
        return distplayer.distplayer([ls.slopestrat(.8),negot.stepannealer([(.8,5),(.5,100)])], [.5, .5])
    elif opponentparams[index][0]=="LearnerThresholdMix":
        return distplayer.distplayer([ucb.TrackBucketUCB(8, opponentparams[index][1], 4, .001, widthexp=1),ls.slopestrat(opponentparams[index][2])],[opponentparams[index][3],1.0-opponentparams[index][3]])
    elif opponentparams[index][0]=="ThresholdThresholdMix":
        return distplayer.distplayer([ls.slopestrat(opponentparams[index][1]), ls.slopestrat(opponentparams[index][2])], [opponentparams[index][3],1.0-opponentparams[index][3]])
    elif opponentparams[index][0]=="StubbornMix":
        return distplayer.distplayer([ls.slopestrat(opponentparams[index][1]), negot.stepannealer([(opponentparams[index][1], opponentparams[index][4]), (opponentparams[index][2], 100)])], [opponentparams[index][3],1.0-opponentparams[index][3]])
    else:
        raise ValueError("Unrecognized Opponent Type: "+opponentparams[index][0])



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
    elif particle[1]=="seqslope":
        return ([negot.stepannealer() for i in range(particle[0])],perturbfunc,perturbargs)
    else:
        raise ValueError("Unrecognized particle type: "+str(particle[1]))


if __name__=="__main__":
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
