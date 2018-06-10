
import reciprocation.teachingstrategies as ts
import reciprocation.teachinglearning as tl
import reciprocation.meshutils as meshutils
import reciprocation.UCB as ucb

import sys

"""
Parameter ideas for UCBTL script
  Initial strategy (variants on simpleteacher)
  discountfactor/iterations
  repetitions when creating mesh
  multiplicative factor for mesh
  opponent/learner
  TLUCB parameters bucketcount/exploration
"""

params=[(.707,0,0,1000,.99,10,100,8,1.0,8,1.0),
        (.588,0,0,1000,.99,10,100,8,1.0,8,1.0),
        (.951,-.4,0,1000,.99,10,100,8,1.0,8,1.0),
        (.707, -1, -1, 1000, .99, 10, 100, 8, 1.0, 8, 1.0),
        (.588, -1, -1, 1000, .99, 10, 100, 8, 1.0, 8, 1.0),
        (.951, -1, -1, 1000, .99, 10, 100, 8, 1.0, 8, 1.0),
        (.707, 0, 0, 1000, .99, 20, 100, 8, 1.0, 8, 1.0),
        (.707, 0, 0, 1000, .99, 100, 100, 8, 1.0, 8, 1.0),
        (.707, 0, 0, 1000, .99, 10, 100, 8, .125, 8, 1.0),
        (.707, 0, 0, 1000, .99, 10, 100, 8, 1.0, 8, 1.0),
        (.707, 0, 0, 1000, .99, 10, 100, 8, 1.0, 8, 1.0),
        (.707, 0, 0, 1000, .99, 10, 100, 8, 1.0, 8, 1.0),
        (.707, 0, 0, 1000, .99, 10, 100, 8, 1.0, 8, 1.0),
        (.707, 0, 0, 1000, .99, 10, 100, 8, 1.0, 8, 1.0),
        (.707, 0, 0, 1000, .99, 10, 100, 8, 1.0, 8, 1.0),
        (.707, 0, 0, 1000, .99, 10, 100, 8, 1.0, 8, 1.0),
        (.707, 0, 0, 1000, .99, 10, 100, 8, 1.0, 8, 1.0)
        ]

def outputmesh(iteration,params,mesh):
    for c in mesh.columns:
        for i in mesh.index:
            print ",".join([str(iteration),str(params),str(i),str(c),str(mesh[c][i])])

if __name__=="__main__":
    p=int(sys.argv[1])
    threshhold,zero,negone,gamelength,discountfactor,iterations,meshmult,ownbucket,ownexp,oppbucket,oppexp=params[p]
    teacher = ts.simpleteacher(threshhold, zero, negone)
    learner = ucb.BucketUCB(bucketcount=oppbucket, exploration=oppexp)
    mesh = meshutils.createmesh(teacher, learner, None, gamelength, discountfactor, iterations,poolsize=20)
    print "iteration,params,startmove,response,score"
    outputmesh(0,p,mesh)
    for i in range(1,10):
        teacher = ucb.BucketUCB(bucketcount=ownbucket,exploration=ownexp,teacher=tl.meshTLteacher(mesh=mesh*meshmult))
        mesh=meshutils.createmesh(teacher, learner, None, gamelength, discountfactor, iterations,poolsize=20)
        outputmesh(i,p, mesh)