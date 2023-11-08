import serial
from turtle import Turtle,Screen
import random
import math
import time
import pygame

pygame.init()

pygame.mixer.init()

screen = Screen()
screen.bgcolor("black")
screen.bgpic("back.gif")
screen.title("Space Invaders!")
screen.tracer(0)

background_music = pygame.mixer.Sound("stranger-things-124008.mp3")
background_music.play(-1)
pen = Turtle()
pen.speed(0)
pen.color("white")
pen.penup()
pen.hideturtle()
player = Turtle()
player.speed(0)
player.penup()
player.shape("triangle")
player.color("yellow")
player.setposition(0,-270)
player.setheading(90)
bullet = Turtle()#for the bullet
bullet.speed(0)
bullet.penup()
bullet.shape('triangle')
bullet.shapesize(0.5,0.5)
bullet.color("red")
bullet.hideturtle()
bullet.setheading(90)
bullet_state = "ready"
ser = serial.Serial('com7',9600)
ser.flushInput()
enemies = []
TheGameIsRunning = True
for i in range(10):
    enemies.append(Turtle())
for enemy in enemies:
    enemy.speed(0)
    enemy.penup()
    enemy.shape('circle')
    enemy.color("red")
    enemy.goto(-280,260)
    enemy.setheading(0)
    enemy.goto(random.randint(-270,270),random.randint(200,265))
def left():
    player.setx(player.xcor() - 10)
    if bullet_state == "ready":
        bullet.goto(player.xcor(),player.ycor() + 10)
        bullet.hideturtle()
    if player.xcor() < -270:
        player.setx(-270)
def right():
    player.setx(player.xcor()+10)
    if bullet_state == "ready":
        bullet.goto(player.xcor(),player.ycor()+10)
        bullet.hideturtle()
    if player.xcor() > 270:
        player.setx(270)
def shoot():
    global bullet_state
    if bullet_state == "ready":
        bullet.goto(player.xcor(),player.ycor()+10)
        bullet_state = "fire"
        bullet.showturtle()
        for i in range(54):
            bullet.sety(bullet.ycor()+2)
score = 0
enemy_speed = 10
num_enemies = 10
while True:
    pen.goto(-280,270)
    pen.write("Score: ",font=("Courier",14,"normal"))
    pen.goto(-215,270)
    pen.write(score,font=("Courier",14,"normal"))
    ser_bytes = ser.readline()
    decoded_bytes = ser_bytes[0:len(ser_bytes)-2].decode("utf-8")#extracts the important data
    print(decoded_bytes)
    if decoded_bytes == "left":
        left()
    elif decoded_bytes == "right":
        right()
    elif decoded_bytes == "down":
        shoot()
    if bullet_state == "fire":
        bullet.showturtle()
        for i in range(54):
            bullet.sety(bullet.ycor() + 1)
    if bullet.ycor() > 265:
        bullet.hideturtle()
        bullet_state = "ready"
        bullet.goto(player.xcor(),player.ycor()+10)
    def collision(ob1,ob2):
        collision=math.sqrt(math.pow(ob1.xcor()-ob2.xcor(),2)+math.pow(ob1.ycor()-ob2.ycor(),2))#calculates the distance between the 2 objects using the pythagorean theoram
        if collision < 25:
            return True
        else:
            return False
    for enemy in enemies:
        if TheGameIsRunning:
            enemy.forward(enemy_speed)
            if enemy.xcor() > 270:
                enemy.right(90)
                enemy.forward(20)
                enemy.right(90)
                bullet.forward(enemy_speed)
            elif enemy.xcor() < -270:
                enemy.left(90)
                enemy.forward(20)
                enemy.left(90)
                bullet.forward(enemy_speed)
            if collision(bullet,enemy):
                enemy.sety(1000)
                bullet.hideturtle()
                bullet_state = "ready"
                pen.clear()
                score += 30
                enemy_speed += 1
                num_enemies -= 1
                bullet.goto(0,0)
            elif collision(enemy,player):
                bullet.hideturtle()
                player.hideturtle()
                for enemy in enemies:
                    enemy.hideturtle()
                pen.clear()
                pen.setposition(-300,-50)
                pen.write("Game Over!",font=("Courier",80,"bold"))
                pen.setposition(-300,-100)
                pen.write("Score: ",font=("Courier",65,"bold"))
                pen.setposition(50,-100)
                pen.write(score,font=("Courier",65,"bold"))
                TheGameIsRunning = False
            if enemy_speed > 20:
                enemy_speed = 20
            if enemy.ycor() < 420 and enemy.ycor() > 300:
                enemy.sety(1000)
    if num_enemies == 0:
        bullet.hideturtle()
        player.hideturtle()
        for enemy in enemies:
            enemy.hideturtle()
        pen.clear()
        pen.setposition(-300,-50)
        time.sleep(0.02)
        pen.write("You Win!",font=("Courier",80,"bold"))
        TheGameIsRunning = False
    screen.update()