
import matplotlib.pyplot as plt

import reciprocation.evaluation as ev

import reciprocation.UCB as ucb
import reciprocation.linearstrat as linear

player1=linear.slopestrat(.95)
player2=ucb.TrackBucketUCB(widthexp=1.0)

results=ev.getOutcome(player1,player2,repetitions=100)

plt.figure(figsize=(8, 6))
plt.hold = True
xvals=range(499)
yvals = results[7]
#yvals=[sum(results[1][10*i:10*i+10])/10.0 for i in range(100)]
errbars = results[2]
errfrom=[x[0] for x in errbars]
errto=[x[1] for x in errbars]
print yvals
print errbars
plt.plot(xvals, yvals)
#plt.fill_between(xvals, errfrom, errto, alpha=.25)
plt.show()