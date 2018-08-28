
import math

x=0.0
y=0.0
n=0
curplayer="y"
df=.999
curdf=1.0
xdf=0.0
ydf=0.0
ndf=0.0

for i in range(1000000):
    if i==0:
        curplayer="y"
    elif math.floor(math.log(i,10))%2==0:
        curplayer="x"
    elif math.floor(math.log(i,10))%2==1:
        curplayer="y"
    else:
        raise ValueError("error")
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