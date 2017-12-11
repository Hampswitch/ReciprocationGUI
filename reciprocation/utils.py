
from matplotlib import pyplot

def showpoly(polygon):
    x,y=polygon.exterior.xy
    fig = pyplot.figure(1, figsize=(5, 5), dpi=90)
    ax = fig.add_subplot(111)
    ax.plot(x, y, color='#6699cc', alpha=0.7,
            linewidth=3, solid_capstyle='round', zorder=2)
    ax.set_title('Polygon')