'''
Created on 28 Jul 2018

@author: Paulo
'''
import pytest

from minesweeper.minesweeper_logic import MinesweeperLogic


def test_IntToCoordinates():
    logic = MinesweeperLogic(16,30,99)
    
    assert logic.IntToCoordinates(30)==(1,0)
    with pytest.raises(ValueError):
        logic.IntToCoordinates(-30)

def test_CoordinatesToInt():
    logic = MinesweeperLogic(16,30,99)
    
    assert logic.CoordinatesToInt(1,0)==30