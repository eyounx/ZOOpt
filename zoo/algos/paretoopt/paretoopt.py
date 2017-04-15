# the python version is 2.7
import sys
import numpy as np
from random import randint
from math import ceil
from math import exp
from NormalizeData import NormlizeDate
from copy import deepcopy
def mutation(s,n):#every bit will be flipped with probability 1/n
    s_temp=deepcopy(s)
    for i in range(1,n+1):
        if randint(1,n)==i:#the probability is 1/n
            s_temp[0,i-1]=(s[0,i-1]+1)%2
    return s_temp


def position(s):#This function is to find the index of s where element is 1
    n=np.shape(s)[1]
    result=[]
    for i in range(0,n):
        if s[0,i]==1:
            result.append(i)
    return result   
        
def paretoopt(X,y,k):
    C=X.T*X
    b=X.T*y
    [m,n]=np.shape(X)#row and column number of the matrix
    population=np.mat(np.zeros([1,n],'int8'))#initiate the population
    fitness=np.mat(np.zeros([1,2]))
    fitness[0,0]=float('inf')
    popSize=1
    t=0#the current iterate count
    T=long(ceil(n*k*k*2*exp(1)))
    while t<T:
        s=population[randint(1, popSize)-1,:]#choose a individual from population randomly
        offSpring=mutation(s, n)#every bit will be flipped with probability 1/n
        offSpringFit=np.mat(np.zeros([1,2]))
        offSpringFit[0,1]=offSpring[0,:].sum()
        if offSpringFit[0,1]==0.0 or offSpringFit[0,1]>=2.0*k:
            offSpringFit[0,0]=float("inf")
        else:
            pos=position(offSpring)
            alpha=(C[pos,:])[:,pos].I*b[pos,:]
            err=y-X[:,pos]*alpha
            offSpringFit[0,0]=err.T*err/m  
        #now we need to update the population
        hasBetter=False    
        for i in range(0,popSize):
            if (fitness[i,0]<offSpringFit[0,0] and fitness[i,1]<=offSpringFit[0,1]) or (fitness[i,0]<=offSpringFit[0,0] and fitness[i,1]<offSpringFit[0,1]):
                hasBetter=True
                break
        if hasBetter==False:#there is no better individual than offSpring
            Q=[]
            for j in range(0,popSize):
                if offSpringFit[0,0]<=fitness[j,0] and offSpringFit[0,1]<=fitness[j,1]:
                    continue
                else:
                    Q.append(j)
            Q.sort()
            fitness=np.vstack((offSpringFit,fitness[Q,:]))#update fitness
            population=np.vstack((offSpring,population[Q,:]))#update population
            
        t=t+1
        popSize=np.shape(fitness)[0]
    resultIndex=-1
    maxSize=-1 
    for p in range(0,popSize):
        if fitness[p,1]<=k and fitness[p,1]>maxSize:
            maxSize=fitness[p,1]
            resultIndex=p    
    #print 'correlation is:%f'%(1-fitness[resultIndex,0])        
    return population[resultIndex,:]        

if __name__=="__main__":
    print "start"
    orginX=NormlizeDate("housing.txt")
    n=np.shape(orginX)[1]
    X=orginX[:,0:n-1]
    y=orginX[:,n-1]
    selectIndex=paretoopt(X, y, 8)
    print selectIndex
    print "end"
    
        
        
                  
    
