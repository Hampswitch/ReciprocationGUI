"""
This file contains code to automatically read and process log files from the /results/scriptprocessor directory.
"""

import SAscript as sas
import reciprocation.evaluation as eva
import reciprocation.seqstrat as seqstrat
import graphs.tfuncgraph as tfg

def processfile(filename):
    file=open(filename,"r")
    results=[]
    for line in file.readlines():
        if line[0]=="(":
            paramcode=int(line[1:].split(",")[0])
            oppcode=sas.combinedparams[paramcode][0]
            opp=sas.getopponent(oppcode)
            discount, iterations, skiprounds = sas.getevalparams(sas.combinedparams[paramcode][1])
        if line[0]=="[":
            strats=line.split("SeqAutocratic")[1:]
            strats=[seqstrat.thresholdfunctionparticle.fromString(s) for s in strats]
            evals=[eva.evaluate(opp,s,iterations,discount,10,skipfirst=skiprounds)[2] for s in strats]
            runresult=sorted([(e,s) for e,s in zip(evals,strats)])[-1][1]
            results.append((runresult,strats))
    return results

if __name__=="__main__":
    results=processfile('../results/scriptprocessor/testresults2.txt')
    tfg.plotroundfunc(results[0][0])
    tfg.plotroundfunc(results[1][0])
    for s in results[0][1]+results[1][1]:
        tfg.plotthreshold(s)
    opp=seqstrat.thresholdfunctionparticle.randomAutocratic()
    print eva.evaluate(opp,results[1][0],1000,.99,100)