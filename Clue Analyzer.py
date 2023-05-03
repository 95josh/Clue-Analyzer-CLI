from clue import CluePlayer
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
            result = readData()
            if result == True: #only if loading data was successful do we play the game
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
            #add new guess
            addGuess()
        elif option == "C":
            #Display user data
            userData()
        elif option == "D":
            #display all users data
            displayAllUsersData()
        elif option == "E":
            #display guesses
            displayGuesses()
        elif option == "F":
            #add/remove players' items
            updatePlayerItems()
        elif option == "G":
            #advanced Analysis
            advancedAnalysis()
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
        
        #load each players's data:
        for player in results['players']:
            #add the player + data to players list.
            players.append(CluePlayer(str(player['name']), list(player['rooms']), list(player['people']), list(player['weapons'])))

        #load the guesses
        for guess in results['guesses']:
            guesses.append(guess)

        advancedAnalysis()
        
        return True 
            
    except Exception as e:
        print("Error loading data.")
        print(e)
        dataFile = "" #clear data file so that the user can enter a new one.
        return False
            

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
    print("  B - ADD NEW GUESS")
    print("  C - DISPLAY DATA FOR A USER")
    print("  D - DISPLAY ALL USERS DATA")
    print("  E - DISPLAY GUESSES")
    print("  F - ADD/REMOVE PLAYERS' ITEMS")
    print("  G - ADVANCED ANALYSIS")
    print("  ? - DISPLAY THIS MENU")
    print("  X - SAVE AND EXIT THIS GAME")

def startup():
    print("CLUE ANALYZER")
    print("\nThis program was made by JOSHUA STAHL for CIS156 at SMCC.")
    print("""\nCLUE ANALYZER was made to help the user with the deductive
reasoning process during a game of clue. Some people are challenged with
the deductive reasoning process, (or make silly mistakes) and this program
will help with that process.""")
    #make purpose statement here
    print("\nHello Clue player! Welcome to Clue Analyzer.")

def newGame():
    global dataFile, players

    #if no dataFile on record, get it
    if dataFile == "" or dataFile == None:
        #ask user for data file
        dataFile = input("\nEnter the location and name of the save file for the new game: ")

    #get information about players:
    numplayers = int(input("\nHow many players are playing? (maximum of 6 and minimum of 2): "))
    while numplayers > 6 or numplayers < 2:
        numplayers = int(input("Invalid input. Enter the number of players (maximum of 6 and minimum of 2): "))
                       
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
    itemsadded = [] #list to store the cards that were added.
    category = "temp" # "N" makes the program not enter any more cards
    while category != "N":
        print("\nCARD CATEGORIES:")
        category = getCategoryIndexExit("Enter the card category (99 to end): ")
        if category == 0:
            print("\nROOM CARDS:")
            
            item = getRoomIndex("Select the card you have: ")
            rooms[item] = "Y"
            itemsadded.append([0, item]) #add the card to items added.
        elif category == 1:
            print("\nPEOPLE CARDS:")
            
            item = getPersonIndex("Select the card you have: ")
            people[item] = "Y"
            itemsadded.append([1, item]) #add the card to items added.
        elif category == 2:
            print("\nWEAPONS CARDS:")
            
            item = getWeaponIndex("Select the card you have: ")
            weapons[item] = "Y"
            itemsadded.append([2, item]) #add the card to items added.
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

    #set the cards added to the program user to N for the other players.
    notUser = allPlayersExcept(0) #all players accept program user (0 is always the program user)

    for card in itemsadded: #loops through all the cards added
        category = card[0] #card[0] is the category number
        cardindex = card[1] #the number of the card in that particular category number
        for player in notUser: #loops through every player (except user of program)
            if category == 0:
                # a room
                player.setRoom(cardindex, "N")
            elif category == 1:
                # a person
                player.setPerson(cardindex, "N")
            else:
                #must be a weapon
                player.setWeapon(cardindex, "N")
    
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
    try:
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
            category = getCategoryIndexExit("Select the category in which you want to make the change (99 to exit): ")
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
                players[selectedp].setPerson(item, changeto) #change the value of the room for the player.
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
                players[selectedp].setWeapon(item, changeto) #change the value of the room for the player.
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
                
    except ValueError: #catch any invalid input
        print("Invalid input. No changes made.")
        

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

def displayCategories():
    print("  0 - Rooms")
    print("  1 - People")
    print("  2 - Weapons")
        
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

def getPlayerIndexExit(msg = "\nEnter the player id (99 to exit)"): #special function to handle exiting at any moment.
    playerID = 10 #the player id.
    displayPlayers()
    while playerID < 0 or (playerID > (len(players) - 1)):
        try:
            playerID = int(input(msg))
            if playerID == 99: #if playerid is 99, return 99.
                return 99
        except ValueError:
            playerID = print("That's not an integer.") #if playerID is not an integer.
            playerID = 10 #reset playerID so an error is not thrown   

    return playerID #if they inputted valid integer, return it.

def getCategoryIndexExit(msg = "\nEnter the card category (99 to end): "):
    categoryID = 10 #the category id.
    displayCategories()
    while categoryID < 0 or categoryID > 2:
        try:
            categoryID = int(input(msg))
            if categoryID == 99: #if category is 99, return 99.
                return 99
        except ValueError:
            categoryID = print("That's not an integer.") #if categoryID is not an integer.
            categoryID = 10 #reset categoryID so an error is not thrown          

    return categoryID #if they inputted valid integer, return it.

def getCategoryIndex(msg = "\nEnter the category id: "):
    categoryID = 10 #the category id.
    displayCategories()
    while categoryID < 0 or categoryID > 2:
        try:
            categoryID = int(input(msg))
        except:
            categoryID = print("That's not an integer.") #if categoryID is not an integer.
            categoryID = 10 #reset categoryID so an error is not thrown

    return categoryID #if they inputted valid integer, return it.

def getRoomIndex(msg = "\nEnter the room id: "):
    roomID = 10 #the room id.
    displayRooms()
    while roomID < 0 or roomID > 8:
        try:            
            roomID = int(input(msg))
        except ValueError:
            roomID = print("That's not an integer.") #if roomID is not an integer.
            roomID = 10 #reset room id so an error is not thrown
            
    return roomID #if they inputted valid integer, return it.

def getPersonIndex(msg = "\nEnter the person id: "):
    personID = 10 #the person id.
    displayPeople()
    while personID < 0 or personID > 5:
        try:            
            personID = int(input(msg))
        except ValueError:
            personID = print("That's not an integer.") #if personID is not an integer.
            personID = 10 #reset personID so an error is not thrown
            
    return personID #if they inputted valid integer, return it.

def getWeaponIndex(msg = "\nEnter the weapon id: "):
    weaponID = 10 #the weapon id.
    displayWeapons()
    while weaponID < 0 or weaponID > 5:
        try:            
            weaponID = int(input(msg))
        except ValueError:
            weaponID = print("That's not an integer.") #if weaponID is not an integer.
            weaponID = 10 #reset weaponID so an error is not thrown
            
    return weaponID #if they inputted valid integer, return it.

def findMutePlayers(guesser, playershowed):
    #this function is to return the players that didn't show a
    #card between the guesser and card shower.
    playersleft = []
    guesserfound = False #keeps track of if the guesser was found.
    showerfound = False #keeps track if the card shower was found.
    for i in range(0, len(players)): #find the starting player (guess maker)        
        if i == guesser: #if guesser (starting player)
            guesserfound = True #set to true, but don't add it new array.
        elif i == playershowed and guesserfound: #if shower (person who showed card) is at i, and the guesser has been found.
            showerfound = True
        elif guesserfound and (showerfound == False):
            #since the card shower hasn't been found yet and 
            #the guesser has been found... add player to new player list.
            playersleft.append(players[i])

    if showerfound == False: #if the shower hasn't been found yet, (meaning that the shower is before the guesser in the list)
        #do the loop again. Shouldn't need to do it again after this.
        for i in range(0, len(players)):     
            if i == playershowed and guesserfound: #if shower (person who showed card) is at i, and the guesser has been found.
                showerfound = True
            elif guesserfound and (showerfound == False):
                #since the card shower hasn't been found yet and 
                #the guesser has been found... add player to new player list.
                playersleft.append(players[i])

    return playersleft

def allPlayersExcept(player):
    #this function returns all the players except for a
    #singular player. Accepts player index number

    playersleft = []
    #add all players to new list except the specified player:
    for i in range(0, len(players)):
        if i != player: #as long as the player is not the specified player
            playersleft.append(players[i])

    return playersleft
    

def basicEditOnGuess(guesser, playershowed, room, person, weapon):
    
    if playershowed != len(players): #if someone other than no-one showed a card
        #copy players list into new list, starting with the guesser
        # and ending with the player who showed his/her card.
        playersleft = findMutePlayers(guesser, playershowed)

        #set the cards guessed to N for the players who didn't say anything.
        for player in playersleft:
            player.setRoom(room, "N")
            player.setPerson(person, "N")
            player.setWeapon(weapon, "N")
        
    else:
        #no one showed a card, so everyone except guesser doesn't have the cards.
        playersleft = allPlayersExcept(guesser) #new list to hold every player except guesser.    

        #loop through the new array and set the guessed cards to N
        for i in playersleft:
            i.setRoom(room, "N")
            i.setPersoneople(person, "N")
            i.setWeapon(weapon, "N")
            
  
def addGuess():
    #get who's guess:
    guesser = getPlayerIndexExit("Who is doing the guessing? (99 to exit): ")
    if guesser == 99: #if the getPlayerIndexExit function returns 99 
        print("No guess added")
    else:
        #print the room names
        print("\nWHICH ROOM WAS GUESSED?")
        print("ROOM NAMES: ")
        #get room id
        roomid = getRoomIndex("\nWhich room was guessed?: ")

        #print the people names
        print("\nWHICH PERSON WAS GUESSED?")
        print("PEOPLE NAMES:")
        #get people id
        personid = getPersonIndex("\nWhich person was guessed?: ")

        #print the weapon names
        print("\nWHICH WEAPON WAS GUESSED?")
        print("WEAPON NAMES:")
        #get weapon id
        weaponid = getWeaponIndex("\nWhich weapon was guessed?: ")

        #get who showed or didn't show a card
        displayPlayers()
        print("{0} - No-one".format(len(players)))
        playershowed = int(input("Who showed a card?: "))
        while (playershowed < 0 or playershowed > (len(players) -1 )) and playershowed != len(players):
            playershowed = int(input("Who showed a card?: "))

        basicEditOnGuess(guesser, playershowed, roomid, personid, weaponid)

        #if the guesser is the user of this program and someone
        #actually showed a card, then ask which card was shown.
        if guesser == 0 and playershowed != len(players):
            print("\nWhat type of card did {0} show you?".format(players[playershowed].getName()))
            print("CARD CATEGORIES:")
            print("  0 - A Room")
            print("  1 - A Person")
            print("  2 - A Weapon")

            #get the category id:
            categoryID = 10 #the category id.
            
            while categoryID < 0 or categoryID > 3:
                try:
                    categoryID = int(input("\nEnter the category id: "))
                except:
                    print("That's not an integer")         

            if categoryID == 0:
                #user got shown a room

                #add "Y" to card shower for the room
                players[playershowed].setRoom(roomid, "Y")

                #set the other players to N
                setOthers(playershowed, 0, roomid, "N")
                
            elif categoryID == 1:
                #user got shown a person

                #add "Y" to card shower for the person
                players[playershowed].setPerson(personid, "Y")

                #set the other players to N
                setOthers(playershowed, 1, personid, "N")
                
            else:
                #user got shown a weapon

                #add "Y" to card shower for the weapon
                players[playershowed].setWeapon(weaponid, "Y")

                #set the other players to N
                setOthers(playershowed, 2, weaponid, "N")
                
     
        #add data to guesses
        guesses.append([guesser, roomid, personid, weaponid, playershowed])

        #advanced analysis:
        advancedAnalysis()

        #save data
        saveData() 

def displayGuesses():

    #print headers:
    print("\n" + "GUESSER".ljust(12) + "ROOM".ljust(19) + "PERSON".ljust(21) + \
          "WEAPON".ljust(17) + "CARD SHOWER".ljust(10) + "\n" + \
          "==========".ljust(12) + "============".ljust(19) + \
          "==========".ljust(21) + "==========".ljust(17) + \
          "==========")
    
    #loop through all the guesses
    for guess in guesses:

        #handle if no one answered so we don't get an index error.
        if guess[4] == len(players): #if no one answered
            answerer = "No-one"
        else: #someone other than no one answered:
            answerer = players[guess[4]].getName()

        #print guess
        print(players[guess[0]].getName().ljust(12) + \
              roomnames[guess[1]].ljust(19) + \
              peoplenames[guess[2]].ljust(21) + \
              weaponnames[guess[3]].ljust(17) + \
              answerer.ljust(10))


def displayAllUsersData():
    for player in players:
        print(player)
        print("\n") #for formatting

def playersHaveExcept(category, index, userexcept):
    #to figure out if any user has a card, except for a specified user

    playersexcept = allPlayersExcept(userexcept)

    for player in playersexcept:
        if category == 0:
            #looking for room.
            if player.getRoom(index) == "Y":
                return True #no need to continue, return true
        elif category == 1:
            #looking for person
            if player.getPerson(index) == "Y":
                return True #no need to continue, return true
        else:
            #looking for weapon
            if player.getWeapon(index) == "Y":
                return True #no need to continue, return true

    return False #no player had the card.

def setOthers(player, category, index, value):
    #to set all the players' specific card to a specific value except for "player"
    otherplayers = allPlayersExcept(player)

    for player in otherplayers:
        if category == 0:
            #set room
            player.setRoom(index, value)
        elif category == 1:
            #set person
            player.setPerson(index, value)
        else:
            #category must be weapon
            player.setWeapon(index, value)

def advancedAnalysis():
    #this function performs advanced analysis on the guesses.
    #the idea is to try to find out the card shower's card he/she
    #showed.

    #loop through all the guesses
    for guess in guesses:
        groom = guess[1] #the guessed room
        gperson = guess[2] #the guessed person
        gweapon = guess[3] #the guessed weapon
        shower = guess[4]
        room = playersHaveExcept(0, groom, shower) #if a user has the room, except for shower
        person = playersHaveExcept(1, gperson, shower) #if a user has the person, except for shower
        weapon = playersHaveExcept(2, gweapon, shower) #if a user has the weapon, except for shower

        #check the possible combinations. If one of these is true, then
        #the shower must have the other.
        if room and person:
            players[shower].setWeapon(gweapon, "Y")
            setOthers(shower, 2, gweapon, "N")
        elif room and weapon:
            players[shower].setPerson(gperson, "Y")
            setOthers(shower, 1, gperson, "N")
        elif person and weapon:
            players[shower].setRoom(groom, "Y")
            setOthers(shower, 0, groom, "N")

    print("Advanced Analysis Complete")   

main()

