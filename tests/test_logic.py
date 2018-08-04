'''
Created on 28 Jul 2018

@author: Paulo
'''
import pytest

from minesweeper.minesweeper_logic import MinesweeperLogic


def test_IntToCoordinates():
    logic = MinesweeperLogic(9,9,10)
    
    assert logic.IntToCoordinates(9)==(1,0)
    with pytest.raises(ValueError):
        logic.IntToCoordinates(-9)

def test_CoordinatesToInt():
    logic = MinesweeperLogic(9,9,10)
    
    assert logic.CoordinatesToInt(1,0)==9