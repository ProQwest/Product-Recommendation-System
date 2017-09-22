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

print userRatings

def transposeRankings(ratings):
    transposed = {}
    for user in ratings:
        for item in ratings[user]:
            transposed.setdefault(item, {})
            transposed[item][user] = ratings[user][item]
    return transposed

def closeMathes(ratings, item, similarity):
    first_item = item
    score = [(similarity(ratings, first_item, second_item), second_item) for second_item in ratings if second_item != first_item]
    scores.sort()
    scores.reverse()
    return scores

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

def itemBasedRecommandations(ratings, MatchiItem, wantPrediction):
    file = open('itemBasedRecords.txt','a')
    for tuple in wantPrediction:
        user = tuple[0]
        itemAsked = tuple[1]

        uRatings = ratings[user]
        scores = {}
        total = {}
        ranks = {}

        #items rated by this user
        for(item, rating) in URatings.items():
            #items that are similar to this one
                for(similarity,item_2) in MatchiItem[item]:
                #don't consider if the user has already rate this item
                if item_2 in uRatings: continue
                scores.setdefault(item_2, 0)
                scores[item_2] += similarity*(rating)

                #sum over similarities
                total[item_2] += similarity
                if total[item_2] == 0:
                    ranks[item_2] = 1
                else:
                    ranks[item_2] = scores[item_2]/total[item_2]
        print ranks[itemAsked]
        file.write(str(ranks[itemAsked]))


def similarItems(ratings, similarity):
    itemList = {}
    itemsRatings = transposeRankings(ratings)
    for item in itemsRatings:
        matches = closeMatches(itemRatings, item, similarity)
        itemList[item] = matches
    return itemList

def mainFunction():
    
    simItems = similarItems(userRatings, compute_cosine_similarity)
    itemBasedRecommandations(userRatings, simItems, toBeRatedList)
    
mainFunction()