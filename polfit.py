import numpy as np

def polfit(x,y):
    n = len(x)
    y = np.matrix(y).transpose()

    coeff = np.matrix(np.zeros([n, n]))
    coeff[:,0]=1
    for j in range(0, n):
        for i in range(1, n):
            coeff[j,i] = x[j]**i
    return coeff**(-1)*y
   
def polfun(t, coeff):
    res =np.zeros(len(t))
    deg = 0
    for j in range(0, coeff.shape[0]):
        res = res + coeff[j,0] * t ** deg
        deg = deg + 1
    return res

coeff = polfit([1,2,3], [4,10,3])
x = polfun(np.array([2,3,5]), coeff)
