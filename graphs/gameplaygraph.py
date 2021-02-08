
"""
Graph that shows how much each player gives to the opponent each round.
  and what each players threshold value was in that round
  Other things that might be good to plot:
    point at which thresholds become compatible
    players total score each round
    Efficiency each round (distance of player scores from origin)



"""

import reciprocation.seqstrat as seq
import matplotlib.pyplot as plt
import math
import tfuncgraph as tfg

def makegamegraph(p1,p2,rounds=1000):
    players=[p1,p2]
    round=0
    move=None
    thresholds=[[],[]]
    moves=[[],[]]
    payoffs=[[],[]]
    compatibility=[]
    efficiency=[0.0]
    opploss=[[],[]]
    while round<rounds:
        response=players[round%2].respond(move)
        moves[round%2].append(response)
        thresholds[0].append(players[0].getThreshold())
        thresholds[1].append(players[1].getThreshold())
        opploss[0].append(players[0].opponentloss)
        opploss[1].append(players[1].opponentloss)
        if thresholds[0][-1]**2+thresholds[1][-1]**2<=1:
            compatibility.append(1)
        else:
            compatibility.append(-1)
        if move is None:
            payoffs[0].append(math.sqrt(1-response**2))
            payoffs[1].append(response)
        else:
            payoffs[round%2].append((response+math.sqrt(1-move**2))/2)
            payoffs[1-round%2].append((move+math.sqrt(1-response**2))/2)
            efficiency.append(math.sqrt(payoffs[0][-1]**2+payoffs[1][-1]**2)/2)
        round=round+1
        move=response
    return moves,thresholds,payoffs,compatibility,efficiency,opploss

if __name__=="__main__":
    p1=seq.thresholdfunctionparticle.fromString("SeqAutocratic 0.1 0 <(1.0,0.0),(0.5,15.0),(0.0,30.0)>")
    p2=tfg.ThresholdFunctions[5][0][0]
    (moves,thresholds,payoffs,compatibility,efficiency,opploss)=makegamegraph(p1,p2,1000)
    p1.plotfunction("Player 1 Threshold Function")
    p2.plotfunction("Player 2 Threshold Function")
    p1round=p1.thresholdfunc.getRoundThresholds()
    plt.plot(range(len(p1round)),p1round)
    plt.show()
    p2round=p2.thresholdfunc.getRoundThresholds()
    plt.plot(range(len(p2round)),p2round)
    plt.show()
    plt.plot(range(200),thresholds[0][:200],"r-")
    plt.plot(range(0,200,2),moves[0][:100],"r:")
    plt.plot(range(200), thresholds[1][:200], "b-")
    plt.plot(range(1,200,2),moves[1][:100],"b:")
    plt.plot([compatibility.index(1)]*2,[-1,1],"k-")
    plt.xlabel("round")
    plt.ylabel("payoff to opponent")
    plt.legend(["p1 threshold","p1 move","p2 threshold","p2 move","threshold compatibility"])
    plt.title("Full Gameplay Graph")
    plt.show()
    plt.plot(range(200),opploss[0][:200])
    plt.plot(range(200),opploss[1][:200])
    plt.legend(["Player 1 opponent loss","Player 2 opponent loss"])
    plt.show()