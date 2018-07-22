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

    def __init__(self, row_size, column_size, number_mines):
        '''
        Constructor
        '''
        self.row_size=row_size
        self.column_size=column_size
        self.number_mines=number_mines
        
        self.game_matrix = []
        
        self.generate_game_matrix(self.generate_mines())
    
    def generate_mines(self):
        mine_coordinates=[]
        mines = sample(range(0, (self.column_size*self.row_size)-1) , self.number_mines)
        
        for mine in mines:
            row = int(mine / self.row_size)
            column = mine % self.column_size    
            
            mine_coordinates.append((row,column))
            
        #print(mine_coordinates)
        return (mine_coordinates)
            
    def generate_game_matrix(self, mines):
        
        self.game_matrix = [[0 for _ in range(self.row_size)] for _ in range(self.column_size)]
        #pprint.pprint(self.game_matrix)
        
        for mine in mines:
            mine_row, mine_column = (mine)
            self.game_matrix[mine_row][mine_column] = -1
            
            row_range = range (mine_row-1, mine_row + 2)
            column_range = range (mine_column -1, mine_column + 2)
            
            for i in row_range:
                for j in column_range:
                    if ( 0 <= i < self.row_size and 0 <= j < self.column_size and self.game_matrix[i][j]!= -1):
                        self.game_matrix[i][j]+=1
        
        #pprint.pprint(self.game_matrix)
    
    def move(self, button_number):
        row = int(button_number / self.row_size)
        column = button_number % self.column_size
        
        return self.game_matrix[row][column]