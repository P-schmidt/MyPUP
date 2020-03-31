import wx
import wx.xrc
import sys
import re
import pickle
import database as db
import optimizer
import bakfiets_vrp_tw as bakfiets_vrp
import InputPanels

###########################################################################
## Class Frame
###########################################################################
class Frame(wx.Frame):

	def __init__(self, parent, title, id = 1, CTA=None):
		wx.Frame.__init__ (self, parent, id = wx.ID_ANY, title = title, pos = wx.DefaultPosition, size = wx.Size(500,300), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL)
		# init variables
		self.init = True 
		self.id = id
		self.selection = []
		self.removed = []
		self.ListboxLocsChoices = []
		self.CTA = CTA

		# Layout choices
		self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)
		self.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW))

		# Menu Bar Layout
		self.menubarMain = wx.MenuBar(0)
		self.Plan = wx.Menu()
		self.menubarMain.Append(self.Plan, u"Planner")
		
		self.menuItemHomeBus = wx.MenuItem(self.Plan, 1, u"Bus", wx.EmptyString, wx.ITEM_NORMAL)
		self.Plan.Append(self.menuItemHomeBus)
		
		self.menuItemHomeBike = wx.MenuItem(self.Plan, 2, u"Bakfiets", wx.EmptyString, wx.ITEM_NORMAL)
		self.Plan.Append(self.menuItemHomeBike)

		self.Edit = wx.Menu()

		self.MenuItemEditAdd = wx.Menu()

		self.MenuItemAddBus = wx.MenuItem(self.MenuItemEditAdd, 3, u"Bus", wx.EmptyString, wx.ITEM_NORMAL)
		self.MenuItemEditAdd.Append(self.MenuItemAddBus)

		self.MenuItemAddBike = wx.MenuItem(self.MenuItemEditAdd, 4, u"Bakfiets", wx.EmptyString, wx.ITEM_NORMAL)
		self.MenuItemEditAdd.Append(self.MenuItemAddBike)

		self.Edit.AppendSubMenu(self.MenuItemEditAdd, u"Voeg locatie toe")


		self.MenuItemEditRemove = wx.MenuItem(self.Edit, 5, u"Verwijder Locatie", wx.EmptyString, wx.ITEM_NORMAL)
		self.Edit.Append(self.MenuItemEditRemove)

		self.MenuItemParameters = wx.MenuItem(self.Edit, 6, u"Wijzig Parameters", wx.EmptyString, wx.ITEM_NORMAL)
		self.Edit.Append(self.MenuItemParameters)

		self.MenuItemAdjust = wx.MenuItem(self.Edit, 7, u"Wijzig bedrijfsgegevens", wx.EmptyString, wx.ITEM_NORMAL)
		self.Edit.Append(self.MenuItemAdjust)	

		self.MenuItemSwitch = wx.Menu()

		self.MenuItemSwitchBus = wx.MenuItem(self.MenuItemSwitch, 10, u"Bus", wx.EmptyString, wx.ITEM_NORMAL)
		self.MenuItemSwitch.Append(self.MenuItemSwitchBus)

		self.MenuItemSwitchBike = wx.MenuItem(self.MenuItemSwitch, 11, u"Bakfiets", wx.EmptyString, wx.ITEM_NORMAL)
		self.MenuItemSwitch.Append(self.MenuItemSwitchBike)

		self.Edit.AppendSubMenu(self.MenuItemSwitch, u"Switch tussen vervoersmiddel")


		self.menubarMain.Append(self.Edit, u"Wijzig Gegevens")

		self.SetMenuBar(self.menubarMain)
		self.Bind(wx.EVT_MENU, self.menuhandler)
		if self.id in [1,2]:
			self.PlanPanel()
			self.init = False
		elif self.id in [3,4]:
			InputPanels.InfoPanel(self.GetTopLevelParent(), self.id)
		elif self.id == 5:
			self.AdjustPanel()
		elif self.id == 6:
			InputPanels.ParamPanel(self.GetTopLevelParent())
		elif self.id in [7, 10, 11]:
			self.AdjustPanel()
		elif self.id in [8,9]:
			InputPanels.InfoPanel(self.GetTopLevelParent(), self.id, self.CTA)
	

		self.Show()
		
	def PlanPanel(self):
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

		self.ButtonPlan = wx.Button(self, wx.ID_ANY, u"Ga naar Planner", wx.DefaultPosition, wx.DefaultSize, 0)
		self.ButtonPlan.Bind(wx.EVT_BUTTON, self.onShowPopup)
		bSizerButtons.Add(self.ButtonPlan, 0, wx.ALIGN_RIGHT|wx.ALL|wx.TOP, 5)
		bSizerMain.Add(bSizerButtons, 0, wx.ALL|wx.EXPAND, 5)
		bSizerFrameMain.Add(bSizerMain, 1, wx.ALL|wx.EXPAND, 0)

		self.SetSizer(bSizerFrameMain)
		self.Layout()
			
	def AdjustPanel(self):
		# sizers for geometric arrangement of widgets
		bSizerFrameMain = wx.BoxSizer(wx.VERTICAL)
		bSizerMain = wx.BoxSizer(wx.VERTICAL)

		self.panelMain = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
		self.panelMain.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW))

		bSizerMainPanel = wx.BoxSizer(wx.VERTICAL)
		bSizerPanel = wx.BoxSizer(wx.VERTICAL)
		
		# Static Header
		if self.id == 5:
			self.StaticHead = wx.StaticText(self.panelMain, wx.ID_ANY, u"Selecteer de locaties die verwijderd moeten worden:", wx.DefaultPosition, wx.DefaultSize, 0)
		elif self.id == 7:
			self.StaticHead = wx.StaticText(self.panelMain, wx.ID_ANY, u"Selecteer de locatie die aangepast moet worden:", wx.DefaultPosition, wx.DefaultSize, 0)
		elif self.id == 10: 
			self.StaticHead = wx.StaticText(self.panelMain, wx.ID_ANY, u"Selecteer de locaties die met de fiets bezorgd moeten worden:", wx.DefaultPosition, wx.DefaultSize, 0)
		elif self.id == 11: 
			self.StaticHead = wx.StaticText(self.panelMain, wx.ID_ANY, u"Selecteer de locaties die met de bus bezorgd moeten worden:", wx.DefaultPosition, wx.DefaultSize, 0)
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
		if self.id == 5:
			self.ButtonRemove = wx.Button(self, wx.ID_ANY, u"Verwijder selectie uit Database", wx.DefaultPosition, wx.DefaultSize, 0)
			self.ButtonRemove.Bind(wx.EVT_BUTTON, self.OnDelete)
			bSizerButtons.Add(self.ButtonRemove, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5)
		elif self.id == 7:
			self.ButtonAdjust = wx.Button(self, wx.ID_ANY, u"Pas geselecteerde bedrijf aan", wx.DefaultPosition, wx.DefaultSize, 0)
			self.ButtonAdjust.Bind(wx.EVT_BUTTON, self.OnAdjust)
			bSizerButtons.Add(self.ButtonAdjust, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5)
		else:
			self.ButtonSwitch = wx.Button(self, wx.ID_ANY, u"Switch bedrijf", wx.DefaultPosition, wx.DefaultSize, 0)
			self.ButtonSwitch.Bind(wx.EVT_BUTTON, self.OnSwitch)
			bSizerButtons.Add(self.ButtonSwitch, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5)

		bSizerButtons.Add((0, 0), 1, wx.EXPAND, 5)
		bSizerMain.Add(bSizerButtons, 0, wx.ALL|wx.EXPAND, 5)
		bSizerFrameMain.Add(bSizerMain, 1, wx.ALL|wx.EXPAND, 0)

		self.SetSizer(bSizerFrameMain)
		self.Layout()

	def OnSwitch(self, event):
		switch = [self.ListboxLocs.GetString(sel) for sel in self.selection]
		if not switch:
			dial = wx.MessageDialog(None, 'Er is geen locatie geselecteerd', '',
			wx.OK | wx.ICON_INFORMATION)
			dial.ShowModal()
		else:
			if self.id == 10:
				with open('data/Mypup_bus.pkl', 'rb') as f:
					database = pickle.load(f)
				for loc in switch:
					info_list = [loc, database[loc]['Address'], database[loc]['Loadtime'], database[loc]['Demands'], database[loc]['Timewindow']]
					db.remove_from_database(loc, 'data/Mypup_bus')
					db.add_to_database(info_list, 'data/Mypup_bakfiets')
			elif self.id == 11:
				with open('data/Mypup_bakfiets.pkl', 'rb') as f:
					database = pickle.load(f)	
				for loc in switch:
					info_list = [loc, database[loc]['Address'], database[loc]['Loadtime'], database[loc]['Demands'], database[loc]['Timewindow']]
					db.remove_from_database(loc, 'data/Mypup_bakfiets')
					db.add_to_database(info_list, 'data/Mypup_bus')

			dial = wx.MessageDialog(None, 'De locaties zijn verplaatst naar de juiste planner!', 'Succes',
				wx.OK | wx.ICON_INFORMATION)
			dial.ShowModal()

	def OnAdjust(self, event):
		CompToAdjust = self.ListboxLocs.GetString(self.selection[0])
		if not CompToAdjust:
			dial = wx.MessageDialog(None, 'Er is geen locatie geselecteerd', '',
			wx.OK | wx.ICON_INFORMATION)
			dial.ShowModal()
		if CompToAdjust in db.database_list('data/Mypup_bus'):
			self.Destroy()
			Frame(None, 'Wijzig Bedrijfsgegevens', id=8, CTA=CompToAdjust)
		else: 
			self.Destroy()
			Frame(None, 'Wijzig Bedrijfsgegevens', id=9, CTA=CompToAdjust)


	def OnDelete(self, event):
		delete = [self.ListboxLocs.GetString(sel) for sel in self.selection]
		if not delete:
			dial = wx.MessageDialog(None, 'Er is geen locatie geselecteerd', '',
			wx.OK | wx.ICON_INFORMATION)
			dial.ShowModal()
		else:
			dial = wx.MessageDialog(None, 'Weet je zeker dat deze locaties verwijderd moeten worden?', '',
			wx.YES_NO | wx.NO_DEFAULT | wx.ICON_INFORMATION)
			ret = dial.ShowModal()

			if ret == wx.ID_YES:
				for loc in delete:
					if loc in db.database_list('data/Mypup_bus'):
						db.remove_from_database(loc, 'data/Mypup_bus')
						dial = wx.MessageDialog(None, 'De locaties zijn uit de database verwijderd!', 'Succes',
							wx.OK | wx.ICON_INFORMATION)
						dial.ShowModal()
					elif loc in db.database_list('data/Mypup_bakfiets'):
						db.remove_from_database(loc, 'data/Mypup_bakfiets')
						dial = wx.MessageDialog(None, 'De locaties zijn uit de database verwijderd!', 'Succes',
							wx.OK | wx.ICON_INFORMATION)
						dial.ShowModal()	
					else:
						dial = wx.MessageDialog(None, 'Deze locatie is al verwijderd', '',
						wx.OK | wx.ICON_INFORMATION)
						dial.ShowModal()
						pass
			else:
				pass
			
	def init_listbox(self):
		"""Create Listbox to select locations."""
		self.get_choices()
		if self.id == 7:
			self.ListboxLocs = wx.ListBox(self.panelMain, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, self.ListboxLocsChoices, style=wx.LB_SINGLE|wx.LB_SORT)
		else:
			self.ListboxLocs = wx.ListBox(self.panelMain, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, self.ListboxLocsChoices, style=wx.LB_MULTIPLE|wx.LB_SORT)
		self.ListboxLocs.Bind(wx.EVT_LISTBOX, self.selection_made)

	def update_listbox(self, remove=False):
		"""Update Listbox Choices. If remove=True, delete selection from choices first. """
		if remove:
			self.get_choices()

		self.ListboxLocs.Clear()
		self.ListboxLocs.Append(self.ListboxLocsChoices)

	def get_choices(self):
		"""If init, get full list of choices from database, depending on id.
		   Else, delete items in selection from choices. """
		if self.init:
			if self.id in [1,10]:
				self.ListboxLocsChoices = sorted(db.database_list('data/Mypup_bus'))
			elif self.id in [2,11]:
				self.ListboxLocsChoices = sorted(db.database_list('data/Mypup_bakfiets'))	
			else:
				self.ListboxLocsChoices = sorted(db.database_list('data/Mypup_bus') + db.database_list('data/Mypup_bakfiets'))	
			while 'Mypup' in self.ListboxLocsChoices:
				self.ListboxLocsChoices.remove('Mypup')	
		else:
			for sel in self.selection:
				self.removed.append(self.ListboxLocs.GetString(sel))
			for idx in reversed(self.selection):
				del self.ListboxLocsChoices[idx]
	
	def reset(self, event):
		self.removed = []
		if self.id == 2:
			self.ListboxLocsChoices = sorted(db.database_list('data/Mypup_bakfiets'))
		else:
			self.ListboxLocsChoices = sorted(db.database_list('data/Mypup_bus'))
		self.ListboxLocsChoices.remove('Mypup')	
		self.update_listbox()


	
	def remove_click(self, event):
		self.update_listbox(remove=True)
		

	def selection_made(self, event):
		"""Update current selection whenever new selection is made. """
		self.selection = self.ListboxLocs.GetSelections()

	def menuhandler(self, event):
		"""Switches between configurations. """
		id = event.GetId()
		if id == 1:
			# self.id= 1
			self.Destroy()
			Frame(None, 'Route Planner Bus', id=1)
		elif id == 2:
			# self.id = 2
			self.Destroy()
			Frame(None, 'Route Planner Bakfiets', id=2)
		elif id == 3:
			self.Destroy()
			Frame(None, 'Voeg Locaties Toe Aan Busroute', id=3)
		elif id == 4:
			self.Destroy()
			Frame(None, 'Voeg Locaties Toe Aan Fietsroute', id=4)
		elif id == 5:
			self.Destroy()
			Frame(None, 'Verwijder Locaties', id=5)
		elif id == 6:
			self.Destroy()
			Frame(None, 'Pas parameters aan', id=6)
		elif id == 7:
			self.Destroy()
			Frame(None, 'Wijzig Bedrijfsgegevens', id=7)
		elif id == 10:
			self.Destroy()
			Frame(None, 'Switch locatie van Bus naar Bakfiets', id=10)
		elif id == 11:
			self.Destroy()
			Frame(None, 'Switch locatie van Bakfiets naar Bus', id=11)
		
	
	def onShowPopup(self, event):
		MyForm(self.GetTopLevelParent(), self.removed, self.id).Show()
		


class RedirectText(object):
	def __init__(self,aWxTextCtrl):
		self.out=aWxTextCtrl

	def write(self,string):
		self.out.WriteText(string)
 
class MyForm(wx.Frame):
 
	def __init__(self, parent, removed, id):
		wx.Frame.__init__(self, parent, wx.ID_ANY, "Route output")
		self.removed = removed
		self.id = id

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
		if self.id == 1:
			optimizer.main(self.removed) 
		if self.id == 2:
			bakfiets_vrp.main(self.removed)


# init and show App
app = wx.App(False)
frame = Frame(None, 'Route Planner Bus')
app.MainLoop()

