import csv
import operator
import math
import numpy as numpy
from sets import Set
from numpy import genfromtxt, savetxt
from sklearn import cross_validation
from sys import argv

f = open("ratings.csv")
ratings_data = csv.reader(f)
listData = list(ratings_data)

VData = {}
VData1 = {}
def GetValidationData(listOfData):
    count = 0
    i = 0
    for data in listData:
        tuplelist = []
        tuplelist1 = []     
        tuplelist.append(data[0])
        tuplelist.append(data[1])
        tuplelist.append(data[2])
        tuplelist1.append(data[0])
        tuplelist1.append(data[1])
        if count < 10:
            count = count + 1
        else :
            VData[i] = tuplelist
            VData1[i] = tuplelist1
            i = i + 1
            count = 0
    return VData, VData1
#----------------------------------------------------------------------
def csv_writer(data, path):

    """
    Write data to a CSV file path
    """
    with open(path, "wb") as csv_file:
        writer = csv.writer(csv_file,delimiter=',')
       
        for i in range(0,len(data)):
            writer.writerow(data[i])
#----------------------------------------------------------------------
if __name__ == "__main__":

    path = "ValidationSet_groundtruth.csv" 
    path1 = "ValidationSet.csv"

    ValidationData_GT,ValidationData = GetValidationData(listData) 

    csv_writer(ValidationData_GT, path)
    csv_writer(ValidationData, path1)