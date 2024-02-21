import random
from collections import deque
import time


class GoL:
    def __init__(self, width=20, height=20, maxgenerations=1_000, maxhistory=10):
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
        
        neighbors_offset = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        for no in neighbors_offset:
            x, y = pos[0] + no[0], pos[1] + no[1]
            if x >= 0 and x < self.width and y >= 0 and y < self.height:
                neighbors.append((x, y))
        
        # x, y = pos

        # for dx in [-1, 0, 1]:
        #     if x + dx < 0 or x + dx > self.width:
        #         continue
        #     for dy in [-1, 0, 1]:
        #         if y + dy < 0 or y + dy > self.height:
        #             continue
        #         if dx == 0 and dy == 0:
        #             continue

        #         neighbors.append((x + dx, y + dy))
        
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

    gol = GoL(50, 50)
    maxgens = 0
    
    for _ in range(10):
        gol.randomPopulate()
    
        while not gol.finished:
            # gol.printGoL()
            # print()
            gol.nextGeneration()
            
        if gol.generation > maxgens:
            maxgens = gol.generation
            
    print(f'maximum generations: {maxgens}')
    
    end = time.perf_counter()       # ^^^^^^^^^^^^^^^^^^^^^^^
    print(f"Total Runtimme: {end - start:0.4f} seconds")
            
        
