
import simplega as sga 
from simplega import select
from simplega import crossover
from simplega import popgen
from simplega import generation
import numpy as np
import matplotlib.pyplot as plt
import time


t = np.linspace(0, 31, num=100)
ylin =sga.objective(t)

ngen = 10000
lchrom = 20
maxpop = 100
psize = 20

pcross = 0.6
pmutation = 0.01


avg = 0.0
min = 0.0
max = 0.0

newpop = popgen(psize, lchrom)
origpop = newpop

plt.ion()
fig, ax = plt.subplots()
x = newpop.xvals
y = newpop.fvals
lin = ax.plot(t,ylin, color='b')
sc = ax.scatter(x, y, color='k')
plt.draw()
ind = np.where(y==np.max(y))[0][0]
xmax = x[ind]
ymax = y[ind]

clrline = '\033[F\033[K\033[F'
first_after_new_max=False

for j in range(0, ngen):
    oldpop = newpop
    newpop = generation(oldpop, oldpop.popsize, lchrom, pcross, pmutation)
    x = newpop.xvals
    y = newpop.fvals
    ind = np.where(y==np.max(y))[0][0]
    
    if y[ind]<=ymax:
        if first_after_new_max:
            first_after_new_max = False
        else:
            print(clrline)
    else:
        xmax=x[ind]
        ymax=y[ind]
        if not first_after_new_max:
            print(clrline)
        first_after_new_max = True
    
    if j<10:
        print("Gen " + str(j) + ": \t\t" + str(x[ind])+ "\t  -> \t " + str(y[ind]) + " \t" + newpop.pop[ind].chrom)
    else:
        print("Gen " + str(j) + ": \t" + str(x[ind])+ "\t  -> \t " + str(y[ind]) + " \t" + newpop.pop[ind].chrom)
    
    freqs = np.array(np.zeros(len(x)))
    for j in range(0, len(x)):
        freqs[j] = sum(x==x[j])
    sc.set_offsets(np.c_[x, y])
    sc.set_sizes(50*freqs)
    yl1 = ax.get_ylim()

    fig.canvas.draw_idle()
    plt.pause(10/psize/lchrom)


