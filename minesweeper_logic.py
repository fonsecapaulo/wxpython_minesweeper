'''
Created on 22 Jul 2018

@author: Paulo
'''
from random import sample
import pprint

class MinesweeperLogic(object):
    '''
    classdocs
    '''

    def __init__(self, rowSize, columnSize, numberMines):
        '''
        Constructor
        '''
        self.NewGame(rowSize, columnSize, numberMines)
    
    def GenerateMines(self):
        mineCoordinates=[]
        mines = sample(range(0, (self.columnSize*self.rowSize)-1) , self.numberMines)
        
        for mine in mines:
            row = int(mine / self.rowSize)
            column = mine % self.columnSize    
            
            mineCoordinates.append((row,column))
            
        #print(mineCoordinates)
        return (mineCoordinates)
            
    def GenerateGameMatrix(self, mines):
        
        matrix = [[0 for _ in range(self.rowSize)] for _ in range(self.columnSize)]
        #pprint.pprint(matrix)
        
        for mine in mines:
            mineRow, mineColumn = (mine)
            matrix[mineRow][mineColumn] = -1
            
            rowRange = range (mineRow-1, mineRow + 2)
            columnRange = range (mineColumn -1, mineColumn + 2)
            
            for i in rowRange:
                for j in columnRange:
                    if ( 0 <= i < self.rowSize and 0 <= j < self.columnSize and matrix[i][j]!= -1):
                        matrix[i][j]+=1
        pprint.pprint(matrix)
        return matrix
    
    def Move(self, buttonNumber):
        result={
            "finish":False,
            "mine":False,
            "propagate_0s":[],
            "tile_info" : 0
            }
        
        row = int(buttonNumber / self.rowSize)
        column = buttonNumber % self.columnSize
        
        self.numberMoves -= 1
        
        
        result['tile_info'] = self.gameMatrix[row][column]
        
        if self.gameMatrix[row][column] == -1:
            result['finish'] = result['mine']= True
                    
        if self.gameMatrix[row][column] == 0:
            pass
            #result["propagate_0s"].append((column+1)+(row*self.columnSize))
            #self.numberMoves -= 1    
        
        if self.numberMoves <= self.numberMines:
            result['finish'] = True
            
        return result
    
    def NewGame(self, rowSize, columnSize, numberMines):
        self.rowSize = rowSize
        self.columnSize = columnSize
        self.numberMines = numberMines
        
        self.numberMoves = self.rowSize * self.columnSize
        
        self.mine_locations =self.GenerateMines()
        self.gameMatrix = self.GenerateGameMatrix(self.mine_locations)