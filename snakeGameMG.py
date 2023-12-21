# region DEFINICE PROMENNYCH
import random
import time
import turtle
import chime

colors = ["blue", "red", "green", "pink", "yellow", "dark slate blue", "lavender"]  # pole na nahodne vybirani barev
score = 19
highScore = 0

# setup okna
window = turtle.Screen()
window.title("○ Snake ○")
window.bgcolor("black")
window.setup(width=600, height=600)  # resolution
window.tracer(0)
# setup hada
snake = turtle.Turtle()
snake.shape("square")
snake.color("white")
snake.penup()
snake.goto(0, 0)
# setup jidla
food = turtle.Turtle()
food.penup()
food.goto(100, 100)
food.shape("circle")
food.color("red")
# setup textu nahore na score a smrt
pen = turtle.Turtle()
pen.color("yellow")
pen.hideturtle()
pen.penup()
pen.goto(0, 260)
pen.write(f"Score: {score}", align="center", font=("calibri", 24, "bold"))
# setup textu na highscore
highScoreDisplay = turtle.Turtle()
highScoreDisplay.color("yellow")
highScoreDisplay.hideturtle()
highScoreDisplay.penup()
highScoreDisplay.goto(0, -260)
highScoreDisplay.write(f"High Score: {highScore}", align="center", font=("calibri", 24, "bold"))

# endregion

# region DEFINICE FUNKCI

def saveHighScore():
    with open("highScoreMG.txt", "w") as file:
        file.write(str(highScore))

def loadHighScore():
    global highScore
    try:
        with open("highScoreMG.txt", "r") as file:
            highScore = int(file.read())
            print(highScore)
            print("score naloadovano")
            updateHighScore()
    except FileNotFoundError:
        print("nenalezeno")
        highScore = 0

def updateHighScore():
    highScoreDisplay.clear()
    highScoreDisplay.write(f"High Score: {highScore}", align="center", font=("calibri", 24, "bold"))

def up():
    if snake.heading() != 270:  # pokud hrac nekouka na primo druhou stranu, otoc se x4
        snake.setheading(90)


def right():
    if snake.heading() != 180:
        snake.setheading(0)


def down():
    if snake.heading() != 90:
        snake.setheading(270)


def left():
    if snake.heading() != 0:
        snake.setheading(180)


def move():  # pohyb dopredu
    previousPosition = snake.position()
    for member in body:
        currentPosition = member.position()
        member.setposition(previousPosition)
        previousPosition = currentPosition
    snake.forward(20)

def roundToTwenty(number):  # pouzite na gridy po dvaceti
    return ((int(number) + 19) // 20) * 20

def clearSnakeBody():
    global body
    for member in body:
        member.goto(1000, 1000)
    body.clear()

def death():  # proste funkce na smrt
    global score
    global highScore
    global body
    snake.goto(0, 0)
    snake.direction = "stop"
    pen.clear()
    pen.color("red")
    pen.goto(0, 260)
    pen.write(f"YOU DIED!", align="center", font=("calibri", 24, "bold"))
    window.update()
    if score > highScore:
        highScore = score
        updateHighScore()
        saveHighScore()
    score = 0
    clearSnakeBody()
    time.sleep(1)


def writeScore():  # zapisovani score
    global score
    pen.color("yellow")
    pen.clear()
    pen.write(f"Score: {score}", align="center", font=("calibri", 24, "bold"))


def testUmrti():  # zkousi jak smrt na borderu tak smrt na vlastni ocas
    #global score
    #if [roundToTwenty(snake.xcor()), roundToTwenty(snake.ycor())] in coordinates[:-1]:
    #    death()
    #    print("umrel sam na sebe")

    if snake.xcor() > 290 or snake.xcor() < -290 or snake.ycor() > 290 or snake.ycor() < -290:
        death()
        print("umrel na hranice")

    for member in body:
        if snake.distance(member) < 15:
            death()
            print("umrel sam na sebe")
    writeScore()


def testJidlo():
    """
    Funkce pro testování, zda hráč snědl jídlo a provedení akcí v případě, že hráč jídlo snědl.
    """
    # jinej komentar pro zkouseni jak se commentuje ve vscodu :D
    global score
    if snake.distance(food) < 20:
        score += 1
        barvaHada = random.choice(colors)  # ac se muze jevit, ze toto ve hre zpusobuje bug, ze se nemeni barva celeho hada, neni to tak
        snake.color(barvaHada)  # tato implemetace simuluje jak se jablko hadovi dostava "do bricha"
        chime.success()
        jidloX = random.randint(-13, 13) * 20
        jidloY = random.randint(-13, 13) * 20
        food.goto(jidloX, jidloY)
        teloHada()
        writeScore()

def teloHada():
    global body
    member = turtle.Turtle()
    member.penup()
    member.shape("square")
    member.color("white")
    member.setpos(snake.position())
    body.insert(0, member)

def sleep():
    global score
    if score < 20:
        return time.sleep(0.2 - (0.01 * score) + 0.02)
    else:
        return time.sleep(0.03)

def listenForKeyInputs():
    window.listen()  # poslouchani keypressu
    window.onkeypress(up, "Up")
    window.onkeypress(right, "Right")
    window.onkeypress(down, "Down")
    window.onkeypress(left, "Left")
# endregion

# region MAIN LOOP A GAME LOOP

loadHighScore()
body = []
listenForKeyInputs()
while True:
    testUmrti()
    testJidlo()
    move()
    window.update()
    sleep()
# endregion
