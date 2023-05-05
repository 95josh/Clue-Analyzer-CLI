from enum import Enum
#Created by Joshua Stahl for CIS156 at SMCC for the Final Project


class CluePlayer():

    def __init__(self, name, cardnumbers, rms = None, peopl = None, weap = None):

        self.__name = name #store the name of the player
        self.__numberofcards = cardnumbers #the number of cards the player has.

        # "-" means "don't know if player has it", "Y" means player has it, "
        # "N" means "player doesn't have it"
        
        self.__rooms = ["-", "-", "-", "-", "-", "-", "-", "-", "-"] # 9 rooms, set temporarily
        #if rms is not set to none, set values to class list
        if rms != None:
            self.setBulkRooms(rms)

        self.__people = ["-", "-", "-", "-", "-", "-"] # 6 people, set temporarily
        #if peopl is not set to none, set values to class list
        if peopl != None:
            self.setBulkPeople(peopl)
            
        self.__weapons = ["-", "-", "-", "-", "-", "-"] # 6 weapons , set temporarily
        #if weap is not set to none, set values to class list
        if weap != None:
            self.setBulkWeapons(weap)            
           
        #room names:
        self.__roomdesc = ["Ball Room", "Billiard Room", "Conservatory", \
                           "Dining Room", "Hall", "Kitchen", "Lounge", \
                           "Library", "Study"] 
        
        #people names:
        self.__peopledesc = ["Mrs. White", "Mrs. Peacock", "Professor Plum", \
                             "Colonel Mustard", "Miss Scarlett", "Reverend Green"] 
        
        #weapon names:
        self.__weaponsdesc = ["Knife", "Revolver", "Rope", "Wrench",\
                              "Candlestick", "Lead Pipe"]
        

    #setters
    def setBulkRooms(self, rooms):
        #useful when reading from a file.
        #if the length of rooms == 9, then the user passed
        #the right number of rooms. Continue. Else, do nothing.
        
        if isinstance(rooms, list) and len(rooms) == 9:
            for i in range(0, 9): #loop through the rooms to add to the class list
                room = rooms[i].upper() #capitalize the room we are on.
                if room == "N":
                    self.__rooms[i] = room
                elif room == "Y":
                    self.__rooms[i] = room
                else:
                    #if a "-" or any other character, set "-"
                    self.__rooms[i] = "-"
        else:
            raise ValueError("Invalid input. Incorrect length or not a list")

    def setBulkPeople(self, people):
        #useful when reading from a file.
        #if the length of people == 6, then the user passed
        #the right number of people. Continue. Else, do nothing.
        
        if isinstance(people, list) and len(people) == 6:
            for i in range(0, 6): #loop through the people to add to the class list
                person = people[i].upper() #capitalize the people we are on.
                if person == "N":
                    self.__people[i] = person
                elif person == "Y":
                    self.__people[i] = person
                else:
                    #if a "-" or any other character, set "-"
                    self.__people[i] = "-"
        else:
            raise ValueError("Invalid input. Incorrect length or not a list")

    def setBulkWeapons(self, weapons):
        #useful when reading from a file.
        #if the length of weapons == 6, then the user passed
        #the right number of weapons. Continue. Else, do nothing.
        
        if isinstance(weapons, list) and len(weapons) == 6:
            for i in range(0, 6): #loop through the people to add to the class list
                weapon = weapons[i].upper() #capitalize the people we are on.
                if weapon == "N":
                    self.__weapons[i] = weapon
                elif weapon == "Y":
                    self.__weapons[i] = weapon
                else:
                    #if a "-" or any other character, set "-"
                    self.__weapons[i] = "-"
        else:
            raise ValueError("Invalid input. Incorrect length or not a list")

    def setName(self, value):
        self.__name = value

    def setRoom(self, idx, value):
        #check to make sure idx is within an appropriate range.
        if idx >= 0 or idx < 9:
            #value shouldn't be outside x, y, and -
            if value == "N" or value == "Y":
                self.__rooms[idx] = value
            else:
                self.__rooms[idx] = "-"
        else:
            raise ValueError("Index not valid")

    def setPerson(self, idx, value):
        #check to make sure idx is within an appropriate range.
        if idx >= 0 or idx < 6:
            #value shouldn't be outside x, y, and -
            if value == "N" or value == "Y":
                self.__people[idx] = value
            else:
                self.__people[idx] = "-"
        else:
            raise ValueError("Index not valid")

    def setWeapon(self, idx, value):
        #check to make sure idx is within an appropriate range.
        if idx >= 0 or idx < 6:
            #value shouldn't be outside x, y, and -
            if value == "N" or value == "Y":
                self.__weapons[idx] = value
            else:
                self.__weapons[idx] = "-"
        else:
            raise ValueError("Index not valid")

    def setNumberOfCards(self, value):
        #sets the number of cards the player has
        #check to see if value is reasonable
        #minimum is 3, maximum is 11
        if value >= 3 and value <= 11:
            self.__numberofcards = value
        
    ###############getters###############
    def dumpRooms(self):
        #dumps information for saving into file
        result = "" #setup result variable
        #there will only be 9 rooms ever
        for i in range(0, 9):
            #if we are not at the last room
            if i < 8:
                result += self.__rooms[i] + ","
            else:
                result += self.__rooms[i]
             
        return result

    def dumpPeople(self):
        #dumps information for saving into file
        result = "" #setup result variable
        #there will only be 6 people ever 
        for i in range(0, 6):
            #if we are not at the last person
            if i < 6:
                result += self.__people[i] + ","
            else:
                result += self.__people[i]
             
        return result

    def dumpWeapons(self):
        #dumps information for saving into file
        result = "" #setup result variable
        #there will only be 6 weapons ever
        for i in range(0, 6):
            #if we are not at the last weapon
            if i < 6:
                result += self.__weapons[i] + ","
            else:
                result += self.__weapons[i]
             
        return result

    def getRoom(self, idx):
        return self.__rooms[idx]

    def getPerson(self, idx):
        return self.__people[idx]

    def getWeapon(self, idx): 
        return self.__weapons[idx]

    def getRooms(self):
        return self.__rooms

    def getPeople(self):
        return self.__people

    def getWeapons(self):
        return self.__weapons

    def getRoomNames(self):
        return self.__roomdesc

    def getPeopleNames(self):
        return self.__peopledesc

    def getWeaponNames(self):
        return self.__weaponsdesc

    def getNumberOfCards(self):
        return self.__numberofcards

    def getName(self):
        return self.__name

    def getEverything(self):
        return {'name':self.getName(), 'cardnums':self.getNumberOfCards(),
                'rooms':self.getRooms(), 'people':self.getPeople(), \
                'weapons':self.getWeapons()}
    
    def __str__(self):

        content = "PLAYER: " + self.getName().upper() + " - Card count: " + \
               str(self.getNumberOfCards()) + "\n\n" + "ROOMS".ljust(19) + \
               "PEOPLE".ljust(21) + "WEAPONS".ljust(17) + "\n" + \
               "============".ljust(19) + "============".ljust(21) + \
               "==========".ljust(17) + "\n"

        for i in range(0, 6): #for just the first 6 rows, then we need to do something different.
            content += (self.getRoomNames()[i] + " (" + self.__rooms[i] + ")").ljust(19) + \
                       (self.getPeopleNames()[i] + " (" + self.__people[i] + ")").ljust(21) + \
                       (self.getWeaponNames()[i] + " (" + self.__weapons[i] + ")").ljust(17) + "\n"

        #display the last 3 rooms:    
        content += (self.getRoomNames()[6] + " (" + self.__rooms[6] + ")") + "\n"
        content += (self.getRoomNames()[7] + " (" + self.__rooms[7] + ")") + "\n"
        content += (self.getRoomNames()[8] + " (" + self.__rooms[8] + ")") + "\n"
        
        return content
        

        
                            

    

