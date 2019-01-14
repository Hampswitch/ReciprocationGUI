import SAscript
import reciprocation.simanneal as sa

c = 22

o, e, a, p = SAscript.combinedparams[c]

print (c, SAscript.opponentparams[o], SAscript.evaluationparams[e], SAscript.annealparams[a], SAscript.particleparams[p])

opponent = SAscript.getopponent(o)

for dupe in range(10):
    particles, perturbfunc, perturbargs = SAscript.getparticleparams(p)
    stepsize, stepratio, minstep, repetitions = SAscript.getannealparams(a)
    discount, iterations, skiprounds = SAscript.getevalparams(e)
    print sa.anneal(particles, opponent, stepsize, stepratio, minstep, perturbfunc,
                    perturbargs, iterations, discount, repetitions, None, skiprounds=skiprounds, verbose=False)