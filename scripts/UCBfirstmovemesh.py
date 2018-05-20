
import reciprocation.scriptutil as util

import multiprocessing
import itertools

def processUCB(params):
    return util.UCB_simple_evaluate(10000,params[2],.999,params[0],params[1],8,1,1,params[3][0],params[3][1],params[3][2])

if __name__=="__main__":
    pool=multiprocessing.Pool(processes=20)
    result=pool.map(processUCB,itertools.product([-x for x in util.rvals[-1:0:-1]]+util.rvals,[-x for x in util.rvals[-1:0:-1]]+util.rvals,range(10,500),util.opplist))
    for r in result:
        print r