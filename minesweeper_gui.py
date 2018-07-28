'''
Created on 21 Jul 2018

@author: Paulo
'''
import wx 
from minesweeper_logic import MinesweeperLogic

NUMBER_MINES = 10			#10		#40		#99
NUMBER_COLUMNS = 9 			#9		#16		#30
NUMBER_ROWS = 9				#9		#16		#16

class MinesweeperGui(wx.Frame):
	
	def __init__(self, parent, title):
		#calls wx.Frame constructor
		super(MinesweeperGui, self).__init__(parent, style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER ^ wx.MAXIMIZE_BOX)
		
		self.parent=parent
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
		
		
		self.InitGUI()
		self.logic = MinesweeperLogic(NUMBER_ROWS, NUMBER_COLUMNS, NUMBER_MINES)
		
	def InitGUI(self): 
		#Frame stuff
		self.SetSize((300, 300))
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
		###################################
		#Create Panel
		self.panel = wx.Panel(self)
		###################################	   
		#Buttons
		self.buttons=[]
		gs = wx.GridSizer(NUMBER_ROWS, NUMBER_COLUMNS,0,0)
		for i in range(0, NUMBER_ROWS*NUMBER_COLUMNS): 
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
		
		###General Button
		self.Bind(wx.EVT_BUTTON, self.OnButton)

		###################################

	def OnQuit(self, e):
		self.Close()
	
	def OnNewGame(self, e):
		self.NewGame()

	def OnButton(self,e):	
		#print("ID = {} or Coordinates: {},{}".format(e.Id, int(e.Id/NUMBER_COLUMNS) , e.Id % NUMBER_COLUMNS))
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
		
	################Aux methods#####################
	def NewGame(self):
		#Clear BTM and Enable all buttons
		for i in self.buttons:
			i.SetBitmap(self.bmpTilePlain)
			i.Enable()
		self.logic.NewGame(NUMBER_ROWS, NUMBER_COLUMNS, NUMBER_MINES)
	
		
if __name__ == '__main__':
	
	app = wx.App()
	ex = MinesweeperGui(None, title=' Minesweeper')
	ex.Show()
	app.MainLoop()
	
