"""
This is another mesh-iteration script - based on more grid values
"""

import reciprocation.teachingstrategies as ts
import reciprocation.teachinglearning as tl
import reciprocation.meshutils as meshutils
import reciprocation.UCB as ucb

import sys

# 0-3
params=[(.7, 0, 0, 1000, .99, 100, 9, 100, 8, .25, None, 8, .25),
        (.7, 0, 0, 1000, .99, 100, 9, 100, 4, .25, None, 8, .25),
        (.7, 0, 0, 1000, .99, 100, 9, 100, 16, .25, None, 8, .25),
        (.7, 0, 0, 1000, .99, 100, 9, 100, 32, .25, None, 8, .25),
        # 4-7
        (.7, 0, 0, 1000, .99, 100, 9, 100, 8, .25, None, 8, .25),
        (.7, 0, 0, 1000, .99, 100, 5, 100, 8, .25, None, 8, .25),
        (.7, 0, 0, 1000, .99, 100, 17, 100, 8, .25, None, 8, .25),
        (.7, 0, 0, 1000, .99, 100, 33, 100, 8, .25, None, 8, .25),
        # 8-11
        (.7, 0, 0, 1000, .99, 100, 9, 100, 8, .25, 0, 8, .25),
        (.7, 0, 0, 1000, .99, 100, 9, 100, 4, .25, 0, 8, .25),
        (.7, 0, 0, 1000, .99, 100, 9, 100, 16, .25, 0, 8, .25),
        (.7, 0, 0, 1000, .99, 100, 9, 100, 32, .25, 0, 8, .25),
        # 12-15
        (.7, 0, 0, 1000, .99, 100, 9, 100, 8, .25, 0, 8, .25),
        (.7, 0, 0, 1000, .99, 100, 5, 100, 8, .25, 0, 8, .25),
        (.7, 0, 0, 1000, .99, 100, 17, 100, 8, .25, 0, 8, .25),
        (.7, 0, 0, 1000, .99, 100, 33, 100, 8, .25, 0, 8, .25),
        # 16-19
        (.7, 0, 0, 1000, .99, 100, 33, 100, 8, .25, 0, 8, .25),
        (.7, 0, 0, 1000, .99, 100, 33, 100, 4, .25, 0, 8, .25),
        (.7, 0, 0, 1000, .99, 100, 33, 100, 16, .25, 0, 8, .25),
        (.7, 0, 0, 1000, .99, 100, 33, 100, 32, .25, 0, 8, .25),
        # 20-23
        (.7, 0, 0, 1000, .99, 100, 33, 100, 8, .25, None, 8, .25),
        (.7, 0, 0, 1000, .99, 100, 33, 100, 4, .25, None, 8, .25),
        (.7, 0, 0, 1000, .99, 100, 33, 100, 16, .25, None, 8, .25),
        (.7, 0, 0, 1000, .99, 100, 33, 100, 32, .25, None, 8, .25),
        # 24-27
        (.7, 0, 0, 10000, .999, 100, 33, 100, 8, .25, 0, 8, .25),
        (.7, 0, 0, 1000, .99, 100, 33, 100, 4, .25, 0, 8, .125),
        (.7, 0, 0, 1000, .99, 100, 33, 100, 16, .25, 0, 8, .0625),
        (.7, 0, 0, 1000, .99, 100, 33, 100, 32, .25, 0, 8, .03125)]

def outputmesh(iteration,params,mesh):
    for c in mesh.columns:
        for i in mesh.index:
            print ",".join([str(iteration),str(params),str(i),str(c),str(mesh[c][i])])

if __name__=="__main__":
    p=int(sys.argv[1])
    threshhold,zero,negone,gamelength,discountfactor,iterations,gridval,meshmult,ownbuckets,ownexp,ownprior,oppbuckets,oppexp=params[p]
    teacher = ts.simpleteacher(threshhold, zero, negone)
    learner = ucb.BucketUCB(bucketcount=oppbuckets, exploration=oppexp,splitthreshhold=1,splitval=1,minbucketsize=.001)
    mesh = meshutils.createmesh(teacher, learner, None, gamelength, discountfactor, iterations,poolsize=20)
    print "iteration,params,startmove,response,score"
    outputmesh(0,p,mesh)
    for i in range(1,10):
        teacher = ucb.BucketUCB(bucketcount=ownbuckets,exploration=ownexp,teacher=tl.meshTLteacher(mesh=mesh*meshmult))
        mesh=meshutils.createmesh(teacher, learner, meshutils.creategridvals(gridval), gamelength, discountfactor, iterations,poolsize=20)
        outputmesh(i,p, mesh)