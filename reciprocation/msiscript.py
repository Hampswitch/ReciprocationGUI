
import learningstrategies as learners
import genetic_alg as ga
import teachingstrategies as teachers

rvals=[0.0,.156,.309,.454,.588,.707,.809,.891,.951,.988,1.0]
opplist=[(.988,-.691,0.0),(.951,-.381,0.0),(.891,-.091,0.0),(.809,0.0,0.0),
         (.707,0.0,0.0),(.588,0.0,0.0),(.454,0.0,0.0),(.309,0.0,0.0),(.156,0.0,0.0),(0.0,0.0,0.0),
         (.988,-1.0,-1.0),(.951,-1.0,-1.0),(.891,-1.0,-1.0),(.809,-1.0,-1.0),
         (.707,-1.0,-1.0),(.588,-1.0,-1.0),(.454,-1.0,-1.0),(.309,-1.0,-1.0),(.156,-1.0,-1.0),(0.0,-1.0,-1.0)]


if __name__=="__main__":
    for (threshhold,zero,negone) in opplist:
        for startmove in [-x for x in rvals[-1:0:-1]]+rvals:
            for initresponse in [-x for x in rvals[-1:0:-1]]+rvals:
                learner=learners.player(learner=learners.UCTlearner(c=1.0),startmove=startmove)
                teacher=teachers.simpleteacher(threshhold,zero,negone,override=[initresponse])
                result=ga.evaluate(learner,teacher,1000,.99,1000)
                print ", ".join([str(x) for x in [threshhold,zero,negone,startmove,initresponse,result[2],result[0]]])
