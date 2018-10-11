"""
This file contains code to calculate the effects of different forgiveness factors in various situations.
It will consist of scripts and helper functions.  If you write something that you want to import somewhere else,
it's probably better to move that thing to a different file
"""

import teachingstrategies as ts

import math

scriptchoice=1

# Forgiveness factor vs. greedy opponent
if __name__=="__main__" and scriptchoice==1:
    teacher=ts.simpleteacher(.707,0,0)
    results=[]
    for ff in [.0125,.025,.05,.1,.2,.3,.4,.5,.6,.7,.8,.9,1.0]:
        totalcost=0
        for i in range(1,100000):
            response=teacher.respond(ff/i)
            cost=1-math.sqrt(1-response**2)
            totalcost=totalcost+cost
        results.append(totalcost)
    print results