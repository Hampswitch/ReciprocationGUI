
import tfuncgraph as tfdata
import reciprocation.evaluation as eval
import reciprocation.seqstrat as seq
import numpy
from statsmodels.stats import api as smsa
import matplotlib.pyplot as plt

def printtable(oppdata):
    for trial,n in zip(oppdata,range(len(oppdata))):
        scores=[x[0] for x in trial]
        print("{:>2} {:>8.4} {:>8.4} {:>8.4} {:>8.4}".format(n+1,numpy.mean(scores),numpy.std(scores),numpy.min(scores),numpy.max(scores)))

if False:
    opp1=seq.thresholdfunctionparticle.fromString(tfdata.opp1)
    opp2=seq.thresholdfunctionparticle.fromString(tfdata.opp2)
    opp3=seq.thresholdfunctionparticle.fromString(tfdata.opp3)
    opp1eval=[[[(eval.evaluate(opp1,func,1000,.99,1)[1],func.opponentloss,func.thresholdfunc.getValue(func.opponentloss)) for func in run] for run in target] for target in tfdata.ThresholdFunctions]
    opp2eval=[[[(eval.evaluate(opp2,func,1000,.99,1)[1],func.opponentloss,func.thresholdfunc.getValue(func.opponentloss)) for func in run] for run in target] for target in tfdata.ThresholdFunctions]
    opp3eval=[[[(eval.evaluate(opp3,func,1000,.99,1)[1],func.opponentloss,func.thresholdfunc.getValue(func.opponentloss)) for func in run] for run in target] for target in tfdata.ThresholdFunctions]
    printtable(opp1eval[5])

# Make Discount table
# 74/75/76/77/78
if True:
    dfs = [.95,.98,.99,.995,.998]
    opp1 = seq.thresholdfunctionparticle.fromString(tfdata.opp1)
    runfuncs=[[sorted([(eval.evaluate(opp1,tf,1000,df)[1],tf) for tf in run])[-1] for run in runs] for df,runs in [(.95,tfdata.ThresholdFunctions[10]),(.98,tfdata.ThresholdFunctions[11]),(.99,tfdata.ThresholdFunctions[9]),(.995,tfdata.ThresholdFunctions[12]),(.998,tfdata.ThresholdFunctions[13])]]

    table=[[[eval.evaluate(opp1,strat[1],1000,df)[1] for strat in run] for df in dfs] for run in runfuncs]
    for row in table:
        s=""
        for target in row:
            s=s+" {:},{:} ".format(numpy.mean(target),smsa.DescrStatsW(target).tconfint_mean(alpha=.05)[0]-numpy.mean(target))
        print(s)

    labels={"g":".05","m":".02","b":".01","c":".005","r":".002"}
    plt.figure(figsize=(6, 4.5))
    for run,c in zip(runfuncs,["g","m","b","c","r"]):
        for strat in run:
            if c in ["r","b","g"]:
                rts=strat[1].thresholdfunc.getRoundThresholds()
                if c in labels:
                    plt.plot(range(0,2*len(rts),2),rts,c,label=labels[c])
                    del labels[c]
                else:
                    plt.plot(range(0,2*len(rts),2), rts, c)
    #plt.yscale("log")
    plt.ylim([0, 1])
    plt.xlim([0, 100])
    plt.xlabel("Round")
    plt.ylabel("Threshold Value")
    plt.legend()
    plt.title("Compromise Rate by Discount Factor")
    plt.show()


print()

# Make Opponent Table
# 71/72/73
if True:
    opp1 = seq.thresholdfunctionparticle.fromString(tfdata.opp1)
    opp2 = seq.thresholdfunctionparticle.fromString(tfdata.opp2)
    opp3 = seq.thresholdfunctionparticle.fromString(tfdata.opp3)

    runfuncs=[[sorted([(eval.evaluate(opp,tf,1000,.99)[1],tf,tf.thresholdfunc.getValue(tf.opponentloss),) for tf in run])[-1] for run in runs] for opp,runs in [(opp1,tfdata.ThresholdFunctions[6]),(opp2,tfdata.ThresholdFunctions[7]),(opp3,tfdata.ThresholdFunctions[8])]]

    table=[[[eval.evaluate(opp,strat[1],1000,.99)[1] for strat in run] for opp in [opp1,opp2,opp3]] for run in runfuncs]

    for row in table:
        s=""
        for target in row:
            s=s+" {:},{:} ".format(numpy.mean(target),smsa.DescrStatsW(target).tconfint_mean(alpha=.05)[0]-numpy.mean(target))
        print(s)

    labels={"r":"Slow Compromiser (30)","b":"Medium Compromiser (20)","g":"Fast Compromiser (10)"}
    plt.figure(figsize=(6, 4.5))
    for run, c in zip(runfuncs, ["r", "b", "g"]):
        for strat in run:
            if c in ["r","g","b"]:
                rts = strat[1].thresholdfunc.getRoundThresholds(strat[2])
                print(len(rts))
                print(rts)
                if c in labels:
                    plt.plot(range(0,2*len(rts),2), rts, c,label=labels[c])
                    del labels[c]
                else:
                    plt.plot(range(0,2*len(rts),2), rts, c)

    #plt.yscale("log")
    plt.ylim([0, 1])
    plt.xlim([0, 60])
    plt.xlabel("Round")
    plt.ylabel("Threshold Value")
    plt.legend()
    plt.title("Compromise Rate by Opponent")
    plt.show()