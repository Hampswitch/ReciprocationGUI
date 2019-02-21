import math

def expectedval(n,discount):
    badguess=sum([discount**(j-1)*math.cos(math.pi*j/(2*n+2)) for i in range(1,n+1) for j in range(1,i)])/n
    goodguess=sum([math.cos(math.pi*i/(2*n+2))*discount**(i-1)/(1-discount) for i in range(1,n+1)])/n
    opponent=2*(1-discount**n)/(n*(1-discount)**2)-1/(1-discount)
    print "{},{},{}".format(badguess,goodguess,opponent)
    return badguess+goodguess+opponent