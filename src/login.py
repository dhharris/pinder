import wx

class LoginDialog(wx.Dialog):
    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, wx.ID_ANY, 'Facebook Login', size= (650,220))
        self.panel = wx.Panel(self,wx.ID_ANY)

        self.lbluser = wx.StaticText(self.panel, label='Username', pos=(20,20))
        self.user = wx.TextCtrl(self.panel, value="", pos=(110,20), size=(500,-1))
        self.lblpassword = wx.StaticText(self.panel, label='Password', pos=(20,60))
        self.password = wx.TextCtrl(self.panel, value="", pos=(110,60), size=(500,-1), style=wx.TE_PASSWORD)
        
        self.submitButton =wx.Button(self.panel, label='Submit', pos=(110,160))
        self.closeButton = wx.Button(self.panel, label='Cancel', pos=(210,160))
        self.submitButton.Bind(wx.EVT_BUTTON, self.SaveConnString)
        self.closeButton.Bind(wx.EVT_BUTTON, self.OnQuit)
        self.Bind(wx.EVT_CLOSE, self.OnQuit)

    def OnQuit(self, event):
        self.result_user = None
        self.EndModal(wx.ID_ABORT)

    def SaveConnString(self, event):
        self.result_user = self.user.GetValue()
        self.result_password = self.password.GetValue()
        self.EndModal(wx.ID_OK)
