
import reciprocation.UCB as ucb
import reciprocation.simanneal as sa
import reciprocation.linearstrat as ls
import sys
import reciprocation.learningstrategies as learn
import reciprocation.KNNUCB as knnucb
import reciprocation.seqstrat as negot
import reciprocation.distplayer as distplayer
import reciprocation.discretegame as discrete

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
                ("StubbornMix",.8,.5,.9,5),
                ("DiscreteUCB", 2.0, 8), #20
                ("DiscreteUCB",1.0,8),
                ("DiscreteUCB",.5,8),
                ("DiscreteUCB",.25,8),
                ("DiscreteUCB",2.0,16),
                ("DiscreteUCB",1.0,16),
                ("DiscreteUCB",.5,16),
                ("DiscreteUCB",.25,16),
                ("DiscreteUCB",2.0,32),
                ("DiscreteUCB",1.0,32),
                ("DiscreteUCB",.5,32), #30
                ("DiscreteUCB",.25,32),
                ("GeneralMixed",("constslope",10),0.0,("constslope",20),0.0,("constslope",30),1.0),
                ("GeneralMixed",("constslope",10),0.0,("constslope",20),1.0,("constslope",30),0.0),
                ("GeneralMixed",("constslope",10),1.0,("constslope",20),0.0,("constslope",30),0.0),
                ("GeneralMixed",("constslope",10),0.33,("constslope",20),0.33,("constslope",30),0.34), #35
                ("RandomAutocratic",),
                ("RandomOppLoss",1,50),
                ("RandomStep",.9,.6,1,50),
                ] #35


# discount, iterations, skiprounds
evaluationparams=[(.99,1000,0),
                  (.99,1000,10),
                  (.99,1000,50),
                  (1.0,1000,10),
                  (1.0,1000,50),
                  (1.0,1000,0), #5
                  (.999,10000,0),
                  (.9999,100000,0),
                  (1.0,10000,0),
                  (.99,10000,0),
                  (.98,10000,0), #10
                  (.96,10000,0),
                  (.92,10000,0),
                  (.95,1000,0),
                  (.98,1000,0),
                  (.995,2000,0), #15
                  (.998,2000,0)]

# stepsize,stepratio,minstep,repetitions
annealparams=[(.2,.99,.01,10),
              (.2,.995,.01,10),
              (.2,.99,.01,20),
              (.2,.997,.01,10),
              (.2,.9985,.01,10),
              (.5,.99,.05,10), #5
              (1,.99,.01,10),
              (.5,.995,.001,1),
              (.5,.99,.01,1),
              (.5,.99,.01,10)]

# perturbfunc,expandfactor,resolution
particleparams=[((10,"regularlinear",33),"fullvertperturb",(8,)),
                ((10, "regularlinear", 17), "fullperturb", (8,)),
                ((10,"regularlinear",65),"fullvertperturb",(8,)),
                ((10,"regularlinear",129),"fullvertperturb",(8,)),
                ((10,"biasedlinear"),"fullvertperturb",(8,)),
                ((10,"seqslope"),"fullpermute",(8,)), #5
                ((10,"discrete",16),"perturbsmall",(8,)),
                ((10,"discrete",16),"perturblarge",(8,)),
                ((10, "discreterandom", 8), "perturbsmall", (8,)),
                ((10, "discreterandom", 16), "perturbsmall", (8,)),
                ((10, "discreterandom", 32), "perturbsmall", (8,)), #10
                ((10,"thresholdfunction",10,20),"perturb",(20,)),
                ((10,"thresholdhillclimb",10,20),"hillclimb",(1,)),
                ((10,"thresholdrandom",10,20),"hillclimb",(1,)),
                ((10,"thresholdrandom",10,30),"hillclimb",(1,))]

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
                (19,0,0,5),
                (20,0,5,6),
                (20,0,5,7),
                (20,0,5,8),
                (20,6,5,8),
                (20,7,5,8), #50
                (25,8,5,9),
                (25, 9, 5, 9),
                (25, 10, 5, 9),
                (25, 11, 5, 9),
                (25, 12, 5, 9),
                (21, 8, 5, 8),
                (25, 8, 5, 9),
                (29, 8, 5, 10),
                (24, 8, 5, 9),
                (25, 8, 5, 9), #60
                (26, 8, 5, 9),
                (27, 8, 5, 9),
                (30,0,0,5),
                (32,0,6,11),
                (32,0,7,11), #65
                (33,0,7,11),
                (34,0,7,11),
                (35,0,7,11),
                (32,0,7,12),
                (32,0,7,13), #70
                (32,0,8,13),
                (33,0,8,13),
                (34,0,8,13),
                (32,0,8,13),
                (32,13,8,13), #75
                (32,14,8,13),
                (32,15,8,13),
                (32,16,8,13),
                (0,0,9,13),
                (1,0,9,13), #80
                (36,0,9,13),
                (37,0,9,13),
                (38,0,9,13),]

# 51-55 - discrete, varying discount factors
# 56-58 - discrete, varying # moves
# 59-62 - discrete, varying exploration

def mksingleopp(params):
    if params[0]=="constslope":
        return negot.thresholdfunctionparticle(points=3,totalloss=params[1])
    if params[0]=="fromstring":
        return negot.thresholdfunctionparticle.fromString(params[1])

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
    elif opponentparams[index][0]=="DiscreteUCB":
        return discrete.discreteucb(discrete.getdiscretemoves(opponentparams[index][2]),player=0,explore=opponentparams[index][1])
    elif opponentparams[index][0]=="GeneralMixed":
        return distplayer.distplayer([mksingleopp(i) for i in opponentparams[index][1:] if type(i)!=float],[i for i in opponentparams[index][1:] if type(i)==float])
    elif opponentparams[index][0]=="RandomAutocratic":
        return negot.thresholdfunctionparticle.randomAutocratic()
    elif opponentparams[index][0]=="RandomOppLoss":
        return negot.thresholdfunctionparticle.randomOppLoss(opponentparams[index][1],opponentparams[index][2])
    elif opponentparams[index][0]=="RandomStep":
        return negot.thresholdfunctionparticle.randomStep(opponentparams[index][1],opponentparams[index][2],opponentparams[index][3],opponentparams[index][4])
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
    elif particle[1]=="discrete":
        return ([discrete.discreteteacher(discrete.getdiscretemoves(particle[2]),player=1) for i in range(particle[0])],perturbfunc,perturbargs)
    elif particle[1]=="discreterandom":
        return ([discrete.randomizingteacher(discrete.getdiscretemoves(particle[2]),player=1) for i in range(particle[0])],perturbfunc,perturbargs)
    elif particle[1]=="thresholdfunction":
        return ([negot.thresholdfunctionparticle(points=particle[2],totalloss=particle[3]) for i in range(particle[0])],perturbfunc,perturbargs)
    elif particle[1]=="thresholdhillclimb":
        return (negot.thresholdfunctionparticle(points=particle[2],totalloss=particle[3]).hillclimb(.5),perturbfunc,perturbargs)
    elif particle[1]=="thresholdrandom":
        return ([negot.thresholdfunctionparticle.fromRandom() for i in range(particle[0])],perturbfunc,perturbargs)
    else:
        raise ValueError("Unrecognized particle type: "+str(particle[1]))


if __name__=="__main__":
    if False:
        c=int(sys.argv[1])
        processes=22
        verbose=False
    else:
        print "HARDCODED PARAMETERS!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
        c=71
        processes=None
        verbose=False
    o,e,a,p=combinedparams[c]

    print (c,opponentparams[o],evaluationparams[e],annealparams[a],particleparams[p])

    opponent=getopponent(o)

    allresults=[]

    opp3=negot.thresholdfunctionparticle.fromString("SeqAutocratic 0.1 0 <(1.0,0.0),(0.5,15.0),(0.0,30.0)>")

    for dupe in range(10):
        particles,perturbfunc,perturbargs=getparticleparams(p)
        stepsize,stepratio,minstep,repetitions=getannealparams(a)
        discount,iterations,skiprounds=getevalparams(e)
        print("Initial Particle: "+str(particles[0]))
        print("Opponent: "+str(opponent))
        result=sa.anneal(particles,opponent,stepsize,stepratio,minstep,perturbfunc,
                    perturbargs,iterations,discount,repetitions,processes=processes,skiprounds=skiprounds,verbose=verbose)
        print result
        allresults.append(result)
    print allresults

