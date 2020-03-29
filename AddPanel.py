# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version 3.9.0 Jan 16 2020)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

###########################################################################
## Class FrameMain
###########################################################################

class FrameMain ( wx.Frame ):

	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"Voeg toe", pos = wx.DefaultPosition, size = wx.Size( 500,300 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
		self.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )

		bSizerFrameMain = wx.BoxSizer( wx.VERTICAL )

		bSizerMain = wx.BoxSizer( wx.VERTICAL )

		self.m_panelMain = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.m_panelMain.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )

		bSizerMainPanel = wx.BoxSizer( wx.VERTICAL )

		bSizerPanel = wx.BoxSizer( wx.VERTICAL )

		self.Explainer = wx.StaticText( self.m_panelMain, wx.ID_ANY, u"Vul de bedrijfsinfo in.  Laat Demand leeg als deze hetzelfde is als de laadtijd. ", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.Explainer.Wrap( -1 )

		bSizerPanel.Add( self.Explainer, 0, wx.ALIGN_CENTER|wx.ALL, 0 )

		self.Explainer1 = wx.StaticText( self.m_panelMain, wx.ID_ANY, u"Laat Time Window leeg als er geen beperkingen voor bezorgtijd zijn. ", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.Explainer1.Wrap( -1 )

		bSizerPanel.Add( self.Explainer1, 0, wx.ALIGN_CENTER|wx.ALL, 0 )

		self.Explainer11 = wx.StaticText( self.m_panelMain, wx.ID_ANY, u"Anders, vul de begin en starttijd in uren als volgt in: 3,4", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.Explainer11.Wrap( -1 )

		bSizerPanel.Add( self.Explainer11, 0, wx.ALIGN_CENTER|wx.ALL, 0 )

		NameSizer = wx.BoxSizer( wx.HORIZONTAL )

		self.Naam = wx.StaticText( self.m_panelMain, wx.ID_ANY, u"Bedrijfsnaam:  ", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.Naam.Wrap( -1 )

		NameSizer.Add( self.Naam, 0, wx.ALIGN_CENTER|wx.ALL, 0 )

		self.NameCtrl = wx.TextCtrl( self.m_panelMain, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		NameSizer.Add( self.NameCtrl, 0, wx.ALIGN_CENTER|wx.ALL, 10 )

		AdressSizer = wx.BoxSizer( wx.HORIZONTAL )

		self.Adres = wx.StaticText( self.m_panelMain, wx.ID_ANY, u"   Adres + Postcode:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.Adres.Wrap( -1 )

		AdressSizer.Add( self.Adres, 0, wx.ALIGN_CENTER|wx.ALL, 0 )

		self.AdresCtrl = wx.TextCtrl( self.m_panelMain, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		AdressSizer.Add( self.AdresCtrl, 0, wx.ALIGN_CENTER|wx.ALL, 5 )


		NameSizer.Add( AdressSizer, 1, wx.EXPAND, 5 )


		bSizerPanel.Add( NameSizer, 1, wx.EXPAND, 5 )


		bSizerMainPanel.Add( bSizerPanel, 1, wx.EXPAND, 0 )

		LoadtimeSizer = wx.BoxSizer( wx.HORIZONTAL )

		self.Laadtijd = wx.StaticText( self.m_panelMain, wx.ID_ANY, u"Laadtijd:            ", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.Laadtijd.Wrap( -1 )

		LoadtimeSizer.Add( self.Laadtijd, 0, wx.ALIGN_CENTER|wx.ALL, 0 )

		self.LoadTimeCtrl = wx.TextCtrl( self.m_panelMain, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		LoadtimeSizer.Add( self.LoadTimeCtrl, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

		DemandSizer = wx.BoxSizer( wx.HORIZONTAL )

		self.Demand = wx.StaticText( self.m_panelMain, wx.ID_ANY, u"    Demand:                 ", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.Demand.Wrap( -1 )

		DemandSizer.Add( self.Demand, 0, wx.ALIGN_CENTER|wx.ALL, 0 )

		self.AdresCtrl2 = wx.TextCtrl( self.m_panelMain, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		DemandSizer.Add( self.AdresCtrl2, 0, wx.ALIGN_CENTER|wx.ALL, 0 )


		LoadtimeSizer.Add( DemandSizer, 1, wx.EXPAND, 0 )


		bSizerMainPanel.Add( LoadtimeSizer, 1, wx.EXPAND, 5 )

		TimeSizer = wx.BoxSizer( wx.HORIZONTAL )

		self.Time Window = wx.StaticText( self.m_panelMain, wx.ID_ANY, u"Time Window : ", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.Time Window.Wrap( -1 )

		TimeSizer.Add( self.Time Window, 0, wx.ALIGN_CENTER|wx.ALL, 0 )

		self.AdresCtrl3 = wx.TextCtrl( self.m_panelMain, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		TimeSizer.Add( self.AdresCtrl3, 0, wx.ALIGN_CENTER|wx.ALL, 5 )


		bSizerMainPanel.Add( TimeSizer, 1, wx.EXPAND, 5 )


		self.m_panelMain.SetSizer( bSizerMainPanel )
		self.m_panelMain.Layout()
		bSizerMainPanel.Fit( self.m_panelMain )
		bSizerMain.Add( self.m_panelMain, 1, wx.EXPAND |wx.ALL, 0 )

		self.m_button10 = wx.Button( self, wx.ID_ANY, u"Voeg toe aan Database", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizerMain.Add( self.m_button10, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL|wx.BOTTOM, 5 )


		bSizerFrameMain.Add( bSizerMain, 1, wx.ALL|wx.EXPAND, 0 )


		self.SetSizer( bSizerFrameMain )
		self.Layout()

	def __del__( self ):
		pass


