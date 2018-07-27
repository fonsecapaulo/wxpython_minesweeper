'''
Created on 22 Jul 2018

@author: Paulo
'''
from random import sample
import pprint

class MinesweeperLogic(object):
	"""classdocs"""

	def __init__(self, rowSize, columnSize, numberMines):
		'''
		Constructor
		'''
		self.NewGame(rowSize, columnSize, numberMines)
	
	def GenerateMines(self):
		mineCoordinates=[]
		mines = sample(range(0, (self.columnSize*self.rowSize)-1) , self.numberMines)
		#print (mines)
		
		for mine in mines:
			mineCoordinates.append(self.IntToCoordinates(mine))
			
		#print(mineCoordinates)
		return ((mines, mineCoordinates))
			
	def GenerateGameMatrix(self, mines):
		
		matrix = [[Cell() for _ in range(self.rowSize)] for _ in range(self.columnSize)]
				
		for mine in mines:
			mineRow, mineColumn = (mine)
			matrix[mineRow][mineColumn].value = -1
			
			rowRange = range (mineRow-1, mineRow + 2)
			columnRange = range (mineColumn -1, mineColumn + 2)
			
			for i in rowRange:
				for j in columnRange:
					if ( 0 <= i < self.rowSize and 0 <= j < self.columnSize and matrix[i][j].value!= -1):
						matrix[i][j].value+=1
		
		#self.PrintGameMatrix(matrix)
		
		return matrix
	
	def NewGame(self, rowSize, columnSize, numberMines):
		self.rowSize = rowSize
		self.columnSize = columnSize
		self.numberMines = numberMines
		
		self.numberMoves = self.rowSize * self.columnSize
		
		self.minesInt, self.minesLocations = self.GenerateMines()
		self.gameMatrix = self.GenerateGameMatrix(self.minesLocations)
	
	def ClickMove(self, buttonNumber):
		result={
			"finish":False,
			"mine":False,
			"tile_info" : []
			}
		
		#Translates the int to Coordinates
		row , column = self.IntToCoordinates(buttonNumber)
		
		#Sets the specific cell as clicked
		self.gameMatrix[row][column].SetClicked()
		#Decreases the number of plays (used to know if game is won)
		self.numberMoves -= 1
		result['tile_info'].append((self.CoordinatesToInt(row, column) ,self.gameMatrix[row][column].value))
		
		if self.gameMatrix[row][column].value == -1:
			result['finish'] = result['mine']= True
					
		if self.gameMatrix[row][column].value == 0:
			#Runs the propagation calculation
			propagateList = self.PropagateZeros(row, column)
			#Updates the number of moves
			self.numberMoves -= len(propagateList)
			for cell in propagateList:
				row, column = cell
				self.gameMatrix[row][column].SetClicked()
				result['tile_info'].append((self.CoordinatesToInt(row, column) ,self.gameMatrix[row][column].value))
			
					
		if self.numberMoves <= self.numberMines:
			result['finish'] = True
			
		return result
	
	def FlagMove(self, buttonNumber):
		#Translates the int to Coordinates
		row , column = self.IntToCoordinates(buttonNumber)
		self.gameMatrix[row][column].ToggleFlag()
	
	def IntToCoordinates(self, i):
		row = int(i / self.rowSize)
		column = i % self.columnSize
		return (row, column)
	
	def CoordinatesToInt(self, row, column):
		return column + row * self.columnSize

	def PropagateZeros(self, row, column):
		propagateList=[]
		def FloodFill(row, column):
			rowRange = range (row-1, row + 2)
			columnRange = range (column -1, column + 2)
			
			for i in rowRange:
				for j in columnRange:
					#Inside row boundaries and Column boundaries and not flagged cell and not the initial cell (row column)
					if ( 0 <= i < self.rowSize and 0 <= j < self.columnSize and self.gameMatrix[i][j].flag == False and self.gameMatrix[i][j].clicked == False and not (i==row and j==column)):
 						if (i,j) in propagateList:
 							continue
 						else:
 							propagateList.append((i,j))
 							if (self.gameMatrix[i][j].value == 0):
							 	FloodFill(i, j)	
		FloodFill(row, column)
		
		return propagateList
	
	def ShowMines(self):
		return self.minesInt
	
	def PrintGameMatrix(self, matrix):
		aux_matrix = [[matrix[p][o].value for o in range(self.rowSize)] for p in range(self.columnSize)]
		pprint.pprint(aux_matrix,indent=4)
	
class Cell():
	
	def __init__(self):
		self.flag = False
		self.clicked = False
		#-1 means mine
		self.value = 0 
		
	def ToggleFlag(self):
		if self.flag == True:
			self.flag = False
		else:
			self.flag = True
	
	def SetClicked(self):
		self.clicked=True				
		