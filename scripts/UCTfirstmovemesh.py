
import reciprocation.scriptutil as util

import multiprocessing
import itertools

rvals=[0.0,.156,.309,.454,.588,.707,.809,.891,.951,.988,1.0]
opplist=[(.988,-.692,0.0),(.951,-.382,0.0),(.891,-.093,0.0),(.809,0.0,0.0),
         (.707,0.0,0.0),(.588,0.0,0.0),(.454,0.0,0.0),(.309,0.0,0.0),(.156,0.0,0.0),(0.0,0.0,0.0),
         (.988,-1.0,-1.0),(.951,-1.0,-1.0),(.891,-1.0,-1.0),(.809,-1.0,-1.0),
         (.707,-1.0,-1.0),(.588,-1.0,-1.0),(.454,-1.0,-1.0),(.309,-1.0,-1.0),(.156,-1.0,-1.0),(0.0,-1.0,-1.0)]

def processUCT(params):
    return util.UCT_simple_evaluate(1000,-1,.99,params[0],params[1],1.0,0,params[3],False,params[2][0],params[2][1],params[2][2])

if __name__=="__main__":
    pool=multiprocessing.Pool(processes=20)
    result=pool.map(processUCT,itertools.product([-x for x in rvals[-1:0:-1]]+rvals,[-x for x in rvals[-1:0:-1]]+rvals,opplist,[2,3,4]))
    for r in result:
        print r