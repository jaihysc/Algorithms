#Based on coding train maze generator https://www.youtube.com/watch?v=HyK_Q5rrcr4
#TODO add A* to this
import pygame #Requires pygame
import math
import random

#Pygame configs---
fps = 500
width = 800
height = 800

pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Maze Generation")
clock = pygame.time.Clock()
#End pygame configs---

#Program configs
cols = 60
rows = 50

colsSize = math.floor(width / cols) #X
rowsSize = math.floor(height / rows) #y

grid = []

stack = []

random.seed()
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
            pygame.draw.rect(screen, color, (x, y, colsSize, rowsSize))

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
    elif stack: #If next is undefined, backtrack through stack
        current = stack.pop(len(stack) - 1) #Pop the last item in the array
        #Backtrack to the previous cell
    else:
        print("Done!")
        doneGenerating = True

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
    screen.fill(55) #Draw items after this

    #Draw cells
    for y in range(rows):
        for x in range(cols):
            grid[y][x].show()

    pygame.display.flip() #Draw items before this
pygame.quit()