import csv
import operator
import math
import numpy as np
from sets import Set
from numpy import genfromtxt, savetxt
from sklearn import cross_validation
from sklearn.cross_validation import StratifiedKFold
from sys import argv

f = open("TrainSet.csv")
ratings_data = csv.reader(f)
listData = list(ratings_data)
X = np.array([listData[0],listData[1],listData[2],listData[3]])
count = 0

y = np.array([0, 0, 1, 1])
skf = StratifiedKFold(y, n_folds=2)
print len(skf)
print skf

