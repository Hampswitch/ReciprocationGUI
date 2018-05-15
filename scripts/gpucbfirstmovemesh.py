
import reciprocation.scriptutil as util

import multiprocessing
import itertools

def processGPUCB(params):
    return util.GPUCB_simple_evaluate(1000,-1,.99,params[0],params[1],.707,0,0)

if __name__=="__main__":
    pool=multiprocessing.Pool(processes=20)
    pool.map(processGPUCB,itertools.product([-x for x in util.rvals[-1:0:-1]]+util.rvals,[-x for x in util.rvals[-1:0:-1]]+util.rvals))