"""
This is a scratch file to calculate solutions for the guess who puzzle found at:
 https://fivethirtyeight.com/features/how-good-are-you-at-guess-who/
 currently assuming that the optimal strategy is to either guess randomly, or split as evenly as possible
"""
if False:
    memoize={}

    def p1odds(p1ct,p2ct):
        """
        This function is based on the assumption that optimal behavior either splits evenly or randomly guesses one
        :param p1ct:
        :param p2ct:
        :return:
        """
        if p1ct==1:
            return 1.0
        if p2ct==1:
            return 1.0/p1ct
        if (p1ct,p2ct) in memoize.keys():
            return memoize[(p1ct,p2ct)]
        if p1ct%2==0:
            return max(1.0/p1ct,1-p1odds(p2ct,p1ct/2))
        else:
            return max(1.0/p1ct,(.5*(p1ct-1)*(1-p1odds(p2ct,.5*(p1ct-1)))+.5*(p1ct+1)*(1-p1odds(p2ct,.5*(p1ct+1))))/p1ct)

    for i in range(16):
        print str(i)+":"+" ".join(["{:^8.4}".format(p1odds(j+1,i+1)) for j in range(16)])

    p1ocmemoize={}

    def p1oddscomplete(p1ct,p2ct):
        """
        This function is based on the assumption that optimal behavior either splits evenly or randomly guesses one
        :param p1ct:
        :param p2ct:
        :return:
        """
        if p1ct==1:
            return 1.0
        if p2ct==1:
            return 1.0/p1ct
        if (p1ct,p2ct) in p1ocmemoize.keys():
            return p1ocmemoize[(p1ct,p2ct)]
        else:
            result=max([1.0/p1ct]+[(float(i)/p1ct)*(1-p1oddscomplete(p2ct,i))+(float(p1ct-i)/p1ct)*(1-p1oddscomplete(p2ct,p1ct-i)) for i in range(1,p1ct)])
            p1ocmemoize[(p1ct,p2ct)]=result
            return result

    for i in range(4):
        print str(i)+":"+" ".join(["{:^8.4}".format(p1oddscomplete(j+1,i+1)) for j in range(4)])

if True:
    import math
    i=11
    while (2.0**i)/(10**math.floor(math.log(2.0**i,10)))>1.003:
        i=i+1
    print(i)
    print(2**i)