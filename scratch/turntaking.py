
import math

x=1.0
y=0.0
n=1
delta=.1
curplayer="y"
df=.999
curdf=1.0
xdf=1.0
ydf=0.0
ndf=1.0

for i in range(1000000):
    if math.sqrt((1-x/n)**2+(y/n)**2)<delta:
        curplayer="y"
        print "switch: "+str(n)
    if math.sqrt((1 - y / n) ** 2 + (x / n) ** 2) < delta:
        curplayer = "x"
        print "switch: "+str(n)
    if curplayer=="x":
        x=x+1
        n=n+1
        curdf=curdf*df
        xdf=xdf+curdf
        ndf=ndf+curdf
    else:
        y=y+1
        n=n+1
        curdf=curdf*df
        ydf=ydf+curdf
        ndf=ndf+curdf
print x
print y
print n
print curplayer
print xdf/ndf
print ydf/ndf
print ndf