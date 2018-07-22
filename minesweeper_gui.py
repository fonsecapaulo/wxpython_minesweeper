'''
Created on 21 Jul 2018

@author: Paulo
'''
import wx 
from random import sample
import minesweeper_logic
from minesweeper_logic import MinesweeperLogic

BOARD_WIDTH = 8
BOARD_HEIGHT = BOARD_WIDTH

class MinesweeperGui(wx.Frame):
    
    def __init__(self, parent, title):
        #calls wx.Frame constructor
        super(MinesweeperGui, self).__init__(parent, style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER ^ wx.MAXIMIZE_BOX)
        
        self.parent=parent
        self.title=title
        
        self.bmp_tile_plain = wx.Bitmap(".\\images\\tile_plain.gif")
        self.bmp_tile_flag = wx.Bitmap(".\\images\\tile_flag.gif")
        self.bmp_tile_clicked = wx.Bitmap(".\\images\\tile_clicked.gif")
        self.bmp_tile_mine = wx.Bitmap(".\\images\\tile_mine.gif")
        self.InitGUI()
        self.logic = MinesweeperLogic()
        
    def InitGUI(self): 
        #Frame stuff
        self.SetSize((300, 300))
        self.SetTitle(self.title)
        self.Centre()
        
        #####################################
        #Create the menu bar
        menubar = wx.MenuBar()
        
        ###File menu
        fileMenu = wx.Menu()
        fileTest = fileMenu.Append(0, '&Test', 'Test')
        fileNewGame = fileMenu.Append(wx.ID_NEW, '&New Game', 'New Game')
        fileQuitItem = fileMenu.Append(wx.ID_EXIT, '&Quit', 'Quit application')
            #qmi = wx.MenuItem(fileMenu, APP_EXIT, '&Quit\tCtrl+Q')
            #qmi.SetBitmap(wx.Bitmap('exit.png'))
        menubar.Append(fileMenu, '&File')
        ###
        self.SetMenuBar(menubar)
        
        ###################################
        #Create Panel
        self.panel = wx.Panel(self)
        ###################################       
        #Buttons
        gs = wx.GridSizer(BOARD_WIDTH, BOARD_HEIGHT,0,0)
        for i in range(0, BOARD_HEIGHT*BOARD_WIDTH): 
            bmpButton = wx.BitmapButton(self.panel, id = i, bitmap = self.bmp_tile_plain, )
            #Bind left Right
            bmpButton.Bind(wx.EVT_RIGHT_UP, self.OnRightClick)
            gs.Add(bmpButton, 0, wx.EXPAND)
        self.panel.SetSizer(gs)
        ###################################
        
        #Bindings
        ###Menu Actions
        self.Bind(wx.EVT_MENU, self.OnQuit, fileQuitItem)
        self.Bind(wx.EVT_MENU, self.OnNewGame, fileNewGame)
        self.Bind(wx.EVT_MENU, self.OnTest, fileTest)
        ###General Button
        self.Bind(wx.EVT_BUTTON, self.OnButton)
 
        ###################################
   
    def OnTest(self,e):
        mines = sample(range(0, 63),16)
        for mine in mines:
            button = wx.Window.FindWindowById(mine, parent=None)
            button.SetBitmapLabel(self.bmp_tile_mine)    
               
    def OnQuit(self, e):
        self.Close()
    
    def OnNewGame(self, e):
        self.logic.test()
        pass
           
    def OnButton(self,e):    
        print("ID = {} or Coordinates: {},{}".format(e.Id, int(e.Id/BOARD_WIDTH) , e.Id % BOARD_HEIGHT))
        e.EventObject.SetBitmapDisabled(self.bmp_tile_clicked)
        e.EventObject.Disable()
   
    def OnRightClick(self,e):
        print("Right ID: {}".format(e.Id))
        if self.bmp_tile_plain.Handle == e.EventObject.GetBitmapLabel().Handle:
            e.EventObject.SetBitmapLabel(self.bmp_tile_flag)
        else:
            e.EventObject.SetBitmapLabel(self.bmp_tile_plain)    
    
    
    ################Aux methods#####################
    def ChangeButton(self):    
        button = wx.Window.FindWindowById(3, parent=None)
        button.SetBitmapLabel(self.bmp_tile_flag)

if __name__ == '__main__':
    
    app = wx.App()
    ex = MinesweeperGui(None, title='wxPython Minesweeper')
    ex.Show()
    app.MainLoop()
    
