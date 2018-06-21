
"""
This file contains scripts to create basic first move meshes
paramcodes:

teachers:
    simpleteacher greedy/generous/fair
    mesh teachers?
learners:
UCB
    high/low explore
    starting buckets
    split/nosplit
    prior (accurate/inaccurate)

"""

import reciprocation.meshutils as meshutils
import reciprocation.teachingstrategies as ts
import reciprocation.UCB as ucb
import reciprocation.teachinglearning as tl

import sys

params=[

    (.707, 0, 0, 8, 1, 1, .001, 1, 1, 1000, .99, 100, None, None, None, None), # ucb split
    (.951, -.4, 0, 8, 1, 1, .001, 1, 1, 1000, .99, 100, None, None, None, None),
    (.588, 0, 0, 8, 1, 1, .001, 1, 1, 1000, .99, 100, None, None, None, None),
    (.707, -1, -1, 8, 1, 1, .001, 1, 1, 1000, .99, 100, None, None, None, None),
    (.951, -1, -1, 8, 1, 1, .001, 1, 1, 1000, .99, 100, None, None, None, None),
    (.588, -1, -1, 8, 1, 1, .001, 1, 1, 1000, .99, 100, None, None, None, None),

    (.707, 0, 0, 8, None, 1, .001, 1, 1, 1000, .99, 100, None, None, None, None), # ucb no split
    (.951, -.4, 0, 8, None, 1, .001, 1, 1, 1000, .99, 100, None, None, None, None),
    (.588, 0, 0, 8, None, 1, .001, 1, 1, 1000, .99, 100, None, None, None, None),
    (.707, -1, -1, 8, None, 1, .001, 1, 1, 1000, .99, 100, None, None, None, None),
    (.951, -1, -1, 8, None, 1, .001, 1, 1, 1000, .99, 100, None, None, None, None),
    (.588, -1, -1, 8, None, 1, .001, 1, 1, 1000, .99, 100, None, None, None, None),

    (.707, 0, 0, 8, 1, 1, .001, 1, .125, 1000, .99, 100, None, None, None, None), # ucb split low explore
    (.951, -.4, 0, 8, 1, 1, .001, 1, .125, 1000, .99, 100, None, None, None, None),
    (.588, 0, 0, 8, 1, 1, .001, 1, .125, 1000, .99, 100, None, None, None, None),
    (.707, -1, -1, 8, 1, 1, .001, 1, .125, 1000, .99, 100, None, None, None, None),
    (.951, -1, -1, 8, 1, 1, .001, 1, .125, 1000, .99, 100, None, None, None, None),
    (.588, -1, -1, 8, 1, 1, .001, 1, .125, 1000, .99, 100, None, None, None, None),

    (.707, 0, 0, 8, None, 1, .001, 1, .125, 1000, .99, 100, None, None, None, None), # ucb no split low explore
    (.951, -.4, 0, 8, None, 1, .001, 1, .125, 1000, .99, 100, None, None, None, None),
    (.588, 0, 0, 8, None, 1, .001, 1, .125, 1000, .99, 100, None, None, None, None),
    (.707, -1, -1, 8, None, 1, .001, 1, .125, 1000, .99, 100, None, None, None, None),
    (.951, -1, -1, 8, None, 1, .001, 1, .125, 1000, .99, 100, None, None, None, None),
    (.588, -1, -1, 8, None, 1, .001, 1, .125, 1000, .99, 100, None, None, None, None),

    (.707, 0, 0, 8, 1, 1, .001, 1, 1, 1000, .99, 100, .707, 0, 0, 1), # prior .707,0,0
    (.951, -.4, 0, 8, 1, 1, .001, 1, 1, 1000, .99, 100, .707, 0, 0, 1),
    (.588, 0, 0, 8, 1, 1, .001, 1, 1, 1000, .99, 100, .707, 0, 0, 1),
    (.707, -1, -1, 8, 1, 1, .001, 1, 1, 1000, .99, 100, .707, 0, 0, 1),
    (.951, -1, -1, 8, 1, 1, .001, 1, 1, 1000, .99, 100, .707, 0, 0, 1),
    (.588, -1, -1, 8, 1, 1, .001, 1, 1, 1000, .99, 100, .707, 0, 0, 1),

    (.707, 0, 0, 8, 1, 1, .001, 1, 1, 1000, .99, 100, .951, -.4, 0, 1), # prior .951,-.4,0
    (.951, -.4, 0, 8, 1, 1, .001, 1, 1, 1000, .99, 100, .951, -.4, 0, 1),
    (.588, 0, 0, 8, 1, 1, .001, 1, 1, 1000, .99, 100, .951, -.4, 0, 1),
    (.707, -1, -1, 8, 1, 1, .001, 1, 1, 1000, .99, 100, .951, -.4, 0, 1),
    (.951, -1, -1, 8, 1, 1, .001, 1, 1, 1000, .99, 100, .951, -.4, 0, 1),
    (.588, -1, -1, 8, 1, 1, .001, 1, 1, 1000, .99, 100, .951, -.4, 0, 1),

    (.707, 0, 0, 8, 1, 1, .001, 1, 1, 1000, .99, 100, .588, 0, 0, 1), # prior .588,0,0
    (.951, -.4, 0, 8, 1, 1, .001, 1, 1, 1000, .99, 100, .588, 0, 0, 1),
    (.588, 0, 0, 8, 1, 1, .001, 1, 1, 1000, .99, 100, .588, 0, 0, 1),
    (.707, -1, -1, 8, 1, 1, .001, 1, 1, 1000, .99, 100, .588, 0, 0, 1),
    (.951, -1, -1, 8, 1, 1, .001, 1, 1, 1000, .99, 100, .588, 0, 0, 1),
    (.588, -1, -1, 8, 1, 1, .001, 1, 1, 1000, .99, 100, .588, 0, 0, 1),

    (.707, 0, 0, 8, 1, 1, .001, 1, 1, 1000, .99, 100, .707, -1, -1, 1), # prior .707 -1 -1
    (.951, -.4, 0, 8, 1, 1, .001, 1, 1, 1000, .99, 100, .707, -1, -1, 1),
    (.588, 0, 0, 8, 1, 1, .001, 1, 1, 1000, .99, 100, .707, -1, -1, 1),
    (.707, -1, -1, 8, 1, 1, .001, 1, 1, 1000, .99, 100, .707, -1, -1, 1),
    (.951, -1, -1, 8, 1, 1, .001, 1, 1, 1000, .99, 100, .707, -1, -1, 1),
    (.588, -1, -1, 8, 1, 1, .001, 1, 1, 1000, .99, 100, .707, -1, -1, 1),

    (.707, 0, 0, 8, 1, 1, .001, 1, 1, 1000, .99, 100, .951, -1, -1, 1), # prior .951 ,-1, -1
    (.951, -.4, 0, 8, 1, 1, .001, 1, 1, 1000, .99, 100, .951, -1, -1, 1),
    (.588, 0, 0, 8, 1, 1, .001, 1, 1, 1000, .99, 100, .951, -1, -1, 1),
    (.707, -1, -1, 8, 1, 1, .001, 1, 1, 1000, .99, 100, .951, -1, -1, 1),
    (.951, -1, -1, 8, 1, 1, .001, 1, 1, 1000, .99, 100, .951, -1, -1, 1),
    (.588, -1, -1, 8, 1, 1, .001, 1, 1, 1000, .99, 100, .951, -1, -1, 1),

    (.707, 0, 0, 8, 1, 1, .001, 1, 1, 1000, .99, 100, .588, -1, -1, 1), # prior .588, -1 , -1
    (.951, -.4, 0, 8, 1, 1, .001, 1, 1, 1000, .99, 100, .588, -1, -1, 1),
    (.588, 0, 0, 8, 1, 1, .001, 1, 1, 1000, .99, 100, .588, -1, -1, 1),
    (.707, -1, -1, 8, 1, 1, .001, 1, 1, 1000, .99, 100, .588, -1, -1, 1),
    (.951, -1, -1, 8, 1, 1, .001, 1, 1, 1000, .99, 100, .588, -1, -1, 1),
    (.588, -1, -1, 8, 1, 1, .001, 1, 1, 1000, .99, 100, .588, -1, -1, 1),

]

def outputmesh(params,mesh):
    for c in mesh.columns:
        for i in mesh.index:
            print ",".join([str(params),str(i),str(c),str(mesh[c][i])])

if __name__=="__main__":
    print "params,startmove,response,score"
    paramlist=[int(x) for x in sys.argv[1].split(":")]
    for paramset in paramlist:
        threshhold,zeroresponse,negoneresponse,bucketcount,splitthreshhold,splitval,minbucketsize,radial,exploration,\
        gamelength,discountfactor,iterations,priorthreshhold,priorzero,priornegone,priorwt=params[paramset]
        teacher=ts.simpleteacher(threshhold,zeroresponse,negoneresponse)

        learnerprior=None
        if priorwt is not None:
            learnerprior = ucb.getprior(ts.simpleteacher(priorthreshhold, priorzero, priornegone), bucketcount, radial, 10, priorwt)
        learner=ucb.BucketUCB(bucketcount,splitthreshhold,splitval,minbucketsize,None,radial,exploration,prior=learnerprior)
        mesh = meshutils.createmesh(teacher, learner, None, gamelength, discountfactor, iterations, poolsize=20)
        outputmesh(paramset,mesh)