'''
Created on 21 Jul 2018

@author: Paulo
'''
import wx 
from minesweeper.minesweeper_logic import MinesweeperLogic

class MinesweeperGui(wx.Frame):
    
    def __init__(self, title):
        #calls wx.Frame constructor
        super(MinesweeperGui, self).__init__(None, style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER ^ wx.MAXIMIZE_BOX)
                
        self.title=title
        
        self.bmpTilePlain = wx.Bitmap("./images/tile_plain.gif")
        self.bmpTileFlag = wx.Bitmap("./images/tile_flag.gif")
        self.bmpTileClicked = wx.Bitmap("./images/tile_clicked.gif")
        self.bmpTileMine = wx.Bitmap("./images/tile_mine.gif")
        self.bmpTileWrong = wx.Bitmap("./images/tile_wrong.gif")
        self.bmpNumbers = [wx.Bitmap("./images/tile_clicked.gif"),
                            wx.Bitmap("./images/tile_1.gif"),
                            wx.Bitmap("./images/tile_2.gif"),
                            wx.Bitmap("./images/tile_3.gif"),
                            wx.Bitmap("./images/tile_4.gif"),
                            wx.Bitmap("./images/tile_5.gif"),
                            wx.Bitmap("./images/tile_6.gif"),
                            wx.Bitmap("./images/tile_7.gif"),
                            wx.Bitmap("./images/tile_8.gif")]
        
        self.TILE_SIZE = 28
        self.MENU_HEIGHT = 60
        
        self.gameSettings=[
                            { 'numberRows': 9, 'numberColumns': 9, 'numberMines': 10 },
                            { 'numberRows': 16, 'numberColumns': 16, 'numberMines': 40 },
                            { 'numberRows': 16, 'numberColumns': 30, 'numberMines': 99 },
                            { 'numberRows': 0, 'numberColumns': 0, 'numberMines': 0 }
                         ]
        #pointer for the gameSettings
        self.gameSettingsPointer = 0
        
        self.InitGUI()
        self.logic = MinesweeperLogic(self.gameSettings[self.gameSettingsPointer]['numberRows'], 
                                      self.gameSettings[self.gameSettingsPointer]['numberColumns'], 
                                      self.gameSettings[self.gameSettingsPointer]['numberMines'])
        
    def InitGUI(self): 
                
        #Frame stuff
        
        self.SetSize((self.gameSettings[self.gameSettingsPointer]['numberColumns'] * self.TILE_SIZE , 
                      self.gameSettings[self.gameSettingsPointer]['numberRows'] * self.TILE_SIZE  + self.MENU_HEIGHT)) 
        self.SetTitle(self.title)
        self.Centre()
                
        icon = wx.Icon()
        icon.CopyFromBitmap(wx.Bitmap(".\images\icon.png", wx.BITMAP_TYPE_ANY))
        self.SetIcon(icon)
        
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
        optionsMenu = wx.Menu()
        settings = optionsMenu.Append(wx.ID_PREFERENCES, '&Settings', 'Settings')
        menubar.Append(optionsMenu, '&Options')
        ###################################
        #Create Panel
        self.panel = wx.Panel(self)
        ###################################       
        #Buttons
        self.buttons=[]
        self.gs = wx.GridSizer(self.gameSettings[self.gameSettingsPointer]['numberRows'], 
                               self.gameSettings[self.gameSettingsPointer]['numberColumns'],
                               0,
                               0)
        for i in range(0, self.gameSettings[self.gameSettingsPointer]['numberRows']*self.gameSettings[self.gameSettingsPointer]['numberColumns']): 
            bmpButton = wx.BitmapButton(self.panel, id = i, bitmap = self.bmpTilePlain, )
            #Bind Right Click
            bmpButton.Bind(wx.EVT_RIGHT_UP, self.OnRightClick)
            self.buttons.append(bmpButton)
            self.gs.Add(bmpButton, 0, wx.EXPAND)
        self.panel.SetSizer(self.gs)
        ###################################
        
        #Bindings
        ###Menu Actions
        self.Bind(wx.EVT_MENU, self.OnQuit, fileQuitItem)
        self.Bind(wx.EVT_MENU, self.OnNewGame, fileNewGame)
        self.Bind(wx.EVT_MENU, self.OnSettings, settings)
        self.Bind(wx.EVT_BUTTON, self.OnButton)

        ###################################

    def OnQuit(self, e):
        self.Close()
    
    def OnNewGame(self, e):
        self.NewGame()

    def OnButton(self,e):    
        #print("ID = {} or Coordinates: {},{}".format(e.Id, int(e.Id/ self.gameSettings[self.gameSettingsPointer]['numberColumns']) , e.Id % self.gameSettings[self.gameSettingsPointer]['numberColumns'] ))
        result = self.logic.ClickMove(e.Id)
        
        if result['mine'] == True:
            for mine in self.logic.ShowMines():
                button = wx.Window.FindWindowById(mine)
                button.SetBitmap(self.bmpTileMine)
            e.EventObject.SetBitmap(self.bmpTileWrong)
            wx.MessageBox("BOOOOMMM - You found a mine!", "GAME OVER", wx.ICON_ERROR)
            self.NewGame()
            
        else:    
            for cell in result["tile_info"]:
                cell_id, value = cell
                button = wx.Window.FindWindowById(cell_id)
                button.SetBitmapDisabled(self.bmpNumbers[value])
                button.Disable()
            
            #To avoid focus going to the next button, set focus on frame
            self.SetFocus()
            
            if result['finish'] == True:
                wx.MessageBox("Congratulations You Won!", "Congratulations")
                self.NewGame()

    def OnRightClick(self,e):
        #print("Right ID: {}".format(e.Id))
        
        self.logic.FlagMove(e.Id)
        
        if self.bmpTilePlain.Handle == e.EventObject.GetBitmapLabel().Handle:
            e.EventObject.SetBitmapLabel(self.bmpTileFlag)
        else:
            e.EventObject.SetBitmapLabel(self.bmpTilePlain)    
    
    def OnSettings(self, e):
        settingsDialog = Settings(parent = self, pointer = self.gameSettingsPointer, settings = self.gameSettings)
        res = settingsDialog.ShowModal()
        
        if res == wx.ID_OK:
            index, rows, columns , mines = settingsDialog.GetSettings()
            self.gameSettingsPointer = index 
            #custom
            if index == 3:
                self.gameSettings[3]['numberRows'] = rows 
                self.gameSettings[3]['numberColumns'] = columns 
                self.gameSettings[3]['numberMines'] = mines
                     
        settingsDialog.Destroy()
            
################Aux methods#####################

    def NewGame(self):
        
        #remove all buttons
        numberButtons = len(self.buttons)
        while self.gs.GetChildren():
            button = self.gs.GetItem(numberButtons - 1).GetWindow()
            # Calling Destroy removes widget from parent and sizer
            button.Destroy()
            numberButtons -= 1
        self.buttons.clear()
        
        #resize gs
        self.gs.SetCols(self.gameSettings[self.gameSettingsPointer]['numberColumns'])
        self.gs.SetRows(self.gameSettings[self.gameSettingsPointer]['numberRows'])
        #add buttons
        for i in range(  self.gameSettings[self.gameSettingsPointer]['numberColumns'] \
                       * self.gameSettings[self.gameSettingsPointer]['numberRows']):
            bmpButton = wx.BitmapButton(self.panel, id = i, bitmap = self.bmpTilePlain, )
            #Bind left Right
            bmpButton.Bind(wx.EVT_RIGHT_UP, self.OnRightClick)
            self.buttons.append(bmpButton)
            self.gs.Add(bmpButton, 0, wx.EXPAND)
        
        self.SetSize((self.gameSettings[self.gameSettingsPointer]['numberColumns'] * self.TILE_SIZE , 
                      self.gameSettings[self.gameSettingsPointer]['numberRows'] * self.TILE_SIZE + self.MENU_HEIGHT))
        
        self.panel.SetSizer(self.gs)
        self.panel.Layout()
        self.Fit()
       
        
        self.logic.NewGame(self.gameSettings[self.gameSettingsPointer]['numberRows'],
                            self.gameSettings[self.gameSettingsPointer]['numberColumns'], 
                            self.gameSettings[self.gameSettingsPointer]['numberMines']
                            )
            
class Settings(wx.Dialog):
    def __init__(self, parent, pointer, settings):
        super().__init__(parent)
        
        self.SetSize((350,200))
        self.SetTitle("Minesweeper Settings")
        icon = wx.Icon()
        icon.CopyFromBitmap(wx.Bitmap(".\images\icon.png", wx.BITMAP_TYPE_ANY))
        self.SetIcon(icon)
        
        self.panel = wx.Panel(self, wx.ID_ANY)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        
        self.radioButtons=[]
        for i in range(4):
            rb = None
            
            if i==0:
                rb = wx.RadioButton(self.panel, 0, label='Easy: 9 x 9 with 10 mines', style = wx.RB_GROUP)
                sz = rb
            elif i==1:
                rb = wx.RadioButton(self.panel, 1, label='Medium: 16 x 16 with 40 mines')
                sz = rb
            elif i==2:
                rb = wx.RadioButton(self.panel, 2, label='Hard: 16 x 30 with 99 mines')
                sz = rb
            else:
                sz = wx.BoxSizer(wx.HORIZONTAL)
                rb = wx.RadioButton(self.panel, 3, label='Custom:')
                sz.Add(rb)
                
                self.inputRows = wx.TextCtrl(self.panel, wx.ID_ANY, '', size=(40,-1))
                sz.Add(self.inputRows ,proportion = 0, flag = wx.RIGHT | wx.LEFT | wx.ALIGN_CENTER_VERTICAL, border = 2)
                self.inputRows.Enable(False)
                
                labelOne = wx.StaticText(self.panel, wx.ID_ANY, 'x')             
                sz.Add(labelOne ,proportion = 0, flag = wx.RIGHT | wx.LEFT | wx.ALIGN_CENTER_VERTICAL, border = 2)
                
                self.inputColumns = wx.TextCtrl(self.panel, wx.ID_ANY, '', size=(40,-1))
                sz.Add(self.inputColumns ,proportion = 0, flag = wx.RIGHT | wx.LEFT | wx.ALIGN_CENTER_VERTICAL, border = 2)
                self.inputColumns.Enable(False)
                
                labelTwo = wx.StaticText(self.panel, wx.ID_ANY, 'with')             
                sz.Add(labelTwo ,proportion = 0, flag = wx.RIGHT | wx.LEFT | wx.ALIGN_CENTER_VERTICAL, border = 2)
                
                self.inputMines = wx.TextCtrl(self.panel, wx.ID_ANY, '', size=(40,-1))
                sz.Add(self.inputMines ,proportion = 0, flag = wx.RIGHT | wx.LEFT | wx.ALIGN_CENTER_VERTICAL, border = 2)
                self.inputMines.Enable(False)
                
                labelThree = wx.StaticText(self.panel, wx.ID_ANY, 'mines')             
                sz.Add(labelThree ,proportion = 0, flag = wx.LEFT | wx.ALIGN_CENTER_VERTICAL, border = 2)
                
                
            self.sizer.Add(sz, proportion = 0, flag = wx.ALL, border = 6)
            self.radioButtons.append(rb)
        
        self.Bind(wx.EVT_RADIOBUTTON, self.onRadioButton)
        
        self.pointer = pointer
            
        self.radioButtons[self.pointer].SetValue(True)
        
         
        if self.pointer == 3:
            self.inputRows.Enable(True); self.inputColumns.Enable(True); self.inputMines.Enable(True);
            self.inputRows.SetValue(str(settings[self.pointer]['numberRows']))
            self.inputColumns.SetValue(str(settings[self.pointer]['numberColumns']))
            self.inputMines.SetValue(str(settings[self.pointer]['numberMines']))
        
        self.buttonSizer = wx.BoxSizer(wx.HORIZONTAL)
        
        self.button_ok = wx.Button(self.panel, label="OK")
        self.button_cancel = wx.Button(self.panel, label="Cancel")
        self.button_ok.Bind(wx.EVT_BUTTON, self.onOk)
        self.button_cancel.Bind(wx.EVT_BUTTON, self.onCancel)
               
        self.buttonSizer.Add(self.button_ok, proportion = 0, flag = wx.ALL, border = 5)
        self.buttonSizer.Add(self.button_cancel, proportion = 0, flag = wx.ALL, border = 5)
        
        self.sizer.Add(self.buttonSizer)

        self.panel.SetSizerAndFit(self.sizer)
               
    def onCancel(self, e):
        self.EndModal(wx.ID_CANCEL)

    def onOk(self, e):
        #Custom entry
        if self.pointer == 3:
            #Validate user input
            try:
                assert (int(self.inputRows.GetValue()) * int(self.inputColumns.GetValue())) > (int(self.inputMines.GetValue()) - 4)
            except ValueError:
                wx.MessageBox("Please insert only numbers in the fields!", "Error", wx.ICON_ERROR)
                return                
            except AssertionError:     
                wx.MessageBox("Number of mines is too big for the board!", "Error", wx.ICON_ERROR)
                return            
        
        self.EndModal(wx.ID_OK)

    def onRadioButton(self, e):
        if e.Id == 3:
            self.inputRows.Enable(True); self.inputColumns.Enable(True); self.inputMines.Enable(True);
        else:
            self.inputRows.Enable(False); self.inputColumns.Enable(False); self.inputMines.Enable(False);    
        
        self.pointer = e.Id
        
    def GetSettings(self):
        i=0
        for rButton in self.radioButtons:
            if rButton.GetValue() == True:
                if i==3:
                    return (i, int(self.inputRows.GetValue()), int(self.inputColumns.GetValue()), int(self.inputMines.GetValue()))
                return (i, 0, 0, 0)
            i+=1
    
        
if __name__ == '__main__':
    
    app = wx.App()
    ex = MinesweeperGui(title=' Minesweeper')
    ex.Show()
    app.MainLoop()
    
