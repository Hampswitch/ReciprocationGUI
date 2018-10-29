

from matplotlib import pyplot as plt
import re
import ast

def dispfunctions(stratlist):
    plt.figure(figsize=(4, 3))
    for strat in stratlist:
        plt.plot([x[0] for x in strat],[x[1] for x in strat])
    plt.xlim(-1,1)
    plt.ylim(-1,1)
    plt.show()

def parseresults(filename):
    result={}
    pat='== Expand: (\d+) == Resolution: (\d+) == Index: (\d+) =====================================================================================================\n'
    f=open(filename,'r')
    l=f.readlines()
    for i in range(len(l)/2):
        key=tuple([int(v) for v in re.match(pat,l[2*i]).groups()])
        value=[]
        for s in l[2*i+1].split("Linear Strat: ")[1:]:
            value.append(ast.literal_eval(s[:-2]))
        result[key]=value
    return result

if __name__=="__main__":
    results=parseresults("../results/SAbaseresults.txt")
    print results
    print results[(2,5,2)]
    dispfunctions(results[(2,9,0)])