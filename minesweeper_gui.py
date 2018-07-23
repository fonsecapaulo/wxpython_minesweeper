'''
Created on 21 Jul 2018

@author: Paulo
'''
import wx 
from random import sample
from minesweeper_logic import MinesweeperLogic

BOARD_WIDTH = 9
BOARD_HEIGHT = BOARD_WIDTH

class MinesweeperGui(wx.Frame):
    
    def __init__(self, parent, title):
        #calls wx.Frame constructor
        super(MinesweeperGui, self).__init__(parent, style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER ^ wx.MAXIMIZE_BOX)
        
        self.parent=parent
        self.title=title
        
        self.bmpTilePlain = wx.Bitmap(".\\images\\tile_plain.gif")
        self.bmpTileFlag = wx.Bitmap(".\\images\\tile_flag.gif")
        self.bmpTileClicked = wx.Bitmap(".\\images\\tile_clicked.gif")
        self.bmpTileMine = wx.Bitmap(".\\images\\tile_mine.gif")
        self.bmpTileWrong = wx.Bitmap(".\\images\\tile_wrong.gif")
        self.bmpNumbers = [wx.Bitmap(".\\images\\tile_clicked.gif"),
                            wx.Bitmap(".\\images\\tile_1.gif"),
                            wx.Bitmap(".\\images\\tile_2.gif"),
                            wx.Bitmap(".\\images\\tile_3.gif"),
                            wx.Bitmap(".\\images\\tile_4.gif"),
                            wx.Bitmap(".\\images\\tile_5.gif"),
                            wx.Bitmap(".\\images\\tile_6.gif"),
                            wx.Bitmap(".\\images\\tile_7.gif"),
                            wx.Bitmap(".\\images\\tile_8.gif")]
        
        
        self.InitGUI()
        self.logic = MinesweeperLogic(BOARD_WIDTH, BOARD_WIDTH, 10)
        
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
        self.buttons=[]
        gs = wx.GridSizer(BOARD_WIDTH, BOARD_HEIGHT,0,0)
        for i in range(0, BOARD_HEIGHT*BOARD_WIDTH): 
            bmpButton = wx.BitmapButton(self.panel, id = i, bitmap = self.bmpTilePlain, )
            #Bind left Right
            bmpButton.Bind(wx.EVT_RIGHT_UP, self.OnRightClick)
            self.buttons.append(bmpButton)
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
            button.SetBitmapLabel(self.bmpTileMine)    
               
    def OnQuit(self, e):
        self.Close()
    
    def OnNewGame(self, e):
        pass
           
    def OnButton(self,e):    
        print("ID = {} or Coordinates: {},{}".format(e.Id, int(e.Id/BOARD_WIDTH) , e.Id % BOARD_HEIGHT))
        result = self.logic.Move(e.Id)
        
        if result['mine'] == True:
            wx.MessageBox("MINE - Game Over")
            e.EventObject.SetBitmapDisabled(self.bmpTileWrong)
            self.NewGame()
        	
        else:    
            e.EventObject.SetBitmapDisabled(self.bmpNumbers[result["tile_info"]])
            e.EventObject.Disable()
            #To avoid focus going to the next button, set focus on frame
            self.SetFocus()
            
            #TODO: Propagate 0s
            #if result["tile_info"] == 0:
            
            if result['finish'] == True:
                wx.MessageBox("FINISH!!!")
                self.NewGame()
   
    def OnRightClick(self,e):
        #print("Right ID: {}".format(e.Id))
        if self.bmpTilePlain.Handle == e.EventObject.GetBitmapLabel().Handle:
            e.EventObject.SetBitmapLabel(self.bmpTileFlag)
        else:
            e.EventObject.SetBitmapLabel(self.bmpTilePlain)    
    
    
    ################Aux methods#####################
    def NewGame(self):
    	for i in self.buttons:
    		i.SetBitmap(self.bmpTilePlain)
    		i.Enable()
    	self.logic.new_game(BOARD_WIDTH, BOARD_WIDTH, 10)
    	
if __name__ == '__main__':
    
    app = wx.App()
    ex = MinesweeperGui(None, title='wxPython Minesweeper')
    ex.Show()
    app.MainLoop()
    
