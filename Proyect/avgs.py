#!/usr/bin/python
"""
	Developers:
	IRENE GONZALEZ VELASCO
	ELENA KALOYANOVA POPOVA
	VICTOR DEL PINO CASTILLA
"""
import string
import sys

categories = ["Platform: ", "Genre: ", "Developer: ", "Month of release: ", "Expected grade: "]
categories2 = ["Platform: ", "Genre: ", "Developer: ", "Expected sales: "]

file_name = sys.argv[1]
file = open(file_name)
option = file.readline()
if  int(option) == 3:
	result = file.readline()
	print("The average is: " + result)
elif int(option) == 1:
	for i in range(5):
		avg = file.readline()
		avg = avg.rstrip("\n")
		print(categories[i] + avg)
	avg = int(avg)
	if avg <= 100 and avg >= 90:
		print("EXCELLENT!")
	elif avg < 90 and avg >= 70:
		print("GREAT")
	elif avg < 70 and avg >= 50:
		print("GOOD")
	else:
		print("SORRY :(")
elif int(option) == 2:
	 for i in range(4):
		avg = file.readline()
		avg = avg.rstrip("\n")
		print(categories2[i] + avg)

file.close()