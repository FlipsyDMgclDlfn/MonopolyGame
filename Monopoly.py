from random import *

def roll():
    return randint(1,6)

class Player:
    def __init__(self, name, color, startingCash):
        self.name = name
        self.color = color
        self.cash = startingCash
        self.position = 0

    def move(self, roll):
        self.positon += roll

class Main:
    def __init__(self, numOfPlayers, startingCash = 1500):
        self.players = []
        self.turn = 0
        self.FPC = 0
        for i in range(0, numOfPlayers):
            name = input("Enter Player " + str(i+1) + "'s name: ")
            color = input("Hi " + name + "! Please choose a color: ")
            self.players += [Player(name, color, startingCash)]
        print("Lets see the order of play!")
        shuffle(self.players)
        for i in range(0, numOfPlayers):
            if i == 0:
                print(str(self.players[i].name) + " goes 1st")
            elif i == 1:
                print(str(self.players[i].name) + " goes 2nd")
            elif i == 2:
                print(str(self.players[i].name) + " goes 3rd")
            else:
                print(str(self.players[i].name) + " goes " + str(i+1) + "th")

Main(4)
