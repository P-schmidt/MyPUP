import wx
import pickle
import database as  db


class MyFrame(wx.Frame):    
    def __init__(self):
        super().__init__(parent=None, title='Route Planner')
        panel = wx.Panel(self)
        my_sizer = wx.BoxSizer(wx.VERTICAL) 
        Bak_btn = wx.Button(panel, label='Bakfiets?')
        Bak_btn.Bind(wx.EVT_BUTTON, self.get_bakfiets_locations)
        my_sizer.Add(Bak_btn, 0, wx.ALL | wx.LEFT, 5)
        
        with open('data/Mypup_bakfiets.pkl', 'rb') as f:
            bak_locations = pickle.load(f)
        locations = list(bak_locations.keys())

        self.listBox = wx.ListBox(panel, -1, (20, 20), (80, 120), locations, wx.LB_MULTIPLE)

        # self.LB = wx.LB_MULTIPLE(panel) # text input
        my_sizer.Add(self.listBox, 0, wx.ALL | wx.EXPAND, 5)        
   
        # Bus_btn = wx.Button(panel, label='Bus?')
        # Bus_btn.Bind(wx.EVT_BUTTON, self.get_companies('data/Mypup_ams_cleaned'))
        # my_sizer.Add(Bus_btn, 0, wx.ALL | wx.RIGHT, 5) 
        panel.SetSizer(my_sizer)
        self.Show()
        

    def on_press(self, event):
        value = self.text_ctrl.GetValue()
        if not value:
         print("You didn't enter anything!")
        else:
            n_v = gf.tester(value)
            print(n_v)
    
    def get_bakfiets_locations(self, event):
        with open('data/Mypup_bakfiets.pkl', 'rb') as f:
            bak_locations = pickle.load(f)
        return bak_locations.keys()

if __name__ == '__main__':
    app = wx.App()
    frame = MyFrame()
    app.MainLoop()