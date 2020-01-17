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
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"Route Planner", pos = wx.DefaultPosition, size = wx.Size( 500,300 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
		self.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )

		bSizerFrameMain = wx.BoxSizer( wx.VERTICAL )

		bSizerMain = wx.BoxSizer( wx.VERTICAL )

		self.m_panelMain = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.m_panelMain.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )

		bSizerMainPanel = wx.BoxSizer( wx.VERTICAL )

		bSizerPanel = wx.BoxSizer( wx.VERTICAL )

		self.StaticHead = wx.StaticText( self.m_panelMain, wx.ID_ANY, u"Selecteer de locaties die niet bezocht worden:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.StaticHead.Wrap( -1 )

		self.StaticHead.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNTEXT ) )

		bSizerPanel.Add( self.StaticHead, 0, wx.ALIGN_CENTER|wx.ALL, 0 )


		bSizerMainPanel.Add( bSizerPanel, 1, wx.EXPAND, 0 )


		self.m_panelMain.SetSizer( bSizerMainPanel )
		self.m_panelMain.Layout()
		bSizerMainPanel.Fit( self.m_panelMain )
		bSizerMain.Add( self.m_panelMain, 1, wx.ALL|wx.EXPAND, 0 )

		bSizerButtons = wx.BoxSizer( wx.HORIZONTAL )

		self.m_buttonReset = wx.Button( self, wx.ID_ANY, u"Reset", wx.DefaultPosition, wx.DefaultSize, 0 )

		self.m_buttonReset.SetBitmapPosition( wx.TOP )
		bSizerButtons.Add( self.m_buttonReset, 0, wx.ALL|wx.EXPAND, 0 )


		bSizerButtons.Add( ( 0, 0), 1, wx.EXPAND, 0 )

		self.ButtonRemove = wx.Button( self, wx.ID_ANY, u"Verwijder Selectie", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizerButtons.Add( self.ButtonRemove, 0, wx.ALIGN_CENTER|wx.ALL, 5 )


		bSizerButtons.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		self.m_button3 = wx.Button( self, wx.ID_ANY, u"Maak Planning", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_button3.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOWTEXT ) )

		bSizerButtons.Add( self.m_button3, 0, wx.ALIGN_RIGHT|wx.ALL|wx.TOP, 5 )


		bSizerMain.Add( bSizerButtons, 0, wx.ALL|wx.EXPAND, 5 )


		bSizerFrameMain.Add( bSizerMain, 1, wx.ALL|wx.EXPAND, 0 )


		self.SetSizer( bSizerFrameMain )
		self.Layout()
		self.menubarMain = wx.MenuBar( 0 )
		self.Plan = wx.Menu()
		self.menubarMain.Append( self.Plan, u"Home" )

		self.Edit = wx.Menu()
		self.m_menuItemEditAdd = wx.MenuItem( self.Edit, wx.ID_ANY, u"Voeg Toe", wx.EmptyString, wx.ITEM_NORMAL )
		self.Edit.Append( self.m_menuItemEditAdd )

		self.m_menuItemEditRemove = wx.MenuItem( self.Edit, wx.ID_ANY, u"Verwijder", wx.EmptyString, wx.ITEM_NORMAL )
		self.Edit.Append( self.m_menuItemEditRemove )

		self.menubarMain.Append( self.Edit, u"Wijzig Adressen" )

		self.SetMenuBar( self.menubarMain )


	def __del__( self ):
		pass


app = wx.App(False)
frame = FrameMain(None)
frame.Show()
app.MainLoop()