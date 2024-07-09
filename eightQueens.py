import random

class eightQueens:
    def __init__(self):
        self.numRestarts = 0
        self.numStateChanges = 0
        self.generateRandomState()


    def generateRandomState(self):
        #create row index array
        rowIndexArray = [0,1,2,3,4,5,6,7]
        #index is row number value is row index 
        queenIndex = []
        newState = [[0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0]]
        
        for row in newState:
            randomIndex = random.randint(0, len(rowIndexArray) - 1)
            #generate random index for next Q in row
            randomIndex = rowIndexArray.pop(randomIndex)
            row[randomIndex] = 1
        # print("New Random State Generated:")
        self.currentLowestHValue = self.getHeuristicValueOfState(newState)
        self.checkForLowerHValue(newState, self.getHeuristicValueOfState(newState))

    def displayState(self, state):
        print("current State:")
        for row in state:
            print(row)

    def checkForLowerHValue(self, state, currentHValue):
        self.numLowerNeighbors = 0
        if currentHValue == 0:
            self.displayState(state)
            print("Solution Found")
            print("State Changes: " + str(self.numStateChanges))
            print("Restarts: " + str(self.numRestarts))
            return
        print("Current States H value: " + str(currentHValue))
        self.displayState(state)
        

        lastHValue = currentHValue
        #Get best H Value using shiftState and getHeuristicValueOfState
        #iterate through columns
        for i in range(0, 8):
            stateColArray = self.shiftState(state, i) # starting with 0 should be i in second arg
            lowestColState, lowestHValue = self.returnLowestHValueState(stateColArray)
            if lowestHValue < lastHValue:
                lastHValue = lowestHValue
                nextState = lowestColState

        #this will run recursively, if h value is 0 it stops
        #if previous h value is lower than currentbest we randomize state
        print("neighbors found with lower h: " + str(self.numLowerNeighbors))
        if currentHValue <= lastHValue:
            print("RESTART")
            print()
            self.numRestarts += 1
            self.numStateChanges += 1
            self.generateRandomState()
        else:
            self.currentLowestHValue = lastHValue
            print("Setting new current state")
            print()
            self.numStateChanges += 1
            self.checkForLowerHValue(nextState, lastHValue)

    def shiftState(self, state, newCol):
        #create an array of states to iterate through later
        stateColArray = []
        for i in range(0, 8):
            newState = [row[:] for row in state]
            for j in range(0,8):
                newState[j][newCol] = 0
            newState[i][newCol] = 1
            stateColArray.append(newState)
        return stateColArray

    def returnLowestHValueState(self, stateColArray):
        lowestHValueState = stateColArray[0]
        lowestHValue = self.getHeuristicValueOfState(stateColArray[0])
        for state in stateColArray:
            if self.getHeuristicValueOfState(state) < self.currentLowestHValue:
                self.numLowerNeighbors += 1
                #print("Value of Current State: " + str(self.getHeuristicValueOfState(state)))
                #print("CurrentLowestHVal: " + str(self.currentLowestHValue))

            if lowestHValue > self.getHeuristicValueOfState(state):
                lowestHValueState = state
                lowestHValue = self.getHeuristicValueOfState(state)

        return lowestHValueState, lowestHValue
            

    def getHeuristicValueofRow(self, queenRow, state):
        queenCount = 0
        for entry in state[queenRow]:
            if entry == 1:
                queenCount += 1
        return self.getHeuristicValueGivenNum(queenCount)

    def getHeuristicValueofCol(self, queenCol,state):
        queenCount = 0
        for num in range(0,8):
            if state[num][queenCol] == 1:
                queenCount +=1
        return self.getHeuristicValueGivenNum(queenCount)

    def getHeuristicValueofDiag(self, queenRow,queenCol, state):
        #check top left diagonal
        queenCount1 = 0
        queenCount2 = 0
        if queenRow > queenCol:
            #iterate starting at state[queenRow-queenCol + i][i]
            for i in range(0, 8 - (queenRow - queenCol)):
                #print(state[queenRow - queenCol + i][i])
                if state[queenRow - queenCol + i][i] == 1:
                    queenCount1 += 1
        else:
            for i in range(0, 8 - (queenCol - queenRow)):
                #print(state[i][queenCol - queenRow + i])
                if state[i][queenCol - queenRow + i] == 1:
                    queenCount1 += 1

        # #check top right diagonal
        if(queenCol == 7 and queenRow == 7): 
            #print(state[7][7])
            queenCount2 += 1
        elif(queenRow + queenCol > 7):
            #get starting column and set row to 7
            startingCol = (queenRow + queenCol) % 7 # equals starting column of starting row
            #starting row is 7 and decreseases by i which ranges from 0 to 8 - starting col
            for i in range(0, 8 - startingCol):
                #print(state[7 - i][startingCol + i])
                if state[7 - i][startingCol + i] == 1:
                    queenCount2 += 1
        else:
            #new row is equal to row + col
            startingRow = queenRow + queenCol

            #col starts at 0 and increases by i which ranges from 0 to 8 - (8-starting row) + 1 for last value
            for i in range(0, 8 - (8 - startingRow) + 1):
                #print(state[startingRow - i][0 + i])
                if state[startingRow - i][0 + i] == 1:
                    queenCount2 += 1
        return (self.getHeuristicValueGivenNum(queenCount1) + self.getHeuristicValueGivenNum(queenCount2))
            

    def getHeuristicValueGivenNum(self, numQueens):
        #calculated by hand, max we'll ever need is 8
        if numQueens == 1:
            return 0
        elif numQueens == 2:
            return 1
        elif numQueens == 3:
            return 3
        elif numQueens == 4:
            return 5
        elif numQueens == 5:
            return 10
        elif numQueens == 6:
            return 15
        elif numQueens == 7:
            return 21
        elif numQueens == 8:
            return 28

    def getHeuristicValueOfState(self, state):
        heuristicSum = 0
        for i in range(0,8):
            for j in range(0, 8):
                if state[i][j] == 1:
                    heuristicSum += self.getHeuristicValueofRow(i, state)
                    heuristicSum += self.getHeuristicValueofCol(j, state)
                    heuristicSum += self.getHeuristicValueofDiag(i, j, state)
        return heuristicSum

eightQueens = eightQueens()

