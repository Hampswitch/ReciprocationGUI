
"""
Graph that shows how much each player gives to the opponent each round.
  and what each players threshold value was in that round

"""

import reciprocation.seqstrat as seq
import matplotlib.pyplot as plt

def makegamegraph(p1,p2,rounds=1000):
    players=[p1,p2]
    round=0
    move=None
    thresholds=[[],[]]
    moves=[[],[]]
    while round<rounds:
        move=players[round%2].respond(move)
        moves[round%2].append(move)
        thresholds[0].append(players[0].getThreshold())
        thresholds[1].append(players[1].getThreshold())
        round=round+1
    return moves,thresholds

if __name__=="__main__":
    p1=seq.thresholdfunctionparticle.fromString("SeqAutocratic 0.1 0 <(1.0,0.0),(0.5,15.0),(0.0,30.0)>")
    p2=seq.thresholdfunctionparticle.fromString("SeqAutocratic 0.1 0 <(1.0,0.0),(1.0,0.04852),(0.9155,0.7278),(0.8514,0.8774),(0.7942,1.825),(0.7421,2.234),(0.5505,2.844),(0.2789,11.34),(0.1878,26.26),(0.1826,28.3)> (1001,1.413,0.819), ")
    p2 = seq.thresholdfunctionparticle.fromString("SeqAutocratic 0.1 0 <(1.0,0.0),(1.0,0.01208),(1.0,0.03183),(0.9432,1.05),(0.9137,6.688),(0.7246,7.073),(0.47,10.21),(0.3851,17.8),(0.005361,29.76),(0.0,79.09)>")
    (moves,thresholds)=makegamegraph(p1,p2,1000)
    plt.plot(range(200),thresholds[0][:200],"r-")
    plt.plot(range(200),thresholds[1][:200],"b-")
    plt.plot(range(0,200,2),moves[0][:100],"b:")
    plt.plot(range(1,200,2),moves[1][:100],"r:")
    plt.legend(["p1 threshold","p2 threshold","p1 move","p2 move"])
    plt.show()