
import reciprocation.seqstrat as negot

import matplotlib.pyplot as plt
colorlist=["r","g","b","k","m","c"]


def make_graph_seq(filelist):
    seq=None
    for filename in filelist:
        fileseq=[]
        with open(filename,"r") as file:
            for s in file.readlines():
                fileseq.append(negot.thresholdfunctionparticle.fromString(s))
        if seq is None:
            seq=[[x] for x in fileseq]
        else:
            seq=[[x]+s for x,s in zip(fileseq,seq)]
    for round in seq:
        plt.figure(figsize=(6, 4.5))
        for strat,c in zip(round,colorlist):
            plt.plot(strat.thresholdfunc.lossvalues, strat.thresholdfunc.thresholdvalues, c)
        plt.ylabel("Threshold Value")
        plt.xlabel("Opponent Loss")
        plt.xlim([0, 60])
        plt.show()

if __name__=="__main__":
    make_graph_seq(["../results/selfplay/selfplay3.txt"])
