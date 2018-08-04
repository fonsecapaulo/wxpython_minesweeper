'''
Created on 28 Jul 2018

@author: Paulo
'''
#import pytest
from minesweeper_logic import MinesweeperLogic


def test_IntToCoordinates():
    logic = MinesweeperLogic(9,9,10)
    
    assert logic.IntToCoordinates(9)==(1,0)