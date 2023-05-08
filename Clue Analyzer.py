from clue import CluePlayer
import json

#Created by Joshua Stahl for CIS156 at SMCC for the Final Project

global dataFile

def main():
    global players, dataFile, guesses, \
           roomnames, peoplenames, weaponnames
    players = []
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
    global players, guesses, dataFile
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
            #re-analyze
            analyzeData()
        elif option == "?":
            #display game menu
            gameloopMenu()
        elif option == "X":
            print("Exiting & saving game.")
            saveData()
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
            players.append(CluePlayer(str(player['name']), int(player['cardnums']), list(player['rooms']), list(player['people']), list(player['weapons'])))

        #load the guesses
        for guess in results['guesses']:
            guesses.append(guess)

        analyzeData()
        
        return True 
            
    except Exception as e:
        print("Error loading data.")
        print(e)
        dataFile = "" #clear data file so that the user can enter a new one.
        return False
            

def saveData(mute = False, ret = False):
    #set ret = true if you want this function to return something.
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

        if mute == False: #checks before displaying message    
            print("Game saved")
        
    except Exception as e:
        print("UNABLE TO SAVE DATA TO DISK")
        print(e)

def gameloopMenu():
    print("\n--- GAME MENU ---")
    print("  A - LIST CURRENT PLAYERS")
    print("  B - ADD A NEW GUESS")
    print("  C - DISPLAY INFO FOR A USER")
    print("  D - DISPLAY ALL USERS' INFO")
    print("  E - DISPLAY GUESSES")
    print("  F - ADD/REMOVE PLAYERS' ITEMS")
    print("  G - RE-ANALYIZE DATA")
    print("  ? - DISPLAY THIS MENU")
    print("  X - SAVE AND EXIT THIS GAME")

def startup():
    print("CLUE ANALYZER")
    print("\nThis program was made by JOSHUA STAHL for CIS156 at SMCC.")
    print("""\nCLUE ANALYZER was made to help the user with the deductive
reasoning process during a game of Clue. Clue is a classic murder
mystery game, where there is three cards hidden in an envelope.
(The murderer, the murder weapon, and the murder location(or room)).
This game requires a lot of deductive reasoning, and since
some people are challenged with the deductive reasoning process,
(or make silly mistakes), this program will help
a user play the game.""")
    #make purpose statement here
    print("\nHello Clue player! Welcome to Clue Analyzer.")

def newGame():
    global dataFile, players

    #if no dataFile on record, get it
    if dataFile == "" or dataFile == None:
        #ask user for data file
        dataFile = input("\nEnter the location and name of the save file for the new game: ")
    numplayers = 10 #temporary so that the code goes into the loop.
    #get information about players:
    while numplayers > 6 or numplayers < 2:
        try:  
            numplayers = int(input("\nHow many players are playing? (maximum of 6 and minimum of 2): "))
        except ValueError:
            print("That is not an Integer")
            
    print("\nENTER INFORMATION ABOUT THE PLAYERS")
    #enter information about self:
    name = input("Enter your name: ")

    #start storing card data (by default player doesn't have anything (an N)):
    rooms = ["N", "N", "N", "N", "N", "N", "N", "N", "N"]
    people = ["N", "N", "N", "N", "N", "N"]
    weapons = ["N", "N", "N", "N", "N", "N"]
    
    print("Now input your cards")
    itemsadded = [] #list to store the cards that were added.
    category = "temp" # "N" makes the program not enter any more cards
    usercardcount = 0 #count the number of cards the user has.
    while category != "N":
        print("\nCARD CATEGORIES:")
        category = getCategoryIndexExit("Enter the card category (99 to end): ")
        if category == 0:
            print("\nROOM CARDS:")
            
            item = getRoomIndex("Select the card you have: ")
            rooms[item] = "Y"
            itemsadded.append([0, item]) #add the card to items added.
            usercardcount += 1
        elif category == 1:
            print("\nPEOPLE CARDS:")
            
            item = getPersonIndex("Select the card you have: ")
            people[item] = "Y"
            itemsadded.append([1, item]) #add the card to items added.
            usercardcount += 1
        elif category == 2:
            print("\nWEAPONS CARDS:")
            
            item = getWeaponIndex("Select the card you have: ")
            weapons[item] = "Y"
            itemsadded.append([2, item]) #add the card to items added.
            usercardcount += 1
        elif category == 99: #exit signal
            #set category to N so loop will end.
            category = "N"                
            #create new clueplayer (for user of program)
            newplayer = CluePlayer(name, usercardcount)
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
        cardnumber = getCardNumber(numplayers, "Enter the number of cards for {0}: ".format(othername))
        players.append(CluePlayer(othername, cardnumber))

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
    return True #the confirmation to continue.

def displayPlayers():
    print("\nCURRENT PLAYERS:")
    idx = 0 #current index
    for player in players:
        print(str(idx) + " - " + player.getName())
        idx += 1

def updatePlayerItems():
    global players, roomnames, peoplenames, weaponnames

    print("\nDANGER. USE AT YOUR OWN RISK. IF YOU MESS UP, \n" + \
          "THERE IS NO GOING BACK.")

    print("\nBEWARE: IF YOU SAY A PLAYER HAS A CARD, THIS \n" + \
          "WILL NOT UPDATE THE OTHER PLAYERS TO SAY THEY \n"  + \
          "DON'T HAVE THAT CARD.")
    
    print("\nEDIT A PLAYER'S CARD:")
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
                analyzeData() #data saving is included
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
                analyzeData() #data saving is included
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
                analyzeData() #data saving is included
            elif category == 99: #exit code
                selectedp = "" #ends the while loop
                analyzeData() #data saving is included
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
    print("\n" + "SHOW DATA FOR A USER")
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

def getCardNumber(numplayers, msg="Enter the number of cards for the user: "):
    #finds the card number for a player and returns the number.
    usercards = 20 #the number of cards a particular user has.
    averagecards = 18 // numplayers
    modcards = 18 % numplayers
    #set min and max, depending if evenly divided or not.
    if modcards == 0:
        maximum = averagecards
    else:
        maximum = averagecards + 1
    
    minimum = averagecards

    #if the card count is unreasonable:
    if minimum == maximum: #if there is only one option for number of cards
        return minimum
    else: #if there is more than one option for the number of cards
        while (usercards != minimum) and (usercards != maximum):
            try:
                usercards = int(input(msg))
                if (usercards != minimum) and (usercards != maximum):
                    print("Not quite. It needs to be either {0} or {1}".\
                          format(minimum, maximum))
            except ValueError:
                print("That's not an integer.") #if usercards is not an integer.
                usercards = 20 #reset usercards so an error is not thrown

    return usercards

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

def getCardName(category, index):
    #this function returns a card name for a given
    #category and index number.

    if category == 0:
        #set room
        return roomnames[index]
    elif category == 1:
        #set person
        return peoplenames[index]
    else:
        #category must be weapon
        return weaponnames[index]

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
            i.setPerson(person, "N")
            i.setWeapon(weapon, "N")
            
  
def addGuess():
    #get who's guess:
    print("\nADD A GUESS:")
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

        #default category and index (used in storing shown card in guesses):
        categoryID = 10
        index = 10
        
        #if the guesser is the user of this program and someone
        #actually showed a card, then ask which card was shown.
        if guesser == 0 and playershowed != len(players):
            print("\nWhat type of card did {0} show you?".format(players[playershowed].getName()))
            print("CARD CATEGORIES:")
            print("  0 - A Room")
            print("  1 - A Person")
            print("  2 - A Weapon")

            #get the category id:
            
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
                index = roomid #set the index for the shown card in the guess
                
            elif categoryID == 1:
                #user got shown a person

                #add "Y" to card shower for the person
                players[playershowed].setPerson(personid, "Y")

                #set the other players to N
                setOthers(playershowed, 1, personid, "N")
                index = personid #set the index for the shown card in the guess
                
            else:
                #user got shown a weapon

                #add "Y" to card shower for the weapon
                players[playershowed].setWeapon(weaponid, "Y")

                #set the other players to N
                setOthers(playershowed, 2, weaponid, "N")
                index = weaponid #set the index for the shown card in the guess

        elif playershowed == 0: #if the player who showed a card is the program user
            print("\nWhat type of card did you show {0}?".format(players[guesser].getName()))
            print("CARD CATEGORIES:")
            print("  0 - A Room")
            print("  1 - A Person")
            print("  2 - A Weapon")

            #get the category id:
            
            while categoryID < 0 or categoryID > 3:
                try:
                    categoryID = int(input("\nEnter the category id: "))
                except:
                    print("That's not an integer")         

            if categoryID == 0:
                #program user showed a room
                index = roomid #set the index for the shown card in the guess
            elif categoryID == 1:
                #program user showed a person
                index = personid #set the index for the shown card in the guess
            else:
                #program user showed a weapon
                index = weaponid #set the index for the shown card in the guess
                
        #check to make sure guess is ok:
        print("\nJust about to add this guess to the program. Does it look good?")
        print("THE GUESS")
        print("  Guesser - {0}".format(players[guesser].getName()))
        print("  Room    - {0}".format(roomnames[roomid]))
        print("  Person  - {0}".format(peoplenames[personid]))
        print("  Weapon  - {0}".format(weaponnames[weaponid]))
        
        #check to make sure card shower isn't "no-one":
        if playershowed == len(players):
            shower = "No One"
        else:
            shower = players[playershowed].getName()
        print("  Shower  - {0}\n".format(shower))
        check = "temp" #temporary, to get into loop.
        while check != "Y" and check !="N":
            check = input("Does this look good? (Y/N): ").upper()

        if check == "Y":
            
            #add data to guesses
            guesses.append([guesser, roomid, personid, weaponid, playershowed, [categoryID, index]])

            #advanced analysis:
            analyzeData() #save data is included, False or blank = display "data saved" message

        else:
            print("Guess not added.")

def displayGuesses():

    #print headers:
    print("\n" + "GUESSER".ljust(12) + "ROOM".ljust(19) + "PERSON".ljust(21) + \
          "WEAPON".ljust(17) + "CARD SHOWER".ljust(13) + "SHOWN CARD".ljust(21) + \
          "\n" + "==========".ljust(12) + "============".ljust(19) + \
          "==========".ljust(21) + "==========".ljust(17) + \
          "===========".ljust(13) + "==========".ljust(21))
    
    #loop through all the guesses
    for guess in guesses:

        #handle if no one answered so we don't get an index error.
        if guess[4] == len(players): #if no one answered
            answerer = "No-one"
            cardshown = "N/A" #since no one answered, set cardshown to na.
        else: #someone other than no one answered:
            answerer = players[guess[4]].getName()

            #set what card is shown.
            if guess[5][0] != 10 and guess[5][1] != 10: #make sure the card shown is not unknown
                cardshown = getCardName(guess[5][0], guess[5][1]) #set card shown to the shown card.
            else: #we don't know the shown card yet
                cardshown = "Unknown"                
            

        #print guess
        print(players[guess[0]].getName().ljust(12) + \
              roomnames[guess[1]].ljust(19) + \
              peoplenames[guess[2]].ljust(21) + \
              weaponnames[guess[3]].ljust(17) + \
              answerer.ljust(13) + cardshown.ljust(21))


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
    #accepts index number of player
    otherplayers = allPlayersExcept(player)

    for player in otherplayers:
        if category == 0:
            #set room
            player.setRoom(index, value)
        elif category == 1:
            #set person
            player.setPerson(index, value)
        elif category == 2:
            #category is a weapon
            player.setWeapon(index, value)

def setEveryone(category, index, value):
    #to set all the players' specific card to a specific value.

    for player in players:
        if category == 0:
            #set room
            player.setRoom(index, value)
        elif category == 1:
            #set person
            player.setPerson(index, value)
        else:
            #category must be weapon
            player.setWeapon(index, value)
            
def noOneHas(category, index):
    #returns True if no player has the card, False if not.

    noOneHas = True #keeps track if a user has the specified card.
                    #(also if we don't know if user has card)
    for player in players:
        if category == 0:
            #get room
            if player.getRoom(index) == "Y" or player.getRoom(index) == "-":
                return False
        elif category == 1:
            #get person
            if player.getPerson(index) == "Y" or player.getPerson(index) == "-":
                return False
        elif category == 2:
            #category must be weapon, get weapon
            if player.getWeapon(index) == "Y" or player.getWeapon(index) == "-":
                return False

    return noOneHas

def someoneHas(category, index):
    #returns True if some player has the card, False if not.

    for player in players:
        if category == 0:
            #get room
            if player.getRoom(index) == "Y":
                return True
        elif category == 1:
            #get person
            if player.getPerson(index) == "Y":
                return True
        elif category == 2:
            #get weapon
            if player.getWeapon(index) == "Y":
                return True

    return False #if no player as the card, return false.

def notHave(player, category, index):
    #returns true if a player does not have a particular card,
    #otherwise returns false.

    if category == 0:
        #get room
        if players[player].getRoom(index) == "N":
            return True
    elif category == 1:
        #get person
        if players[player].getPerson(index) == "N":
            return True
    elif category == 2:
        #get weapon
        if players[player].getWeapon(index) == "N":
            return True

    return False #player didn't not have the card, so return false.

def mysteryCardCheck():
    #this function checks for a singular card in each of the
    #categories that no one has. If there is more than one card
    #that no one has in a category, this function does nothing.
    #If there is only one card in a category, then this function
    #has effectivly found a card in the secret envelope. It will
    #then set the card to "N" for each of the players.

    #function also checks to see if there is a card no one has.

    #set variables:
    secretroom = False #if the murder location has been found
    secretperson = False #if the murderer has been found
    secretweapon = False #if the murder weapon has been found

    #check the rooms
    roomlist = [] #a list of index numbers of the rooms that no one has
    for room in range(0, 9): #for each of the rooms
        if not someoneHas(0, room): #if no player has the room
            roomlist.append(room)

    #check to see if there is one room no one has.
    #(that room is the murder location)
    if len(roomlist) == 1:
        setEveryone(0, roomlist[0], "N") #no one will have this room.
        secretroom = True


    #check the people
    peoplelist = [] #a list of index numbers of the people that no one has
    for person in range(0, 6): #for each of the people
        if not someoneHas(1, person): #if no player has the person
            peoplelist.append(person)

    #check to see if there is one person no one has.
    #(that person is the murderer)
    if len(peoplelist) == 1:
        setEveryone(1, peoplelist[0], "N") #no one will have this person.
        secretperson = True


    #check the weapons
    weaponlist = [] #a list of index numbers of the weapons that no one has
    for weapon in range(0, 6): #for each of the weapons
        if not someoneHas(2, weapon): #if no player has the weapon
            weaponlist.append(weapon)

    #check to see if there is one weapon no one has.
    #(that weapon is the murder weapon)
    if len(weaponlist) == 1:
        setEveryone(2, weaponlist[0], "N") #no one will have this weapon.
        secretweapon = True


    #check to see if there is a card that no one has

    #check every room:
    for i in range(0, 9):
        if noOneHas(0, i):
            print(roomnames[i] + " is the murder location...")
            secretroom = True #found murder location
            break #no need to loop any more, found murder location


    #check every person:
    for i in range(0, 6):
        if noOneHas(1, i):
            print(peoplenames[i] + " is the murderer...")
            secretperson = True #found the murderer
            break #no need to loop any more, found the murderer


    #check every weapon:
    for i in range(0, 6):
        if noOneHas(2, i):
            print(weaponnames[i] + " is the murder weapon...")
            secretweapon = True #found the murder weapon
            break #no need to loop any more, found the murder weapon
    
    
    #if all the secret items are found
    if secretroom and secretperson and secretweapon:
        print("\n######  YOU CAN MAKE YOUR GUESS ON THE SECRET CARDS!  ######\n")

def AnalysisSetRoom(guess, discoveries):
    #This function takes a guess and makes the necessary changes
    #to it. It sets the guessed room to yes for the shower
    #and the others to no.
    
    guesser = guess[0] #the guesser
    groom = guess[1] #the guessed room
    gperson = guess[2] #the guessed person
    gweapon = guess[3] #the guessed weapon
    shower = guess[4] #the shower

    if players[shower].getRoom(groom) != "Y": #this means this has not been discovered before.
        discoveries.append([shower, 0, groom]) #add item to list of discoveries
        
    players[shower].setRoom(groom, "Y") #set room to yes for shower
    setOthers(shower, 0, groom, "N") #the others don't have the room
    guess[5] = [0, groom] #set the shown card in the guess

    return (guess, counter, discoveries) #return a tuple.

def AnalysisSetPerson(guess, discoveries):
    #This function takes a guess and makes the necessary changes
    #to it. It sets the guessed person to yes for the shower
    #and the others to no.
    
    guesser = guess[0] #the guesser
    gperson = guess[2] #the guessed person
    shower = guess[4] #the shower

    if players[shower].getPerson(gperson) != "Y": #this means this has not been discovered before.
        discoveries.append([shower, 1, gperson]) #add item to list of discoveries
        
    players[shower].setPerson(gperson, "Y") #set person to yes for shower
    setOthers(shower, 1, gperson, "N") #the others don't have the person
    guess[5] = [1, gperson] #set the shown card in the guess

    return (guess, counter, discoveries) #return a tuple.

def AnalysisSetWeapon(guess, discoveries):
    #This function takes a guess and makes the necessary changes
    #to it. It sets the guessed weapon to yes for the shower
    #and the others to no.
    
    guesser = guess[0] #the guesser
    gweapon = guess[3] #the guessed weapon
    shower = guess[4] #the shower

    if players[shower].getWeapon(gweapon) != "Y": #this means this has not been discovered before.
        discoveries.append([shower, 2, gweapon]) #add item to list of discoveries
        
    players[shower].setWeapon(gweapon, "Y") #set weapon to yes for shower
    setOthers(shower, 2, gweapon, "N") #the others don't have the weapon
    guess[5] = [2, gweapon] #set the shown card in the guess

    return (guess, discoveries) #return a tuple.

def displayDiscoveries(discoveries):
    for discov in discoveries:
            #figure out what the middle text of the print statement should be
            #based on what was discovered. Also figure out name of what was
            #discovered
            if discov[1] == 0:
                #a room was discovered
                middle = " has the "
                itemname = roomnames[discov[2]]
            elif discov[1] == 1:
                #a person was discovered
                middle = " has "
                itemname = peoplenames[discov[2]]
            elif discov[1] == 2:
                #a weapon was discovered
                middle = " has the "
                itemname = weaponnames[discov[2]]
                
            print(players[discov[0]].getName() + middle + itemname)

def analyzeData(mute = True):
    #this function performs advanced analysis on the guesses.
    #the idea is to try to find out the card shower's card he/she
    #showed.

    #analysis discovery counter:
    counter = 0

    #loop through all the guesses
    for guess in guesses:

        guesser = guess[0] #the guesser
        groom = guess[1] #the guessed room
        gperson = guess[2] #the guessed person
        gweapon = guess[3] #the guessed weapon
        shower = guess[4] #the shower
        
            
        if guess[4] != len(players): #make sure the guess is not no-one.

            discoveries = [] #a list to hold the discoveries (if any)
            
            otherroom = playersHaveExcept(0, groom, shower) #if a user has the room, except for shower
            otherperson = playersHaveExcept(1, gperson, shower) #if a user has the person, except for shower
            otherweapon = playersHaveExcept(2, gweapon, shower) #if a user has the weapon, except for shower

            #check the possible combinations, if a combination is
            #true, then the shower must have the other.

            #***************** CHECK WHAT THE PLAYERS (besides guesser) HAVE *******************
            
            #if other people besides the shower have the room and person
            #then the shower has the weapon
            if otherroom and otherperson:
                #set the weapon to true for the shower and so on.
                guess, discoveries = AnalysisSetWeapon(guess, discoveries)
                
            #if other people besides the shower have the room and weapon
            #then the shower has the person
            elif otherroom and otherweapon:
                #set the person to true for the shower and so on.
                guess, discoveries = AnalysisSetPerson(guess, discoveries)

            #if other people besides the shower have the person and weapon
            #then the shower has the room
            elif otherperson and otherweapon:
                #set the room to true for the shower and so on.
                guess, discoveries = AnalysisSetRoom(guess, discoveries)


            #*************** CHECK WHAT THE SHOWER DOESN'T HAVE AND WHAT THE OTHERS DO ***********#
                

            #if the shower doesn't have the room, and other people have
            #the person then shower has the weapon
            elif notHave(shower, 0, groom) and otherperson:
                #set the weapon to true for the shower and so on.
                guess, discoveries = AnalysisSetWeapon(guess, discoveries)             

            #if the shower doesn't have the room, and other people have
            #the weapon then shower has the person
            elif notHave(shower, 0, groom) and otherweapon:
                #set the person to true for the shower and so on.
                guess, discoveries = AnalysisSetPerson(guess, discoveries)

            #if the shower doesn't have the person, and other people have
            #the room then shower has the weapon
            elif notHave(shower, 1, gperson) and otherroom:
                #set the weapon to true for the shower and so on.
                guess, discoveries = AnalysisSetWeapon(guess, discoveries)

            #if the shower doesn't have the person, and other people have
            #the weapon then shower has the room
            elif notHave(shower, 1, gperson) and otherweapon:
                #set the room to true for the shower and so on.
                guess, discoveries = AnalysisSetRoom(guess, discoveries)

            #if the shower doesn't have the weapon, and other people have
            #the room then shower has the person
            elif notHave(shower, 2, gweapon) and otherroom:
                #set the person to true for the shower and so on.
                guess, discoveries = AnalysisSetPerson(guess, discoveries)

            #if the shower doesn't have the weapon, and other people have
            #the person then shower has the room
            elif notHave(shower, 2, gweapon) and otherperson:
                #set the room to true for the shower and so on.
                guess, discoveries = AnalysisSetRoom(guess, discoveries)


            #*************** CHECK WHAT THE SHOWER DOESN'T HAVE ****************#

            #if the shower doesn't have the room nor the person
            #then shower has the weapon
            elif notHave(shower, 0, groom) and notHave(shower, 1, gperson):
                #set the weapon to true for the shower and so on.
                guess, discoveries = AnalysisSetWeapon(guess, discoveries)

            #if the shower doesn't have the room nor the weapon
            #then shower has the person
            elif notHave(shower, 0, groom) and notHave(shower, 2, gweapon):
                #set the person to true for the shower and so on.
                guess, discoveries = AnalysisSetPerson(guess, discoveries)

            #if the shower doesn't have the person nor the weapon
            #then shower has the room
            elif notHave(shower, 1, gperson) and notHave(shower, 2, gweapon):
                #set the room to true for the shower and so on.
                guess, discoveries = AnalysisSetRoom(guess, discoveries)
            
    #card count analysis:
    cardCountAnalysis()

    #mystery card check:
    mysteryCardCheck()

    if len(discoveries) == 1: #count for printing anomaly
        print("Finished Analyzing: 1 new discovery")
        displayDiscoveries(discoveries)
    else: #everything else
        print("Finished Analyzing: {0} new discoveries".format(len(discoveries)))
        #loop through the discoveries:
        displayDiscoveries(discoveries)
        
        
    saveData(mute) #muted save data, takes input from user.

def returnCardsHave(player):
    #this function returns the cards a player has
    #in an array of arrays. Accepts a clue player object

    cards = [] #the array of cards a player has
    
    #check every room:
    for i in range(0, 9):
        if player.getRoom(i) == "Y":
            cards.append([0, i])

    #check every person:
    for i in range(0, 6):
        if player.getPerson(i) == "Y":
            cards.append([1, i])


    #check every weapon:
    for i in range(0, 6):
        if player.getWeapon(i) == "Y":
            cards.append([2, i])

    return cards

def setRestOfCardsToNo(player, cards):
    #this function will set all the cards to N
    #for a player (clue player object)
    #then set the specific cards back to Y.

    rooms = ["N", "N", "N", "N", "N", "N", "N", "N", "N"]
    people = ["N", "N", "N", "N", "N", "N"]
    weapons = ["N", "N", "N", "N", "N", "N"]

    #set all cards to N
    player.setBulkRooms(rooms)
    player.setBulkPeople(people)
    player.setBulkWeapons(weapons)

    #set all the other cards back to Y
    for i in cards:
        category = i[0]
        index = i[1]
        if category == 0:
            #get room
            player.setRoom(index, "Y")
        elif category == 1:
            #get person
            player.setPerson(index, "Y")
        elif category == 2:
            #get weapon
            player.setWeapon(index, "Y")

def returnCountUnknowns(player):
    #this function returns the unknown cards for a player
    #in an array of arrays. Accepts a clue player object

    cards = [] #the array of unknown cards for the player
    
    #check every room:
    for i in range(0, 9):
        if player.getRoom(i) == "-":
            cards.append([0, i])

    #check every person:
    for i in range(0, 6):
        if player.getPerson(i) == "-":
            cards.append([1, i])


    #check every weapon:
    for i in range(0, 6):
        if player.getWeapon(i) == "-":
            cards.append([2, i])

    return cards

def cardCountAnalysis():
    #this function counts cards. If we have a player with 5 cards, 
    #count all the cards with a "Y", and if that equals the number of cards,
    #then we know we can set all the other cards to N.

    #also this function looks at how many cards more can the user have.
    #if the amount of unknown cards (-) equals the number of cards the user
    #can have, then that user has those unknown cards.

    #get all the players except for the user of the program:
    otherplayers = allPlayersExcept(0)

    #loop through the players for the analysis.
    for i in range(0, len(players)):
        player = players[i]
        cardshave = returnCardsHave(player)
        unknowncards = returnCountUnknowns(player)
        
        #if the number of cards the user has is equal
        #to the number of cards the user should have,
        #and there is something to set(e.g. we haven't figured out all their cards),
        #then set the rest of that player's cards to N.
        if (len(cardshave) == player.getNumberOfCards()) and (len(unknowncards) > 0):
            setRestOfCardsToNo(player, cardshave)
            print("ALL INFORMATION IS KNOWN ABOUT {0}".format(player.getName()))

        #if the number of unknown cards the user has plus the
        #number of cards the user has equals the number of cards
        #the player should have, then set those unknown cards to Y,
        #all the other cards to N for that player, and set the other
        #players' cards to N based on the unknown cards of the player
        #we are working on. Also make sure that there is at least
        #one unknown card.
        elif (player.getNumberOfCards() == (len(cardshave) + len(unknowncards))) and \
             len(unknowncards) != 0:

            #loop through the unknown cards:
            for card in unknowncards:
                category = card[0]
                index = card[1]
                if category == 0:
                    #get room
                    player.setRoom(index, "Y")
                    setOthers(i, category, index, "N") 
                elif category == 1:
                    #get person
                    player.setPerson(index, "Y")
                    setOthers(i, category, index, "N") 
                elif category == 2:
                    #get weapon
                    player.setWeapon(index, "Y")
                    setOthers(i, category, index, "N")

            #now to set the rest of the player's other cards to N.
            cardshave = returnCardsHave(player) #get new list of cardshave, since we updated it.
            
            #tell the user what just happened
            print("ALL INFORMATION IS KNOWN ABOUT {0}".format(player.getName()))        

        
main()
