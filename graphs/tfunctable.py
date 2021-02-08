
import tfuncgraph as tfdata
import reciprocation.evaluation as eval
import reciprocation.seqstrat as seq
import numpy

def printtable(oppdata):
    for trial,n in zip(oppdata,range(len(oppdata))):
        scores=[x[0] for x in trial]
        print("{:>2} {:>8.4} {:>8.4} {:>8.4} {:>8.4}".format(n+1,numpy.mean(scores),numpy.std(scores),numpy.min(scores),numpy.max(scores)))

if __name__=="__main__":
    opp1=seq.thresholdfunctionparticle.fromString(tfdata.opp1)
    opp2=seq.thresholdfunctionparticle.fromString(tfdata.opp2)
    opp3=seq.thresholdfunctionparticle.fromString(tfdata.opp3)
    opp1eval=[[[(eval.evaluate(opp1,func,1000,.99,1)[1],func.opponentloss,func.thresholdfunc.getValue(func.opponentloss)) for func in run] for run in target] for target in tfdata.ThresholdFunctions]
    opp2eval=[[[(eval.evaluate(opp2,func,1000,.99,1)[1],func.opponentloss,func.thresholdfunc.getValue(func.opponentloss)) for func in run] for run in target] for target in tfdata.ThresholdFunctions]
    opp3eval=[[[(eval.evaluate(opp3,func,1000,.99,1)[1],func.opponentloss,func.thresholdfunc.getValue(func.opponentloss)) for func in run] for run in target] for target in tfdata.ThresholdFunctions]
    printtable(opp1eval[5])