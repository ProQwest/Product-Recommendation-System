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

TrainData = {}
TrainData1 = {}
TData = {}
TData1 = {}
VData = {}
VData1 = {}

def GetTest_TrainData(listOfData):
    count = 0
    i = 0
    j = 0
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
            TrainData[j] = tuplelist
            j = j + 1
        else :
            TData[i] = tuplelist
            TData1[i] = tuplelist1
            i = i + 1
            count = 0
    return TData, TData1, TrainData

def GetValidationData(listOfData1):
    count = 0
    i = 0
    j = 0
    print len(listOfData1)
    for k in range(0,len(listOfData1)):
        tuplelist = []
        tuplelist.append(listOfData1[k][0])
        tuplelist.append(listOfData1[k][1])
        tuplelist.append(listOfData1[k][2])
        tuplelist1 = []
        tuplelist1.append(listOfData1[k][0])
        tuplelist1.append(listOfData1[k][1])
        if count < 10:
            count = count + 1
            TrainData1[j] = tuplelist
            j = j + 1
        else :
            VData1[i] = {}
            VData[i] = tuplelist
            VData1[i]= tuplelist1
            i = i + 1
            count = 0
    return VData, VData1, TrainData1

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

    path = "TestSet_groundtruth.csv" 
    path1 = "TestSet.csv"
    path2 = "TrainSet.csv"
    path3 = "ValidationSet_groundtruth.csv"
    path4 = "ValidationSet.csv"

    TestData_GT, TestData, TrainingData = GetTest_TrainData(listData) 
    print TrainingData[0][0]
    ValidationData_GT, ValidationData, TrainingData1 = GetValidationData(TrainingData)

    csv_writer(TestData_GT, path)
    csv_writer(TestData, path1)

    csv_writer(ValidationData_GT, path3)
    csv_writer(ValidationData, path4)
    csv_writer(TrainingData1, path2)

