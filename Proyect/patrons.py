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
		avgMC = int(metacritic_critics)/mn
		avgMU = int(metacritic_users)/mn
		avgs.append(str(avgMC))
		avgs.append(str(avgMU))
	if ingn > 0: # same with IGN
		avgIC = int(ign_criticts)/ingn
		avgs.append(str(avgIC))
	if len(avgs) > 0:
		avg = (avgMC+avgMU+avgIC)/len(avgs)
	else:
		avg = 0
	return avgs,avg

def platform_avg(ignData,metacriticData,sc,platform):
	#Do the statisticts related to the given platform

	# Search in Metacritic CSV
	platformMetacritic = metacriticData.filter(lambda line: platform in line).map(lambda line: (line[0],line[5],line[6]))

	if platformMetacritic.isEmpty() is False: # if asked data is not on the CSV we just ignore it
		platformMCritics = platformMetacritic.map(lambda line: (line[1])).reduce(lambda x,y: x+y)
		platformMUsers = platformMetacritic.map(lambda line: (line[2])).reduce(lambda x,y: x+y)
		platformMCount = platformMetacritic.count()
	else:
		platformMCritics = 0
		platformMUsers = 0
		platformMCount = 0

	# Search in IGN CSV
	platformIgn = ignData.filter(lambda line: platform in line).map(lambda line: (line[0],line[1]))

	if platformIgn.isEmpty() is False:
		platformICritics = platformIgn.map(lambda line: (line[1])).reduce(lambda x,y: x+y)
		platformICount = platformIgn.count()
	else:
		platformICritics = 0
		platformICount = 0

	#Calculate averega grade
	avgs_list,avg = average(platformMCritics,platformMUsers,platformICritics,platformMCount,platformICount)

	result = sc.parallelize(avgs_list,1)
	result.saveAsTextFile("platforms.txt")
	return avg

def platform_sales(metacriticData,sc,platform):
	#Do the statisticts related to the given platform

	# Search in Metacritic CSV
	platformMetacritic = metacriticData.filter(lambda line: platform in line).map(lambda line: (line[0],line[4]))

	if platformMetacritic.isEmpty() is False: # if asked data is not on the CSV we just ignore it
		platformSales = platformMetacritic.map(lambda line: (line[1])).reduce(lambda x,y: x+y)
		platformMCount = platformMetacritic.count()
	else:
		platformSales = 0
		platformMCount = 0

	#Calculate averege sales
	avg = round((platformSales*1000000)/platformMCount,2)

	result = sc.parallelize([avg],1)
	result.saveAsTextFile("platforms_sales.txt")
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
		genreMCritics = 0
		genreMUsers = 0
		genreMCount = 0

	# Search in IGN CSV
	genreIgn = ignData.filter(lambda line: genre in line).map(lambda line: (line[2],line[1]))
	if genreIgn.isEmpty() is False:
		genreICritics = genreIgn.map(lambda line: (line[1])).reduce(lambda x,y: x+y)
		genreICount = genreIgn.count()
	else:
		genreICritics = 0
		genreICount = 0

	#Calculate averega grade
	avgs_list,avg = average(genreMCritics,genreMUsers,genreICritics,genreMCount,genreICount)

	result = sc.parallelize(avgs_list,1)
	result.saveAsTextFile("genres.txt")
	return avg

def genre_sales(metacriticData,sc,genre):
	#Do the statisticts related to the given genre

	# Search in Metacritic CSV
	genreMetacritic = metacriticData.filter(lambda line: genre in line).map(lambda line: (line[2],line[4]))

	if genreMetacritic.isEmpty() is False: # if asked data is not on the CSV we just ignore it
		genreSales = genreMetacritic.map(lambda line: (line[1])).reduce(lambda x,y: x+y)
		genreMCount = genreMetacritic.count()
	else:
		genreSales = 0
		genreMCount = 0

	#Calculate averege sales
	avg = round((genreSales*1000000)/genreMCount,2)

	result = sc.parallelize([avg],1)
	result.saveAsTextFile("genres_sales.txt")
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
		developerMCritics = 0
		developerMUsers = 0
		developerMCount = 0

	#Calculate averega grade
	avgs_list,avg = average(developerMCritics,developerMUsers,0,developerMCount,0)

	result = sc.parallelize(avgs_list,1)
	result.saveAsTextFile("developers.txt")
	return avg

def developer_sales(metacriticData,sc,developer):
	#Do the statisticts related to the given developer

	# Search in Metacritic CSV
	developerMetacritic = metacriticData.filter(lambda line: developer in line).map(lambda line: (line[3],line[4]))

	if developerMetacritic.isEmpty() is False: # if asked data is not on the CSV we just ignore it
		developerSales = developerMetacritic.map(lambda line: (line[1])).reduce(lambda x,y: x+y)
		developerMCount = developerMetacritic.count()
	else:
		eveloperSales = 0
		developerMCount = 0

	#Calculate averege sales
	avg = round((developerSales*1000000)/developerMCount,2)

	result = sc.parallelize([avg],1)
	result.saveAsTextFile("developers_sales.txt")
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
		yearMCritics = 0
		yearMUsers = 0
		yearMCount = 0

	#Calculate averega grade
	avgs_list,avg = average(yearMCritics,yearMUsers,0,yearMCount,0)

	result = sc.parallelize(avgs_list,1)
	result.saveAsTextFile("years.txt")
	return avg

def year_sales(metacriticData,sc,year):
	#Do the statisticts related to the given year

	# Search in Metacritic CSV
	yearMetacritic = metacriticData.filter(lambda line: year in line).map(lambda line: (line[1],line[4]))

	if yearMetacritic.isEmpty() is False: # if asked data is not on the CSV we just ignore it
		yearSales = yearMetacritic.map(lambda line: (line[1])).reduce(lambda x,y: x+y)
		yearMCount = yearMetacritic.count()
	else:
		yearSales = 0
		yearMCount = 0

	#Calculate averega grade
	avg = round((yearSales*1000000)/yearMCount,2)

	result = sc.parallelize([avg],1)
	result.saveAsTextFile("years_sales.txt")
	return avg

def month_avg(ignData,sc,month):
	#Do the statisticts related to the given month

	# Search in IGN CSV
	monthIgn = ignData.filter(lambda line: int(month) in line).map(lambda line: (line[4],line[1]))
	if monthIgn.isEmpty() is False:
		monthICritics = monthIgn.map(lambda line: (line[1])).reduce(lambda x,y: x+y)
		monthICount = monthIgn.count()
	else:
		monthICritics = 0
		monthICount = 0

	#Calculate averega grade
	avgs_list,avg = average(0,0,monthICritics,0,monthICount)

	result = sc.parallelize(avgs_list,1)
	result.saveAsTextFile("months.txt")
	return avg

def main():

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

	op = args[0]

	if int(op) == 1 or int(op) == 2:
		platform = args[1]
		genre = args[2]
		developer = args[3]
		month = args[4]
		file.close()
	elif int(op) == 3:
		version = args[1]
		category = args[2]
		version = int(version)
		category = int(category)

	avgs = []
	avgs.append(op)

	gradesAvg = 0
	salesAvg = 0

	if int(op) == 1:
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
		for i in range(len(avgs)):
			if i != 0:
				gradesAvg = gradesAvg + avgs[i]
		avgs.append(gradesAvg/(len(avgs)-1))
		final = sc.parallelize(avgs,1)
	
	elif int(op) == 2:
		if platform != "NO":
			platformSales = platform_sales(metacriticData,sc,platform)
			avgs.append(platformSales)
		if genre != "NO":
			genreSales = genre_sales(metacriticData,sc,genre)
			avgs.append(genreSales)
		if developer != "NO":
			developerSales = developer_sales(metacriticData,sc,developer)
			avgs.append(developerSales)
		for i in range(len(avgs)):
			if i != 0:
				salesAvg = salesAvg + avgs[i]
		avgs.append(round(salesAvg/(len(avgs)-1),2))
		final = sc.parallelize(avgs,1)

	elif int(op) == 3:
		avg = 0
		value = args[3]
		if version == 1: # grades avg
			if category == 1:
				avg = platform_avg(ignData,metacriticData,sc,value)
			elif category == 2:
				avg = genre_avg(ignData,metacriticData,sc,value)
			elif category == 3:
				avg = developer_avg(metacriticData,sc,value)
			elif category == 4:
				avg = month_avg(ignData,sc,value)
			elif category == 5:
				avg = year_avg(ignData,metacriticData,sc,value)
		elif version == 2:
			if category == 1:
				avg = platform_sales(metacriticData,sc,value)
			elif category == 2:
				avg = genre_sales(metacriticData,sc,value)
			elif category == 3:
				avg = developer_sales(metacriticData,sc,value)
			elif category == 4:
				print("No data on this moment about month sales")
			elif category == 5:
				avg = year_sales(metacriticData,sc,value)
		final = sc.parallelize(["3",str(avg)],1)

	final.saveAsTextFile("result.txt")
	

main()