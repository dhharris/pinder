import wx
import pynder as t
from urllib.request import urlopen
import io
from geopy.geocoders import Nominatim
import threading
import auth
import os
import time
from login import LoginDialog

class PinderApp(wx.App):
    def __init__(self, redirect=False):
        '''
        Takes a location as a tuple of the form (LAT, LON)
        '''
        # App fields
        wx.App.__init__(self, redirect)
        self.frame = wx.Frame(None, title='Pinder')

        self.panel = wx.Panel(self.frame)

        self.PhotoMaxSize = 240


        self.createWidgets()
        self.frame.Show()


        # Authenticate Facebook token
        self.login()
        
        # Start pynder session
        self.start_session()
        
        # Geopy fields
        self.location = 'Somewhere'
        self.latlon = None

        # Ask for initial location
        self.onChangeLoc(None)

        self.users = []
        self.users_index = 0
        self.hopeful = None
        self.update_user()
        
    def start_session(self):
        # Create pynder session
        self.facebook_id = auth.get_fb_id(self.facebook_token)
        self.session = t.Session(self.facebook_id, self.facebook_token)
        self.prof = self.session.profile
        self.canlike = self.session.likes_remaining != 0
    
    def login(self):
        try:
            # Check for previous token
            with open('.token', 'r') as f:
                self.facebook_token = f.read()
        except:
            tokget = False
            while not tokget:
                # Ask for username and password
                dlg = LoginDialog(parent=self.frame)
                if dlg.ShowModal() == wx.ID_OK:
                    # do something here
                    username = dlg.result_user
                    password = dlg.result_password
                    dlg.Destroy()
                else:
                    dlg.Destroy()
                    print('Exiting')
                    os._exit(0)
                try:
                    self.facebook_token = auth.get_fb_access_token(username, password)
                    if type(self.facebook_token) != dict:
                        tokget = True
                except:
                    print('Login failed')
                
            # Write token to file to keep user logged in
            with open('.token', 'w+') as f:
                f.write(self.facebook_token)
                

    def createWidgets(self):

        # Image control
        img = wx.Image(240, 240)
        self.imageCtrl = wx.StaticBitmap(self.panel, wx.ID_ANY,
                                         wx.Bitmap(img))

        # Label for name, age
        self.namelbl = wx.StaticText(self.panel, label='N/A')

        # Like, dislike, superlike buttons
        likeBtn = wx.Button(self.panel, label='Like')
        likeBtn.Bind(wx.EVT_BUTTON, self.onLike)
        dislikeBtn = wx.Button(self.panel, label='Dislike')
        dislikeBtn.Bind(wx.EVT_BUTTON, self.onDislike)
        superLikeBtn = wx.Button(self.panel, label='Super Like')
        superLikeBtn.Bind(wx.EVT_BUTTON, self.onSuperLike)

        # Change location
        changeLocBtn = wx.Button(self.panel, label='Change Location')
        changeLocBtn.Bind(wx.EVT_BUTTON, self.onChangeLoc)

        # Undo
        undoBtn = wx.Button(self.panel, label='Undo')
        undoBtn.Bind(wx.EVT_BUTTON, self.onUndo)
        
        # Logout
        logoutBtn = wx.Button(self.panel, label='Logout')
        logoutBtn.Bind(wx.EVT_BUTTON, self.onLogout)


        # Main frame, image
        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.mainSizer.Add(wx.StaticLine(self.panel, wx.ID_ANY), 0, wx.ALL | wx.EXPAND, 5)
        self.mainSizer.Add(self.namelbl, 0, wx.ALL, 5)
        self.mainSizer.Add(self.imageCtrl, 0, wx.ALL, 5)
        
        # Add like buttons
        self.sizer.Add(dislikeBtn, 0, wx.ALL, 5)
        self.sizer.Add(superLikeBtn, 0, wx.ALL, 5)
        self.sizer.Add(likeBtn, 0, wx.ALL, 5)
        
        # Add other buttons
        self.mainSizer.Add(changeLocBtn, 0, wx.ALL, 5)
        self.mainSizer.Add(logoutBtn, 0, wx.ALL | wx.ALIGN_RIGHT | wx.ALIGN_TOP, 5)
        self.mainSizer.Add(undoBtn, 0, wx.ALL | wx.ALIGN_RIGHT | wx.ALIGN_TOP, 5)





        self.mainSizer.Add(self.sizer, 0, wx.ALL, 5)
        
        self.panel.SetSizer(self.mainSizer)
        self.mainSizer.Fit(self.frame)
        
        self.panel.Layout()

    def update_user(self):
        # Update pynder user(s)
        if self.users_index < 0 or self.users_index >= len(self.users) - 1:
            # Get more users nearby
            self.users = self.session.nearby_users()
            self.users_index = 0
        else:
            # We have list of users so go to next one
            self.users_index += 1

        if self.users != None and len(self.users) > 0 and self.session.likes_remaining != 0:
            # Set hopeful
            self.last = self.hopeful  # Set previous hopeful for undo function
            self.hopeful = self.users[self.users_index]

        else:
            self.canlike = False
        self.update_image()

    def onLike(self, event):
        """
        Like the current user
        """
        if self.canlike:
            self.hopeful.like()
            self.update_user()

    def onSuperLike(self, event):
        """
        Super Like the current user
        """
        if self.canlike:
            self.hopeful.superlike()
            self.update_user()

    def onDislike(self, event):
        """
        Dislike the current user
        """
        if self.canlike:
            self.hopeful.dislike()
            self.update_user()


    def onChangeLoc(self, event):
        '''
        Change location
        '''
        loc_set = False
        while not loc_set:
            dlg = wx.TextEntryDialog(self.frame, 'Please enter a location', 'Current location: ' + self.location)
            if dlg.ShowModal() == wx.ID_OK:
                # do something here
                loc = str(dlg.GetValue())
            else:
                # handle dialog being cancelled or ended by some other button
                loc = None

            dlg.Destroy()
            
            geolocator = Nominatim()
            # Look up location given
            try:
                l = geolocator.geocode(loc, exactly_one=True)
                self.latlon = (l.latitude, l.longitude)
                self.location = loc
                loc_set = True
    
            except Exception as e:
                print('Error setting location\n' + str(e))
        self.session.update_location(self.latlon[0], self.latlon[1])


    def onUndo(self, event):
        self.users_index -= 1
        self.hopeful = self.last
        self.update_image()
        
    def onLogout(self, event):
        os.remove('.token')
        self.login()
    '''
    UTILITY FUNCTIONS
    '''

    def timer_daemon(self):
        delta = self.session.can_like_in
        while True:
            m, s = divmod(delta, 60)
            h, m = divmod(m, 60)
            tstamp = '{}:{}:{}'.format(int(h), int(m), int(s))
            self.namelbl.SetLabel('Out of likes. Get more in ' + tstamp)
            time.sleep(1)
            delta -= 1



    def update_label(self):
        # Set image label
        if self.canlike:
            nameage = '{}, {}'.format(self.hopeful.name, self.hopeful.age)
            self.namelbl.SetLabel(nameage)
        elif self.session.likes_remaining != 0:
            self.namelbl.SetLabel('No one around you. Change location to find more people')
        else:
            t = threading.Thread(target=self.timer_daemon)
            t.daemon = True  # thread dies when main thread exits
            t.start()




    def update_image(self):
        '''
        Updates image and name, age text
        '''

        # Fetch and open image
        if self.canlike:
            fd = urlopen(self.hopeful.photos[0])
            image_file = io.BytesIO(fd.read())
        else:
            if self.session.likes_remaining != 0:
                image_file = './jackie_chan.jpg'
            else:
                image_file = './whyyy.jpg'
        self.view(image_file)
        self.update_label()

    def view(self, file):
        '''
        Called when loading a new image. Pass arg bytesIO image file
        '''
        img = wx.Image(file, wx.BITMAP_TYPE_ANY)
        # scale the image, preserving the aspect ratio
        W = img.GetWidth()
        H = img.GetHeight()
        if W > H:
            NewW = self.PhotoMaxSize
            NewH = self.PhotoMaxSize * H / W
        else:
            NewH = self.PhotoMaxSize
            NewW = self.PhotoMaxSize * W / H
        img = img.Scale(NewW, NewH)

        self.imageCtrl.SetBitmap(wx.BitmapFromImage(img))
        self.panel.Refresh()
