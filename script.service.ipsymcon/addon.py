import sys, os
import urlparse, urllib
import xbmc, xbmcgui, xbmcplugin, xbmcaddon

__settings__    = xbmcaddon.Addon()
__addonname__   = __settings__.getAddonInfo('name')
__icon__        = __settings__.getAddonInfo('icon')

root = xbmc.translatePath(__settings__.getAddonInfo('path'))
sys.path.append(root + '/resources/lib/python-suds-0.4')

from suds.client import Client
from suds.xsd.doctor import Import, ImportDoctor

class IPSymcon():

    CINEMA_START = int( __settings__.getSetting('script-id-start') )
    CINEMA_END = int( __settings__.getSetting('script-id-end') )
    CINEMA_PAUSE = int( __settings__.getSetting('script-id-pause') )
    CINEMA_RESUME = int( __settings__.getSetting('script-id-resume') )
  
    scriptEngine = None

    def __init__(self):
      imp = Import('http://schemas.xmlsoap.org/soap/encoding/')
      d = ImportDoctor(imp)
      storage_path = xbmc.translatePath(__settings__.getAddonInfo('profile'))
      wsdl = os.path.join(storage_path, 'IIPS_ScriptEngine.xml')
      if not os.path.isfile(wsdl):
        try:
          urllib.urlretrieve(
            'http://{}/wsdl/IIPSScriptEngine'.format(
              __settings__.getSetting('host'),
            ),
            wsdl,
          ) 
        except:
          line1 = 'Failed to fetch wsdl (incorrect hostname?)'
          xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(__addonname__,line1, 5000, __icon__))
          sys.exit()
      self.scriptEngine = Client(
        self.path2url(wsdl), 
        location='http://{}/soap/IIPSScriptEngine'.format(
          __settings__.getSetting('host'),
        ),
        doctor=d,
      ).service

    def playBackStarted(self):
      self.scriptEngine.ExecuteScript(self.CINEMA_START) 

    def playBackEnded(self):
      self.scriptEngine.ExecuteScript(self.CINEMA_END) 

    def playBackStopped(self):
      self.playBackEnded()

    def playBackPaused(self):
      self.scriptEngine.ExecuteScript(self.CINEMA_PAUSE) 

    def playBackResumed(self):
      self.scriptEngine.ExecuteScript(self.CINEMA_RESUME) 

    def path2url(self, path):
      return urlparse.urljoin('file:', urllib.pathname2url(path))

class Player(xbmc.Player):
 
    def __init__(self):
      xbmc.Player.__init__(self)
 
    def onPlayBackStarted(self):
      if xbmc.Player().isPlayingVideo():
        ipsymcon.playBackStarted()

    def onPlayBackEnded(self):
      if (VIDEO == 1):
        ipsymcon.playBackEnded()
 
    def onPlayBackStopped(self):
      if (VIDEO == 1):
        ipsymcon.playBackStopped()
 
    def onPlayBackPaused(self):
      if xbmc.Player().isPlayingVideo():
        ipsymcon.playBackPaused()
 
    def onPlayBackResumed(self):
      if xbmc.Player().isPlayingVideo():
        ipsymcon.playBackResumed()

ipsymcon = IPSymcon()
player = Player()
 
VIDEO = 0
 
while(not xbmc.abortRequested):
    if xbmc.Player().isPlaying():
      if xbmc.Player().isPlayingVideo():
        VIDEO = 1
      else:
        VIDEO = 0
    xbmc.sleep(1000)
