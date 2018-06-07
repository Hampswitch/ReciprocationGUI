
import reciprocation.teachingstrategies as ts
import reciprocation.teachinglearning as tl
import reciprocation.meshutils as meshutils
import reciprocation.UCB as ucb

def outputmesh(iteration,mesh):
    for c in mesh.columns:
        for i in mesh.index:
            print ",".join([str(iteration),str(i),str(c),str(mesh[c][i])])

if __name__=="__main__":
    teacher = ts.simpleteacher(.707, 0, 0)
    learner = ucb.BucketUCB(bucketcount=8, exploration=1.0)
    mesh = meshutils.createmesh(teacher, learner, None, 1000, .99, 10,poolsize=20)
    print "iteration,startmove,response,score"
    outputmesh(0,mesh)
    for i in range(1,10):
        teacher = ucb.BucketUCB(bucketcount=8,exploration=1.0,teacher=tl.meshTLteacher(mesh=mesh*100))
        mesh=meshutils.createmesh(teacher, learner, None, 1000, .99, 10,poolsize=20)
        outputmesh(i, mesh)