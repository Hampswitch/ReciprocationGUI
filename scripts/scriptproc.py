"""
This file contains code to automatically read and process log files from the /results/scriptprocessor directory.
"""

import SAscript as sas
import reciprocation.evaluation as eva
import reciprocation.seqstrat as seqstrat

def processfile(filename):
    file=open(filename,"r")
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
            print(runresult)

if __name__=="__main__":
    processfile('../results/scriptprocessor/testresults.txt')