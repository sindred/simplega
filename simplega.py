
import random
import numpy as np
from polfit import polfit, polfun

def convert(s):
  
    new = ""
  
    for x in s:
        new += x 
  
    return new

nfrac = 15

nmutation = 0

class GrowingList(list):
    def __setitem__(self, index, value):
        if index >= len(self):
            self.extend([None]*(index + 1 - len(self)))
        list.__setitem__(self, index, value)
    def grow(self, value):
        self.__setitem__(self.__len__(), value)

xsample = [0,5,10,15,20,25,30]
ysample = [0,10,30,25,30,40,25]

coeff = polfit(xsample,ysample)

def objective(t):
    return polfun(t,coeff)

class Individual:
    chrom = None
    fitness = 0
    parent1 = None
    parent2 = None
    xsite = None

    def __init__(self, chrom = chrom, parent1 = parent1, parent2 = parent2, xsite = None) -> None:
        self.chrom = chrom
        self.parent1 = parent1
        self.parent2 = parent2
        self.xsite = xsite
            #//

    def __str__(self):
        return self.chrom
     
    @property
    def x(self):
        return int(self.chrom, 2)/(2**nfrac)

    @property
    def fitness(self):
        return objective(np.array([self.x]))[0]

    @property
    def Summary(self):
        return "Chromosome: " + self.chrom + ', Phenotype: ' + str(self.x) + ', Fitness: ' + str(self.fitness)

class Population:
    pop = GrowingList([])
    def __init__(self, pop):
        self.pop = GrowingList(pop)
    
    def grow(self, ind):
        self.pop.grow(ind)
        

    @property 
    def xvals(self):
        res = np.array([])
        for x in self.pop:
            res = np.append(res, x.x)
        return np.array(res)

    @property
    def fvals(self):
        res = []
        for x in self.pop:
            res = res + [x.fitness]
        return np.array(res)

    @property
    def Summary(self):
        res = ''
        for x in self.pop:
            res = res + "\n" + x.Summary
        return res

    @property
    def sumfitness(self):
        sf = 0
        for x in self.pop:
            sf = sf+x.fitness
        return sf
    
    @property
    def popsize(self):
        return self.pop.__len__()



def select(pop):
    rand = pop.sumfitness * random.uniform(0,1)
    partsum=0.0
    j = 0
    while(partsum<rand and j<pop.popsize):
        j=j+1
        partsum = partsum + pop.pop[j-1].fitness
    return j-1

def popgen(popsize, stringlen):
    pop = [[]]*popsize
    i = 0
    while(i<popsize): 
        j = 0
        temp = ''
        while(j<stringlen):
            temp = temp + str(random.randint(0,1))
            j = j + 1
        pop[i] = Individual(temp)
        i = i + 1
    return Population(pop)


def flip(p=0.5):
    return random.uniform(0,1)<p

def mutation(parent, pmutation, nmutation):
    return None

def charnot(x):
    return str(int(not int(x)))


def crossover(parent1, parent2, lchrom, pcross, pmutation):
    child01, child02, jcross = crossover_list(parent1.chrom, parent2.chrom, lchrom, pcross, pmutation)
    child1 = Individual(child01, parent1, parent2, jcross)
    child2 = Individual(child02, parent1, parent2, jcross)
    return child1, child2

def crossover_list(parent1, parent2, lchrom, pcross, pmutation):
    child1 = [None]*lchrom
    child2 = [None]*lchrom
    if flip(pcross):
        jcross = random.randint(1, lchrom)
    else:
        jcross = lchrom

    for j in range(0, jcross):
        child1[j] = mutation(parent1[j], pmutation)
        child2[j] = mutation(parent2[j], pmutation)

    if jcross != lchrom:
        for j in range(jcross, lchrom):
            child1[j] = mutation(parent2[j], pmutation)
            child2[j] = mutation(parent1[j], pmutation)

    return convert(child1), convert(child2), jcross

def mutation(alleleval, pmutation):
    global nmutation
    mutate = flip(pmutation)
    if mutate:
        nmutation = nmutation + 1
        mutation = charnot(alleleval)
    else:
        mutation = alleleval
    return mutation

def generation(oldpop, popsize, lchrom, pcross, pmutation):
    j=0
    newpop_list = GrowingList([])
    while j<popsize:
        mate1 = oldpop.pop[select(oldpop)]
        mate2 = oldpop.pop[select(oldpop)]
        child1, child2 = crossover(mate1, mate2, lchrom, pcross, pmutation)
        newpop_list[j] = child1
        newpop_list[j+1] = child2
        j = j + 2
    return Population(newpop_list)
