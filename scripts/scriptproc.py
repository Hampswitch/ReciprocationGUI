from reciprocation import seqstrat as seqstrat, evaluation as eva
from scripts import SAscript as sas


def processfile(filename):
    file=open(filename,"r")
    results=[]
    paramcode=None
    for line in file.readlines():
        if line[0]=="(":
            paramcode=int(line[1:].split(",")[0])
            oppcode=sas.combinedparams[paramcode][0]
            opp=sas.getopponent(oppcode)
            discount, iterations, skiprounds = sas.getevalparams(sas.combinedparams[paramcode][1])
        if line[0]=="[" and line[1]!="[":
            strats=line.split("SeqAutocratic")[1:]
            strats=[seqstrat.thresholdfunctionparticle.fromString(s) for s in strats]
            evals=[eva.evaluate(opp,s,iterations,discount,10,skipfirst=skiprounds)[2] for s in strats]
            runresult=sorted([(e,s) for e,s in zip(evals,strats)])[-1][1]
            results.append((runresult,strats))
    if paramcode is not None:
        return paramcode,results,opp
    else:
        return -1,[],None