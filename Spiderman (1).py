import cv2
import turtle

IMAGE = "spiderman.png"
img = cv2.imread(IMAGE)

if img is None:
    print("Image not found!")
    exit()

height = 700
ratio = height / img.shape[0]
width = int(img.shape[1] * ratio)
img = cv2.resize(img, (width, height))
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

_, thresh = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY_INV)
contours, _ = cv2.findContours(
    thresh,
    cv2.RETR_EXTERNAL,
    cv2.CHAIN_APPROX_NONE
)


contours = [c for c in contours if cv2.contourArea(c) > 15]


contours = sorted(contours, key=cv2.contourArea, reverse=True)

screen = turtle.Screen()
screen.bgcolor("white")
screen.setup(width=800, height=575)
screen.tracer(1,5)  

pen = turtle.Turtle()
pen.speed(3)
pen.hideturtle()
pen.color("black")
pen.pensize(1)

scale = 0.8

UPDATE_EVERY = 3


def map_point(px, py):
    
    tx = (px - width / 2) * scale
    ty = (height / 2 - py) * scale  
    return tx, ty

point_counter = 0
for contour in contours:
    points = contour.reshape(-1, 2)  #

    if len(points) < 2:
        continue

    x0, y0 = map_point(points[0][0], points[0][1])
    pen.penup()
    pen.goto(x0, y0)
    pen.pendown()
    pen.begin_fill()

    for px, py in points[1:]:
        x, y = map_point(px, py)
        pen.goto(x, y)

        point_counter += 1
        if point_counter % UPDATE_EVERY == 0:
            screen.update()

    pen.goto(x0, y0)  # close the shape
    pen.end_fill()
    screen.update()  # make sure this contour's fill shows before moving on

screen.tracer(0)
pen.speed(0)
turtle.done()