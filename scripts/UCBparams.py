
import reciprocation.scriptutil as util

import multiprocessing
import itertools

def processUCB(params):
    util.UCB_simple_evaluate(10000,params[4],.999,None,None,params[0],params[1],params[2],params[3][0],params[3][1],params[3][2])

if __name__=="__main__":
    pool=multiprocessing.Pool(processes=20)
    result=pool.map(processUCB,itertools.product([4,8,12,16],[0,1],[.0625,.25,1.0,4.0],util.opplist,range(10)))
    for r in result:
        print r