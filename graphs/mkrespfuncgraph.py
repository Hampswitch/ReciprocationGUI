"""
This file contains code to produce a graph of response functions for various threshold values
"""

from matplotlib import pyplot as plt

import math

thresholds=[.95,math.sqrt(2)/2,.5]
resolution=200

def autocratic(threshold,move):
    if move>threshold:
        return math.sqrt(1-threshold**2)
    x=threshold*math.sqrt(1-move**2)-move*math.sqrt(1-threshold**2)
    return -threshold*x+math.sqrt((threshold**2-1)*(x**2-1))

if __name__=="__main__":
    plt.figure(figsize=(8, 6))
    plt.hold=True

    for threshold in thresholds:
        xdata=[-1+i*2.0/(resolution-1) for i in range(resolution)]
        ydata=[autocratic(threshold,x)+math.sqrt(1-x*x) for x in xdata]
        plt.plot(xdata, ydata)
        plt.xlim(-1, 1)
        plt.ylim(-1, 2)
        plt.xlabel("Amount given to autocratic player")
        plt.ylabel("Total payoff to other player")

    plt.title("Achievable payoffs against autocratic players")
    plt.legend(["Threshold {:.3f} Ratio 1:{:.3f}".format(t,math.sqrt(1-t**2)/t) for t in thresholds])
    plt.show()