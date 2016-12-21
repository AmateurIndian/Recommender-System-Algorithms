from math import sqrt
import codecs
example = {"Amy": {"Taylor Swift": 4, "PSY": 3, "Whitney Houston": 4},
 "Ben": {"Taylor Swift": 5, "PSY": 2},
 "Clara": {"PSY": 3.5, "Whitney Houston": 4},
 "Daisy": {"Taylor Swift": 5, "Whitney Houston": 3}}


example2 = {"A": {"HP1": 4.0, "TW": 5.0, "SW1": 1.0},
          "B": {"HP1": 5.0, "HP2": 5.0, "HP3": 4.0},
          "C": {"TW": 2.0, "SW1": 4.0, "SW2": 5.0},
          "D": {"HP2": 3.0, "SW3": 3.0}}

def loadMovieLens(path=''):
	data = {}
	i = 0
	f = codecs.open(path + 'u1.base', 'r', 'ascii')
	for line in f:
		fields = line.split('\t')
		user = fields[0]
		movie = fields[1]
		rating = int(fields[2].strip().strip('"'))
		#print(fields[0] + '\t' + fields[1] + '\t' + fields[2])
		if user in data:
			currentRatings = data[user]
		else:
			currentRatings = {}
		currentRatings[movie] = rating
		data[user] = currentRatings
	f.close()
	#print('loaded')
	return data

def calcDeviations( data ):
	deviation = {}
	total = {}
	movieList = []

	for ratings in data.itervalues():
		for (movie, value) in ratings.iteritems():
			for (secMovie, secVal) in ratings.iteritems():
				pair = movie + secMovie
				deviation[pair] = 0 
				total[pair] = 0


	
	for ratings in data.itervalues():
		for (movie, value) in ratings.iteritems():
			for (secMovie, secVal) in ratings.iteritems():
				pair = movie + secMovie
				deviation[pair] += (value -secVal)
				total[pair] += 1
			if movie not in movieList:
				movieList.append(movie)

	for (pair, value) in deviation.iteritems():
		deviation[pair] = value/total[pair]

	
	# CODE TO CALCULATE ALL MISSING RATINGS
	'''
	result = 0
	for (user, ratings) in data.iteritems():
		for movie in movieList:
			if movie not in ratings:
				result = calculateRating (user, movie, deviation, data, total)
				print ("The predicted rating of " + movie +" by " + user + " would be:" + str(result))'''
			

	return deviation

def calcCardinality(data):
	total = {}

	for ratings in data.itervalues():
		for (movie, value) in ratings.iteritems():
			for (secMovie, secVal) in ratings.iteritems():
				pair = movie + secMovie
				total[pair] = 0


	
	for ratings in data.itervalues():
		for (movie, value) in ratings.iteritems():
			for (secMovie, secVal) in ratings.iteritems():
				pair = movie + secMovie
				total[pair] += 1

	return total
			
def calculateRating(user, newmovie, deviation, data, card ):
	num = 0
	denom = 0

	for (movie, rating) in data[user].iteritems():
		pair = newmovie+movie
		if ((pair in deviation) and (pair in card)):
			rate = (rating + deviation[pair])* card[pair]
			num += rate
			denom += card[pair]
		
		if (denom == 0):
			return 0
		else : return num/denom
		


def mainFunction(path=''):
	data = loadMovieLens('ml-100k/')
	deviationMatrix = calcDeviations(data)
	cardinalityMatrix = calcCardinality(data)

	f = codecs.open(path + 'u3.test', 'r', 'ascii')
	cnt = 0
	dif = 0
	sum = 0
	for line in f:
		fields = line.split('\t')
		user = fields[0]
		movie = fields[1]
		rating = int(fields[2].strip().strip('"'))
		calculated = calculateRating(user, movie, deviationMatrix, data, cardinalityMatrix)		
		if calculated is not 0:
			dif = (calculated - rating) ** 2
			sum = sum + dif
			cnt = cnt + 1
	f.close()
	rmse = sqrt(sum/cnt)
	print rmse 

#simArray = computeNearestNeighbor("Angelica", "The Strokes", data, simMatrix)
#print calculateRating("Angelica", "The Strokes", data, simMatrix)
mainFunction('ml-100k/')