from random import *

def roll():
    return randint(1,6)

class Tile:
    def __init__(self, name, position, typeOfTile, prop):## = Property("",0,{})): ##typeOfTile: 0 = Property, 1 = Chance, 2 = Community Chest, 3 = Free Parking, 4 = To Jail, 5 = Jail, 6 = Go, 7 = Income Tax, 8 = Luxury Tax
        self.name = name
        self.position = position
        self.typeOfTile = typeOfTile
        self.prop = prop

class Property:
    def __init__(self, name, cost, rent, typeOfProp, owner, color = "black"): ##typeOfProp: 0 = Normal Property, 1 = Railroad, 2 = Utility
        self.name = name
        self.owner = owner
        self.cost = cost
        self.rent = rent        
        self.typeOfProperty = typeOfProp
        self.color = color
        self.house = 0
        self.hotel = 0
        self.mortgage = False
        if typeOfProp == 0:
            self.color = "white"

    def calcRent(self, rolls):
        numOfColor = 0
        for prop in self.owner.properties:
            if prop.color == self.color:
                numOfColor += 1
        if self.typeOfProperty == 2:
            rent = self.rent[numOfColor] * rolls
        if self.typeOfProperty == 1:
            rent = 25 * (2**(numOfColor-1))
        if self.typeOfProperty == 0:
            rent = self.rent[5 * self.hotel + self.house]
            if ((5 * self.hotel + self.house) == 0) and (((self.color == "blue" or self.color == "brown") and numOfColor == 2) or (numOfColor == 3)):
                rent *= 2
        return rent

class Player:
    def __init__(self, name, color, startingCash):
        self.name = name
        self.color = color
        self.cash = startingCash
        self.position = 0
        self.properties = []
        self.jailed = False
        self.turnsInJail = 0
        self.numOfJF = 0
        
    def move(self, roll):
        self.position += roll
        if self.position > 39:
            print("Passed Go! Collect $200")
            self.position -= 40
            self.cash += 200

class Main:
    def __init__(self, numOfPlayers, startingCash = 1500):
        if numOfPlayers < 2:
            print("Need at least two players for this game")
            quit()
        self.bank = Player("Bank", "black", 9999999)
        self.players = []
        pholder = Property("",0,{},-1,self.bank,"blank")
        self.properties = [Property("Mediterranean Avenue", 60, {0:2,1:10,2:30,3:90,4:160,5:250}, 0, self.bank, "brown"), Property("Baltic Avenue", 60, {0:4,1:20,2:60,3:180,4:320,5:450}, 0, self.bank, "brown"), Property("Oriental Avenue", 100, {0:6,1:30,2:90,3:270,4:400,5:550}, 0, self.bank, "light blue"), Property("Vermont Avenue", 100, {0:6,1:30,2:90,3:270,4:400,5:550}, 0, self.bank, "light blue"), Property("Connecticut Avenue", 120, {0:8,1:40,2:100,3:300,4:450,5:600}, 0, self.bank, "light blue"), Property("St. Charles Place", 140, {0:10,1:50,2:150,3:450,4:625,5:750}, 0, self.bank, "pink"), Property("States Avenue", 140, {0:10,1:50,2:150,3:450,4:625,5:750}, 0, self.bank, "pink"), Property("Virginia Avenue", 160, {0:12,1:60,2:180,3:500,4:700,5:900}, 0, self.bank, "pink"), Property("St. James Place", 180, {0:14,1:70,2:200,3:550,4:750,5:950}, 0, self.bank, "orange"), Property("Tennessee Avenue", 180, {0:14,1:70,2:200,3:550,4:750,5:950}, 0, self.bank, "orange"), Property("New York Avenue", 200, {0:16,1:80,2:220,3:600,4:800,5:1000}, 0, self.bank, "orange"), Property("Kentucky Avenue", 220, {0:18,1:90,2:250,3:700,4:875,5:1050}, 0, self.bank, "red"), Property("Indiana Avenue", 220, {0:18,1:90,2:250,3:700,4:875,5:1050}, 0, self.bank, "red"), Property("Illinois Avenue", 240, {0:20,1:100,2:300,3:750,4:925,5:1100}, 0, self.bank, "red"), Property("Atlantic Avenue", 260, {0:22,1:110,2:330,3:800,4:975,5:1150}, 0, self.bank, "yellow"), Property("Ventnor Avenue", 260, {0:22,1:110,2:330,3:800,4:975,5:1150}, 0, self.bank, "yellow"), Property("Marvin Gardens", 280, {0:24,1:120,2:360,3:850,4:1025,5:1200}, 0, self.bank, "yellow"), Property("Pacific Avenue", 300, {0:26,1:130,2:390,3:900,4:1100,5:1275}, 0, self.bank, "green"), Property("Pacific Avenue", 300, {0:26,1:130,2:390,3:900,4:1100,5:1275}, 0, self.bank, "green"), Property("North Carolina Avenue", 300, {0:26,1:130,2:390,3:900,4:1100,5:1275}, 0, self.bank, "green"), Property("Pennsylvania Avenue", 320, {0:28,1:150,2:450,3:1000,4:1200,5:1400}, 0, self.bank, "green"), Property("Park Place", 350, {0:35,1:175,2:500,3:1100,4:1300,5:1500}, 0, self.bank, "blue"), Property("Boardwalk", 500, {0:50,1:200,2:600,3:1400,4:1700,5:2000}, 0, self.bank, "blue"), Property("Reading Railroad", 200, {0:25,1:50,2:100,3:200}, 1, self.bank, "black"), Property("Pennsylvania Railroad", 200, {0:25,1:50,2:100,3:200}, 1, self.bank, "black"), Property("B&O Railroad", 200, {0:25,1:50,2:100,3:200}, 1, self.bank, "black"), Property("Short Line", 200, {0:25,1:50,2:100,3:200}, 1, self.bank, "black"), Property("Electric Company", 150, {0:4, 1:10}, 2, self.bank, "white"), Property("Water Works", 150, {0:4, 1:10}, 2, self.bank, "white")]
        self.tiles = [Tile("Go!",0,6,pholder), Tile("Mediterranean Avenue",1,0,self.properties[0]), Tile("Community Chest",2,2,pholder), Tile("Baltic Avenue",3,0,self.properties[1]), Tile("Income Tax",4,7,pholder), Tile("Reading Railroad",5,0,self.properties[22]), Tile("Oriental Avenue",6,0,self.properties[2]), Tile("Chance",7,1,pholder), Tile("Vermont Avenue",8,0,self.properties[3]), Tile("Connecticut Avenue",9,0,self.properties[4]), Tile("Jail",10,5,pholder), Tile("St. Charles Place",11,0,self.properties[5]), Tile("Electric Company",12,0,self.properties[26]), Tile("States Avenue",13,0,self.properties[6]), Tile("Virginia Avenue",14,0,self.properties[7]), Tile("Pennsylvania Railroad",15,0,self.properties[23]), Tile("St. James Place",16,0,self.properties[8]), Tile("Community Chest",17,2,pholder), Tile("Tennessee Avenue",18,0,self.properties[9]), Tile("New York Avenue",19,0,self.properties[10]), Tile("Free Parking",20,3,pholder), Tile("Kentucky Avenue",21,0,self.properties[11]), Tile("Chance",22,1,pholder), Tile("Indiana Avenue",23,0,self.properties[12]), Tile("Illinois Avenue",24,0,self.properties[13]), Tile("B&O Railroad",25,0,self.properties[24]), Tile("Atlantic Avenue",26,0,self.properties[14]), Tile("Ventnor Avenue",27,0,self.properties[15]), Tile("Water Works",28,0,self.properties[27]), Tile("Marvin Gardens",29,0,self.properties[16]), Tile("Go To Jail",30,4,pholder), Tile("Pacific Avenue",31,0,self.properties[17]), Tile("North Carolina Avenue",32,0,self.properties[18]), Tile("Community Chest",33,2,pholder), Tile("Pennsylvania Avenue",34,0,self.properties[19]), Tile("Short Line",35,0,self.properties[25]), Tile("Chance",36,1,pholder), Tile("Park Place",37,0,self.properties[20]), Tile("Luxury Tax",38,8,pholder), Tile("Boardwalk",39,0,self.properties[21])]
        self.rounds = -1
        self.FPC = 0
        doubles = 0
        self.lastRoll = 0
        gameOver = False
        self.bank.properties = self.properties
        for i in range(0, numOfPlayers):
            name = ""
            while name == "":
                name = input("Enter Player " + str(i+1) + "'s name: ")
                if name == "Bank":
                    print("Chose another name")
                    name == ""
            color = input("Hi " + name + "! Please choose a color: ")
            self.players += [Player(name, color, startingCash)]
        print("Lets see the order of play!")
        shuffle(self.players)
        for i in range(0, numOfPlayers):
            if i == 0:
                print(self.players[i].name + " goes 1st")
            elif i == 1:
                print(self.players[i].name + " goes 2nd")
            elif i == 2:
                print(self.players[i].name + " goes 3rd")
            else:
                print(self.players[i].name + " goes " + str(i+1) + "th")

        while not gameOver:
            self.rounds += 1
            if self.rounds >= len(self.players):
                self.rounds -= len(self.players)
            player = self.players[self.rounds]
            if True: ##Didnt want to unindent everything after
                print("It's " + str(player.name) + "'s turn!")
                if player.jailed == True:
                    player.turnsInJail += 1
                    print("You're in Jail!")
                    print("You can Roll, Pay, Manage, Trade, or type \"Help\" to get information on your options")
                    
                else:
                    option = ""
                    while option == "":
                        print("You can Roll, Manage, Trade, or type \"Help\" to get information on your options")
                        option = input("What do you want to do? \n")
                        if option != "Roll" and option != "Manage" and option != "Trade" and option != "Help":
                            print(option + " is not an option")
                            option = ""
                            
                        if option == "Roll":
                            print("Let's see your roll!")
                            roll1 = roll()
                            roll2 = roll()
                            self.lastRoll = roll1 + roll2
                            print("You rolled a " + str(roll1) + " and a " + str(roll2))
                            if roll1 == roll2:
                                doubles += 1
                                if doubles == 3:
                                    print("Three doubles in a row. You go to Jail!")
                                    doubles = 0
                                    player.jailed = True
                                    player.position = 10
                                else:
                                    print("You rolled doubles! You will take another turn after this")
                                    print("Be carfull though. If you roll doubles 3 times in a row, you go to Jail")
                                    self.rounds -= 1
                            
                            if player.jailed == False:
                                player.move(self.lastRoll)
                                tile = self.tiles[player.position]
                                print(player.name + " landed on " + tile.name)
                                
                                t = tile.typeOfTile
                                if t == 0:
                                    if tile.prop in self.bank.properties:
                                        print("This property is owned by the bank and can be bought for $" + str(tile.prop.cost) + " or auctioned to the highest bidder")
                                        option1 = ""
                                        while option1 == "":
                                            print("You can Buy, Auction, or type \"Help\" to get information on your options")
                                            option1 = input("What do you want to do? \n")
                                            if option1 != "Buy" and option1 != "Auction" and option1 != "Help":
                                                print(option + " is not an option")
                                                option1 = ""
                                                    
                                            if option1 == "Buy":
                                                if player.cash < tile.prop.cost:
                                                    print("You don't have enough for this property")
                                                    option1 = ""
                                                else:
                                                    player.cash -= tile.prop.cost
                                                    self.bank.properties.remove(tile.prop)
                                                    player.properties += [tile.prop]
                                                    tile.prop.owner = player
                                                    print(player.name + " bought " + tile.prop.name + " for $" + str(tile.prop.cost) + " and now has $" + str(player.cash))
                                                
                                            if option1 == "Auction":
                                                highestBid = 0
                                                high = player
                                                droppedOut = []
                                                turn = 0
                                                while len(droppedOut) + 1 < len(self.players):
                                                    if (turn % len(self.players)) in droppedOut:
                                                        turn += 1
                                                    print(high.name + " is the highest bidder with $" + str(highestBid))
                                                    auction = ""
                                                    while auction == "":
                                                        print(self.players[turn % len(self.players)].name + ", what do you want to do?")
                                                        auction = input("You can bid a higher amount or Drop Out \n")
                                                        if auction == "Drop Out":
                                                            droppedOut += [turn % len(self.players)]
                                                            turn += 1
                                                        else:
                                                            try:
                                                                auction = int(auction)
                                                                if self.players[turn % len(self.players)].cash < auction:
                                                                    print("You don't have that much!")
                                                                    auction = ""
                                                                elif auction <= highestBid:
                                                                    print("Must bid a value more than $" + str(highestBid) + " or Drop Out")
                                                                    auction = ""
                                                                else:
                                                                    highestBid = auction
                                                                    high = self.players[turn % len(self.players)]
                                                                    turn += 1
                                                            except(ValueError):
                                                                print("Not valid input, try again")
                                                                auction = ""
                                                print(high.name + " won the auction for " + tile.prop.name + " for $" + str(highestBid))
                                                high.cash -= highestBid
                                                self.bank.properties.remove(tile.prop)
                                                high.properties += [tile.prop]
                                                tile.prop.owner = high
                                    else:
                                        for p in self.players:
                                            if p != player:
                                                if tile.prop in p.properties:
                                                    if not tile.prop.mortgage:
                                                        rent = tile.prop.calcRent(self.lastRoll)
                                                        print(p.name + " ownes this property and you owe $" + str(rent) + " to them")
                                                        if rent > player.cash:
                                                            print("You dont have enough money!")
                                                            option1 = ""
                                                            while option1 == "":
                                                                print("You can Pay, Manage, Trade, Declare Bankrupcy or type \"Help\" to get information on your options")
                                                                option1 = input("What do you want to do? \n")
                                                                if option1 != "Pay" and option1 != "Declare Bankrupcy" and option1 != "Manage" and option1 != "Trade" and option1 != "Help":
                                                                    print(option1 + " is not an option")
                                                                    option1 = ""
                                                                if option1 == "Pay":
                                                                    if player.cash >= 100:
                                                                        player.cash -= 100
                                                                        self.FPC += 100
                                                                    else:
                                                                        print("Still not enough money")
                                                                        option1 = ""
                                                                if option1 == "Declare Bankrupcy":
                                                                    self.rounds -= 1
                                                                    p.cash += player.cash
                                                                    auctionList = player.properties
                                                                    self.players.remove(player)
                                                                    if len(self.players) == 1:
                                                                        gameOver = True
                                                                    else:
                                                                        for prop in auctionList:
                                                                            print("Time to auction " + prop.name)
                                                                            highestBid = 0
                                                                            high = self.players[0]
                                                                            droppedOut = []
                                                                            turn = 0
                                                                            while len(droppedOut) + 1 < len(self.players):
                                                                                if (turn % len(self.players)) in droppedOut:
                                                                                    turn += 1
                                                                                print(high.name + " is the highest bidder with $" + str(highestBid))
                                                                                auction = ""
                                                                                while auction == "":
                                                                                    print(self.players[turn % len(self.players)].name + ", what do you want to do?")
                                                                                    auction = input("You can bid a higher amount or Drop Out \n")
                                                                                    if auction == "Drop Out":
                                                                                        droppedOut += [turn % len(self.players)]
                                                                                        turn += 1
                                                                                    else:
                                                                                        try:
                                                                                            auction = int(auction)
                                                                                            if self.players[turn % len(self.players)].cash < auction:
                                                                                                print("You don't have that much!")
                                                                                                auction = ""
                                                                                            elif auction <= highestBid:
                                                                                                print("Must bid a value more than $" + str(highestBid) + " or Drop Out")
                                                                                                auction = ""
                                                                                            else:
                                                                                                highestBid = auction
                                                                                                high = self.players[turn % len(self.players)]
                                                                                                turn += 1
                                                                                        except(ValueError):
                                                                                            print("Not valid input, try again")
                                                                                            auction = ""
                                                                            print(high.name + " won the auction for " + tile.prop.name + " for $" + str(highestBid))
                                                                            high.cash -= highestBid
                                                                            self.bank.properties.remove(tile.prop)
                                                                            high.properties += [tile.prop]
                                                                            tile.prop.owner = high
                                                                if option1 == "Manage":
                                                                    print("do")
                                                                    option1 = ""
                                                                if option1 == "Trade":
                                                                    print("do")
                                                                    option1 = ""
                                                                if option1 == "Help":
                                                                    print("do")
                                                                    option1 = ""
                                                        else:
                                                            player.cash -= rent
                                                            p.cash += rent
                                                                                                                
                                elif t == 1:
                                    print("do")
                                elif t == 2:
                                    print("do")
                                elif t == 3:
                                    print(player.name + " landed on Free Parking and got $" + str(self.FPC))
                                    player.cash += self.FPC
                                    self.FPC = 0
                                elif t == 4:
                                    print(player.name + " is going to Jail! Don't pass Go!, don't collect $200!")
                                    player.jailed = True
                                    player.position = 10
                                elif t == 5:
                                    print(player.name + " is just visiting Jail")
                                elif t == 6:
                                    print(player.name + " landed on Go! and collected $200!")
                                elif t == 7:
                                    print(player.name + " landed on Income Tax and owes $200! The money is going to Free Parking")
                                    if player.cash < 200:
                                        print("You dont have enough money!")
                                        option1 = ""
                                        while option1 == "":
                                            print("You can Pay, Manage, Trade, Declare Bankruptcy or type \"Help\" to get information on your options")
                                            option1 = input("What do you want to do? \n")
                                            if option1 != "Pay" and option1 != "Declare Bankruptcy" and option1 != "Manage" and option1 != "Trade" and option1 != "Help":
                                                print(option1 + " is not an option")
                                                option1 = ""
                                            if option1 == "Pay":
                                                if player.cash >= 200:
                                                    player.cash -= 200
                                                    self.FPC += 200
                                                else:
                                                    print("Still not enough money")
                                                    option1 = ""
                                            if option1 == "Declare Bankruptcy":
                                                self.rounds -= 1
                                                self.FPC += player.cash
                                                auctionList = player.properties
                                                self.players.remove(player)
                                                if len(self.players) == 1:
                                                    gameOver = True
                                                else:
                                                    for prop in auctionList:
                                                        print("Time to auction " + prop.name)
                                                        highestBid = 0
                                                        high = self.players[0]
                                                        droppedOut = []
                                                        turn = 0
                                                        while len(droppedOut) + 1 < len(self.players):
                                                            if (turn % len(self.players)) in droppedOut:
                                                                turn += 1
                                                            print(high.name + " is the highest bidder with $" + str(highestBid))
                                                            auction = ""
                                                            while auction == "":
                                                                print(self.players[turn % len(self.players)].name + ", what do you want to do?")
                                                                auction = input("You can bid a higher amount or Drop Out \n")
                                                                if auction == "Drop Out":
                                                                    droppedOut += [turn % len(self.players)]
                                                                    turn += 1
                                                                else:
                                                                    try:
                                                                        auction = int(auction)
                                                                        if self.players[turn % len(self.players)].cash < auction:
                                                                            print("You don't have that much!")
                                                                            auction = ""
                                                                        elif auction <= highestBid:
                                                                            print("Must bid a value more than $" + str(highestBid) + " or Drop Out")
                                                                            auction = ""
                                                                        else:
                                                                            highestBid = auction
                                                                            high = self.players[turn % len(self.players)]
                                                                            turn += 1
                                                                    except(ValueError):
                                                                        print("Not valid input, try again")
                                                                        auction = ""
                                                        print(high.name + " won the auction for " + tile.prop.name + " for $" + str(highestBid))
                                                        high.cash -= highestBid
                                                        self.bank.properties.remove(tile.prop)
                                                        high.properties += [tile.prop]
                                                        tile.prop.owner = high
                                    else:
                                        player.cash -= 200
                                        self.FPC += 200
                                        
                                elif t == 8:
                                    print(player.name + " landed on Luxury Tax and owes $100! The money is going to Free Parking")
                                    if player.cash < 100:
                                        print("You dont have enough money!")
                                        option1 = ""
                                        while option1 == "":
                                            print("You can Pay, Manage, Trade, Declare Bankruptcy or type \"Help\" to get information on your options")
                                            option1 = input("What do you want to do? \n")
                                            if option1 != "Pay" and option1 != "Declare Bankruptcy" and option1 != "Manage" and option1 != "Trade" and option1 != "Help":
                                                print(option1 + " is not an option")
                                                option1 = ""
                                            if option1 == "Pay":
                                                if player.cash >= 100:
                                                    player.cash -= 100
                                                    self.FPC += 100
                                                else:
                                                    print("Still not enough money")
                                                    option1 = ""
                                            if option1 == "Declare Bankruptcy":
                                                self.rounds -= 1
                                                self.FPC += player.cash
                                                auctionList = player.properties
                                                self.players.remove(player)
                                                if len(self.players) == 1:
                                                    gameOver = True
                                                else:
                                                    for prop in auctionList:
                                                        print("Time to auction " + prop.name)
                                                        highestBid = 0
                                                        high = self.players[0]
                                                        droppedOut = []
                                                        turn = 0
                                                        while len(droppedOut) + 1 < len(self.players):
                                                            if (turn % len(self.players)) in droppedOut:
                                                                turn += 1
                                                            print(high.name + " is the highest bidder with $" + str(highestBid))
                                                            auction = ""
                                                            while auction == "":
                                                                print(self.players[turn % len(self.players)].name + ", what do you want to do?")
                                                                auction = input("You can bid a higher amount or Drop Out \n")
                                                                if auction == "Drop Out":
                                                                    droppedOut += [turn % len(self.players)]
                                                                    turn += 1
                                                                else:
                                                                    try:
                                                                        auction = int(auction)
                                                                        if self.players[turn % len(self.players)].cash < auction:
                                                                            print("You don't have that much!")
                                                                            auction = ""
                                                                        elif auction <= highestBid:
                                                                            print("Must bid a value more than $" + str(highestBid) + " or Drop Out")
                                                                            auction = ""
                                                                        else:
                                                                            highestBid = auction
                                                                            high = self.players[turn % len(self.players)]
                                                                            turn += 1
                                                                    except(ValueError):
                                                                        print("Not valid input, try again")
                                                                        auction = ""
                                                        print(high.name + " won the auction for " + tile.prop.name + " for $" + str(highestBid))
                                                        high.cash -= highestBid
                                                        self.bank.properties.remove(tile.prop)
                                                        high.properties += [tile.prop]
                                                        tile.prop.owner = high
                                    else:
                                        player.cash -= 100
                                        self.FPC += 100
                    option3 = ""
                    while option3 == "":
                        print("You Manage, Trade, End Turn, or type \"Help\" to get information on your options")
                        option3 = input("What do you want to do? \n")
                        if option3 != "End Turn" and option3 != "Manage" and option3 != "Trade" and option3 != "Help":
                            print(option3 + " is not an option")
                            option3 = ""
                        if option3 == "Trade":
                            print("do")
                            option3 = ""
                        if option3 == "Manage":
                            print("do")
                            option3 = ""
                        


Main(3)
