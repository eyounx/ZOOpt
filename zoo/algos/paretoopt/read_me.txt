Before call the function paretoopt in paretoopt.py,we must normalize the data to make the matrix have mean 0 and variance 1 for each column.

The input of function NormalizeDate in NormalizeDate.py is the file path of the data. The result of function NormalizeDate is a matrix which 
is normalized.

The input of function paretoopt in paretoopt.py is the feature matrix X and predictor vector y and the number of selected feature.The result
of paretoop is a 0-1 vector which 1 means the corresponding feature is selected.

To get result like this:
    orginX=NormlizeDate("housing.txt") #get normalized date
    n=np.shape(orginX)[1]              # n means the number of feature
    X=orginX[:,0:n-1]                  # X means the feature matrix
    y=orginX[:,n-1]                    # y means the predictor vector
    selectIndex=paretoopt(X, y, 8)     # get result
