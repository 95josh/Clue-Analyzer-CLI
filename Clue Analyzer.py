from clue import CluePlayer, Rooms, People, Weapons
import json

global dataFile

def main():
    global players, dataFile, inGame, guesses, roomnames, peoplenames, weaponnames
    players = []
    inGame = False
    dataFile = "" #set datafile to nothing
    guesses = []
    startup()
    roomnames = ["Ball Room", "Billiard Room", "Conservatory", \
                           "Dining Room", "Hall", "Kitchen", "Lounge", \
                           "Library", "Study"]
    peoplenames = ["Mrs. White", "Mrs. Peacock", "Professor Plum", \
                             "Colonel Mustard", "Miss Scarlett", "Reverend Green"]

    weaponnames = ["Knife", "Revolver", "Rope", "Wrench",\
                              "Candlestick", "Lead Pipe"]
    
    #The main menu has the user choose to continue a previous game or start a
    #new one.
    option = "temp" 
    while option != "X":
        #get user input
        option = input("\nEnter N to start a New " + \
                       "game, L to Load an old game and X to quit: ").upper()
        if option == "N":
            #initialize new game
            newGame()
            gameLoop()
        elif option == "L":
            #load old game and start it up.
            #get data file:
            dataFile = input("Enter the name/location of the game save file: ")
            readData()
            gameLoop()
        elif option == "X":
            #exit program
            print("\nThanks for using Clue Analyzer! Come back soon.")
        else:
            #user entered something invalid.
            print("Not a valid option. Please try again.")
                 
def gameLoop():
    global players, dataFile
    option = "temp" #set option to anything but N, as that quits the program.
    gameloopMenu()
    while option != "X":
        option = input("\nEnter your menu option. (? to display menu): ").upper()
        if option == "A":
            displayPlayers()
        elif option == "B":
            #add/remove players' items
            updatePlayerItems()
        elif option == "C":
            #Display user data
            userData()
        elif option == "D":
            #add new guess
            addGuess()
        elif option == "?":
            #display game menu
            gameloopMenu()
        elif option == "X":
            print("Exiting & saving game.")
            dataFile = "" #reset the data file location
            #empty current lists, so we don't get double data when we load a game.
            players = []
            guesses = []
        else:
            print("Invalid option. Please try again.")

def readData():
    global dataFile, players, guesses

    try:
        #read in json data
        with open(dataFile,encoding="utf8") as json_in:
            results = json.load(json_in)
        guesses = results['guesses']
        #load each players's data:
        for player in results['players']:
            #add the player + data to players list.
            players.append(CluePlayer(str(player['name']), list(player['rooms']), list(player['people']), list(player['weapons'])))
            
    except Exception as e:
        print("Error loading data.")
        print(e)
            

def saveData():
    global dataFile, players, guesses
    try:
        
        playeroutput = []
        guessesoutput = []
        #get player data
        for player in players:
            playeroutput.append(player.getEverything())
        #get guess data
        for guess in guesses:
            guessesoutput.append(guess)
        
        data = {'players':playeroutput, 'guesses':guessesoutput}

        with open(dataFile, 'w') as json_output:
            json.dump(data, json_output, ensure_ascii=True, indent=4) # encode data into json

        print("Game saved")
    except Exception as e:
        print("Unable to save data. ")
        print(e)

def gameloopMenu():
    print("\n--- GAME MENU ---")
    print("  A - LIST CURRENT PLAYERS")
    print("  B - ADD/REMOVE PLAYERS' ITEMS")
    print("  C - DISPLAY DATA FOR A USER")
    print("  D - ADD NEW GUESS")
    print("  ? - DISPLAY THIS MENU")
    print("  X - SAVE AND EXIT THIS GAME")

def startup():
    print("CLUE ANALYZER")
    print("\nThis program was made by JOSHUA STAHL for CIS156 at SMCC.")
    #make purpose statement here
    print("\nHello Clue player! Welcome to Clue Analyzer.")

def newGame():
    global dataFile, players

    #if no dataFile on record, get it
    if dataFile == "" or dataFile == None:
        #ask user for data file
        dataFile = input("\nEnter the location and name of the save file for the new game: ")

    #get information about players:
    numplayers = int(input("\nHow many players are playing? (maNimum of 6 and minimum of 2): "))
    while numplayers > 6 or numplayers < 2:
        numplayers = int(input("Invalid input. Enter the number of players (maNimum of 6 and minimum of 2): "))
                       
    print("\nENTER INFORMATION ABOUT THE PLAYERS")
    #enter information about self:
    name = input("Enter your name: ")

    #create new clueplayer (for user of program)
    newplayer = CluePlayer(name)

    #start storing card data (by default player doesn't have anything (an N)):
    rooms = ["N", "N", "N", "N", "N", "N", "N", "N", "N"]
    people = ["N", "N", "N", "N", "N", "N"]
    weapons = ["N", "N", "N", "N", "N", "N"]
    
    print("Now input your cards")
    category = "temp" # "N" makes the program not enter any more cards
    while category != "N":
        print("\nCARD CATEGORIES:")
        print("  0 - Rooms")
        print("  1 - People")
        print("  2 - Weapons")
        category = int(input("Enter the card category (99 to end): "))
        if category == 0:
            print("\nROOM CARDS:")
            roomnames = newplayer.getRoomNames()
            idx = 0
            for name in roomnames:
                print(str(idx) + " - " + name)
                idx += 1
            item = int(input("Select the card you have: "))
            while item < 0 or item > 8:
                item = int(input("Select the card you have: "))
            rooms[item] = "Y"
        elif category == 1:
            print("\nPEOPLE CARDS:")
            roomnames = newplayer.getPeopleNames()
            idx = 0
            for name in roomnames:
                print(str(idx) + " - " + name)
                idx += 1
            item = int(input("Select the card you have: "))
            while item < 0 or item > 6:
                item = int(input("Select the card you have: "))
            people[item] = "Y"
        elif category == 2:
            print("\nWEAPONS CARDS:")
            roomnames = newplayer.getWeaponNames()
            idx = 0
            for name in roomnames:
                print(str(idx) + " - " + name)
                idx += 1
            item = int(input("Select the card you have: "))
            while item < 0 or item > 6:
                item = int(input("Select the card you have: "))
            weapons[item] = "Y" 
        elif category == 99: #exit signal
            #set category to N so loop will end.
            category = "N"
            #save playerdata and save player to list of players
            newplayer.setBulkRooms(rooms)
            newplayer.setBulkPeople(people)
            newplayer.setBulkWeapons(weapons)
            players.append(newplayer)
            saveData() #save data
        else:
            print("Invalid category. Please try again.")


    #add the remaining players to the players list
    print("\nADD THE OTHER PLAYERS. ENTER THEM IN CLOCKWISE DIRECTION ONLY")
    for i in range(0, numplayers - 1):
        othername = input("Enter the name of Player {0}: ".format(i + 2))
        players.append(CluePlayer(othername))
        saveData() #save player data

def displayPlayers():
    print("\nCURRENT PLAYERS:")
    idx = 0 #current index
    for player in players:
        print(str(idx) + " - " + player.getName())
        idx += 1

def updatePlayerItems():
    global players, roomnames, peoplenames, weaponnames

    changes = False #keeps track if changes were made.
    
    #get the player you want to edit:
    displayPlayers()
    selectedp = input("\nWhich player's items do you want to edit? (blank to cancel): ")
    while selectedp != "":
        selectedp = int(selectedp) #try to convert to int
        #while the selected player is invalid:
        while selectedp < 0 or selectedp > (len(players) -1 ):
            selectedp = int(input("Invalid player index. Which player's items do you want to edit?: "))
        else:
            print("Editing {0}'s cards...".format(players[selectedp].getName()))
        print("\nCARD CATEGORIES:")
        print("  0 - Rooms")
        print("  1 - People")
        print("  2 - Weapons")
        category = int(input("Select the category in which you want to make the change (99 to exit): "))
        if category == 0:
            print("\n{0}'s ROOM CARDS:".format(players[selectedp].getName()))
            playerrooms = players[selectedp].getRooms()
            idx = 0
            #display rooms
            for name in roomnames:
                print(str(idx) + " - " + name + "(" + playerrooms[idx] + ")")
                idx += 1
            #get which card to change
            item = int(input("Select the card you want to change: "))
            while item < 0 or item > 8:
                item = int(input("Select the card you want to change: "))

            #what to change it to?
            changeto = input("What is the change? (Y = YES, N = NO, '-' = Don't know): ").upper()
            while changeto != "N" and changeto != "Y" and changeto != "-":
                changeto = input("Invalid input. What is the change? (Y = YES, N = NO, '-' = Don't know): ").upper()
            players[selectedp].setRoom(item, changeto) #change the value of the room for the player.
            changes = True #a change was made
            saveData()
        elif category == 1:
            print("\n{0}'s PEOPLE CARDS:".format(players[selectedp].getName())) 
            #display people
            playerpeople = players[selectedp].getPeople()
            idx = 0
            for name in peoplenames:
                print(str(idx) + " - " + name + "(" + playerpeople[idx] + ")")
                idx += 1
            #get which card to change
            item = int(input("Select the card you want to change: "))
            while item < 0 or item > 6:
                item = int(input("Select the card you want to change: "))
            #what to change it to?
            changeto = input("What is the change? (Y = YES, N = NO, '-' = Don't know): ").upper()
            while changeto != "N" and changeto != "Y" and changeto != "-":
                changeto = input("Invalid input. What is the change? (Y = YES, N = NO, '-' = Don't know): ").upper()
            players[selectedp].setPeople(item, changeto) #change the value of the room for the player.
            changes = True #a change was made
            saveData()
        elif category == 2:
            print("\n{0}'s WEAPON CARDS:".format(players[selectedp].getName()))
            playerweapons = players[selectedp].getWeapons()
            idx = 0
            #display weapons
            for name in weaponnames:
                print(str(idx) + " - " + name + "(" + playerweapons[idx] + ")")
                idx += 1
            #get which card to change
            item = int(input("Select the card you want to change: "))
            while item < 0 or item > 6:
                item = int(input("Select the card you want to change: "))

            #what to change it to?
            changeto = input("What is the change? (Y = YES, N = NO, '-' = Don't know): ").upper()
            while changeto != "N" and changeto != "Y" and changeto != "-":
                changeto = input("Invalid input. What is the change? (Y = YES, N = NO, '-' = Don't know): ").upper()
            players[selectedp].setWeapons(item, changeto) #change the value of the room for the player.
            changes = True #a change was made
            saveData()
        elif category == 99: #exit code
            selectedp = "" #ends the while loop
            saveData()
        else:
            print("Invalid category choice. No changes made.")
    else:
        if selectedp == "" and changes == False: #if the user decided to quit at the beginning.
            print("No changes made")
        elif changes == False and selectedp != "": #if the user decided to put in a bad user id.
            print("Invalid user id. No changes made.")

def userData():
    displayPlayers()
    selectedp = input("\nWhich player's information do you want to display? (blank to cancel): ")
    if selectedp != "":
        selectedp = int(selectedp)
        if selectedp > -1 and selectedp < (len(players)):
            #convert selected player to integer 
            print(players[int(selectedp)])
        else:
            print("Invalid player id number.")
            userData()

def displayRooms():
    idx = 0
    for name in roomnames:
        print(str(idx) + " - " + name)
        idx += 1

def displayPeople():
    idx = 0
    #display people
    for name in peoplenames:
        print(str(idx) + " - " + name)
        idx += 1

def displayWeapons():
    idx = 0
    #display people
    for name in weaponnames:
        print(str(idx) + " - " + name)
        idx += 1
  
def addGuess():
    #get who's guess:
    displayPlayers()
    guesser = input("Who is doing the guessing? (blank to exit): ")
    if guesser == "":
        print("No guess added")
    else:
        guesser = int(guesser)
        #print the room names
        print("ROOM NAMES: \n")
        displayRooms()
        #get room id
        roomid = int(input("Which room was guessed?: "))
        room = Rooms(roomid)

        #print the people names
        print("PEOPLE NAMES: \n")
        displayPeople()
        #get people id
        personid = int(input("Which person was guessed? :"))
        person = People(personid)

        #print the weapon names
        print("WEAPON NAMES: \n")
        displayWeapons()
        #get weapon id
        weaponid = int(input("Which weapon was guessed? :"))
        weapon = People(weaponid)

        #get who showed or didn't show a card
        print("CURRENT PLAYERS: \n")
        displayPlayers()
        print("{0} - No-one".format(len(players)))
        playershowed = int(input("Who showed a card?: "))
        while (playershowed < 0 or playershowed > (len(players) -1 )) and playershowed != len(players):
            playershowed = int(input("Who showed a card?: "))

        
        

        
                     

main()

