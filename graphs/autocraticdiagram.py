"""
This file contains a script to make a diagram showing how autocratic functions work
"""

from matplotlib import pyplot as plt

from mkrespfuncgraph import autocratic

import math

resolution=101

plt.figure(figsize=(6, 6))
plt.hold=True
plt.xlim(-2, 2)
plt.ylim(-2, 2)
plt.xlabel("Amount given to autocratic player")
plt.ylabel("Amount given to other player")

# Axises
plt.plot([0,0],[-2,2],'k')
plt.plot([-2,2],[0,0],'k')
# Boundary of the choice set
plt.plot([math.sin(2*math.pi*x/(resolution-1)) for x in range(resolution)],[math.cos(2*math.pi*x/(resolution-1)) for x in range(resolution)],'k')
# Threshold move
plt.plot([0,.8],[0,.6],'k')
plt.plot([.8,.8],[0,.6],'k')
plt.plot([.8,1.6],[.6,1.2],'k:')
plt.plot([-.6,.6],[.8,-.8],'k')

plt.plot([-.8,0],[.6,0],'b')
plt.plot([-.8,0],[.6,0],'b:')
#plt.plot([0,.8],[0,-.6],'b:')
plt.text(-.85,.65,'1')
#plt.text(.85,-.65,"1'")

# sample move
m=-.1
r=autocratic(.8,m)
plt.plot([0,m],[0,math.sqrt(1-m*m)],'c')
#plt.plot([0,math.sqrt(1-r*r)],[0,r],'c:')
plt.plot([m,m+math.sqrt(1-r*r)],[math.sqrt(1-m*m),r+math.sqrt(1-m*m)],'c:')

plt.text(m,math.sqrt(1-m*m)+.05,'2')
#plt.text(math.sqrt(1-r*r)+.05,r,"2'")

m=.6
r=autocratic(.8,m)
plt.plot([0,m],[0,math.sqrt(1-m*m)],'g')
#plt.plot([0,math.sqrt(1-r*r)],[0,r],'g:')
plt.plot([m,m+math.sqrt(1-r*r)],[math.sqrt(1-m*m),r+math.sqrt(1-m*m)],'g:')

plt.text(m,math.sqrt(1-m*m)+.05,'3')
#plt.text(math.sqrt(1-r*r)+.05,r,"3'")

m=.98
r=.6
plt.plot([0,m],[0,math.sqrt(1-m*m)],'r')
#plt.plot([0,math.sqrt(1-r*r)],[0,r],'r:')
plt.plot([m,m+math.sqrt(1-r*r)],[math.sqrt(1-m*m),r+math.sqrt(1-m*m)],'r:')

plt.text(m+.01,math.sqrt(1-m*m)-.05,'4')
#plt.text(math.sqrt(1-r*r)+.05,r,"4'")

plt.text(.85,.55,'T')
plt.text(.75,-.09,'0.8')

plt.title("Autocratic Strategy Diagram")
plt.show()