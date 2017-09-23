import csv
import operator
import math
import numpy as numpy
from sets import Set
from numpy import genfromtxt, savetxt
from sklearn import cross_validation
from sklearn.cross_validation import StratifiedKFold
from sys import argv

f = open("TrainSet.csv")
ratings_data = csv.reader(f)
listData = list(ratings_data)


f = open("ValidationSet.csv")
toBeRated = csv.reader(f)
toBeRatedList = list(toBeRated)

itemsRatings = {}
userRatings = {}

users = sorted(listData, key = operator.itemgetter(0))

u_prev = 0
for i in range (0, len(users)):

    userID = users[i][0]
    itemID = users[i][1]
    itemRating = users[i][2]
    if(u_prev == userID):
        userRatings[userID][itemID] = itemRating
        u_prev = userID
    else:
        userRatings[userID] = {}
        userRatings[userID][itemID] = itemRating
        u_prev = userID

#print userRatings

def transposeRankings(ratings):
    transposed = {}
    print "Transposed......"
    for user in ratings:
        for item in ratings[user]:
            transposed.setdefault(item, {})
            transposed[item][user] = ratings[user][item]
    return transposed


# Calculating Cosine Similarity 
def compute_cosine_similarity(ratings, user_1, user_2):
	similarity = {}

	for item in ratings[user_1]:
		if item in ratings[user_2]:
			similarity[item] = 1
	numSim =len(similarity)
	if numSim == 0:
		return 0
	userOneRatingsArray = ([ratings[user_1][s] for s in similarity])
	userOneRatingsArray = map(int, userOneRatingsArray)
	userTwoRatingsArray = ([ratings[user_2][s] for s in similarity])
	userTwoRatingsArray = map(int, userTwoRatingsArray)

	
	sum_xx, sum_yy, sum_xy = 0,0,0

	for i in range(len(userOneRatingsArray)):
		x = userOneRatingsArray[i]
		y = userTwoRatingsArray[i]

		sum_xx += x*x
		sum_yy += y*y
		sum_xy += x*y

	return sum_xy/math.sqrt(sum_xx*sum_yy)

def closeMatches(ratings, item,compute_cosine_similarity):
    #print "Match similar items......"
    scores = {}
    first_item = item
    COUNT = 0
    for second_item in ratings:
        if second_item == first_item: continue
        similarity = {}

        for user in ratings[first_item]:
            if user in ratings[second_item]:
                similarity[user] = 1
                COUNT = COUNT+1
        numSim =len(similarity)
        
        if numSim == 0:
            S = 0
        else:
            userOneRatingsArray = ([ratings[first_item][s] for s in similarity])
            userOneRatingsArray = map(int, userOneRatingsArray)
            userTwoRatingsArray = ([ratings[second_item][s] for s in similarity])
            userTwoRatingsArray = map(int, userTwoRatingsArray)

                
            sum_xx, sum_yy, sum_xy = 0,0,0

            for i in range(len(userOneRatingsArray)):
                x = userOneRatingsArray[i]
                y = userTwoRatingsArray[i]

                sum_xx += x*x
                sum_yy += y*y
                sum_xy += x*y
            S = sum_xy/math.sqrt(sum_xx*sum_yy)
            #print second_item
            #a = compute_cosine_similarity(ratings, first_item, second_item)           
            scores[second_item] = S
    #print COUNT
    #print scores
    Scores = sorted(scores, key = operator.itemgetter(0))
    #scores.sort()
    #scores.reverse()
    return Scores   

def similarItems(ratings, similarity):
    print "Start Matching......."
    itemList = {}
    itemsRatings = transposeRankings(ratings)
    count = 0
    for item in itemsRatings:
        #print "....................."
        #print item
        if count < 1000:
            matches = closeMatches(itemsRatings, item, compute_cosine_similarity)
            itemList[item] = matches
            count = count+1
    #print itemList
    print "finish Matching......"
    return itemList

def itemBasedRecommandations(ratings, MatchiItem, wantPrediction):
    file = open('itemBasedRecords.txt','a')
    count = 0
    for tuple in wantPrediction:
        if count < 3:

            user = tuple[0]
            itemAsked = tuple[1]
            print ratings[user]
            if ratings[user] != None:
                uRatings = ratings[user]
                scores = {}
                total = {}
                ranks = {}

                #items rated by this user
                for(item, rating) in uRatings.items():
                    #items that are similar to this one
                        print MatchiItem[item]
                        for(similarity,item_2) in MatchiItem[item]:
                        #don't consider if the user has already rate this item
                            if(item_2 in uRatings): continue
                            scores.setdefault(item_2, 0)
                            scores[item_2] += similarity*(rating)

                            #sum over similarities
                            total[item_2] += similarity
                            if(total[item_2] == 0):
                                ranks[item_2] = 1
                            else:
                                ranks[item_2] = scores[item_2]/total[item_2]
                #print ranks[itemAsked]
                count = count+1
                file.write(str(ranks[itemAsked]))



def mainFunction():
    
    simItems = similarItems(userRatings, compute_cosine_similarity)
 
    itemBasedRecommandations(userRatings, simItems, toBeRatedList)
    
mainFunction()