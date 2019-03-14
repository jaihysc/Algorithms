#March 10, 2019
import pygame #Requires pygame
import math
import random
import tensorflow as tf #Requires tensorflow

#Pygame config
fps = 30
width = 600
height = 600

pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Linear Regression")
clock = pygame.time.Clock()

#Screen variables
cols = 20 #Y
rows = 20 #X
grid = [] #Index as X Y

borderWidth = 1

gridWidth = (width - borderWidth) / cols
gridHeight = (height - borderWidth) / rows

#Main variables
xPoints = []
yPoints = []

#Create tf variables
random.seed()
m = tf.get_variable("m", random.randrange(1), dtype=tf.int32) #Watch the type of the variable
b = tf.get_variable("b", random.randrange(1), dtype=tf.int32)
#b = tf.Variable(random.randrange(1))
#Initialize the variables
SESSION = tf.Session()
SESSION.run(tf.global_variables_initializer())

tf.math.multiply(tf.constant([1, 2]), m)
input()

def normalize(val, max, min):
    return (val - min) / (max - min)

def deNormalize(val, max, min):
    return (val - min) * max

def predict(xArr):
    #convert x array into tensor
    xTens = tf.constant(xArr)
    print(xTens, m)
    #y = mx + b
    mx = tf.math.multiply(xTens, m)
    yTens = tf.math.add(mx, b) #Apply line formula to x
    return yTens

def loss(pred, labels):
    return pred.sub(labels).square().mean()


#Draw
running = True
while running:
    #Keep loop running at right speed
    clock.tick(fps)

    #Process events
    for event in pygame.event.get():
        #Window close
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            norXPoint = normalize(pygame.mouse.get_pos()[0], width, 0)
            norYPoint = normalize(pygame.mouse.get_pos()[1], height, 0)
            xPoints.append(norXPoint)
            yPoints.append(norYPoint)

    #Update - Logic

    # Draw
    screen.fill((255, 255, 255))

    #Only optimize if we have some variables
    if len(xPoints) > 1:
		# tf.tidy(() => {
		# 	yTens = tf.constant(yPoints)
		# 	optimizer.minimize(() => loss(predict(xPoints), yTens)) #Optimize with predict and loss
		# })
        pass
	
    # background(0, 0, 0)
    # stroke(255)
    # strokeWeight(8)
	
    #Denormalizes and draws the points
    for i in range(len(xPoints)):
        px = deNormalize(xPoints[i], width, 0)
        py = deNormalize(yPoints[i], height, 0)

        point(px, py)		

    #Don't forget to clean up!!
    #Take 2 points and draw it
    xs = [0, 1] # bottom and top
    ys = predict(xs)

    #Denormalize
    x1 = deNormalize(xs[0], width, 0)
    x2 = deNormalize(xs[1], width, 0)

    #Get the values of ys back from tensors
    result = SESSION.run(gg)
    
    lineY = ys.dataSync()
    y1 = deNormalize(lineY[0], height, 0) # switch 0, height around to make it perpendicular
    y2 = deNormalize(lineY[1], height, 0)

    # strokeWeight(1)
    # stroke(255, 0, 0)
    # line(x1, y1, x2, y2)

    ys.dispose()
    pygame.display.flip() #Actually show the items to the screen

print("Press ENTER to exit")
input()
pygame.quit()