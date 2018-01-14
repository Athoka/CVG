#!/usr/bin/python
"""
	Developers:
	IRENE GONZALEZ VELASCO
	ELENA KALOYANOVA POPOVA
	VICTOR DEL PINO CASTILLA
"""

from pyspark import SparkConf, SparkContext
import string
import sys

def average(metacritic_critics,metacritic_users,ign_criticts,mn,ingn):
	avgMC = 0 # average of the grades given by the Metacritic members
	avgMU = 0 # average of the grades given by the Metacritic users
	avgIC = 0 # average of the grades given by IGN
	avgs = []
	if mn > 0: # if we don't have the data we just ignore Metacritic
		avgMC = metacritic_critics/mn
		avgMU = metacritic_users/mn
		avgs.append(str(avgMC))
		avgs.append(str(avgMU))
	if ingn > 0: # same with IGN
		avgIC = ign_criticts/ingn
		avgs.append(str(avgIC))
	avg = (avgMC+avgMU+avgIC)/len(avgs)
	return avgs,avg

def empty_metacriticRDD(v1,v2,v3):
	v1 = 0
	v2 = 0
	v3 = 0

def empty_ignRDD(v1,v2):
	v1 = 0
	v2 = 0

def platform_avg(ignData,metacriticData,sc,platform):
	#Do the statisticts related to the given platform

	# Search in Metacritic CSV
	platformMetacritic = metacriticData.filter(lambda line: platform in line).map(lambda line: (line[0],line[5],line[6]))

	if platformMetacritic.isEmpty() is False: # if asked data is not on the CSV we just ignore it
		platformMCritics = platformMetacritic.map(lambda line: (line[1])).reduce(lambda x,y: x+y)
		platformMUsers = platformMetacritic.map(lambda line: (line[2])).reduce(lambda x,y: x+y)
		platformMCount = platformMetacritic.count()
	else:
		empty_metacriticRDD(platformMCritics,platformMUsers,platformMCount)

	# Search in IGN CSV
	platformIgn = ignData.filter(lambda line: platform in line).map(lambda line: (line[0],line[1]))

	if platformIgn.isEmpty() is False:
		platformICritics = platformIgn.map(lambda line: (line[1])).reduce(lambda x,y: x+y)
		platformICount = platformIgn.count()
	else:
		empty_ignRDD(platformICritics,platformICount)

	#Calculate averega grade
	avgs_list,avg = average(platformMCritics,platformMUsers,platformICritics,platformMCount,platformICount)

	result = sc.parallelize(avgs_list,1)
	result.saveAsTextFile("platforms.txt")
	return avg

def genre_avg(ignData,metacriticData,sc,genre):
	#Do the statisticts related to the given genre

	# Search in Metacritic CSV
	genreMetacritic = metacriticData.filter(lambda line: genre in line).map(lambda line: (line[2],line[5],line[6]))

	if genreMetacritic.isEmpty() is False: # if asked data is not on the CSV we just ignore it
		genreMCritics = genreMetacritic.map(lambda line: (line[1])).reduce(lambda x,y: x+y)
		genreMUsers = genreMetacritic.map(lambda line: (line[2])).reduce(lambda x,y: x+y)
		genreMCount = genreMetacritic.count()
	else:
		empty_metacriticRDD(genreMCritics,genreMUsers,genreMCount)

	# Search in IGN CSV
	genreIgn = ignData.filter(lambda line: genre in line).map(lambda line: (line[2],line[1]))
	if genreIgn.isEmpty() is False:
		genreICritics = genreIgn.map(lambda line: (line[1])).reduce(lambda x,y: x+y)
		genreICount = genreIgn.count()
	else:
		empty_ignRDD(genreICritics,genreICount)

	#Calculate averega grade
	avgs_list,avg = average(genreMCritics,genreMUsers,genreICritics,genreMCount,genreICount)

	result = sc.parallelize(avgs_list,1)
	result.saveAsTextFile("genres.txt")
	return avg

def developer_avg(metacriticData,sc,developer):
	#Do the statisticts related to the given developer

	# Search in Metacritic CSV
	developerMetacritic = metacriticData.filter(lambda line: developer in line).map(lambda line: (line[3],line[5],line[6]))

	if developerMetacritic.isEmpty() is False:
		developerMCritics = developerMetacritic.map(lambda line: (line[1])).reduce(lambda x,y: x+y)
		developerMUsers = developerMetacritic.map(lambda line: (line[2])).reduce(lambda x,y: x+y)
		developerMCount = developerMetacritic.count()
	else:
		empty_metacriticRDD(developerMCritics,developerMUsers,developerMCount)

	#Calculate averega grade
	avgs_list,avg = average(developerMCritics,developerMUsers,0,developerMCount,0)

	result = sc.parallelize(avgs_list,1)
	result.saveAsTextFile("developers.txt")
	return avg

def year_avg(ignData,metacriticData,sc,year):
	#Do the statisticts related to the given year

	# Search in Metacritic CSV
	yearMetacritic = metacriticData.filter(lambda line: year in line).map(lambda line: (line[1],line[5],line[6]))

	if yearMetacritic.isEmpty() is False:
		yearMCritics = yearMetacritic.map(lambda line: (line[1])).reduce(lambda x,y: x+y)
		yearMUsers = yearMetacritic.map(lambda line: (line[2])).reduce(lambda x,y: x+y)
		yearMCount = yearMetacritic.count()
	else:
		empty_metacriticRDD(yearMCritics,yearMUsers,yearMCount)

	#Calculate averega grade
	avgs_list,avg = average(yearMCritics,yearMUsers,0,yearMCount,0)

	result = sc.parallelize(avgs_list,1)
	result.saveAsTextFile("years.txt")
	return avg

def month_avg(ignData,sc,month):
	#Do the statisticts related to the given month

	# Search in IGN CSV
	monthIgn = ignData.filter(lambda line: int(month) in line).map(lambda line: (line[4],line[1]))
	if monthIgn.isEmpty() is False:
		monthICritics = monthIgn.map(lambda line: (line[1])).reduce(lambda x,y: x+y)
		monthICount = monthIgn.count()
	else:
		empty_ignRDD(monthICritics,monthICount)

	#Calculate averega grade
	avgs_list,avg = average(0,0,monthICritics,0,monthICount)

	result = sc.parallelize(avgs_list,1)
	result.saveAsTextFile("months.txt")
	return avg

def main():

	"""
	Recolects the data from the user and gives him the results.
	"""

	#Spark configuration
	conf = SparkConf().setMaster('local').setAppName('GamePatrons')
	sc = SparkContext(conf = conf)

	#Load the main CSV files
	RDDign = sc.textFile("ign.csv")
	RDDmetacritic = sc.textFile("metacritic.csv")

	# (Platform,Grade,Genre,Year,Month)
	ignData = RDDign.map(lambda line: 
		(str(line.split(',')[1]),int(line.split(',')[2]),str(line.split(',')[3]),int(line.split(',')[4]),int(line.split(',')[5])))
	# (Platform,Year,Genre,Publisher,Millions Sales,Critics Grade, Users Grade)
	metacriticData = RDDmetacritic.map(lambda line: 
		(str(line.split(',')[1]),int(line.split(',')[2]),str(line.split(',')[3]),str(line.split(',')[4]),float(line.split(',')[5]),int(line.split(',')[6]),int(line.split(',')[7])))


	#Collects the data from the user
	file_name = sys.argv[1]
	file = open(file_name)
	data = file.readline()
	args = data.split(",")
	platform = args[0]
	genre = args[1]
	developer = args[2]
	month = args[3]
	file.close()

	avgs = []

	if platform != "NO":
		platformAVG = platform_avg(ignData,metacriticData,sc,platform)
		avgs.append(platformAVG)
	if genre != "NO":
		genreAVG = genre_avg(ignData,metacriticData,sc,genre)
		avgs.append(genreAVG)
	if developer != "NO":
		developerAVG = developer_avg(metacriticData,sc,developer)
		avgs.append(developerAVG)
	if month != "NO":
		monthAVG = month_avg(ignData,sc,month)
		avgs.append(monthAVG)

	gradesAvg = 0

	for i in range(len(avgs)):
		gradesAvg = gradesAvg + avgs[i]
	avgs.append(gradesAvg/len(avgs))

	final_grade = sc.parallelize(avgs,1)
	final_grade.saveAsTextFile("grade.txt")

main()