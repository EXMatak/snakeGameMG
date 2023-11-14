#region DEFINICE PROMENNYCH
import random
import time
import turtle

colors = ["blue", "red", "green", "pink", "yellow", "dark slate blue", "lavender"]  # pole na nahodne vybirani barev
score = 0

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
snake.goto(100, 0)
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

# zapamatuj si kolik segmentu mas
segments = []
coordinates = []
#endregion

#region DEFINICE FUNKCI
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
    snake.forward(20)

def clearSegments():
    for segment in segments:
        segment.clear()
        segment.reset()
    segments.clear()

def roundToTwenty(number):
    return ((int(number) + 19) // 20) * 20

def death():
    global score
    clearSegments()
    coordinates.clear()
    snake.goto(0, 0)
    snake.direction = "stop"
    pen.clear()
    pen.color("red")
    pen.goto(0, 260)
    pen.write(f"YOU DIED!", align="center", font=("calibri", 24, "bold"))
    window.update()
    score = 0
    time.sleep(1)


def writeScore():
    global score
    pen.color("yellow")
    pen.clear()
    pen.write(f"Score: {score}", align="center", font=("calibri", 24, "bold"))

def testUmrti():
    global score
    if [roundToTwenty(snake.xcor()), roundToTwenty(snake.ycor())] in coordinates[:-1]:
        death()
        print("umrel sam na sebe")
    
    if snake.xcor() > 290 or snake.xcor() < -290 or snake.ycor() > 290 or snake.ycor() < -290:
        death()
        print("umrel na hranice")
    writeScore()


def testJidlo():
    """
    Funkce pro testování, zda hráč snědl jídlo a provedení akcí v případě, že hráč jídlo snědl.
    """
    global segment
    global score
    if snake.distance(food) < 20:
        score += 1
        barvaHada = random.choice(colors)    # ac se muze jevit, ze toto ve hre zpusobuje bug, ze se nemeni barva celeho hada, neni to tak
        snake.color(barvaHada)               # tato implemetace simuluje jak se jablko hadovi dostava "do bricha"
        segment.color(barvaHada)
        jidloX = random.randint(-13, 13) * 20
        jidloY = random.randint(-13, 13) * 20
        food.goto(jidloX, jidloY)
        writeScore()
#endregion

#region MAIN LOOP A GAME LOOP

window.listen()
window.onkeypress(up, "Up")
window.onkeypress(right, "Right")
window.onkeypress(down, "Down")
window.onkeypress(left, "Left")
while True:
    testUmrti()

    # udelej novej segment a pridej ho k listu
    segment = turtle.Turtle()
    segment.shape("square")
    segment.color("white")
    segment.penup()
    segments.append(segment)
    segment.goto(snake.xcor(), snake.ycor())
    coordinates.append([roundToTwenty(snake.xcor()), roundToTwenty(snake.ycor())])

    if len(segments) > score:
        # maz posledni segment, pokud je delsi nez score (cim vetsi score, tim delsi had)
        segments[0].clear()
        segments[0].reset()
        segments.pop(0)
        coordinates.pop(0)


    #region DEBUG TOOLS
    # if [int(snake.xcor()), int(snake.ycor())] in poleSouradnic[:-1]:
    #     print("Aktualni souradnice je v poli")
    # else:
    #     print("Aktualni souradnice neni v poli")

    # print(f"X:{roundToTwenty(snake.xcor())} ; Y:{roundToTwenty(snake.ycor())}")
    # print(coordinates)
    # print(segments)
    #endregion
    
    move()

    if score < 20:
        time.sleep(0.2 - (0.01 * score))


    window.update()
    testJidlo()
#endregion