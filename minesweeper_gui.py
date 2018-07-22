'''
Created on 21 Jul 2018

@author: Paulo
'''
import wx 
from wx import Bitmap

BOARD_WIDTH = 8
BOARD_HEIGHT = BOARD_WIDTH

class MinesweeperGui(wx.Frame):
    
    def __init__(self, parent, title):
        #calls wx.Frame constructor
        super(MinesweeperGui, self).__init__(parent)
        
        self.parent=parent
        self.title=title
        
        self.InitGUI()
        
    def InitGUI(self): 
        #Frame stuff
        #self.SetSize((300, 300))
        self.SetTitle(self.title)
        self.Centre()
        
        #####################################
        #Create the menu bar
        menubar = wx.MenuBar()
        
        ###File menu
        fileMenu = wx.Menu()
        fileNewGame = fileMenu.Append(wx.ID_NEW, '&New Game', 'New Game')
        fileQuitItem = fileMenu.Append(wx.ID_EXIT, '&Quit', 'Quit application')
            #qmi = wx.MenuItem(fileMenu, APP_EXIT, '&Quit\tCtrl+Q')
            #qmi.SetBitmap(wx.Bitmap('exit.png'))
        menubar.Append(fileMenu, '&File')
        ###
        self.SetMenuBar(menubar)
        ###################################       
        #Buttons
        gs = wx.GridSizer(BOARD_WIDTH, BOARD_HEIGHT, -1, -1)
        self.bmp_tile_plain = wx.Bitmap(".\\images\\tile_plain.gif")
        for i in range(0, BOARD_HEIGHT*BOARD_WIDTH): 
            bmpButton = wx.BitmapButton(self, id = i, bitmap = self.bmp_tile_plain, size=(self.bmp_tile_plain.GetWidth()+1, self.bmp_tile_plain.GetHeight()+1))
            bmpButton.Bind(wx.EVT_RIGHT_UP, self.OnRightClick)
            gs.Add(bmpButton, 0, wx.EXPAND)
        self.SetSizer(gs)
        ###################################
        #Bindings
        ###Menu Actions
        self.Bind(wx.EVT_MENU, self.OnQuit, fileQuitItem)
        self.Bind(wx.EVT_MENU, self.OnNewGame, fileNewGame)
        ###
        self.Bind(wx.EVT_BUTTON, self.OnButton)
 
        ###################################
        
               
    def OnQuit(self, e):
        self.Close()
    
    def OnNewGame(self, e):
        pass
    
    def OnButton(self,e):    
        print("ID = {} or Coordinates: {},{}".format(e.Id, int(e.Id/BOARD_WIDTH) , e.Id % BOARD_HEIGHT))
        e.EventObject.Disable()
   
    def OnRightClick(self,e):
        print("Right ID: {}".format(e.Id))
        if self.bmp_tile_plain.Handle == e.EventObject.GetBitmapLabel().Handle:
            e.EventObject.SetBitmapLabel(Bitmap(".\\images\\tile_flag.gif"))
        else:
            e.EventObject.SetBitmapLabel(self.bmp_tile_plain)    
        

if __name__ == '__main__':
    
    app = wx.App()
    ex = MinesweeperGui(None, title='wxPython Minesweeper')
    ex.Show()
    app.MainLoop()
    
