import math

from matplotlib import pyplot

def showpoly(polygon):
    x,y=polygon.exterior.xy
    fig = pyplot.figure(1, figsize=(5, 5), dpi=90)
    ax = fig.add_subplot(111)
    ax.plot(x, y, color='#6699cc', alpha=0.7,
            linewidth=3, solid_capstyle='round', zorder=2)
    ax.set_title('Polygon')


def autocratic(threshold,move):
    if move>threshold:
        return math.sqrt(1-threshold**2)
    x=threshold*math.sqrt(1-move**2)-move*math.sqrt(1-threshold**2)
    return -threshold*x+math.sqrt((threshold**2-1)*(x**2-1))