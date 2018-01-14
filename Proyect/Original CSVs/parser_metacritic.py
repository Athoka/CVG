import sys
import re

linea = 0
ignorar = ""

def correct(word):
	if word == "0000":
		return "NO"
	elif word == "2001":
		return "NO"
	elif word == "2011":
		return "NO"
	elif word == "2009":
		return "NO"
	elif word == "2005":
		return "NO"
	elif word == "2002":
		return "NO"
	elif word == "2007":
		return "NO"
	elif word == "2003":
		return "NO"
	elif word == "2010":
		return "NO"
	elif word == "2004":
		return "NO"
	else:
		return "YES"

for line in sys.stdin:
	if linea == 0:
		re.sub( r'^\W+|\W+$', '' , ignorar)
		linea = linea + 1
	else:
		line = re.sub( r'^\W+|\W+$', '', line ) # parsear linea	
		words = line.split(',', 17) # se trocea la linea para obtener los datos
		if len(words) > 12:
			if words[12] != "":
				if len(words) == 16 or (len(words)==17 and correct(words[3]) == "YES"):
					user = int(float(words[12])*10)
					if words[10] == "":
						critics = "50"
					else:
						critics = words[10]
					print(words[0] + "," + words[1] + "," + words[2] + "," + words[3] + "," + words[4] + "," + words[9] + "," + critics + ","  + str(user))
				elif len(words) == 17:
					if words[11] == "":
						critics = "50"
					else:
						critics = words[11]
					user = int(float(words[13])*10)
					print(words[0] + words[1] + "," + words[2] + "," + words[3] + "," + words[4] + "," + words[5] + "," + words[10] + "," + critics + ","  + str(user))
				