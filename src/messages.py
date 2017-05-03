import wx
from wx.lib import scrolledpanel
import pynder as t
from urllib.request import urlopen
import io

class Messages(wx.Frame):
    def __init__(self, parent, session):
        wx.Frame.__init__(self, parent, wx.ID_ANY, 'Messages', size=(240,500))
        self.panel = scrolledpanel.ScrolledPanel(parent = self, id = -1)
        self.panel.SetupScrolling()
        self.SetBackgroundColour(wx.Colour(100,100,100))
        
        self.session = session
        self.display_matches()
    
    
    
    def display_matches(self):
        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.images = []
        self.labels = []
        m = self.session.matches()

        for i in range(len(m)):
            match = m[i]
            # Thumb
            fd = urlopen(match.user.thumbnails[0])
            file = io.BytesIO(fd.read())
            img = wx.Image(file, wx.BITMAP_TYPE_ANY)
            self.images.append(wx.StaticBitmap(self.panel, wx.ID_ANY,
                                         wx.Bitmap(img)))
            self.images[i].Bind(wx.EVT_BUTTON, self.onClick)
            # Label for name
            self.labels.append(wx.StaticText(self.panel, label=match.user.name))
            
            # Add to sizer
            self.mainSizer.Add(self.labels[i], 0, wx.ALL, 5)
            self.mainSizer.Add(self.images[i], 0, wx.ALL, 5)
        
        self.mainSizer.Add(self.sizer, 0, wx.ALL, 5)
        self.panel.SetSizer(self.mainSizer)
        self.panel.Layout()
        self.panel.Refresh()
        
    def onClick(self, event):
        print('clicked')
        ...
