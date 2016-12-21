from math import sqrt
import codecs
data = {"Angelica": {"Blues Traveler": 3.5, "Broken Bells": 2.0,"Norah Jones": 4.5, "Phoenix": 5.0,"Slightly Stoopid": 1.5, "The Strokes": 2.5, "Vampire Weekend": 2.0}, "Bill": {"Blues Traveler": 2.0, "Broken Bells": 3.5, "Deadmau5": 4.0, "Phoenix": 2.0, "Slightly Stoopid": 3.5, "Vampire Weekend": 3.0}, "Chan": {"Blues Traveler": 5.0, "Broken Bells": 1.0, "Deadmau5": 1.0, "Norah Jones": 3.0, "Phoenix": 5, "Slightly Stoopid": 1.0}, "Dan": {"Blues Traveler": 3.0, "Broken Bells": 4.0, "Deadmau5": 4.5, "Phoenix": 3.0, "Slightly Stoopid": 4.5, "The Strokes": 4.0, "Vampire Weekend": 2.0}, "Hailey": {"Broken Bells": 4.0, "Deadmau5": 1.0, "Norah Jones": 4.0, "The Strokes": 4.0, "Vampire Weekend": 1.0}, "Jordyn": {"Broken Bells": 4.5, "Deadmau5": 4.0, "Norah Jones": 5.0, "Phoenix": 5.0, "Slightly Stoopid": 4.5, "The Strokes": 4.0, "Vampire Weekend": 4.0}, "Sam": {"Blues Traveler": 5.0, "Broken Bells": 2.0, "Norah Jones": 3.0, "Phoenix": 5.0, "Slightly Stoopid": 4.0, "The Strokes": 5.0}, "Veronica": {"Blues Traveler": 3.0, "Norah Jones": 5.0, "Phoenix": 4.0, "Slightly Stoopid": 2.5,"The Strokes": 3.0} }

dataLeo = {11: {111:1, 333:2, 444:1}, 
		22: {333:4, 444:2},
		33: {111:3, 222:5, 444:4, 333:4},
		44: {222:3, 555:5}}

dataSarjel = {"A": {"HP1": 4.0, "TW": 5.0, "SW1": 1.0},
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

def normalizeData( data ):
	normalised = {}

	for user in data:
		userSum = 0
		userAvg = 0
		ratingCount = 0
		userNormalised = {}
		for rating in data[user].itervalues():
			ratingCount += 1
			userSum += rating
		userAvg = userSum/ratingCount
		for (movie,rating) in data[user].iteritems():
			userNormalised[movie] = (rating - userAvg)
		normalised[user] = userNormalised

	return normalised        

def calcSim (user, userOther, data):
	sum_xy = 0
	sum_x2 = 0
	sum_y2 = 0
	n = 0
	rating1 = data[user]
	rating2 = data[userOther]

	for key in rating1:
		if key in rating2:
			n += 1
			sum_xy += rating1[key]*rating2[key]
			

	if n == 0:
		return 0
	else:

		for value in rating1.itervalues():
			sum_x2 += value**2
		for value in rating2.itervalues():
			sum_y2 += value**2

		denominator = sqrt(sum_x2) * sqrt(sum_y2)

		if denominator == 0:
			return 0
		else:
			return sum_xy/denominator

def createSimMatrix(data):

	normalizedMatrix = normalizeData(data) 

	simMatrix = {}
	sumNum = 0
	sumUser = 0
	sumOtherUser = 0

	for user in normalizedMatrix:
		#print ("for user " + user)
		sim = {}

		for userOther in normalizedMatrix:
			k = calcSim (user, userOther, normalizedMatrix)
			sim[userOther] = k			
			#print ("sim("+user+","+userOther+") ="+str(k))


		simMatrix[user] = sim

	return simMatrix

def computeNearestNeighbor(username, movie, data, simMatrix):
	simUser = simMatrix.get(username)
	sorted_simUser = sorted(simUser.items(), key=lambda x: -x[1])
	#print sorted_simUser
	simArray = []
	cnt1 = 0
	cnt2 = 0
	for u in sorted_simUser:
		cnt1 = cnt1 + 1
		
		if cnt1 is not 1:
			if data.get(u[0]).get(movie) is not None:
				temp = (u[0], u[1])
				simArray.append(temp)
				cnt2 = cnt2 + 1
				#print u[0]
				#print data.get(u[0]).get(movie)
		if cnt2 is 50:
			break
	
	return simArray

def calcMovieAvg(data):
	movieAvgs = {}
	movieTots = {}

	users = normalizeData(data)

	for user in users:
		for (movie,rating) in users[user].iteritems():
			movieAvgs[movie] = 0
			movieTots[movie] = 0

	for user in users:
		for (movie,rating) in users[user].iteritems():
			movieAvgs[movie] += rating
			movieTots[movie] += 1

	for movie in movieAvgs:
		movieAvgs[movie] = movieAvgs[movie]/ movieTots[movie]

	return movieAvgs

def calcUserAvg(data):
	ux = 0
	userAvgs = {}
	nx = 0

	users = normalizeData(data)

	for user in users:
		for value in users[user].itervalues():
			ux += value
			nx += 1
		ux = ux/nx
		userAvgs[user] = ux

	return userAvgs

def calcGlobal(data):
	u = 0
	n = 0

	users = normalizeData(data)

	for user in users:
		for value in users[user].itervalues():
			u += value
			n += 1
	u = u/n	
	return u

def calculateRating(username, movie, data, simMatrix, u, ui, ux):
	currentUser = data.get(username)
	simArray = computeNearestNeighbor(username, movie, data, simMatrix)
	denominator_sum = 0
	total = 0
	length = len(simArray)
	for el in simArray:
		total = total + el[1]*data[el[0]][movie]
		denominator_sum = denominator_sum + el[1]
	div = 0

	if ((username in ui) and (movie in ux)):
		userAvg = ui[username] - u
		movieAvg = ux[movie] - u
		baseline = u + userAvg + movieAvg
		if denominator_sum > 0.00000000000001:
			div = total/denominator_sum
		#print simArray
		return baseline + div
	else:
		return 0

def mainFunction(path=''):
	data = loadMovieLens('ml-100k/')
	userAvg = calcUserAvg(data)
	movieAvg = calcMovieAvg(data)
	globalAvg = calcGlobal(data)
	simMatrix = createSimMatrix(data)
	f = codecs.open(path + 'u3.test', 'r', 'ascii')
	cnt = 0
	dif = 0
	sum = 0
	for line in f:
		fields = line.split('\t')
		user = fields[0]
		movie = fields[1]
		rating = int(fields[2].strip().strip('"'))
		calculated = calculateRating(user, movie, data, simMatrix, globalAvg, userAvg, movieAvg)		
		if calculated is not 0:
			dif = (calculated - rating) ** 2
			sum = sum + dif
			cnt = cnt + 1
		#print cnt
	f.close()
	rmse = sqrt(sum/cnt)
	print rmse



#simArray = computeNearestNeighbor("Angelica", "The Strokes", data, simMatrix)
#print calculateRating("Angelica", "The Strokes", data, simMatrix)
mainFunction('ml-100k/')