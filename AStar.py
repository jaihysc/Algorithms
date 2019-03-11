#Based on Coding train AStar https://www.youtube.com/watch?v=aKYlikFAV4k
#March 10, 2019
import pygame #Requires pygame
import math
import random

#Pygame config
fps = 30
width = 600
height = 600

pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("A*")
clock = pygame.time.Clock()

#Main variables
cols = 20 #Y
rows = 20 #X
grid = [] #Index as X Y

borderWidth = 1

w = (width - borderWidth) / cols
h = (height - borderWidth) / rows

random.seed()
class Cell():
    def __init__(self, cellX, cellY):
        self.x = cellX
        self.y = cellY

        self.f = 0
        self.g = 0
        self.h = 0
        
        self.neighbours = []
        self.previous = None

        self.isWall = False
        if random.randrange(5) == 0: #Randomly generate walls
            self.isWall = True

    def show(self, color):
        if self.isWall:
            color = (0, 0, 0)
        pygame.draw.rect(screen, color, (self.x*w + borderWidth, self.y*h + borderWidth, w - borderWidth, h - borderWidth))

    def addNeighbours(self, masterGrid):
        if self.x < cols - 1:
            self.neighbours.append(masterGrid[self.y][self.x + 1])
        if self.x > 0:
            self.neighbours.append(masterGrid[self.y][self.x - 1])

        if self.y < rows - 1:
            self.neighbours.append(masterGrid[self.y + 1][self.x])
        if self.y > 0:
            self.neighbours.append(masterGrid[self.y - 1][self.x])

        # #Diagonals
        # if self.x > 0 and self.y < rows - 1:
        #     self.neighbours.append(masterGrid[self.y + 1][self.x - 1]) #DL
        # if self.x < cols - 1 and self.y < rows - 1:
        #     self.neighbours.append(masterGrid[self.y + 1][self.x + 1]) #DR

        # if self.y > 0 and self.x > 0:
        #     self.neighbours.append(masterGrid[self.y - 1][self.x - 1]) #UL
        # if self.y > 0 and self.x < cols - 1:
        #     self.neighbours.append(masterGrid[self.y - 1][self.x + 1]) #UR

#Make 2D array
for i in range(rows):
    grid.append([Cell(0,0)] * cols)

for y in range(rows):
    for x in range(cols):
        grid[y][x] = Cell(x, y)
#These 2 fors above can be simplified into 1

#Make neighbours
for y in range(rows):
    for x in range(cols):
        grid[y][x].addNeighbours(grid)

openSet = [] #Nodes that NEED to be evaluated
closedSet = [] #Nodes FINISHED evaluating

start = grid[0][0] #Start location
end = grid[rows - 1][cols - 1] #Target destination

start.isWall = False
end.isWall = False

openSet.append(start) #Starting with start location

def itemIncluded(inputList, item):
    for i in range(len(inputList)):
        if inputList[i] == item:
            return True
    return False

def heuristic(a, c):
    #Calculate distance between the 2 points
    # #Pythagorium therum distance
    # #Use this when diagonals are on
    # #A
    # #|     \ S3
    # #| S1      \
    # #B ------------ C
    # #       S2
    # bx = a.x
    # by = c.y

    # s1 = c.y - a.y
    # s2 = c.x - bx
    # s3 = math.sqrt(math.pow(s1, 2) + math.pow(s2, 2))
    # return abs(s3)
    #Manhattan distance
    return abs(a.x - c.x) + abs(a.y - c.y)
#Draw
running = True
findPath = False
while running:
    #Keep loop running at right speed
    clock.tick(fps)

    #Process events
    for event in pygame.event.get():
        #Window close
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                findPath = True

    #Update - Logic
    if findPath == True:
        if openSet: #Keep evaluating as long as openset is not empty
            
            lowestIndex = 0 # Index of the best choice (lowest f score)
            for i in range(len(openSet)):
                if openSet[i].f < openSet[lowestIndex].f:
                    lowestIndex = i # If this one's f score is lower, this becomes the new lowestIndex

            current = openSet[lowestIndex]

            #Add / remove from open / closed sets
            openSet.remove(current)
            closedSet.append(current)

            #See if we reached the goal
            if current == end:
                #We done lads!
                print("Done")
                running = False

            for i in range(len(current.neighbours)):
                neighbour = current.neighbours[i]

                #Find if closed set contains neighbour
                if not itemIncluded(closedSet, neighbour) and not neighbour.isWall:
                    #Increase g score (cost)
                    tempG = current.g + 1

                    newPath = False
                    #Check if this item has been evaluated before in openset
                    if itemIncluded(openSet, neighbour):
                        #If so, is there a better g score?
                        if tempG < neighbour.g:
                            neighbour.g = tempG
                            newPath = True
                    else: #Discovered a new node
                        #Set the lowest G
                        neighbour.g = tempG
                        newPath = True
                        openSet.append(neighbour)
                
                    if newPath:
                        #Make an educated guess
                        neighbour.h = heuristic(neighbour, end) #This beauty right here is what makes it A*
                        neighbour.f = neighbour.g + neighbour.h #This is the total cost, compared between all path options
                        neighbour.previous = current
        else:
            print("No solution")
            break

    # Draw
    screen.fill((255, 255, 255))

    #Debugging
    for y in range(cols):
        for x in range(rows):
            grid[x][y].show((100, 100, 100))

    for i in range(len(closedSet)):
        closedSet[i].show((255, 0, 0))

    for i in range(len(openSet)):
        openSet[i].show((0, 255, 0))

    if findPath:
        #Draw path
        #Trace the path
        temp = current
        path = []
        path.append(temp)
        while temp.previous:
            path.append(temp.previous)
            temp = temp.previous

        for i in range(len(path)):
            path[i].show((0, 0, 255))

    pygame.display.flip() #Actually show the items to the screen
print("Press ENTER to exit")
input()
pygame.quit()