import wx
import wx.xrc
import re
import pickle
import database as db

#### Panel layout for adding companies and adjusting company information
class InfoPanel(wx.Panel):
	def __init__(self, parent, id=3, CompToAdjust=None):
		wx.Panel.__init__(self, parent=parent, id=id)
		self.id = id
		self.CompToAdjust = CompToAdjust

		bSizerFrameMain = wx.BoxSizer(wx.VERTICAL)
		bSizerMain = wx.BoxSizer(wx.VERTICAL)

		self.m_panelMain = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
		self.m_panelMain.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW))

		bSizerMainPanel = wx.BoxSizer(wx.VERTICAL)

		self.bsizerPanel = wx.BoxSizer(wx.VERTICAL)

		self.AddStatic()
		
		if self.id == 8:
			with open('data/Mypup_bus.pkl', 'rb') as f:
				self.database = pickle.load(f)
		elif self.id == 9:
			with open('data/Mypup_bakfiets.pkl', 'rb') as f:
				self.database = pickle.load(f)
		
		NameSizer = wx.BoxSizer(wx.HORIZONTAL)

		self.Naam = wx.StaticText(self.m_panelMain, wx.ID_ANY, u"Bedrijfsnaam:  ", wx.DefaultPosition, wx.DefaultSize, 0)
		self.Naam.Wrap(-1)
		self.Naam.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNTEXT))

		NameSizer.Add(self.Naam, 0, wx.ALIGN_CENTER|wx.ALL, 0)
		
		if self.id in [3,4]:
			self.NameCtrl = wx.TextCtrl(self.m_panelMain, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
		else:
			self.NameCtrl = wx.TextCtrl(self.m_panelMain, wx.ID_ANY, f'{self.CompToAdjust}', wx.DefaultPosition, wx.DefaultSize, 0)

		NameSizer.Add(self.NameCtrl, 0, wx.ALIGN_CENTER|wx.ALL, 10)

		AddressSizer = wx.BoxSizer(wx.HORIZONTAL)

		self.Adres = wx.StaticText(self.m_panelMain, wx.ID_ANY, u"   Adres + Postcode:", wx.DefaultPosition, wx.DefaultSize, 0)
		self.Adres.Wrap(-1)
		self.Adres.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNTEXT))

		AddressSizer.Add(self.Adres, 0, wx.ALIGN_CENTER|wx.ALL, 0)
		if self.id in [3,4]:
			self.AddressCtrl = wx.TextCtrl(self.m_panelMain, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
		else:
			self.AddressCtrl = wx.TextCtrl(self.m_panelMain, wx.ID_ANY, f"{self.database[self.CompToAdjust]['Address']}", wx.DefaultPosition, wx.DefaultSize, 0)
		AddressSizer.Add(self.AddressCtrl, 0, wx.ALIGN_CENTER|wx.ALL, 5)


		NameSizer.Add(AddressSizer, 1, wx.EXPAND, 5)
		self.bsizerPanel.Add(NameSizer, 1, wx.EXPAND, 5)
		bSizerMainPanel.Add(self.bsizerPanel, 1, wx.EXPAND, 0)

		LoadtimeSizer = wx.BoxSizer(wx.HORIZONTAL)

		self.Laadtijd = wx.StaticText(self.m_panelMain, wx.ID_ANY, u"Laadtijd:            ", wx.DefaultPosition, wx.DefaultSize, 0)
		self.Laadtijd.Wrap(-1)
		self.Laadtijd.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNTEXT))

		LoadtimeSizer.Add(self.Laadtijd, 0, wx.ALIGN_CENTER|wx.ALL, 0)
		
		if self.id in [3,4]:
			self.LoadTimeCtrl = wx.TextCtrl(self.m_panelMain, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
		else:
			self.LoadTimeCtrl = wx.TextCtrl(self.m_panelMain, wx.ID_ANY, f"{self.database[self.CompToAdjust]['Loadtime']}", wx.DefaultPosition, wx.DefaultSize, 0)

		LoadtimeSizer.Add(self.LoadTimeCtrl, 0, wx.ALIGN_CENTER|wx.ALL, 5)

		DemandSizer = wx.BoxSizer(wx.HORIZONTAL)

		self.Demand = wx.StaticText(self.m_panelMain, wx.ID_ANY, u"    Demand:                 ", wx.DefaultPosition, wx.DefaultSize, 0)
		self.Demand.Wrap(-1)
		self.Demand.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNTEXT))

		DemandSizer.Add(self.Demand, 0, wx.ALIGN_CENTER|wx.ALL, 0)

		if self.id in [3,4]:
			self.DemandCtrl = wx.TextCtrl(self.m_panelMain, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
		else:
			self.DemandCtrl = wx.TextCtrl(self.m_panelMain, wx.ID_ANY, f"{self.database[self.CompToAdjust]['Demands']}", wx.DefaultPosition, wx.DefaultSize, 0)

		DemandSizer.Add(self.DemandCtrl, 0, wx.ALIGN_CENTER|wx.ALL, 0)


		LoadtimeSizer.Add(DemandSizer, 1, wx.EXPAND, 0)

		bSizerMainPanel.Add(LoadtimeSizer, 1, wx.EXPAND, 5)

		TimeSizer = wx.BoxSizer(wx.HORIZONTAL)

		self.TimeWindow = wx.StaticText(self.m_panelMain, wx.ID_ANY, u"Time Window : ", wx.DefaultPosition, wx.DefaultSize, 0)
		self.TimeWindow.Wrap(-1)
		self.TimeWindow.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNTEXT))

		TimeSizer.Add(self.TimeWindow, 0, wx.ALIGN_CENTER|wx.ALL, 0)

		if self.id in [3,4]:
			self.TimeCtrl = wx.TextCtrl(self.m_panelMain, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
		else:
			TimeWindow = self.FormatTW(self.database[self.CompToAdjust]['Timewindow'], to_seconds=False)
			self.TimeCtrl = wx.TextCtrl(self.m_panelMain, wx.ID_ANY, TimeWindow, wx.DefaultPosition, wx.DefaultSize, 0)
		TimeSizer.Add(self.TimeCtrl, 0, wx.ALIGN_CENTER|wx.ALL, 5)

		bSizerMainPanel.Add(TimeSizer, 1, wx.EXPAND, 5)


		self.m_panelMain.SetSizer(bSizerMainPanel)
		self.m_panelMain.Layout()
		bSizerMainPanel.Fit(self.m_panelMain)
		bSizerMain.Add(self.m_panelMain, 1, wx.EXPAND |wx.ALL, 0)
		
		if self.id in [3,4]:
			self.AddButton = wx.Button(self, wx.ID_ANY, u"Voeg toe aan Database", wx.DefaultPosition, wx.DefaultSize, 0)
			self.AddButton.Bind(wx.EVT_BUTTON, self.OnAdd)
			bSizerMain.Add(self.AddButton, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.BOTTOM, 5)
		else:
			self.AdjustButton = wx.Button(self, wx.ID_ANY, u"Pas bedrijfsgegevens aan", wx.DefaultPosition, wx.DefaultSize, 0)
			self.AdjustButton.Bind(wx.EVT_BUTTON, self.OnAdjustAction)
			bSizerMain.Add(self.AdjustButton, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.BOTTOM, 5)			

		bSizerFrameMain.Add(bSizerMain, 1, wx.ALL|wx.EXPAND, 0)

		self.SetSizer(bSizerFrameMain)
		self.Layout()

	def AddStatic(self):
		""" Adds header depending on id"""
		if self.id in [3,4]:
			self.Explainer = wx.StaticText(self.m_panelMain, wx.ID_ANY, u"Vul de bedrijfsinfo in.  Laat Demand leeg als deze hetzelfde is als de laadtijd. ", wx.DefaultPosition, wx.DefaultSize, 0)
			self.Explainer.Wrap(-1)
			self.Explainer.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNTEXT))

			self.bsizerPanel.Add(self.Explainer, 0, wx.ALIGN_CENTER|wx.ALL, 0)

			self.Explainer1 = wx.StaticText(self.m_panelMain, wx.ID_ANY, u"Laat Time Window leeg als er geen beperkingen voor bezorgtijd zijn. ", wx.DefaultPosition, wx.DefaultSize, 0)
			self.Explainer1.Wrap(-1)
			self.Explainer1.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNTEXT))

			self.bsizerPanel.Add(self.Explainer1, 0, wx.ALIGN_CENTER|wx.ALL, 0)

			self.Explainer11 = wx.StaticText(self.m_panelMain, wx.ID_ANY, u"Anders, vul de begin en eindtijd in uren als volgt in: 3,4", wx.DefaultPosition, wx.DefaultSize, 0)
			self.Explainer11.Wrap(-1)
			self.Explainer11.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNTEXT))


			self.bsizerPanel.Add(self.Explainer11, 0, wx.ALIGN_CENTER|wx.ALL, 0)
		else:
			self.Explainer = wx.StaticText(self.m_panelMain, wx.ID_ANY, u"Pas waar nodig de bedrijfsgegevens aan.  ", wx.DefaultPosition, wx.DefaultSize, 0)
			self.Explainer.Wrap(-1)
			self.Explainer.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNTEXT))

			self.bsizerPanel.Add(self.Explainer, 0, wx.ALIGN_CENTER|wx.ALL, 0)


	def OnAdd(self, event):
		"""Handles the back end functionality for the addition of companies """
		Name = self.NameCtrl.GetValue()
		Address = self.AddressCtrl.GetValue()
		LoadTime = int(self.LoadTimeCtrl.GetValue())
		Demand = LoadTime if self.DemandCtrl.GetValue()	== "" else int(self.DemandCtrl.GetValue())
		TimeWindow = self.FormatTW(self.TimeCtrl.GetValue())
		if TimeWindow == 2:
			dial = wx.MessageDialog(None, 'De vroegste tijd moet vroeger zijn dan de uiterlijke tijd.', 'Time Window',
				wx.OK | wx.ICON_ERROR)
			dial.ShowModal()
		elif TimeWindow == 3:
			dial = wx.MessageDialog(None, 'De uiterlijke tijd kan niet groter zijn dan 4 uur.', 'Time Window',
				wx.OK | wx.ICON_ERROR)
			dial.ShowModal()
		else:
			info_list = [Name, Address, LoadTime, Demand, TimeWindow]
			if self.id == 3:
				db.add_to_database(info_list, 'data/Mypup_bus')
			else:
				db.add_to_database(info_list, 'data/Mypup_bakfiets')
			dial = wx.MessageDialog(None, 'De nieuwe locatie is toegevoegd aan de database!', 'Succes',
			wx.OK | wx.ICON_INFORMATION)
			dial.ShowModal()
	
	def FormatTW(self, TW, to_seconds=True):
		"""Formats Time window correctly. to_seconds decides the direction of formatting. """
		if to_seconds:
			if TW == "":
				return "(0, 14400)"
			else:
				TW = [int(float(n)*3600) for n in re.findall(r'-?\d+\.?\d*', TW)]
				if TW[0] > TW[1]:
					return 2
				elif TW[1] > 14400:
					return 3
				else:
					return f"({TW[0]}, {TW[1]})"
		else:
			TW = [int(n)/3600 for n in re.findall(r'-?\d+\.?\d*', TW)]
			return f"{int(TW[0])},{int(TW[1])}"

	def OnAdjustAction(self, event):
		"""Handles the back end functionality for adjustments of company data. """
		Name = self.NameCtrl.GetValue()
		Address = self.AddressCtrl.GetValue()
		LoadTime = int(self.LoadTimeCtrl.GetValue())
		Demand = LoadTime if self.DemandCtrl.GetValue()	== "" else int(self.DemandCtrl.GetValue())
		TimeWindow = self.FormatTW(self.TimeCtrl.GetValue())
		if TimeWindow == 2:
			dial = wx.MessageDialog(None, 'De vroegste tijd moet vroeger zijn dan de uiterlijke tijd.', 'Time Window',
				wx.OK | wx.ICON_ERROR)
			dial.ShowModal()
		elif TimeWindow == 3:
			dial = wx.MessageDialog(None, 'De uiterlijke tijd kan niet groter zijn dan 4 uur.', 'Time Window',
				wx.OK | wx.ICON_ERROR)
			dial.ShowModal()
		else:
			info_list = [Name, Address, LoadTime, Demand, TimeWindow]
			if self.id == 8:
				db.remove_from_database(self.CompToAdjust, 'data/Mypup_bus')
				db.add_to_database(info_list, 'data/Mypup_bus')
			elif self.id == 9:
				db.remove_from_database(self.CompToAdjust, 'data/Mypup_bakfiets')
				db.add_to_database(info_list, 'data/Mypup_bakfiets')
			dial = wx.MessageDialog(None, 'De gegevens zijn gewijzigd', 'Succes',
			wx.OK | wx.ICON_INFORMATION)
			dial.ShowModal()

### Panel layout for adjustments in the model parameters
class ParamPanel(wx.Panel):
	def __init__(self, parent):
		wx.Panel.__init__(self, parent=parent)
		
		bSizerFrameMain = wx.BoxSizer(wx.VERTICAL)

		bSizerMain = wx.BoxSizer(wx.VERTICAL)

		self.m_panelMain = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
		self.m_panelMain.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_BTNTEXT))

		bSizerMainPanel = wx.BoxSizer(wx.VERTICAL)

		bSizerPanel = wx.BoxSizer(wx.VERTICAL)

		self.Explainer = wx.StaticText(self.m_panelMain, wx.ID_ANY, u"Pas waar nodig de parameters aan. Blijf binnen de aangegeven limieten. ", wx.DefaultPosition, wx.DefaultSize, 0)
		self.Explainer.Wrap(-1)

		bSizerPanel.Add(self.Explainer, 0, wx.ALIGN_CENTER|wx.ALL, 0)

		bSizerMainPanel.Add(bSizerPanel, 1, wx.EXPAND, 0)

		CapSizer = wx.BoxSizer(wx.HORIZONTAL)

		self.Cap = wx.StaticText(self.m_panelMain, wx.ID_ANY, u"Begin Capaciteit:", wx.DefaultPosition, wx.DefaultSize, 0)
		self.Cap.Wrap(-1)

		CapSizer.Add(self.Cap, 0, wx.ALIGN_CENTER|wx.ALL, 0)

		self.CapCtrl = wx.TextCtrl(self.m_panelMain, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
		CapSizer.Add(self.CapCtrl, 0, wx.ALIGN_CENTER|wx.ALL, 5)


		bSizerMainPanel.Add(CapSizer, 1, wx.EXPAND, 5)

		LfSizer = wx.BoxSizer(wx.HORIZONTAL)

		self.LF = wx.StaticText(self.m_panelMain, wx.ID_ANY, u"Load Factor:", wx.DefaultPosition, wx.DefaultSize, 0)
		self.LF.Wrap(-1)

		LfSizer.Add(self.LF, 0, wx.ALIGN_CENTER|wx.ALL, 0)

		self.LfCtrl = wx.TextCtrl(self.m_panelMain, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
		LfSizer.Add(self.LfCtrl, 0, wx.ALIGN_CENTER|wx.ALL, 5)


		bSizerMainPanel.Add(LfSizer, 1, wx.EXPAND, 5)

		WaitTimeSizer = wx.BoxSizer(wx.HORIZONTAL)

		self.WaitTime = wx.StaticText(self.m_panelMain, wx.ID_ANY, u"Maximale wachttijd:", wx.DefaultPosition, wx.DefaultSize, 0)
		self.WaitTime.Wrap(-1)

		WaitTimeSizer.Add(self.WaitTime, 0, wx.ALIGN_CENTER|wx.ALL, 0)

		self.WaitTimeCtrl = wx.TextCtrl(self.m_panelMain, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
		WaitTimeSizer.Add(self.WaitTimeCtrl, 0, wx.ALIGN_CENTER|wx.ALL, 5)


		bSizerMainPanel.Add(WaitTimeSizer, 1, wx.EXPAND, 5)

		MaxTimeSizer = wx.BoxSizer(wx.HORIZONTAL)

		self.MaxTime = wx.StaticText(self.m_panelMain, wx.ID_ANY, u"Maximale tijd per voertuig:", wx.DefaultPosition, wx.DefaultSize, 0)
		self.MaxTime.Wrap(-1)

		MaxTimeSizer.Add(self.MaxTime, 0, wx.ALIGN_CENTER|wx.ALL, 0)

		self.MaxTimeCtrl = wx.TextCtrl(self.m_panelMain, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
		MaxTimeSizer.Add(self.MaxTimeCtrl, 0, wx.ALIGN_CENTER|wx.ALL, 5)


		bSizerMainPanel.Add(MaxTimeSizer, 1, wx.EXPAND, 5)


		self.m_panelMain.SetSizer(bSizerMainPanel)
		self.m_panelMain.Layout()
		bSizerMainPanel.Fit(self.m_panelMain)
		bSizerMain.Add(self.m_panelMain, 1, wx.EXPAND |wx.ALL, 0)

		self.m_button1 = wx.Button(self, wx.ID_ANY, u"Pas parameters aan", wx.DefaultPosition, wx.DefaultSize, 0)
		
		bSizerMain.Add(self.m_button1, 0, wx.ALL, 5)
		bSizerFrameMain.Add(bSizerMain, 1, wx.ALL|wx.EXPAND, 0)
		self.SetSizer(bSizerFrameMain)
		self.Layout()
