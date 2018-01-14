#!/usr/bin/python
"""
	Developers:
	IRENE GONZALEZ VELASCO
	ELENA KALOYANOVA POPOVA
	VICTOR DEL PINO CASTILLA
"""
import string
import sys

def main_menu():
	print("1.Calculate your grade")
	print("2.Show statistics")
	print("0.Exit")
	print("Choose your option:")
	option = input()
	if option >= 0 and option < 3:
		return option,True
	else:
		print("Wrong option!")
		return -1,False

def calculate_grade():
	platforms = ["PS4","XOne","WiiU","PSV", "3DS", "PC", "Android"]
	correct = False
	while correct is False:
		platform = raw_input("Platform:")
		if platform in platforms:
			correct = True
			genre = raw_input("Genre:")
			dev = raw_input("Developer:")
			month = raw_input("Month of release (1-12):")
			if month < 1 or month > 12:
				correct = False
				print("Wrong month!")
			else:
				correct = True
		else:
			print("Wrong platform, correct ones are: " + str(platforms))
	file = open("data.txt", "w")
	file.write(platform + "," + genre + "," + dev + "," + month + "\n")
	file.close()

def show_statistics():
	print("We are working on it")
	
def menu():
	print("Welcome to CalculateVideogamesGrade")
	option,go_on = main_menu()
	while go_on is not True:
		option,go_on = main_menu()
	if int(option) == 1:
		calculate_grade()
	elif int(option) == 2:
		show_statistics()
	elif int(option) == 0:
		print("Bye!")
menu()