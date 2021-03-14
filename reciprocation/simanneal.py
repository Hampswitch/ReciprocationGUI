"""
This file contains a simulated annealing program intended to work on linear strategies
"""

import multiprocessing
import dill
import genetic_alg as ga
import linearstrat as ls
import UCB as ucb
import reciprocation.evaluation
import distplayer


def evalwrap(dillarglist):
    opponent,particle,iterations,discountfactor,repetitions,skiprounds=dill.loads(dillarglist)
    if "getSamples" in dir(opponent):
        result = 0.0
        for o in opponent.getSamples(repetitions):
            result = result + \
                     reciprocation.evaluation.evaluate(o, particle, iterations, discountfactor, 1, skipfirst=skiprounds)[1]
        result=result / repetitions
    elif isinstance(opponent, distplayer.distplayer):
        result = 0.0
        for player, wt in zip(opponent.playerlist, opponent.weights):
            result = result + wt * reciprocation.evaluation.evaluate(player, particle, iterations, discountfactor, repetitions,
                                                                     skipfirst=skiprounds)[1 if repetitions == 1 else 2]
    else:
        result=reciprocation.evaluation.evaluate(opponent, particle, iterations, discountfactor, repetitions, skipfirst=skiprounds)[1 if repetitions == 1 else 2]
    return result

def paralleleval(opponent,population,iterations,discountfactor,repetitions,skiprounds,processes=4):
    pool=multiprocessing.Pool(processes=processes)
    results=[]
    for p in population:
        results.append(pool.apply_async(evalwrap,(dill.dumps((opponent,p,iterations,discountfactor,repetitions,skiprounds)),)))
    pool.close()
    pool.join()
    return [r.get() for r in results]

def nonparalleleval(opponent,population,iterations,discountfactor,repetitions,skiprounds):
    results=[]
    for p in population:
        if "getSamples" in dir(opponent):
            result=0.0
            for o in opponent.getSamples(repetitions):
                result=result+ reciprocation.evaluation.evaluate(o, p, iterations, discountfactor, 1, skipfirst=skiprounds)[1]
            results.append(result/repetitions)
        elif isinstance(opponent,distplayer.distplayer):
            result = 0.0
            for player, wt in zip(opponent.playerlist, opponent.weights):
                result = result + wt * reciprocation.evaluation.evaluate(player, p, iterations, discountfactor, repetitions, skipfirst=skiprounds)[1 if repetitions==1 else 2]
            results.append(result)
        else:
            results.append(reciprocation.evaluation.evaluate(opponent, p, iterations, discountfactor, repetitions, skipfirst=skiprounds)[1 if repetitions==1 else 2])
    return results

def anneal(population,opponent,stepsize,stepratio,minstep,perturbfunc="perturb",perturbargs=[],iterations=1000,discountfactor=.99,repetitions=1,processes=4,verbose=False,skiprounds=0):
    while stepsize>minstep:
        # Create potential children
        expandpop=population+[perturbed for member in population for perturbed in getattr(member,perturbfunc)(stepsize,*perturbargs)]
        # Evaluate potential children
        if processes is not None:
            evaluations=paralleleval(opponent,expandpop,iterations,discountfactor,repetitions,skiprounds,processes)
        else:
            evaluations=nonparalleleval(opponent,expandpop,iterations,discountfactor,repetitions,skiprounds)
        if verbose:
            print "Step size: {}".format(stepsize)
            print max(evaluations)
            print(sum(evaluations)/len(evaluations))
        # Select best children
        population=[expandpop[i] for s,i in sorted([(y,x) for x,y in enumerate(evaluations)])[-len(population):]]
        stepsize=stepsize*stepratio
    return population

if __name__=="__main__":
    learner=ucb.TrackBucketUCB(8,1,4,.001,None,True,0)
    print anneal([ls.regularlinearstrat.random(9) for i in range(10)],learner,.2,.95,.05,"splitperturb",[4],1000,.99,10,None,True)