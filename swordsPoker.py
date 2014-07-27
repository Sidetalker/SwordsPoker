import console, sys

weaponData = 'weapons.txt'
shieldData = 'shields.txt'
saveData = 'save.txt'

# ANSI options for multiplatform colored terminal text
class TerminalColor:
    PINK = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    NONE = ''
    END = '\033[0m'

# Suit comparisons
class Suit:
	HEART = 0
	DIAMOND = 1
	SPADE = 2
	CLUB = 3

	def sameColor(self, suitA, suitB):
		if ((suitA == HEART) and (suitB == HEART)) or ((suitA == HEART) and (suitB == DIAMOND)) or ((suitA == DIAMON) and (suitB == HEART)) or ((suitA == DIAMOND) and (suitB == DIAMOND)):
			return True

		return False

	def getSymbol(self, entry):
		if entry == self.HEART:
			return getColor(u'\u2665'.encode('utf-8'), TerminalColor.RED)
		elif entry == self.DIAMOND:
			return getColor(u'\u2666'.encode('utf-8'), TerminalColor.RED)
		elif entry == self.SPADE:
			return u'\u2660'.encode('utf-8')
		elif entry == self.CLUB:
			return u'\u2663'
		elif entry == -1:
			return ''
		else:
			return '?'

# Non-number ranks
class Rank:
	ACE = 1
	JACK = 11
	QUEEN = 12
	KING = 13
	JOKER = 14

# Describes poker hands 
class Hand:
	ONEPAIR = 0
	TWOPAIR = 1
	THREEPAIR = 2
	STRAIGHT = 3
	FLUSH = 4
	FULLHOUSE = 5
	FOURPAIR = 6
	STRAIGHTFLUSH = 7
	ROYALFLUSH = 8
	FIVEPAIR = 9

	def getString(self, value):
		if value == 0:
			return 'One Pair'
		elif value == 1:
			return 'Two Pair'
		elif value == 2:
			return 'Three of a Kind'
		elif value == 3:
			return 'Straight'
		elif value == 4:
			return 'Flush'
		elif value == 5:
			return 'Full House'
		elif value == 6:
			return 'Four of a Kind'
		elif value == 7:
			return 'Straight Flush'
		elif value == 8:
			return 'Royal Flush'
		elif value == 9:
			return 'Five of a Kind'

	def getStringDescription(self, value):
		if value == 0:
			return 'Any two cards of the same rank.'
		elif value == 1:
			return 'Any two cards of the same rank together with another two cards of the same rank.'
		elif value == 2:
			return 'Any three cards of the same rank.'
		elif value == 3:
			return 'Any five consecutive cards of different suits. Aces can count as either a high or a low card.'
		elif value == 4:
			return 'Any five cards of the same suit (not consecutive).'
		elif value == 5:
			return 'Any three cards of the same rank together with any two cards of the same rank'
		elif value == 6:
			return 'Any four cards of the same rank'
		elif value == 7:
			return 'Any straight with all five cards of the same suit.'
		elif value == 8:
			return 'A straight from a ten to an ace with all five cards of the same suit.'
		elif value == 9:
			return 'Any five cards of the same rank'

# Describes weapon effects 
class WeaponEffect:
	ABSORB = 0
	BLEED = 1
	BURN = 2
	DISCARD = 3
	FORGET = 4
	PARALYSIS = 5
	PENETRATE = 6
	POISON = 7
	SILENCE = 8
	STEAL = 9

	def getString(self, value):
		if value == 0:
			return 'Absorb'
		elif value == 1:
			return 'Bleed'
		elif value == 2:
			return 'Burn'
		elif value == 3:
			return 'Discard'
		elif value == 4:
			return 'Forget'
		elif value == 5:
			return 'Paralysis'
		elif value == 6:
			return 'Penetrate'
		elif value == 7:
			return 'Poison'
		elif value == 8:
			return 'Silence'
		elif value == 9:
			return 'Steal'

	def getStringDescription(self, value):
		if value == 0:
			return 'Absorb: Heal yourself based off a %% of your hand DMG.'
		elif value == 1:
			return 'Bleed: Enemies take bonus DMG each of your turns this round.'
		elif value == 2:
			return 'Burn: Boosts hand DMG; DMG enemy each of their turns this round.'
		elif value == 3:
			return 'Discard: A random card in the enemy''s hand will be discarded.'
		elif value == 4:
			return 'Forget: Disable all enemy weapon effects on their next turn.'
		elif value == 5:
			return 'Paralysis: Paralyzes enemy; preventing them from taking their next turn.'
		elif value == 6:
			return 'Penetrate: Bypass the enemy shield and directly DMG them.'
		elif value == 7:
			return 'Poison: Enemy suffers DMG at the end of the round.'
		elif value == 8:
			return 'Silence: Enemy cannot cast magic till the end of round.'
		elif value == 9:
			return 'Steal: Take a random card from the enemy''s hand at the end of the turn.'

# Stores all information for a single playing card
class Card:
	def __init__(self):
		self.suit = -1
		self.color = -1
		self.rank = -1

# Stores all information for a hand of cards
class Hand:
	def __init__(self):
		self.cards = [Card() for x in range(4)];

# Stores a board state
class Board:
	def __init__(self, ranks, suits):
		self.ranks = ranks
		self.suits = suits

	def printBoard(self):
		padding = [0 for i in range(5)]

		print 'Board:'

		for i in range(5):
			for x in range(5):
				curRank = self.ranks[i][x]
				
				if curRank == 11:
					curRank = 'J'
				elif curRank == 12:
					curRank = 'Q'
				elif curRank == 13:
					curRank = 'K'
				elif curRank == 1:
					curRank = 'A'
				elif curRank == -1:
					curRank = ' '

				if self.ranks[i][x] == 10 or sum(padding[i:]) == 0:
					sys.stdout.write(Suit().getSymbol(self.suits[i][x]))
					sys.stdout.write(str(curRank) + ' ' + sum(padding[i:]) * ' ')
				else:
					sys.stdout.write(Suit().getSymbol(self.suits[i][x]))
					sys.stdout.write(str(curRank) + '  ' + sum(padding[i:]) * ' ')

			sys.stdout.flush()
			print

	def getBoardRaw(self):
		returnString = ''

		for i in range(5):
			for x in range(5):
				returnString += str(self.ranks[i][x]) + ' '
				returnString += str(self.suits[i][x]) + ' '
			returnString += '\n'

		return returnString

# Stores all information for a single weapon
class Weapon:
	def __init__(self, weaponName):
		self.name = weaponName
		self.attacks = []
		self.effects = []

	def addAttacks(self, attackString):
		self.attacks = [int(i) for i in attackString.split()]

	def addEffects(self, effectString):
		self.effects = [int(i) for i in effectString.split()]

	def getDetails(self):
		print TerminalColor.BLUE + name +TerminalColor.END
		
		for i in range(10):
			if i == 0:
				tempString = str(attacks[i])

				if effects[i] != -1:
					tempString += ' (' + WeaponEffect.getString(self.effects[i])

# Stores all information for a single shield
class Shield:
	def __init__(self, shieldName):
		self.name = shieldName
		self.defense = -1
		self.resistance = -1

	def getDetails(self):
		print TerminalColor.BLUE + name +TerminalColor.END
		
		for i in range(10):
			if i == 0:
				tempString = str(attacks[i])

				if effects[i] != -1:
					tempString += ' (' + WeaponEffect.getString(self.effects[i])

# Stores all information about the current player
class Player:
	def __init__(self):
		self.availableWeapons = []
		self.availableShields = []
		self.currentShield = -1
		self.currentWeapon = -1
		self.health = -1
		self.monsterHealth = -1
		self.healthRefills = -1
		self.board = -1

	def printBoard(self):
		self.board.printBoard()

	def getBoardRaw(self):
		return self.board.getBoardRaw()

	def printStats(self):
		print getColor('Your Health:\t', TerminalColor.NONE) + str(self.health)
		print getColor('Health Refills:\t', TerminalColor.NONE) + str(self.healthRefills)
		print getColor('Monster Health:\t', TerminalColor.NONE) + str(self.monsterHealth)
		print 'Current Weapon:\t' + self.availableWeapons[self.currentWeapon].name
		print 'Current Shield:\t' + self.availableShields[self.currentShield].name + '\n'

		self.printBoard()

# Returns a string centered for the console
def centerString(text, color = TerminalColor.NONE):
	centeredString = color + text + TerminalColor.END
	(termWidth, termHeight) = console.getTerminalSize()

	return centeredString.center(termWidth)

def getColor(text, color):
	return color + text + TerminalColor.END

# Parse the weapon data file
def parseWeapons():
	weaponArray = []
	tempWeapon = Weapon('init')
	parseFlag = 0

	# Build the Weapon object and add it to the array
	with open(weaponData, 'r') as data:
		for line in data:
			if line.strip():
				if parseFlag == 0:
					tempWeapon = Weapon(line.strip())
					parseFlag += 1
				elif parseFlag == 1:
					tempWeapon.addAttacks(line.strip())
					parseFlag += 1
				elif parseFlag == 2:
					tempWeapon.addEffects(line.strip())
					weaponArray.append(tempWeapon)
					parseFlag = 0

	return weaponArray

def parseShields():
	shieldArray = []

	tempShield = Shield('None')
	tempShield.defense = 0
	tempShield.resistance = -1

	shieldArray.append(tempShield)

	parseFlag = 0

	# Build each Shield object and add it to the array
	with open(shieldData, 'r') as data:
		for line in data:
			if line.strip():
				if parseFlag == 0:
					tempShield = Shield(line.strip())
					parseFlag += 1
				elif parseFlag == 1:
					info = line.strip().split()
					tempShield.defense = int(info[0])
					tempShield.resistance = int(info[1])
					shieldArray.append(tempShield)
					parseFlag = 0

	return shieldArray

# Parse the weapon data file
def parseSave():
	saveArray = []
	ranks = []
	suits = []
	tempPlayer = Player()
	parseFlag = 0

	# Break the save file into a list of integers
	with open(saveData, 'r') as data:
		for line in data:
			if line.strip():
					saveArray.append([int(i) for i in line.strip().split()])

	# Apply player attributes
	for i in range(len(saveArray)):
		curRanks = []
		curSuits = []

		for x in range(len(saveArray[i])):
			if i == 0:
				if saveArray[0][x] == -1:
					return Player()

				if x == 0:
					tempPlayer.currentWeapon = saveArray[0][x]
				elif x == 1:
					tempPlayer.health = saveArray[0][x]
				elif x == 2:
					tempPlayer.healthRefills = saveArray[0][x]
				elif x == 3:
					tempPlayer.monsterHealth = saveArray[0][x]
				elif x == 4:
					tempPlayer.currentShield = saveArray[0][x]
			else:
				if (x % 2) == 0:
					curRanks.append(saveArray[i][x])
				else:
					curSuits.append(saveArray[i][x])

		if i > 0:
			ranks.append(curRanks)
			suits.append(curSuits)

	tempPlayer.board = Board(ranks, suits)

	return tempPlayer

# Parse any escape sequences initiated by the user
def parseEscape(entry):
	if entry[1:5] == 'help':
		helpSplit = entry.split()

		if len(helpSplit) == 1:
			print escapeStrings()
			return

		if helpSplit[1] == 'handHelp':
			print 'yay'
			return 

# Returns string of all possible escape sequences
def escapeStrings():
	returnString = 'Here are all the available escape sequences:\n'
	returnString += '/help [handHelp, handPeek]'

	return returnString

# Save to file
# TODO Error handling
def save(gameMaster):
	f = open(saveData,'w')
	f.write(str(gameMaster.currentWeapon) + ' ' + str(gameMaster.health) + ' ' + str(gameMaster.healthRefills) + ' ' + str(gameMaster.monsterHealth) + ' ' + str(gameMaster.currentShield) + '\n')
	f.write(gameMaster.getBoardRaw())
	f.close()

	print getColor('\nSaved Successfully!', TerminalColor.GREEN)

# Get game info
def getInfo(gameMaster):
	print 'Go ahead and select your current weapon from the list below:'

	for i in range(len(gameMaster.availableWeapons)):
		print '(' + str(i) + ') ' + gameMaster.availableWeapons[i].name 

	gameMaster.currentWeapon = int(raw_input('Selection: '))
	gameMaster.health = int(raw_input('How much health do you have: '))
	gameMaster.healthRefills = int(raw_input('How many health refills do you have: '))
	gameMaster.monsterHealth = int(raw_input('How much health does the monster have: '))

	rankArray = []
	suitArray = []
	i = 0

	print 'Enter card values seperated by spaces for each line (use J,Q,K,A,-):'

	while i < 5:
		tempInput = raw_input('Line ' + str(i) + ': ')

		if tempInput[:1] == '/':
			parseEscape(tempInput)
		else:
			inputArray = tempInput.strip().split()
			lineArray = []

			for value in inputArray:
				if value == 'J':
					lineArray.append(Rank.JACK)
				elif value == 'Q':
					lineArray.append(Rank.QUEEN)
				elif value == 'K':
					lineArray.append(Rank.KING)
				elif value == 'A':
					lineArray.append(Rank.ACE)
				elif value == '-':
					lineArray.append(-1)
				else:
					lineArray.append(int(value))
			rankArray.append(lineArray)
			i += 1

	i = 0
	print 'Enter card suits seperated by spaces for each line (use H,D,S,C,-):'

	while i < 5:
		tempInput = raw_input('Line ' + str(i) + ': ')

		if tempInput[:1] == '/':
			parseEscape(tempInput)
		else:
			inputArray = [x for x in tempInput.strip().split()]
			lineArray = []

			for value in inputArray:
				if value == 'H':
					lineArray.append(Suit.HEART)
				elif value == 'D':
					lineArray.append(Suit.DIAMOND)
				elif value == 'C':
					lineArray.append(Suit.CLUB)
				elif value == 'S':
					lineArray.append(Suit.SPADE)
				elif value == '-':
					lineArray.append(-1)
				else:
					lineArray.append('?')

			suitArray.append(lineArray)
			i += 1

	gameMaster.board = Board(rankArray, suitArray)

	return gameMaster


# Main function
if __name__ == '__main__':
	# Obtain weapons from text file
	gameMaster = parseSave()
	gameMaster.availableWeapons = parseWeapons()
	gameMaster.availableShields = parseShields()

	# Print a happy little welcome message
	print centerString('Welcome to the Swords Poker Helper!', TerminalColor.BLUE)

	# If we didn't find any save data...
	if gameMaster.currentWeapon == -1:
		# Print greeting for starting a fresh game w/o save data
		print centerString('No Save Data Found\n', TerminalColor.RED)
		print 'Let''s get started... you can type /? at any prompt for a list of commands'
		print 'You can also type /s at any time to save your game'

		# Prompt user for all information
		gameMaster = getInfo(gameMaster)

		# Print the current game information
		print getColor('Game Statistics', TerminalColor.BLUE)
		gameMaster.printStats()

		# Print save the game
		save(gameMaster)

	else:
		print centerString('Save Data Loaded\n', TerminalColor.GREEN)

		# Print the current game information
		print getColor('Game Statistics', TerminalColor.BLUE)
		gameMaster.printStats()
		# print '- Q K 10 -'
		# print '- D D S -'















