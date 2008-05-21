
import dMVC.remoteclient
import pygame
import GG.utils
import GG.model.ggsystem
import time
import pygame.locals
import sys

import ocempgui.widgets


class GenteGuada:

  def __init__(self):
    self.screen = None
    self.system = None
    self.player = None
    self.isoHud = None
    self.session = None
    self.client = None

  def input(self, events):
    for event in events:
      #print event
      if event.type == pygame.locals.QUIT:
        self.finish()
      if event.type == pygame.locals.KEYDOWN:
        if event.key == pygame.locals.K_ESCAPE:
          self.finish()
        elif event.key == pygame.locals.K_RETURN: 
          self.isoHud.chatMessageEntered()
      if event.type == pygame.locals.MOUSEBUTTONDOWN:
        cordX, cordY = pygame.mouse.get_pos()
        if (GG.utils.UPPERPANNEL_OR[0] <= cordX <= (GG.utils.UPPERPANNEL_OR[0] + GG.utils.UPPERPANNEL_SZ[0])) \
            and (GG.utils.UPPERPANNEL_OR[1] <= cordY <= (GG.utils.UPPERPANNEL_OR[1] + GG.utils.UPPERPANNEL_SZ[1])):
          # Upper pannel
          pass
        elif cordY > GG.utils.GAMEZONE_SZ[1]:
          # Chat & inventory
          pass
        else:  
          dest = self.isoHud.getIsoviewRoom().findTile([cordX, cordY])
          if not dest == [-1, -1]:
            self.isoHud.getIsoviewRoom().getModel().clickedByPlayer(self.player, [dest[0], 0, dest[1]])
    self.isoHud.widgetContainer.distribute_events(*events)
      #self.isoHud.frameInventory.distribute_events(event)

  def finish(self):
    #print dMVC.utils.statClient.strClient()
    #print dMVC.utils.statEventTriggered.strEvent()
    pygame.mixer.music.stop()
    sys.exit(0)
  
  """
  def connectEvent(self, widget, event, method):
    widget.connect_signal(event,method)
  """

  def start(self, params):
    pygame.init()
    #self.screen = pygame.display.set_mode(GG.utils.SCREEN_SZ,pygame.HWSURFACE|pygame.FULLSCREEN,0)
    self.screen = pygame.display.set_mode(GG.utils.SCREEN_SZ)
    pygame.display.set_caption(GG.utils.VERSION)

    if params.ip:
      try:
        self.client = dMVC.remoteclient.RClient(params.ip)
      except Exception, excep:
        print excep, "No hay conexion con el servidor"
        self.finish()
      self.system = self.client.getRootModel()
    else:
      self.system = GG.model.ggsystem.GGSystem()

    login = self.system.login(params.user, params.password)
    if not login[0]:
      print login[1]
      self.finish()
    self.session = login[1] 
    if self.client:
      self.client.registerSession(self.session)
    self.player = self.session.getPlayer()
    self.isoHud = self.session.defaultView(self.screen)
    #self.isoHud.setParent(self)
    self.isoHud.draw()
    while True:
      time.sleep(GG.utils.ANIM_DELAY)
      self.input(pygame.event.get())
      self.isoHud.updateFrame()
  
