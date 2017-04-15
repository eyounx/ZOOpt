#this code is to standardize the variable to get mean 0 and variance 1.
#python version is 2.7
import sys
from re import split
import numpy as np
def NormlizeDate(filepath):
    try:
        myfile=open(filepath)
        lines = myfile.readlines()
        dataMatrix=[]
        for line in lines:
            lineArray=split(r'\s+',line)
            lineArray = filter(lambda x: x !='', lineArray)
            dataMatrix.append(lineArray)
        dataMatrix=np.mat(dataMatrix,dtype="float64")
        matSize=np.shape(dataMatrix)
        for i in range(0,matSize[1]):
            theColum=dataMatrix[:,i]
            columnMean=sum(theColum)/matSize[0]
            minusColumn=np.mat(theColum-columnMean)
            std=np.sqrt(np.transpose(minusColumn)*minusColumn/matSize[0])
            dataMatrix[:,i]=(theColum-columnMean)/std
            '''
        normDateFile=open('housingNormdata.txt','w')
        for i in range(0,matSize[0]):
            for j in range(0,matSize[1]):
                normDateFile.write("%f "%dataMatrix[i,j])
            normDateFile.write("\n")
           ''' 
        return dataMatrix
    except  Exception as e:
        print  e
    finally:
        myfile.close()
        #normDateFile.close()

if __name__=="__main__":
    NormlizeDate('housing.txt')