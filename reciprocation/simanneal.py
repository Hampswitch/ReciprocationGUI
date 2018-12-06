"""
This file contains a simulated annealing program intended to work on linear strategies
"""

import multiprocessing
import dill
import genetic_alg as ga
import linearstrat as ls
import UCB as ucb

def evalwrap(dillarglist):
    arglist=dill.loads(dillarglist)
    opponent,particle,iterations,discountfactor,repetitions,skiprounds=dill.loads(dillarglist)
    result=ga.evaluate(opponent,particle,iterations,discountfactor,repetitions,skipfirst=arglist[5])
    if arglist[4]<2:
        return result[1]
    else:
        return result[2]

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
        if repetitions<2:
            results.append(ga.evaluate(opponent, p, iterations, discountfactor, repetitions,skipfirst=skiprounds)[1])
        else:
            results.append(ga.evaluate(opponent,p,iterations,discountfactor,repetitions,skipfirst=skiprounds)[2])
    return results

def anneal(population,opponent,stepsize,stepratio,minstep,perturbfunc="perturb",perturbargs=[],iterations=1000,discountfactor=.99,repetitions=1,processes=4,verbose=False,skiprounds=0):
    while stepsize>minstep:
        # Create potential children
        expandpop=[perturbed for member in population for perturbed in getattr(member,perturbfunc)(stepsize,*perturbargs)]
        # Evaluate potential children
        if processes is not None:
            evaluations=paralleleval(opponent,expandpop,iterations,discountfactor,repetitions,skiprounds,processes)
        else:
            evaluations=nonparalleleval(opponent,expandpop,iterations,discountfactor,repetitions,skiprounds)
        if verbose:
            print stepsize
            print(sum(evaluations)/len(evaluations))
        # Select best children
        population=[expandpop[i] for s,i in sorted([(y,x) for x,y in enumerate(evaluations)])[-len(population):]]
        stepsize=stepsize*stepratio
    return population

if __name__=="__main__":
    learner=ucb.TrackBucketUCB()
    print anneal([ls.linearstrat.regularlinear(5) for i in range(10)],learner,.2,.9,.001,"fullvertperturb",[4],1000,.99,1,None,True)