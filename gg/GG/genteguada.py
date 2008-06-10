import datetime
import os
import pygame
import pygame.locals
import stat
import sys
import time
import time

import dMVC.remoteclient

import GG.isoview.login
import GG.model.ggsystem
import GG.utils


class GenteGuada:

  def __init__(self):
    self.screen = None
    self.system = None
    self.isoHud = None
    self.session = None
    self.client = None
    GenteGuada.instance = self
    self.clearCache()
    self.activeScreen = None

  @staticmethod
  def getInstance():
    return GenteGuada.instance
  
  """
  def input(self, events):
    for event in events:
      if event.type == pygame.locals.QUIT:
        self.finish()
      if event.type == pygame.locals.KEYDOWN:
        if event.key == pygame.locals.K_ESCAPE:
          self.finish()
        elif event.key == pygame.locals.K_RETURN: 
          self.isoHud.chatMessageEntered()
      if event.type == pygame.locals.MOUSEBUTTONDOWN:
        cordX, cordY = pygame.mouse.get_pos()
        if 0 <= cordY <= GG.utils.HUD_OR[1]:
          dest = self.isoHud.getIsoviewRoom().findTile([cordX, cordY])
          if not dest == [-1, -1]:
            self.isoHud.getIsoviewRoom().getModel().clickedByPlayer(self.isoHud.getPlayer(), [dest[0], 0, dest[1]])
    self.isoHud.widgetContainer.distribute_events(*events)
  """

  def finish(self):
    #print dMVC.utils.statClient.strClient()
    #print dMVC.utils.statEventTriggered.strEvent()
    pygame.mixer.music.stop()
    sys.exit(0)
  
  def start(self, params):
    pygame.init()
    pygame.display.list_modes(32)
    #self.screen = pygame.display.set_mode(GG.utils.SCREEN_SZ, pygame.HWSURFACE|pygame.FULLSCREEN,0)
    self.screen = pygame.display.set_mode(GG.utils.SCREEN_SZ)
    pygame.display.set_caption(GG.utils.VERSION)
    self.__getSystem(params.ip) 
    winLogin = GG.isoview.login.Login(self.screen, self)
    #self.session = winLogin.draw()
    self.session = winLogin.draw(params.user, params.password)
    self.initGame()

  def __getSystem(self, ipAddress):
    if ipAddress:
      try:
        self.client = dMVC.remoteclient.RClient(ipAddress, autoEvents=False)
      except Exception, excep:
        print excep, "No hay conexion con el servidor"
        self.finish()
      self.system = self.client.getRootModel()
    else:
      self.system = GG.model.ggsystem.GGSystem()

  def initGame(self):
    self.isoHud = self.session.defaultView(self.screen,self)
    self.isoHud.draw()
    self.activeScreen = self.isoHud

    intentedFPS = 100
    fpsCounter = 0
    fpsTotal = 0

    theClock = pygame.time.Clock()
    while True:
      #time.sleep(GG.utils.ANIM_DELAY)
      ellapsedTime = theClock.tick(intentedFPS)
      fpsCounter += 1
      if fpsCounter == intentedFPS:
        averageFps = fpsTotal / intentedFPS
        print "Average FPS: " + str(1000.0 / averageFps)
        fpsCounter = 0
        fpsTotal = 0
        newFps = int(((intentedFPS + averageFps) / 2) * 1.2)
        if intentedFPS != newFps:
          print "NEW FPS: " + str(newFps)
          intentedFPS = newFps
      else:
        fpsTotal += ellapsedTime

      now = time.time() * 1000
      if self.client:
        self.client.processEvents()

      self.activeScreen.processEvent(pygame.event.get())
      self.activeScreen.updateFrame(now)
      #self.input(pygame.event.get())
      #self.isoHud.updateFrame(now)


  def getDataPath(self, img):
    #return os.path.join(GG.utils.DATA_PATH, img)
    if isinstance(self.system,GG.model.ggsystem.GGSystem):
      return os.path.join(GG.utils.DATA_PATH, img)
    else:
      newImgName = img.replace("/","-")
      pathFile = os.path.join(GG.utils.LOCAL_DATA_PATH, newImgName)
      #if os.path.isfile(pathFile):
      #  dateFile = os.stat(pathFile)[stat.ST_MTIME]
      #else:
      #  dateFile = None
      if os.path.isfile(pathFile):
        return os.path.join(GG.utils.LOCAL_DATA_PATH, newImgName)

      imgData = self.system.getResource(img, None)#dateFile) 
      if imgData:
        imgFile = open(os.path.join(GG.utils.LOCAL_DATA_PATH, newImgName), "wb")
        imgFile.write(imgData)
        imgFile.close()
      return os.path.join(GG.utils.LOCAL_DATA_PATH, newImgName)

  def getListDataPath(self, imgList):
    result = []
    for imgName in imgList:
      result.append(self.getDataPath(imgName))
    return result
  
  def clearCache(self):
    now = datetime.datetime.today()
    limitDate = now - datetime.timedelta(weeks=GG.utils.CLEAR_CACHE_WEEKS)
    limitTime = time.mktime(limitDate.timetuple())
    toRemove = []
    for file in os.listdir(GG.utils.LOCAL_DATA_PATH):
      pathFile = os.path.join(GG.utils.LOCAL_DATA_PATH, file) 
      if os.path.isfile(pathFile):
        accessTime = os.stat(pathFile)[stat.ST_ATIME]
        if accessTime < limitTime:
          toRemove.append(file)
    for file in toRemove:
      pathFile = os.path.join(GG.utils.LOCAL_DATA_PATH, file) 
      os.remove(pathFile)
