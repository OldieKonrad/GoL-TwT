import random
from collections import deque
import time
import math


NEIGHBORS_OFFSET = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
POLARCONV = {0: (1,0), 90: (0, 1), 180: (-1, 0), 270: (0, -1)}

def getBitsReverse(someint: int):
    sibl = [x == '1' for x in (bin(someint)[2:])[::-1]]
    for b in sibl:
        yield b

def getSpiralCoords(start: tuple):
    usedCoords = set()
    lastCoord = start
    usedCoords.add(lastCoord)
    direction = 0             # just to start to the right
    yield lastCoord                 

    while True:
        turndirection = (direction+90)%360
        turnoffset = POLARCONV[turndirection]
        turnpoint = (lastCoord[0] + turnoffset[0], lastCoord[1] + turnoffset[1])
        if turnpoint in usedCoords:             # keep direction
            nextoffset = POLARCONV[direction]
            nextpoint = (lastCoord[0] + nextoffset[0], lastCoord[1] + nextoffset[1])
            lastCoord = nextpoint
        else:                                   # make a turn
            direction = turndirection
            lastCoord = turnpoint

        usedCoords.add(lastCoord)
        yield lastCoord


class GoL:
    def __init__(self, width=20, height=20, maxgenerations=9_999, maxhistory=10):
        self.width = width
        self.height = height
        self.maxhistory = maxhistory
        self.maxgenerations = maxgenerations
        self.neighborsDict = dict()
        
        self.reset()
        
    def reset(self):
        self.curLivings = set()
        self.generation = 0
        self.startset = set()
        self.history = deque() #deque([set() for _ in range(self.maxhistory)], self.maxhistory)
        self.finished = False
        self.cycletime = 0

    def randomPopulate(self):
        self.reset()
        
        maxliving = (self.width * self.height) // 4
        
        self.curLivings = set([(random.randrange(0, self.height), random.randrange(0, self.width)) for _ in range(maxliving)])
        self.startset = self.curLivings 

    def populateSpiral(self, someint: int):
        self.reset()

        center = (math.ceil(self.width/2)-1, math.ceil(self.height/2)-1)
        spiral = getSpiralCoords(center)
        for b in getBitsReverse(someint):
            cell = next(spiral)
            assert(not (cell[0]<0 or cell[1]<0 or cell[0]>=self.width or cell[1]>=self.height))
            if b:
                self.curLivings.add(cell)
        self.startset = self.curLivings

    def nextGeneration(self):
        if self.finished:
            return
        if self.generation >= self.maxgenerations:
            self.finished = True
            
        allNeighbors = set()
        newLivings = set()

        for cell in self.curLivings:
            cellneighbors = self.getNeighbors(cell)

            liveneighbors = set(filter(lambda x: x in self.curLivings, cellneighbors))

            if len(liveneighbors) in [2, 3]:
                newLivings.add(cell)
            allNeighbors.update(cellneighbors.difference(liveneighbors))
        
        for cell in allNeighbors:
            cellneighbors = self.getNeighbors(cell)
            liveneighbors = set(filter(lambda x: x in self.curLivings, cellneighbors))

            if len(liveneighbors) == 3:
                newLivings.add(cell)
        
        
        try:    # check if already in history
            self.cycletime = self.history.index(newLivings)+1
            # found in history
            self.finished = True
            return
        except ValueError:
            self.generation += 1    # not in history

        self.history.appendleft(self.curLivings)  
        self.curLivings = newLivings
        
        if len(newLivings)==0:
            self.finished = True

    def getNeighbors(self, pos):
        neighbors = self.neighborsDict.get(pos)
        if neighbors:
            return neighbors
        
        neighbors = []
        

        for no in NEIGHBORS_OFFSET:
            x, y = pos[0] + no[0], pos[1] + no[1]
            if x >= 0 and x < self.width and y >= 0 and y < self.height:
                neighbors.append((x, y))
        
        neighbors = set(neighbors)
        self.neighborsDict[pos] = neighbors
        
        return neighbors
    
    def toggleCell(self, cell):
        if cell in self.curLivings:
            self.curLivings.remove(cell)
        else:
            self.curLivings.add(cell)
        return
        
    def printGoL(self):
        for x in range(self.width):
            for y in range(self.height):
                if (x, y) in self.curLivings:
                    print('x', end="")
                else:
                    print('-', end="")
            print()
        return
            



##########################
if __name__ == "__main__":
    
    start = time.perf_counter()     # vvvvvvvvvvvvvvvvvvvvvvvvv

    gol = GoL(64, 64)
    maxgens = 0
    
    for someint in range(2**4):
        #gol.randomPopulate()
        gol.populateSpiral(someint)
    
        while not gol.finished:
            # gol.printGoL()
            # print()
            gol.nextGeneration()
            
        if gol.generation > maxgens:
            maxgens = gol.generation

        if gol.generation > 999:
            print(f'Spiralint: {someint} Generations: {gol.generation} Cycletime: {gol.cycletime}')
            
    #print(f'maximum generations: {maxgens}')
    
    end = time.perf_counter()       # ^^^^^^^^^^^^^^^^^^^^^^^
    print(f"Total Runtimme: {end - start:0.4f} seconds")
            
        
