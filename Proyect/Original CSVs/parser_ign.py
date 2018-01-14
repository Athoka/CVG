import sys
import re

linea = 0
ignorar = ""

def parse(word1,word2):
	word1 = word1.lstrip('"')
	word2 = word2.rstrip('"')
	word3 = word1 + word2
	return word3

def parse2(word1,word2,word3):
	word1 = word1.lstrip('"')
	word3 = word3.rstrip('"')
	word4 = word1 +  word2 + word3
	return word4

def translate_platform(platform):
	return {
		"PlayStation Vita":"PSV",
		"PlayStation Portable":"PSP",
		"PlayStation":"PS",
		"PlayStation 2":"PS2",
		"PlayStation 3":"PS3",
		"PlayStation 4":"PS4",
		"Xbox":"XB",
		"Xbox 360":"X360",
		"Xbox One":"XOne",
		"PC":"PC",
		"Pocket PC":"PPC",
		"Nintendo DS":"DS",
		"Nintendo 3DS":"3DS",
		"Nintendo 64":"Nintendo64",
		"Nintendo 64DD":"Nintendo64DD",
		"Game Boy Advance":"GBA",
		"Game Boy Color":"GBC",
		"Game Boy":"GB",
		"GameCube":"GameCube",
		"Wii":"Wii",
		"Wii U":"WiiU",
		"Linux":"Linux",
		"Macintosh":"Macintosh",
		"iPad":"iPad",
		"iPhone":"iPhone",
		"Android":"Android",
		"Saturn":"Saturn",
		"Lynx":"Lynx",
		"Dreamcast":"Dreamcast",
		"Dreamcast VMU":"DreamcastVMU",
		"NeoGeo Pocket Color":"NPC",
		"Game.Com":"Game.Com",
		"WonderSwan":"WonderSwan",
		"WonderSwan Color":"WonderSwanC",
		"Arcade":"Arcade",
		"Wireless":"Wireless",
	}.get(platform,"Other")

def get_genre(word1,word2):
	if word2 == "Y" or word2 == "N":
		return word1,False
	else:
		word1 = word1.lstrip('"')
		word2 = word2.rstrip('"')
		word3 = word1 + word2
		return word3,True

for line in sys.stdin:
	if linea == 0:
		re.sub( r'^\W+|\W+$', '' , ignorar)
		linea = linea + 1
	else:
		line = re.sub( r'^\W+|\W+$', '', line ) # parsear linea	
		words = line.split(',', 12) # se trocea la linea para obtener los datos
		if len(words) > 11 and words[4][0] == '/':
			result = parse(words[2], words[3])
			platform = translate_platform(words[5])
			grade = int(float(words[6])*10)
			genre,multi = get_genre(words[7],words[8])
			if multi is True:
				year = words[10]
				month = words[11]
			else:
				year = words[9]
				month = words[10]
		elif len(words) > 11 and words[5][0] == '/':
			result = parse2(words[2],words[3],words[4])
			platform = translate_platform(words[6])
			grade = int(float(words[7])*10)
			genre,multi = get_genre(words[7],words[8])
			if multi is True:
				year = words[11]
				month = words[12]
			else:
				year = words[10]
				month = words[11]
		else:
			result = words[2]
			platform = translate_platform(words[4])
			grade = int(float(words[5]) * 10)
			genre,multi = get_genre(words[6],words[7])
			if multi is True:
				year = words[9]
				month = words[10]
			else:
				year = words[8]
				month = words[9]
		print(result+ "," + platform + "," + str(grade) + "," + genre + "," + year + "," + month)