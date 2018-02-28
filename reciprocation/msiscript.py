
import math
import learningstrategies as learners
import genetic_alg as ga
import teachingstrategies as teachers

rvals=[0.0,.156,.309,.454,.588,.707,.809,.891,.951,.988,1.0]

if __name__=="__main__":
    for threshhold in [x for x in rvals if x<1]:
        for zero in [-x for x in rvals if 1 - x < 2 * math.sqrt(1 - threshhold * threshhold)]:
            for negone in [-x for x in rvals]:
                for startmove in [-x for x in rvals[-1:0:-1]]+rvals:
                    for initresponse in [-x for x in rvals[-1:0:-1]]+rvals:
                        learner=learners.player(learner=learners.UCTlearner(c=1.0),startmove=startmove)
                        teacher=teachers.simpleteacher(threshhold,zero,negone,override=[initresponse])
                        result=ga.evaluate(learner,teacher,1000,.99,1000)
                        f=open("firstmovedata.csv","a")
                        f.write(", ".join([str(x) for x in [threshhold,zero,negone,startmove,initresponse,result[2]]])+"\n")
                        f.close()