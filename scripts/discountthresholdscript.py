"""
This is a script to calculate the discounted payoff of various thresholds against UCB split for a set of discount values
"""

import reciprocation.evaluation as eval
import reciprocation.linearstrat as linstrat
import reciprocation.UCB as ucb

from matplotlib import pyplot as plt


import timeit
import math

length=1000
repetition=100

thresholds=[.95,.85,.707,.5]

discounts=[.001,.0025,.005,.01,.025,.05,.1,.2,.4]

result={}
for t in thresholds:
    result[t]=[]

start=timeit.default_timer()
for discount in discounts:
    strat1=ucb.TrackBucketUCB(4,1,4,.001,0,0)
    print discount
    for t in thresholds:
        strat2=linstrat.slopestrat(t)
        evalresult = eval.evaluate(strat1, strat2, length, 1.0-discount, repetition)
        result[t].append(evalresult[2])

stop=timeit.default_timer()
print("Time: ",stop-start)

plt.figure(figsize=(8, 6))
plt.hold=True


xdata=discounts
for t in thresholds:
    plt.plot(xdata, result[t])
plt.xscale('log')
plt.xlabel("Discount Factor")
plt.ylabel("Total Discounted Payoff")

plt.title("Effect of Threshold Value on Discounted Payoff")
plt.legend(["Threshold {:.3f} Ratio 1:{:.3f}".format(t,math.sqrt(1-t**2)/t) for t in thresholds])
plt.show()