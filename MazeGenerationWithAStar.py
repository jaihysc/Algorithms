import pygame #Requires pygame
import math
import random

#Pygame configs---
fps = 500
width = 800
height = 700

pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Maze Generation w/ A*")
clock = pygame.time.Clock()
#End pygame configs---

#Program configs
cols = 50
rows = 50

colsSize = math.floor(width / cols) #X
rowsSize = math.floor(height / rows) #y

grid = []
AStarGrid = []

stack = []

random.seed()
class AStarCell():
    def __init__(self, cellX, cellY):
        self.x = cellX
        self.y = cellY

        self.f = 0
        self.g = 0
        self.h = 0
        
        self.neighbours = []
        self.previous = None

    def show(self, color, previous, line):
        if line:
            pygame.draw.line(screen, color, (previous.x * colsSize + colsSize / 2, previous.y * rowsSize + rowsSize / 2), (self.x * colsSize + colsSize / 2, self.y * rowsSize + rowsSize / 2))
        else:
            pygame.draw.rect(screen, color, (self.x * colsSize + 5, self.y * rowsSize + 5, colsSize - 10, rowsSize - 10))

    def addNeighbours(self, masterGrid, mazeGrid):
        #Check to see if there is an open path between the neighbours as defined by maze generation
        if self.y > 0 and (not mazeGrid[self.y][self.x].walls[0] and not mazeGrid[self.y - 1][self.x].walls[2]): #T
            self.neighbours.append(masterGrid[self.y - 1][self.x])

        if self.x < cols - 1 and (not mazeGrid[self.y][self.x].walls[1] and not mazeGrid[self.y][self.x + 1].walls[3]): #R
            self.neighbours.append(masterGrid[self.y][self.x + 1])

        if self.y < rows - 1 and (not mazeGrid[self.y][self.x].walls[2] and not mazeGrid[self.y + 1][self.x].walls[0]): #B
            self.neighbours.append(masterGrid[self.y + 1][self.x])

        if self.x > 0 and (not mazeGrid[self.y][self.x].walls[3] and not mazeGrid[self.y][self.x - 1].walls[1]): #L
            self.neighbours.append(masterGrid[self.y][self.x - 1])



class Cell():
    def __init__(self, selfX, selfY):
        self.x = selfX
        self.y = selfY
        self.walls = [True, True, True, True] #TRBL
        self.visited = False

    def show(self):
        x = self.x * colsSize
        y = self.y * rowsSize + 1

        if self.visited:
            color = (255, 20, 255)
            #pygame.draw.rect(screen, color, (x, y, colsSize, rowsSize))

        color = (255, 255, 255)
        #Draw the 4 sides of each cell
        if self.walls[0]:
            pygame.draw.line(screen, color, (x, y), (x + colsSize, y)) #T
        if self.walls[1]:
            pygame.draw.line(screen, color, (x + colsSize - 1, y), (x + colsSize - 1, y + rowsSize)) #R
        if self.walls[2]:
            pygame.draw.line(screen, color, (x, y + rowsSize), (x + colsSize, y + rowsSize)) #B
        if self.walls[3]:
            pygame.draw.line(screen, color, (x, y), (x, y + rowsSize)) #L

        #X, Y, XLength, YLength
    def highlight(self):
        color = (0, 255, 0)
        pygame.draw.rect(screen, color, (self.x * colsSize, self.y * rowsSize, colsSize, rowsSize))

    def checkNeighbours(self):
        neighbours = []
        
        if self.y > 0: #T
            top = grid[self.y - 1][self.x]
            if not top.visited:
                neighbours.append(top)

        if self.x < cols - 1: #R
            right = grid[self.y][self.x + 1]
            if not right.visited:
                neighbours.append(right)

        if self.y < rows - 1: #B
            bottom = grid[self.y + 1][self.x]
            if not bottom.visited:
                neighbours.append(bottom)

        if self.x > 0: #L
            left = grid[self.y][self.x - 1]
            if not left.visited:
                neighbours.append(left)

        #Pick a random neighbour
        if len(neighbours) > 0:
            rt = neighbours[random.randrange(len(neighbours))]
            return rt

        return None
#Setup
for y in range(rows): #Creates grid
    tempGrid = []
    for x in range(cols):
        tempGrid.append(Cell(x, y))
    grid.append(tempGrid)

current = grid[0][0]

#Functions
def removeWalls(curr, ahed):
    x = ahed.x - curr.x
    y = ahed.y - curr.y

    if y == -1: #Top
        ahed.walls[2] = False
        curr.walls[0] = False
    elif x == 1: #Right
        ahed.walls[3] = False
        curr.walls[1] = False
    elif y == 1: #Bottom
        ahed.walls[0] = False
        curr.walls[2] = False
    elif x == -1: #Left
        ahed.walls[1] = False
        curr.walls[3] = False

#Main
doneGenerating = False
while not doneGenerating:
    current.visited = True
    nextCell = current.checkNeighbours()
    #current.highlight()

    if nextCell:
        nextCell.visited = True
        stack.append(current) #Push stack
        removeWalls(current, nextCell)
        current = nextCell

    #Randomly pop stacks to increase randomness
    if (not nextCell and stack): #or random.randrange(5) == 0: #If next is undefined, backtrack through stack
        current = stack.pop(len(stack) - 1) #Pop the last item in the array
        #Backtrack to the previous cell
        
    if not stack:
        print("Maze generation complete")
        doneGenerating = True

#A STAR -----------------------------
#Make 2D array
for i in range(rows):
    AStarGrid.append([AStarCell(0, 0)] * cols)

for y in range(rows):
    for x in range(cols):
        AStarGrid[y][x] = AStarCell(x, y)
#These 2 fors above can be simplified into 1

#Make neighbours
for y in range(rows):
    for x in range(cols):
        AStarGrid[y][x].addNeighbours(AStarGrid, grid)

#AStar variables
openSet = [] #Nodes that NEED to be evaluated
closedSet = [] #Nodes FINISHED evaluating

start = AStarGrid[rows - 1][0] #Start location
end = AStarGrid[0][cols - 1] #Target destination

openSet.append(start) #Starting with start location

def itemIncluded(inputList, item):
    for i in range(len(inputList)):
        if inputList[i] == item:
            return True
    return False

def heuristic(a, c):
    #Calculate distance between the 2 points
    #Manhattan distance
    return abs(a.x - c.x) + abs(a.y - c.y)

#A* for the path
findPath = True
while findPath:
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
            print("A* pathfinding complete")
            findPath = False
            break

        for i in range(len(current.neighbours)):
            neighbour = current.neighbours[i]

            #Find if closed set contains neighbour
            if not itemIncluded(closedSet, neighbour):
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
        findPath = False
        break

#Display
running = True
while running:
    #Keep loop running at right speed
    clock.tick(fps)

    #Process events
    for event in pygame.event.get():
        #Window close
        if event.type == pygame.QUIT:
            running = False

    # Draw
    screen.fill((255, 20, 255)) #Draw items after this

    #Debugging
    # for y in range(cols):
    #     for x in range(rows):
    #         AStarGrid[x][y].show((100, 100, 100))

    # for i in range(len(closedSet)):
    #     if i > 0:
    #         closedSet[i].show((255, 0, 0), closedSet[i - 1], False)

    # for i in range(len(openSet)):
    #     if i > 0:
    #         openSet[i].show((0, 255, 0), openSet[i - 1], False)

    #Draw path
    #Trace the path
    temp = current
    path = []
    path.append(temp)
    while temp.previous:
        path.append(temp.previous)
        temp = temp.previous

    for i in range(len(path)):
        if i > 0:
            path[i].show((0, 0, 255), path[i - 1], True)

    #Draw cells
    for y in range(rows):
        for x in range(cols):
            grid[y][x].show()

    pygame.display.flip() #Draw items before this
pygame.quit()