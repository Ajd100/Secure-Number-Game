#This is importing the rand module
import random
import logging

#Setting up the debugging environment
fh = logging.FileHandler("debuggingLog.log")
sh = logging.StreamHandler()

fh.setLevel(logging.WARNING)
sh.setLevel(logging.DEBUG)


logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

logger.addHandler(fh)
logger.addHandler(sh) #Comment this one out


#Play is the "main" function of the game, it calls all other functinos
def play():
	try:
		print('Hello friend! Let\'s get started! \nAll you have to do is guess a number!')
		rnum = random.randint(1,25)
		logger.debug("Checking the random function for random number: %s" %rnum)
		print("The random number is between 1 and 25")
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
					play_again()
					
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
	
#This function checks the user's input against the random number and returns either true or false
def num_check(usrNum, ranNum):
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

#This function asks if the user would like to play again and catches bad input for the very specific requirements to leave the game.
def play_again():
	try:
		logger.debug("Starting the play_again() method")
		print("Would you like to play again??")
		a = True
		while a:
			usr_input = input("Type 'yes' if you would like to play, 'quit' to end the game ")
			if(usr_input.title() == 'Yes'):
				logger.debug("user would like to play again, going back to play(), argument passed: %s" %usr_input)
				a = False
				play()
				
				
			elif(usr_input.title() == 'Quit'):
				print('\nGoodybye! Thanks for playing!')
				logger.debug("user does not want to play again, argument passed: %s" %usr_input)
				break
				
			else:
				print("Invalid input, please use either 'yes' or 'quit'")
				logger.warning("User input an invalid argument: %s" %usr_input)
				a = True
	except KeyboardInterrupt:
		logger.warning("The user has used Control^c")
		print("\nGoodybye! Thanks for playing!")		
play()
