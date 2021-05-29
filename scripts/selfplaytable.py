
import reciprocation.evaluation as eva
import reciprocation.seqstrat as negot

iterations=1000
discount=.99
repetitions=1

def mktable(filename):
    with open(filename,"r") as file:
        fullsequence=[negot.thresholdfunctionparticle.fromString(s) for s in file.readlines()]
    for s1 in fullsequence:
        outstr = ""
        for s2 in fullsequence:
            result = eva.evaluate(s2, s1, iterations, discount, repetitions)
            if s1 == s2:
                outstr = outstr + " ({:.2f})".format(result[1])
            else:
                outstr = outstr + "  {:.2f} ".format(result[1])
        print(outstr)

if __name__=="__main__":
    mktable("../results/selfplay/selfplay3.txt")
