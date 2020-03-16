import wx
import wx.xrc
import sys
import database as db
import optimizer
import bakfiets_vrp_tw as bakfiets_vrp
import t

###########################################################################
## Class Frame
###########################################################################

class Frame(wx.Frame):

	def __init__(self, parent, title, init=True):
		wx.Frame.__init__ (self, parent, id = wx.ID_ANY, title = title, pos = wx.DefaultPosition, size = wx.Size(500,300), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL)
		# init variables
		self.init = init
		self.config = 'bus'
		self.selection = []
		self.removed = []
		self.ListboxLocsChoices = []

		# Layout choices
		self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)
		self.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW))

		# set up main frame
		if self.init:
			self.MainFrame()
			self.init = False
		self.Show()
		
	def MainFrame(self):
		# sizers for geometric arrangement of widgets
		bSizerFrameMain = wx.BoxSizer(wx.VERTICAL)
		bSizerMain = wx.BoxSizer(wx.VERTICAL)

		self.panelMain = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
		self.panelMain.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW))

		bSizerMainPanel = wx.BoxSizer(wx.VERTICAL)
		bSizerPanel = wx.BoxSizer(wx.VERTICAL)
		
		# Static Header
		self.StaticHead = wx.StaticText(self.panelMain, wx.ID_ANY, u"Selecteer de locaties die niet bezocht worden:", wx.DefaultPosition, wx.DefaultSize, 0)
		self.StaticHead.Wrap(-1)
		self.StaticHead.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNTEXT))
		bSizerPanel.Add(self.StaticHead, 0, wx.ALIGN_CENTER|wx.ALL, 0)

		# Create initial Listbox
		self.init_listbox()
		
		# Sizers and Panels
		bSizerPanel.Add(self.ListboxLocs, 1, wx.ALIGN_CENTER|wx.EXPAND|wx.ALL, 0)
		bSizerMainPanel.Add(bSizerPanel, 1, wx.EXPAND, 0)

		self.panelMain.SetSizer(bSizerMainPanel)
		self.panelMain.Layout()
		bSizerMainPanel.Fit(self.panelMain)
		bSizerMain.Add(self.panelMain, 1, wx.ALL|wx.EXPAND, 0)

		# Buttons for control of application
		bSizerButtons = wx.BoxSizer(wx.HORIZONTAL)

		self.ButtonReset = wx.Button(self, wx.ID_ANY, u"Reset", wx.DefaultPosition, wx.DefaultSize, 0)
		self.ButtonReset.Bind(wx.EVT_BUTTON, self.reset)
		bSizerButtons.Add(self.ButtonReset, 0, wx.ALL|wx.EXPAND, 0)

		bSizerButtons.Add((0, 0), 1, wx.EXPAND, 0)

		self.ButtonRemove = wx.Button(self, wx.ID_ANY, u"Verwijder Selectie", wx.DefaultPosition, wx.DefaultSize, 0)
		self.ButtonRemove.Bind(wx.EVT_BUTTON, self.remove_click)
		bSizerButtons.Add(self.ButtonRemove, 0, wx.ALIGN_CENTER|wx.ALL, 5)

		bSizerButtons.Add((0, 0), 1, wx.EXPAND, 5)

		# btn = wx.Button(self, label="Open Popup")
		# btn.Bind(wx.EVT_BUTTON, self.onShowPopup)

		self.ButtonPlan = wx.Button(self, wx.ID_ANY, u"Maak Planning", wx.DefaultPosition, wx.DefaultSize, 0)
		self.ButtonPlan.Bind(wx.EVT_BUTTON, self.onShowPopup)
		bSizerButtons.Add(self.ButtonPlan, 0, wx.ALIGN_RIGHT|wx.ALL|wx.TOP, 5)
		bSizerMain.Add(bSizerButtons, 0, wx.ALL|wx.EXPAND, 5)
		bSizerFrameMain.Add(bSizerMain, 1, wx.ALL|wx.EXPAND, 0)

		self.SetSizer(bSizerFrameMain)
		self.Layout()
		
		# Menu Bar Layout
		self.menubarMain = wx.MenuBar(0)
		self.Plan = wx.Menu()
		self.menubarMain.Append(self.Plan, u"Home")
		
		self.menuItemHomeBus = wx.MenuItem(self.Plan, 11, u"Bus", wx.EmptyString, wx.ITEM_NORMAL)
		self.Plan.Append(self.menuItemHomeBus)
		
		self.menuItemHomeBike = wx.MenuItem(self.Plan, 12, u"Bakfiets", wx.EmptyString, wx.ITEM_NORMAL)
		self.Plan.Append(self.menuItemHomeBike)

		self.Edit = wx.Menu()
		self.menuItemEditAdd = wx.MenuItem(self.Edit, wx.ID_ANY, u"Voeg adres toe", wx.EmptyString, wx.ITEM_NORMAL)
		self.Edit.Append(self.menuItemEditAdd)

		self.MenuItemEditRemove = wx.MenuItem(self.Edit, wx.ID_ANY, u"Verwijder adres", wx.EmptyString, wx.ITEM_NORMAL)
		self.Edit.Append(self.MenuItemEditRemove)

		self.MenuItemParameters = wx.MenuItem(self.Edit, wx.ID_ANY, u"Wijzig Parameters", wx.EmptyString, wx.ITEM_NORMAL)
		self.Edit.Append(self.MenuItemParameters)

		self.menubarMain.Append(self.Edit, u"Wijzig Variabelen")

		self.SetMenuBar(self.menubarMain)
		self.Bind(wx.EVT_MENU, self.menuhandler)



	def __del__(self):
		pass
	
	def init_listbox(self):
		"""Create Listbox to select locations."""
		self.get_choices()
		self.ListboxLocs = wx.ListBox(self.panelMain, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, self.ListboxLocsChoices, style=wx.LB_MULTIPLE|wx.LB_SORT)
		self.ListboxLocs.Bind(wx.EVT_LISTBOX, self.selection_made)

	def update_listbox(self, remove=False):
		"""Update Listbox Choices. If remove=True, delete selection from choices first. """
		if remove:
			self.get_choices()

		self.ListboxLocs.Clear()
		self.ListboxLocs.Append(self.ListboxLocsChoices)

	def get_choices(self):
		"""If init, get full list of choices from database, depending on config.
		   Else, delete items in selection from choices. """
		if self.init:
			if self.config == 'bike':
				self.ListboxLocsChoices = sorted(db.database_list('data/Mypup_bakfiets'))
				
			else:
				self.ListboxLocsChoices = sorted(db.database_list('data/Mypup_bus'))
			self.ListboxLocsChoices.remove('Mypup')	
		else:
			for sel in self.selection:
				self.removed.append(self.ListboxLocs.GetString(sel))
			# self.remov	ed.append([self.ListboxLocs.GetString(selection) for selection in self.selection])
			print(self.removed)
			for idx in reversed(self.selection):
				del self.ListboxLocsChoices[idx]
	
	def reset(self, event):
		self.removed = []
		if self.config == 'bike':
			self.ListboxLocsChoices = sorted(db.database_list('data/Mypup_bakfiets'))
		else:
			self.ListboxLocsChoices = sorted(db.database_list('data/Mypup_bus'))
		self.ListboxLocsChoices.remove('Mypup')	
		self.update_listbox()


	
	def remove_click(self, event):
		self.update_listbox(remove=True)
		

	def plan_click(self):
		if self.config == 'bike':
			bakfiets_vrp.main(self.removed, True)
		if self.config == 'bus':
			optimizer.main(self.removed, True)	
		


	def selection_made(self, event):
		"""Update current selection whenever new selection is made. """
		self.selection = self.ListboxLocs.GetSelections()
		# selections = [self.ListboxLocs.GetString(selection) for selection in self.selection]

	

	def menuhandler(self, event):
		"""Switches between bike and bus configuration. """
		id = event.GetId()
		if id == 11:
			self.config = 'bus'
		elif id == 12:
			self.config = 'bike'
		self.reset(1)
	
	def onShowPopup(self, event):
		MyForm(self.GetTopLevelParent(), self.removed, self.config).Show()
		


class RedirectText(object):
	def __init__(self,aWxTextCtrl):
		self.out=aWxTextCtrl

	def write(self,string):
		self.out.WriteText(string)
 
class MyForm(wx.Frame):
 
	def __init__(self, parent, removed, config):
		wx.Frame.__init__(self, parent, wx.ID_ANY, "Route output")
		self.removed = removed
		self.config = config

		# Add a panel so it looks the correct on all platforms
		panel = wx.Panel(self, wx.ID_ANY)
		
		# Static Header
		self.StaticHead = wx.StaticText(panel, wx.ID_ANY, u"De resulterende routes worden hieronder geprint:", wx.DefaultPosition, wx.DefaultSize, 0)
		self.StaticHead.Wrap(-1)
		self.StaticHead.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNTEXT))
		

		log = wx.TextCtrl(panel, wx.ID_ANY, size=(300,100),
						  style = wx.TE_MULTILINE|wx.TE_READONLY|wx.HSCROLL)
		btn = wx.Button(panel, wx.ID_ANY, 'Maak Planning')
		self.Bind(wx.EVT_BUTTON, self.onButton, btn)

		# Add widgets to a sizer
		sizer = wx.BoxSizer(wx.VERTICAL)
		sizer.Add(self.StaticHead, 0, wx.ALIGN_CENTER|wx.ALL, 0)
		sizer.Add(log, 1, wx.ALL|wx.EXPAND, 5)
		sizer.Add(btn, 0, wx.ALL|wx.CENTER, 5)
		panel.SetSizer(sizer)

		# redirect text here
		redir=RedirectText(log)
		sys.stdout=redir

	def onButton(self, event):  
		if self.config == 'bike':
			bakfiets_vrp.main(self.removed, True)
		if self.config == 'bus':
			optimizer.main(self.removed, True) 

# init and show App
app = wx.App(False)
frame = Frame(None, 'Route Planner')
app.MainLoop()