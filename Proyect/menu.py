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
	"""
	Main menu of the application.
	"""
	print("1.Calculate your grade")
	print("2.Calculate your sales")
	print("3.Show statistics")
	print("0.Exit")
	print("Choose your option:")
	option = input()
	if option >= 0 and option < 4:
		return option
	else:
		print("Wrong option!")
		return -1

def stats_menu():
	"""
	Auxiliar menu for the stats.
	"""
	go_on = False
	while go_on is False:
		print("1.Grades")
		print("2.Sales")
		print("0.Exit")
		print("Choose your option:")
		option = input()
		if option >= 0 and option < 3:
			return option
		else:
			print("Wrong option!")

def stats_op_menu():
	"""
	Main menu for the stats.
	"""
	go_on = False
	while go_on is False:
		print("1.Platform")
		print("2.Genre")
		print("3.Developer")
		print("4.Month")
		print("5.Year")
		print("0.Exit")
		print("Choose your option:")
		option = input()
		if option >= 0 and option < 6:
			return option
		else:
			print("Wrong option!")

def get_data(op):
	platforms = ["PS4","XOne","WiiU","PSV", "3DS", "PC", "Android"] # the ones used on this moment
	correct = False
	while correct is False:
		platform = raw_input("Platform:")
		if platform in platforms:
			correct = True
			genre = raw_input("Genre:")
			dev = raw_input("Developer:")
			month = int(raw_input("Month of release (1-12):"))
			if month < 1 or month > 12:
				correct = False
				print("Wrong month!")
			else:
				correct = True
		else:
			print("Wrong platform, correct ones are: " + str(platforms))
	# Write down the data on a file which is going to be read later by the main program.
	file = open("data.txt", "w")
	file.write(str(op) + "," + platform + "," + genre + "," + dev + "," + str(month) + "\n")
	file.close()

def show_statistics():
	version = stats_menu()
	if version != 0:
		stat = stats_op_menu()
		if stat != 0:
			value = raw_input("Wanted: ")
			# Write down the data on a file which is going to be read later by the main program.
			file = open("data.txt", "w")
			file.write("3," + str(version) + "," + str(stat) + "," + value + "\n")
			file.close()

def menu():
	print("Welcome to CalculateVideogamesGrade")
	option = main_menu()
	while option == -1:
		option = main_menu()

	if int(option) == 1:
		get_data(1)
	elif int(option) == 2:
		get_data(2)
	elif int(option) == 3:
		show_statistics()
	elif int(option) == 0:
		print("Bye")

menu()