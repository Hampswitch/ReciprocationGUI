
import math

import reciprocation.linearstrat as ls

# threshold is value received by player 1
threshold=.707
lastmove=0
forgivenessfactor=.1

p1strat=ls.slopestrat(threshold)
p2strat=ls.slopestrat(math.sqrt(1-threshold**2))

# p1 is the only agent with a forgiveness factor - p2's forgiveness factor is 0
# p1 uses a constant forgiveness factor
# play starts with p1
while lastmove<threshold:
    p1response=p1strat.respond(lastmove+forgivenessfactor)
    lastmove=p2strat.respond(p1response)
    print 1
print 2