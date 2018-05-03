#Anthony Decker
#Creating a "Secure" Python number game
#Takes a username, checks password - allows play of game

#This is importing the required modules for the game
import random, logging, sys, optparse

#Setting up the debugging environment
fh = logging.FileHandler("debuggingLog.log")
sh = logging.StreamHandler()

fh.setLevel(logging.WARNING)
sh.setLevel(logging.DEBUG)

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

logger.addHandler(fh)
#logger.addHandler(sh) #Comment this one out

def main():
	"""Main method of the game, grabs information from
	   Command Line and sends them to check user"""

	#Grabbing options from the Command Line
	parser = optparse.OptionParser('use these two flags to login, if there is a space, \nsurround them in quotes i.e "Anthony Decker": -u' + ' <username> -p <password>')
	parser.add_option('-u', dest='usrInfo', type='string', help='specify the username')
	parser.add_option('-p', dest='usrPass', type='string', help='specify the password')

	(options, args) = parser.parse_args()

	#Assigning variables to the parsed options
	usrInfo = options.usrInfo
	usrPass = options.usrPass

	#If there is nothing, exit
	if ((usrInfo == None) | (usrPass == None)):
		print (parser.usage)
		exit(0)

	#Checking the user and pass against the file
	checkUser(usrInfo, usrPass)

def checkUser(username, password):
	"""This method will check the username and password against the file to
	   see if it's there, if so, accept and allow the game to be played"""
	#Creating booleans to check later in the method for correct credentials
	checkUserName = False
	checkPass = False

	#Opening the file, converting it to a list
	with open("user_list.txt") as checkFile:
		pFile = checkFile.read().strip().split('\n')
		#While statement variables
		a = True
		i = 3
		while a:
			try:
				logger.debug("Checking the passed username: %s" %username )
				logger.debug("Checking the passed password: %s" %password)
				#Checking if the username is in the list
				if (username in pFile):
					#Making sure that the username is only at an even index as all passwords are stored at odd indices
					if (pFile.index(username) % 2 == 0):
						logger.debug("Username has been found in list at index: " + str(pFile.index(username))) #This is to see what my method is doing
						checkUserName = True
						#Grabbing the index of the array and adding one to check password
						usernameIndex = pFile.index(username)
						usernameIndex += 1
						logger.debug("Index of the password: %s" %usernameIndex)

						#If it is there, check the next index for the password and if it's correct, break out of the loop
						if (password == pFile[usernameIndex]):
							checkPass = True
							a = False
						else:
						#If the password is not correct, it will move onto the tryAgain method and try there
							i -= 1
							print("You have netered an incorrect password, try again - Tries remaining: %s" %i)
							#If tryAgain passes True, it will break out of the loop and continue
							if (tryAgain(username, i, pFile, usernameIndex) == True):
								checkPass = True
								a = False
							#If there are too many incorrect passwords, it will kill the game
							else:
								print("Too many incorrect passwords, exiting game... ")
								quit()
					else:
						print("Hmm... There's something wrong with that Username, try a new one - we might as well try a new password too!")
						username = str(input("Enter a new username: "))
						password = str(input("Enter the password: "))
				#If the username is not defined, it will give the user the ability to create an account
				else:
					#Prompting the user for a choice of creating a user, trying again, or exiting the game
					usr_choice = str(input("Username not found in the system, would you like to create an account, or Try again? (create, again, no): "))
					logger.debug("User has chosen: %s" %usr_choice)
					try:
						while True:
							#If they'd like to make an account, moves to createUser()
							if(usr_choice.lower() == 'create'):
								createUser()
								break
							#If they'd like to try again, moves to tryUserAgain()
							elif(usr_choice.lower() == 'again'):
								logger.debug("Sending the file over to trying again %s " %pFile)
								tryUserAgain(pFile)
								break
							elif(usr_choice.lower() == 'no'):
								#Kills the game because they don't want to create a username
								print("Since you don't want to cooperate, I'm going to kick you out. BYE! ")
								quit()
								break
							else:
								print("I'm only going to accept create, again, or no, choose one of those!")
								usr_choice = str(input("Create, Again, No?: "))
								continue
					except Exception as e:
						print(e)
						break
			except Exception as e:
				print(e)
				break

	#If both things are true, play the game - sending username to play()
	if (checkUserName == True and checkPass == True):
		logger.debug("Sending the username back to the play method: %s" %username)
		play(username)

def tryUserAgain(pFile):
	while True:
		#Trying the user again
		username = str(input("Enter a username: "))
		logger.debug("Input username is: %s" %username)
		if (username in pFile):
			if (pFile.index(username) % 2 == 0):
				#Making sure the username is at the index of a username then asking for a password
				password = str(input("Enter the password: "))
				logger.debug("Input password is: %s" %password)
				break
			else:
				#If the username input is a password, it will not allow it to be used
				print("Hmm... There's something wrong with that string, lets try a new one.")
				continue
		else:
			#If the user wasn't found, it will ask to create one
			userChoice = str(input("Username not found in the file, would you like to create a User? (Yes or No)"))
			logger.debug("User has input: %s" %userChoice)
			#If the user would like to create a username, it will send them to createUser()
			if (userChoice.lower() == 'yes'):
				createUser()
				break
			#Quitting the game if the user doesn't want to make a username
			elif (userChoice.lower() == 'no'):
				print("Since you don't want to cooperate, I'm going to kick you out. BYE! ")
				quit()
				break
			else:
				print("Sorry, I'm picky. I'm only accepting Yes or No")
				continue
	checkUser(username, password)

def createUser():
	"""Allows the consumer to create a username and password to play the game"""
	c = True
	try:
		while c:
			with open("user_list.txt", "r+") as addFile:
				#Asking for the new username
				newUser = str(input("Please enter a new username, type quit if you don't want quit: "))
				if (newUser.lower() == 'quit'):
					print("\nI'm sad to see you go, but thanks for playing!")
					quit()
				print("Checking if you can use this username... ")
				pFile = addFile.read().strip().split('\n')
				logger.debug("Making sure we can read and check the list: %s" %pFile) #Debugging
				#Making sure the username is not whitespace
				if (not newUser.isspace() and newUser != ''):
					if (newUser not in pFile):
						#If the username is not in the file, go ahead and move onto the password
						logger.debug("Checking again... %s" %pFile) #Debugging
						print("Username accepted!")
						while True:
							#Asking the user for a new password
							newPass = str(input("Please enter a new password or type quit to quit: "))
							newPass = str(newPass.strip(''))
							if (newPass.lower() == 'quit'):
								print("\nI'm sad to see you go, but thanks for playing!")
								quit()
							#Asking for a verification of the password
							confirmPass = str(input("Please enter your password again to confirm: "))
							if (confirmPass == newPass):
								newPass = confirmPass.strip('')
								#Stripping and making sure that the password is NOT whitespace
								if (not newPass.isspace() and newPass != ''):
									#Making sure the password and username are NOT the same
									if (newPass != newUser):
										#Writing both the username and password
										logger.debug("User's new username: %s" %newUser)
										logger.debug("User's new password: %s" %newPass)
										addFile.write(newUser+'\n')
										addFile.write(newPass+'\n')
										c = False
										break
									else:
										print("Password cannot be the same as your user, try again!")
										continue
								else:
									print("Password cannot be whitespace, try again!")
									continue
							else:
								print("Passwords do not match, try again!")
								continue
					else:
						print("Username already in use, try again!")
				else:
					print("Username cannot be whitespace, try again!")

		checkUser(str(newUser), str(newPass))
	except Exception as e:
		print(e)

def tryAgain(username, i, pFile, usernameIndex):
	"""This is the method that allows the user to try entering a password
	   again, if it is incorrect too many times, it will kill the game"""
	logger.debug("Printing all passed variables: %s %s %s %s" % (username, str(i), pFile, str(usernameIndex)))
	try:
		#This loop will ONLY run while the user still has password attemps
		while (i != 0):
			logger.debug("Value of i: %d" %i)
			password = input("Please try the password again: ")
			#Trying the password again, if it's correct, it will go return true to the previous method and continue
			if (password == pFile[usernameIndex]):
				return True
			else:
				#Decrementing tries so that the user will be booted after too many attemps - states how many attemps are left
				i -= 1
				print("You have entered an incorrect password, try again - Tries remaining: %s" %i)
				logger.debug("Value of i after failure: %d" %i)
		return False
	except Exception as e:
		print(e)

def play(username):
	"""Play is the "main" function of the game,
	   it calls all other functinos"""
	try:
		print('Hello %s! Let\'s get started!' %username)
		bad_level = True
		#While loop to make sure the user chooses a correct level value
		while bad_level:
			try:
				usr_select = int(input('Choose a level from 0, 1, 2, or 3!\n(0=beginner, 1=easy, 2=medium, 3=hard)\n'))
				logger.debug("Checking user input: %d" %usr_select)
				#These if else statements are the levels, user chooses one of these levels and the random number is generated likewise
				if(usr_select == 0):
					rnum = random.randint(1,10)
					print("The random number is between 1 and 10\nUse an integer between 1 and 10")
					bad_level = False

				elif(usr_select == 1):
					rnum = random.randint(1,25)
					print("The random number is between 1 and 25\nUse an integer between 1 and 25")
					bad_level = False

				elif(usr_select == 2):
					rnum = random.randint(1,50)
					print("The random number is between 1 and 50\nUse an integer between 1 and 50")
					bad_level = False

				elif(usr_select == 3):
					rnum = random.randint(1,100)
					print("The random number is between 1 and 100\nUse an integer between 1 and 100")
					bad_level = False

				else:
					print("Bad level chosen")
					#bad_level = True
			except ValueError:
				print("Enter an integer, not a string")

		logger.debug("Checking the random function for random number: %s" %rnum)
		count = 100
		b = True
		while b:
			#This try except makes sure the user uses integers, not strings
			try:
				unum = int(input('GUESS? '))
				logger.debug("Making sure the number the user input was generated: %s" %unum)
				#My work of art right here -- Checks if the number was guess correctly and ends the current game if so
				if(num_check(unum, rnum) == True):
					logger.debug("User has guessed correctly")
					b = False
					print("Your score for the game is: " + str(count) +"/100")
					logger.debug("Going into the play_again() method")
					play_again(username)

				else:
					logger.debug("User has guessed incorrectly")
					#Protects the score variable -- Makes sure it doesn't drop below 0
					if(count > 0):
						count -= 7

					else:
						count = 0

			except ValueError:
				logger.warning("User has input an invalid argument, argument passed:")
				print("Use an integer, not a string. (i.e 1,8,5...)")
	except KeyboardInterrupt:
		logger.warning("User has used Control^c to end the game")
		print("\nI'm sad to see you go, but thanks for playing!")
		quit()

def num_check(usrNum, ranNum):
	"""This function checks the user's input against the
	   random number and returns either true or false"""
	try:
		logger.debug("Checking user number against random Number (User's: %s" %usrNum + ")")
		if (usrNum == ranNum):
			print("Correct! You guessed the right number!")
			logger.debug("Going back to (if(num_check(unum,rnum) == true)) ")
			return True

		elif (usrNum < ranNum):
			print("Wrong! You guessed too low! Try again!")
			logger.debug("Going back to (if(num_check(unum,rnum) == true))'s else statement ")
			return False

		else:
			print("Wrong! You guessed too high! Try again!")
			logger.debug("Going back to (if(num_check(unum,rnum) == true))'s else statement ")
			return False
	except KeyboardInterrupt:
		logger.warning("User has used Control^c to end the game")
		print("I'm sad to see you go, but thanks for playing!")

def play_again(username):
	"""This function asks if the user would like to play again and catches
	   bad input for the very specific requirements to leave the game."""
	try:
		logger.debug("Starting the play_again() method")
		print("Would you like to play again??")
		a = True
		while a:
			usr_input = input("Type 'yes' if you would like to play, 'quit' to end the game ")
			#Taking the user's input and choosing which method to go to
			if(usr_input.title() == 'Yes'):
				logger.debug("user would like to play again, going back to play(), argument passed: %s" %usr_input)
				a = False
				play(username)

			elif(usr_input.title() == 'Quit'):
				print('Goodybye! Thanks for playing!')
				logger.debug("user does not want to play again, argument passed: %s" %usr_input)
				quit()

			else:
				print("Invalid input, please use either 'yes' or 'quit'")
				logger.warning("User input an invalid argument: %s" %usr_input)
				a = True
	except KeyboardInterrupt:
		logger.warning("The user has used Control^c")
		print("\nGoodybye! Thanks for playing!")

try:
	if __name__ == "__main__":
		"""Starting the main method..."""
		main()
except KeyboardInterrupt:
	logger.warning("User has used Control^c to end the game")
	print("\nI'm sad to see you go, but thanks for playing!")
