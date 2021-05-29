
import reciprocation.simanneal as sa
import reciprocation.seqstrat as negot

import reciprocation.evaluation as eva

if __name__=="__main__":

    generations=100

    iterations=1000
    discount=.99
    repetitions=1
    skiprounds = 0

    particlecount=40
    stepsize=.5
    stepratio=.99
    minstep=0.01
    perturbfunc="hillclimb"
    perturbargs=(1,)

    verbose=True
    processes=None

    filename="../results/selfplay/selfplay5.txt"

    opponent=negot.thresholdfunctionparticle.fixedOppLoss(30)

    fullsequence=[]
    for i in range(generations):
        particles=[negot.thresholdfunctionparticle.fromRandom() for i in range(particlecount)]
        result = sa.anneal(particles, opponent, stepsize, stepratio, minstep, perturbfunc,
                       perturbargs, iterations, discount, repetitions, processes=processes, skiprounds=skiprounds,
                       verbose=verbose)
        fullsequence.append(result[0])
        print(result[0])
        opponent=result[0]
    with open(filename,"w") as file:
        file.writelines([str(s) for s in fullsequence])
