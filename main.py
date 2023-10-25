import serial
from turtle import Turtle,Screen
import random
import math
import time
screen = Screen()#for screen
screen.bgcolor("black")
screen.title("Space Invaders!")
screen.tracer(0)
pen = Turtle()#pen for displaying score, 'game over', 'you win'.
pen.speed(0)
pen.color("white")
pen.penup()
pen.hideturtle()
player = Turtle()#for player
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
ser = serial.Serial('com7',9600)#sets the serial port and baud rate
ser.flushInput()
enemies = []
TheGameIsRunning = True
for i in range(10):# creates a turtle 10 times
    enemies.append(Turtle())
for enemy in enemies:#for every enemy these are the things it should do
    enemy.speed(0)
    enemy.penup()
    enemy.shape('circle')
    enemy.color("red")
    enemy.goto(-280,260)
    enemy.setheading(0)
    enemy.goto(random.randint(-270,270),random.randint(200,265))
def left():#for making the player go left, basically decreases the x coor, however if it tries to go out of the screen then it will not allow the player to go more left
    player.setx(player.xcor() - 10)
    if bullet_state == "ready":
        bullet.goto(player.xcor(),player.ycor() + 10)
        bullet.hideturtle()
    if player.xcor() < -270:
        player.setx(-270)
def right():#for making the player go right, basically increases the x coor, however if it tries to go out of the screen then it will not allow the player to go more right
    player.setx(player.xcor()+10)
    if bullet_state == "ready":
        bullet.goto(player.xcor(),player.ycor()+10)
        bullet.hideturtle()
    if player.xcor() > 270:
        player.setx(270)
def shoot():
    global bullet_state
    if bullet_state == "ready":#if bullet state ready then only will it shoot and change the state to fire, otherwise not
        bullet.goto(player.xcor(),player.ycor()+10)
        bullet_state = "fire"
        bullet.showturtle()
        for i in range(54):
            bullet.sety(bullet.ycor()+2)
score = 0
enemy_speed = 10
num_enemies = 10
while True:
    pen.goto(-280,270)#displays score
    pen.write("Score: ",font=("Courier",14,"normal"))
    pen.goto(-215,270)
    pen.write(score,font=("Courier",14,"normal"))
    ser_bytes = ser.readline()#reads incoming data from the serial port
    decoded_bytes = ser_bytes[0:len(ser_bytes)-2].decode("utf-8")#extracts the important data
    print(decoded_bytes)
    if decoded_bytes == "left":#calls certain functions when reads different things from the serial port
        left()
    elif decoded_bytes == "right":
        right()
    elif decoded_bytes == "down":
        shoot()
    if bullet_state == "fire":#if bullet state is in the fire mode, then the bullet should fire
        bullet.showturtle()
        for i in range(54):
            bullet.sety(bullet.ycor() + 1)
    if bullet.ycor() > 265:# if bullet goes of the screen then the state will be set to ready again, so that the player can fire the bullet
        bullet.hideturtle()
        bullet_state = "ready"
        bullet.goto(player.xcor(),player.ycor()+10)
    def collision(ob1,ob2):#function checks whether 2 objects have collided or not
        collision=math.sqrt(math.pow(ob1.xcor()-ob2.xcor(),2)+math.pow(ob1.ycor()-ob2.ycor(),2))#calculates the distance between the 2 objects using the pythagorean theoram
        if collision < 25:#cheks if the distance between the 2 objects falls under a certain value and gives a boolean value based on that
            return True
        else:
            return False
    for enemy in enemies:# for every enemy:
        if TheGameIsRunning:# if the the game is running
            enemy.forward(enemy_speed)#enemy moves in a zig-zag pattern like the the enemies in the original space invaders do
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
            if collision(bullet,enemy):#if the bullet and the enemy have collided, then that enemy will disappear and the number of enemies will decrease and the bullet state will be set to ready
                enemy.sety(1000)
                bullet.hideturtle()
                bullet_state = "ready"
                pen.clear()
                score += 30
                enemy_speed += 1
                num_enemies -= 1
                bullet.goto(0,0)
            elif collision(enemy,player):#if the player and one of the enemies collide then the game is over.
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
    if num_enemies == 0:#if all the enemies are dead then the player wins.
        bullet.hideturtle()
        player.hideturtle()
        for enemy in enemies:
            enemy.hideturtle()
        pen.clear()
        pen.setposition(-300,-50)
        time.sleep(0.02)
        pen.write("You Win!",font=("Courier",80,"bold"))
        TheGameIsRunning = False
    screen.update()#updates the screen
