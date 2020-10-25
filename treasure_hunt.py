# -*- coding: utf-8 -*-
"""
Created on Mon Aug  3 12:14:55 2020

@author: Jason
"""


import turtle
import tkinter
import random
import math
import time

delay = 0.1
score = 0

wn = turtle.Screen()
wn.bgcolor("black")
wn.title("Treasure Hunt")
wn.setup(width = 700, height = 700)
wn.tracer(3)

#Register shapes/icons
icons = ["creature.gif", "wall.gif", "player.gif", "treasure.gif", "down.gif", "up.gif", "left.gif", "right.gif"]
for icon in icons:
    turtle.register_shape(icon)

#create pen
class Pen(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("wall.gif")
        self.color("white")
        self.penup()
        self.speed(0)

#create player
class Player(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("player.gif")
        self.penup()
        self.speed(0)
        self.gold = 0

    def go_up(self):
        move_to_x = self.xcor()
        move_to_y = self.ycor() + 24
        self.shape("up.gif")

        if (move_to_x, move_to_y) not in walls:
            self.goto(move_to_x, move_to_y)

    def go_down(self):
        move_to_x = self.xcor()
        move_to_y = self.ycor() - 24
        self.shape("down.gif")

        if (move_to_x, move_to_y) not in walls:
            self.goto(move_to_x, move_to_y)

    def go_left(self):
        move_to_x = self.xcor() - 24
        move_to_y = self.ycor()
        self.shape("left.gif")

        if (move_to_x, move_to_y) not in walls:
            self.goto(move_to_x, move_to_y)

    def go_right(self):
        move_to_x = self.xcor() + 24
        move_to_y = self.ycor()
        self.shape("right.gif")

        if (move_to_x, move_to_y) not in walls:
            self.goto(move_to_x, move_to_y)

    def collide(self, other):
        a = self.xcor() - other.xcor()
        b = self.ycor() - other.ycor()
        distance = math.sqrt((a**2)+(b**2))

        if distance < 5:
            return True
            
        else:
            return False

#create creature
class Creature(turtle.Turtle):
    def __init__(self, x, y):
        turtle.Turtle.__init__(self)
        self.shape("creature.gif")
        self.penup()
        self.speed(1)
        self.goto(x, y)
        self.direction = random.choice(["up", "down", "left", "right"])

    def move(self):
        if self.direction == "up":
            dx = 0
            dy = 24
        
        elif self.direction == "down":
            dx = 0
            dy = -24

        elif self.direction == "left":
            dx = -24
            dy = 0

        elif self.direction == "right":
            dx = 24
            dy = 0

        else:
            dx = 0
            dy = 0

        #move in direction of player
        if self.aggro(player):
            if player.xcor() < self.xcor():
                dx = -24

            elif player.xcor() > self.xcor():
                dx = 24

            elif player.ycor() < self.ycor():
                dy = -24

            elif player.ycor() > self.ycor():
                dy = 24

        #d = delta = displacement
        move_to_x = self.xcor() + dx
        move_to_y = self.ycor() + dy

        if (move_to_x, move_to_y) not in walls:
            self.goto(move_to_x, move_to_y)
            
        else:
            self.direction = random.choice(["up", "down", "left", "right"])

    def aggro(self, other):
        a = self.xcor() - other.xcor()
        b = self.ycor() - other.ycor()
        distance = math.sqrt((a**2)+(b**2))
        
        if distance < 120:
            return True
        else:
            return False
                

#create treasure
class Treasure(turtle.Turtle):
    def __init__(self, x, y):
        turtle.Turtle.__init__(self)
        self.shape("treasure.gif")
        self.penup()
        self.speed(0)
        self.goto(x, y)
        self.gold = 10

    def consumed(self):
        self.hideturtle()

#create levels list
levels = [""]

#define first level
first_level = [
"XXXXXXXXXXXXXXXXXXXXXXXXX",
"XXXXXXX                XX",
"XXXXXXX                XX",
"XXXXXXX T      X XX  XXXX",
"XXXXXXX  C     X XX  XXXX",
"XXXXXXXXXX             XX",
"XXXX   XXX             XX",
"X       XX  XXXXX   XXXXX",
"X       XX  XXXXXXXXXXXXX",
"XX      XX  XXXXXXXXXXXXX",
"XXXX    XX   XXXXXXXXXXXX",
"XXXX           XXXXXXXXXX",
"XXXX                    X",
"XXXX  XXXXXXXXXXX       X",
"XXXX  XXXXXXXXXXX  XXXXXX",
"XXXX  XXXXXXXXXXX  XXXXXX",
"XXXX  XXXXXXXXXX      XXX",
"XXXX               T  XXX",
"XXXX  XXXXXXXXXX      XXX",
"XXXX  XXXXXXXXXX C    XXX",
"XXXX     XXXXXXXXXX  XXXX",
"XXXX           XXXX  XXXX",
"X       X      XXXX  XXXX",
"XXXX                    X",
"XXXX           XXXX    TX",
"XXXXXXXXXXXXXXXXXXXXXXXXX",
]

#add tunnel level
levels.append(first_level)

#create level setup function
def setup_tunnel(level):
    #nested loop
    for y in range(len(level)):
        for x in range(len(level[y])):
            character = level[y][x]
            treasure = level[y][x]
            screen_x = -288 + (x * 24)
            screen_y = 288 - (y * 24)

            if character == "X":
                pen.goto(screen_x, screen_y)
                pen.shape("wall.gif")
                pen.stamp()
                #add walls list
                walls.append((screen_x, screen_y))

            if character == "C":
                creatures.append(Creature(screen_x, screen_y))

            if treasure == "T":
                #place treasure at location
                treasures.append(Treasure(screen_x, screen_y))

#create class instance
pen = Pen()
score = Pen()
score.hideturtle()
score.goto(0, 300)
player = Player()

#create list constructors for creatures & treasures
creatures = []
treasures = []
walls = []

#setup levels
setup_tunnel(levels[1])

#keyboard bindings
turtle.listen()
turtle.onkeypress(player.go_up, "w")
turtle.onkeypress(player.go_down, "s")
turtle.onkeypress(player.go_left, "a")
turtle.onkeypress(player.go_right, "d")

wn.tracer(10)
game_loop = True
#game loop
while game_loop:

    for treasure in treasures:
        if player.collide(treasure):
            player.gold += treasure.gold
            print("Player's gold increased by {}!".format(player.gold))
            score.clear()
            score.write("Gold: {}".format(player.gold), align = "center", font = ("Arial", 24, "normal"))
            treasure.consumed()
            treasures.remove(treasure)

    for creature in creatures:
        creature.move()
        #time.sleep(delay)
        
##        if creature.aggro(player):
##            print("Aggro")
            
        if player.collide(creature):
            print("Game Over!")
            score.clear()
            score.write("Game Over!", align = "center", font = ("Arial", 24, "normal"))
            game_loop = False
            break

    #set boundaries
    if player.ycor() > 300:
        player.goto(player.xcor(), player.ycor()-24)
        
    if player.ycor() < -324:
        player.goto(player.xcor(), player.ycor()+24)

    if player.xcor() > 300:
        player.goto(player.xcor()-24, player.ycor())

    if player.xcor() < -300:
        player.goto(player.xcor()+24, player.ycor())

    wn.update()



