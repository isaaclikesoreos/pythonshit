import sys
import numpy as np
from time import sleep
import copy as copy
MIN_PLAYERS = 2
MAX_PLAYERS = 8
DICE_VAL_MIN = 1
DICE_VAL_MAX = 7
NUM_OF_DICE = 5
starting_players = 0 #keeps track of how many people are playing
positions = ["first", "second", "third", "fourth", "fifth", "sixth", "seventh", "eighth"] #list of positions
#TODO fix player array
player = ["", "", "", "", "", "", "", ""] #prebuilt list for player names

rolls = 0 #tracks how many times dice have been rolled
player_rolls = np.zeros((8, 5)) # an empty matrix to be filled with values from player rolls
#TODO is y being used?
y = 0
liar = False
turn_tracker = 1 # used to kept track of whos turn it is
#TODO rename
counter_2 = 1 # used to make sure proper values are compared when betting
#TODO rebuild as custom object
bets = np.array([[0], [0]]) # keeps track of current bets

print("Hello, would you like to play a game? (y/n)") #intro
a = input()
if a == "y":
    print("How many players? (number of players must be more than 1 but no more than 8)")
elif a == "n":
    print("terminated")
    sys.exit()
else:
    print("Try again next time")
    sys.exit()

number_of_players = int(input())

if number_of_players > MIN_PLAYERS <= MAX_PLAYERS: # player count
    while starting_players < number_of_players:
        print("enter the name of the " + positions[starting_players] + " player:")
        player[starting_players] = input()
        starting_players = starting_players + 1
elif number_of_players > MAX_PLAYERS:
    print("Number of players is too great")
elif number_of_players < MIN_PLAYERS:
    print("Number of players is too few")
else:
    print("please enter a value between " + str(MIN_PLAYERS) +" and " + str(MAX_PLAYERS))

print("Welcome to Liar's Dice")
sleep(2)
print("Do you know the rules? (yes/no)")
knowledge = input()

if knowledge == "yes": # show dem the rules
    print("Alright y'all are ready to roll")
elif knowledge == "no":
    print("Alright here's some knowledge")
    print("Enter this link into browser \n https://images.restorationhardware.com/content/catalog/product/pdfs/prod13240107_info.pdf \n No numbers are wild in this game")
    sleep(2)
    print("Are you ready now? (y/n)")
    ready = input()
    if ready == "y":
        print("Alright now y'all are ready to roll")
    else:
        print("well that's too bad cause we are starting")
        sleep(3)
else:
    print("Please enter in the (yes/no) format")
    knowledge = input()

while rolls < number_of_players: #rolling the dice for each player and adding to player_rolls matrix
    print("Everyone but " + player[rolls] + " close your eyes")
    print("You may want to write this down")
    sleep(2)
    player_rolls[rolls] = np.random.randint(DICE_VAL_MIN, DICE_VAL_MAX, NUM_OF_DICE)
    print(player[rolls] + " your roll is " + str(player_rolls[rolls]))
    print("\n \n \n \n \n \n")
    sleep(2)
    rolls = rolls + 1

while not liar:
    if turn_tracker == number_of_players + 1: #resets this counter after each play has had their turn, starting again with the first
        turn_tracker = 1
    try:
        print(player[turn_tracker - 1] + " make your bet")  #collectig the initial bet from the player and storing the values
        print(bets)
        print("Dice Value")
        bet_value = int(input())
        print("Number of said dice")
        bet_number = input()
        bet_number = int(bet_number)
        bets = np.append(bets, np.array([[bet_value], [bet_number]]), axis=1)
        print(bets)
        print(bets[[0], [turn_tracker - 1]])
        print(bets[[0], [counter_2]])
        print(bets[[1], [turn_tracker - 1]])
        print(bets[[1], [counter_2]])
        print(turn_tracker)
        print(counter_2)
        x = bets[[0], [turn_tracker + counter_2 - 1]] >= bets[[0], [counter_2]] and bets[[1], [turn_tracker + counter_2 - 1]] <= bets[[1], [counter_2]]
        print(x)
        if bets[[0], [turn_tracker - 1]] >= bets[[0], [counter_2]] and bets[[1], [turn_tracker - 1]] >= bets[[1], [counter_2]]: #this will compare the bet to the last bet to make
            raise ValueError                                                                                            #it follows the rules and is legal bet, if not the player
    except ValueError:                                                                                                  # must bet again
        counter_2 = counter_2 + 1
        print("Your bet number or bet value must be greater than the last players bet")
        continue
    else:
        turn_tracker = turn_tracker + 1 #if the bet is legal, it is advanced to the next player's turn, where they must chose either bet or liar
        print(player[turn_tracker - 1] + " it's your turn, would you like to bet or call player one a liar? format(bet/liar)")
        decesion = input()
        if decesion == "liar": #if choice is liar a matrix is create
            guess_key = np.full((8, 5), bet_value) #if choice is liar a matrix is created that is the same size as the one that holds all the players rolls, and filled with the
            true_number = np.sum(guess_key == player_rolls) # dice value that was bet, this matrix is then compared with player rolls matrix to count how many of said dice were
            if true_number < bet_number: #rolled, then if that number is greater than the number bet, the last to bet was a liar
                print("The number of " + str(bet_value) + "'s rolled was " + str(true_number))
                print(player[turn_tracker - 2] + " you are a dirty liar")
                sys.exit()
            else:
                print("The number of " + str(bet_value) + "'s rolled was " + str(true_number)) #if not, then that player was telling the truth.
                print(turn_tracker)
                print(player[turn_tracker - 1] + " watch your mouth when speaking to a honest man")
                sys.exit()
        elif decesion == "bet": #if they choose to bet they should be kicked to the top of the while loop starting over with the player that just choose to bet placing their bet
            continue

        else:
            print("please enter 'bet' or 'liar'")
            continue





