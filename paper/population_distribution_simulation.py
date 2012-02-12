

# Author: Sorathan (Tum) Chaturapruek and John Peebles
# MCM Competition
# Population
import random
import math

AXIS_X = 'X'
AXIS_Y = 'Y'
AXIS_Z = 'Z'
nPL = 54


#----------------------plotting!
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from matplotlib import pylab

#----------------end plotting
def main():
    #nSize = input("What levels?: ")
    nPeople = input("How many people?: ")
    nSize = input("What level: ")
    theTown = Town(nSize)
    #nPeople = input("How many people?: ")
    communicate(nPeople, theTown)
    print(theTown)
    print(total(theTown))
    print("1PL: = "+str(total(theTown)/nPL))
    #print(str(total(theTown)/nPL))
    print("1PL & 1 location: = "+str(total(theTown)/nPL/(6*nSize*nSize)))
    plot(theTown)

def plot(theTown):
    size = theTown.size
    town = theTown.town
    
    fig = plt.figure()
    ax = Axes3D(fig)
    
    for oneLine in town:
        x = [A.x  for A in oneLine]
        y = [A.y for A in oneLine]
        z = [A.score for A in oneLine]
        barband = range(-45, 45, 3)
        for modifier in barband:
            ax.bar(y, z, [t + modifier/100.0 for t in x]\
                   ,zdir='y', color='b', alpha=1)
    
    ax.set_xlabel('X Corrdinate')
    ax.set_ylabel('Y Coordinate')
    ax.set_zlabel('The Number of Repeaters Needed Per Area')

    plt.show()
    
def total(theTown):
    size = theTown.size
    town = theTown.town
    total = 0
    for i in range(2*size+1):
        for j in range(2*size+1):
            total += town[i][j].score
    return total

def convertTown(theTown):
    size = theTown.size
    town = theTown.town
    newTown = Town(size)
    newTownMatrix = newTown.town
    
    for i in range(2*size+1):
        for j in range(2*size+1):
            A = town[i][j]
            newTownMatrix[i][j].x = A.x + A.y*0.5
            newTownMatrix[i][j].y = A.y*1.732/2.0
            newTownMatrix[i][j].score = A.score
    return newTown
            
def convert(A):
    newX = A.x*1.0 + A.y*0.5
    newY = A.y*1.732/2
    newPoint = Point(newX,newY)
    newPoint.score = A.score
    return newPoint

class Point(object):
        ''' A Point'''
        def __init__(self, x, y):
            self.x = x
            self.y = y
            self.score = 0
            
        def __repr__(self):
            #return "(" + str(self.x) + "," + str(self.y) + "): " \
            #       +str(round(self.score, 2))
            return str(round(self.score, 2))

def communicate(nPeople, theTown):
    size = theTown.size
    town = theTown.town
    for i in range(nPeople/2):
        rand1t = randomNormal(town,0.2)
        rand1 = randomNormal(rand1t,0.2)
        #rand1 = random.choice(random.choice(town))
        # rand1 is a Point
        while(abs(rand1.x+rand1.y)>size):
            #rand1 = random.choice(random.choice(town))
            rand1t = randomNormal(town,0.2)
            rand1 = randomNormal(rand1t,0.2)

        rand2t = randomNormal(town,0.2)
        rand2 = randomNormal(rand2t,0.2)
        #rand2 = random.choice(random.choice(town))
        # rand2 is a Point
        while(abs(rand2.x+rand2.y)>size):
            #rand2 = random.choice(random.choice(town))
            rand2t = randomNormal(town,0.2)
            rand2 = randomNormal(rand2t,0.2)
        theTown.processBetter(rand1,rand2)

def randomNormal(listN, center):
    rand1n = random.normalvariate(center,0.5)
    if(rand1n<0):
        rand1n = 0
    if(rand1n>=1):
        rand1n = 0.999
    return listN[int(math.floor(rand1n*len(listN)))]
        
class Town(object):
    ''' A Town'''
    def __init__(self, size):
        self.size = size
        self.town = []
        for i in range(2*self.size+1):
            self.town.append([])
            for j in range(2*self.size+1):
                self.town[i].append(Point(i-size,j-size))
            
    def __repr__(self):
        string = ""
        for i in range(2*self.size+1):
            for j in range(2*self.size+1):
                string += str(self.town[i][j]) +"\t"
            string += "\n"
        return str(string)

    def processBetter(self, A, B):
        # this is a correct version
        deltaX = B.x-A.x
        deltaY = B.y-A.y
        weight = numWays(A,B)
        if(deltaX * deltaY >= 0):
            # do x,y
            for i in range(abs(deltaX)+1):
                for j in range(abs(deltaY)+1):
                    Ax_new = A.x + i*sign(deltaX)
                    Ay_new = A.y + j*sign(deltaY)
                    C = self.town[Ax_new+self.size][Ay_new+self.size]
                    C.score += (1.0*numWays(A, C)*numWays(C, B))/weight
        elif(abs(deltaX) >= abs(deltaY)):
            # do x and z
             for i in range(abs(deltaX)-abs(deltaY)+1):
                for j in range(abs(deltaY)+1): # this is for z
                    Ax_new = A.x +i*sign(deltaX)+ j*sign(deltaX)
                    Ay_new = A.y                + j*sign(deltaY)
                    C = self.town[Ax_new+self.size][Ay_new+self.size]
                    C.score += (1.0*numWays(A, C)*numWays(C, B))/weight
        else:
            # do y and z
             for i in range(abs(deltaX)+1): # this is for z
                for j in range(abs(deltaY)-abs(deltaX)+1): 
                    Ax_new = A.x + i*sign(deltaX)
                    Ay_new = A.y + i*sign(deltaY)  + j*sign(deltaY)
                    C = self.town[Ax_new+self.size][Ay_new+self.size]
                    C.score += (1.0*numWays(A, C)*numWays(C, B))/weight
                

                
    def process(self, A,B):
        # it could be improved if we use numWays directly to
        # that point times the numWays to the destination!
        deltaX = B.x-A.x
        deltaY = B.y-A.y
        
        # base case
        if(deltaX==0 and deltaY==0):
            A.score += 1
        
        elif(deltaX!=0 and deltaY==0):
            A.score += 1
            newA = self.move(A, AXIS_X, sign(deltaX))
            self.process(newA,B)
            
        elif(deltaX==0 and deltaY!=0):
            A.score += 1
            newA = self.move(A, AXIS_Y, sign(deltaY))
            self.process(newA,B)

        # recursive case
        elif(deltaX * deltaY > 0):
            # slide->x
            newA = self.move(A, AXIS_X, sign(deltaX))
            A.score += numWays(newA, B)
            self.process(newA,B)
            # slide->y
            newA = self.move(A, AXIS_Y, sign(deltaY))
            A.score += numWays(newA, B)
            self.process(newA,B)
            
        elif(deltaX *deltaY < 0 and abs(deltaX) >= abs(deltaY)):
            # in this case, we'll use only x and z axes
            # slide->z
            newA = self.move(A, AXIS_Z,sign(deltaX))
            A.score += numWays(newA, B)
            self.process(newA,B)
            # slide->x
            newA = self.move(A, AXIS_X,sign(deltaX))
            A.score += numWays(newA, B)
            self.process(newA,B)
        elif (deltaX *deltaY < 0 and abs(deltaX) < abs(deltaY)):
            # in this case, we'll use only y and z axes
            # slide->z
            newA = self.move(A, AXIS_Z,sign(deltaX))
            A.score += numWays(newA, B)
            self.process(newA,B)
            # slide->y
            newA = self.move(A, AXIS_Y,sign(deltaY))
            A.score += numWays(newA, B)
            self.process(newA,B)

    def move(self,A,axis,direction):
        '''just move. no brain!'''
        if(axis==AXIS_X):
            Ax_new = A.x + direction
            Ay_new = A.y
        elif(axis==AXIS_Y):
            Ax_new = A.x 
            Ay_new = A.y + direction
        elif(axis==AXIS_Z):
            Ax_new = A.x + direction
            Ay_new = A.y - direction
            
        return self.town[Ax_new+self.size][Ay_new+self.size]

        
def sign(n):
    if(n==0):
        return 0;
    else:
        return abs(n)/n

def numWays(A,B):
    deltaX = B.x-A.x
    deltaY = B.y-A.y
    if(deltaX*deltaY >= 0):
        return choose(abs(deltaX + deltaY),abs(deltaX))
    else:
        smaller = min(abs(deltaX),abs(deltaY))
        bigger = min(abs(deltaX),abs(deltaY))
        return choose(bigger,smaller)

def choose(n,r):
    if(r==0):
        return 1;
    if(n-r < r):
        return choose(n,n-r)
    return (n*choose(n-1,r-1))/r

def factorial(n):
    if n==0:
        return 1
    else:
        return n*factorial(n-1)
    
if __name__ == "__main__" : main()
