#Based on Coding train Binary search tree https://www.youtube.com/watch?v=ZNH0MuQ51m4&index=2&list=PLRqwX-V7Uu6bePNiZLnglXUp2LXIjlCdb
#March 11, 2019
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

masterNodeList = []

#Main variables
class Node():
    def __init__(self, value):
        self.value = value

        self.left = None
        self.right = None

        self.x = 0
        self.y = 0
        self.spacing = 0
        self.level = 0
    def addNode(self, n):
        #If a add is requested, compare and see if it is smaller / bigger
        #To place on Left or right side
        if n.value < self.value:
            if not self.left:
                self.left = n #Sets the node once there is no more further entries
            else:
                self.left.addNode(n) #Calls itself for recursion to find the right place in the tree to place

        elif n.value > self.value:
            if not self.right:
                self.right = n #Set node when there is no more entries ahead
            else:
                self.right.addNode(n) #Otherwise keep going

        else: #If equal, it does not get added
            pass
    def setLevel(self, level):
        masterNodeList.append(self) #Add this to the masterNodeList for use later when organizing by levels

        self.level = level
        print(level)

        newLevel = level + 1
        #Increment the level for each additional node visited
        if self.left: #Only visit if it is not null
            self.left.setLevel(newLevel) #Increment the level for each additional node visited

        if self.right:
            self.right.setLevel(newLevel) #Increment the level for each additional node visited
    def setSpacing(self, allNodes):
        currentLevelAmt = 0
        #Count the number of nodes at the current level
        for i in range(len(allNodes)):
            if allNodes[i].level == self.level:
                currentLevelAmt += 1

        self.spacing = currentLevelAmt * 40 #Set spacing based of number of nodes at current level

        if self.left: #Only visit if it is not null
            self.left.setSpacing(allNodes)

        if self.right:
            self.right.setSpacing(allNodes)
        
    def visit(self, previous):
        #Draw line between previous and current node
        if previous:
            #print(previous.x, previous.y)
            pygame.draw.line(screen, (100, 100, 0), (previous.x + 10, previous.y + 10), (self.x  + 10, self.y  + 10)) #+10 to offset line into right place for looks

        if self.left: #Only visit if it is not null
            self.left.visit(self)

        text = str(self.value)
        font = pygame.font.SysFont('Arial', 26)
        text = font.render(text, True, (0, 0, 0))
        screen.blit(text, (self.x, self.y))

        if self.right:
            self.right.visit(self)
    def search(self, n):
        if self.value == n:
           return self

        if n < self.value and self.left: #If N is less than the current number, keep traveling left
            return self.left.search(n)
            
        elif n > self.value and self.right: #If N is greater than the current number, travel right
            return self.right.search(n)

        return None #Return this if nothing is found
    def setXY(self):
        if self.left:
            self.left.x = self.x - self.left.spacing #Set the x/y cords of the nodes beside it
            self.left.y = self.y + 20
            
            self.left.setXY()

        if self.right:
            self.right.x = self.x + self.right.spacing #Set the x/y cords of the nodes beside it
            self.right.y = self.y + 20

            self.right.setXY()


class Tree():
    def __init__(self):
        self.root = None

    def addValue(self, val):
        n = Node(val)
        #Initialize as root if empty
        if not self.root:
            self.root = n

            self.root.x = width / 2 #Put the root node at the top
            self.root.y = 0

        else: #Otherwise add on to existing node
            self.root.addNode(n)
    def traverse(self):
        self.root.visit(None)
    def search(self, n):
        return self.root.search(n)
    def setNodeLevels(self):
        self.root.setLevel(0)
    def setNodeSpacing(self, allNodes):
        #Count all the nodes
        self.root.setSpacing(allNodes)
    def setNodeXY(self):
        self.root.setXY()
        

binaryTree = Tree()

for i in range(40):
    binaryTree.addValue(random.randrange(20))

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

    #Update - Logic

    # Draw
    screen.fill((255, 255, 255))

    binaryTree.setNodeLevels()
    binaryTree.setNodeSpacing(masterNodeList)
    binaryTree.setNodeXY()
    #print(binaryTree.root.left.level)

    binaryTree.traverse()

    pygame.display.flip() #Actually show the items to the screen
    input()
print("Press ENTER to exit")
input()
pygame.quit()