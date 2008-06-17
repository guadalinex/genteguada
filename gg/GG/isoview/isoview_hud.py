import pygame
import GG.utils
import isoview
import isoview_inventoryitem
import ocempgui.widgets
import ocempgui.draw
import copy
import random
import avatareditor
import animation

from pygame.locals import * # faster name resolution


class IsoViewHud(isoview.IsoView):
  """ IsoViewHud class.
  Defines the HUD.
  """
  
  def __init__(self, model, screen, parent):
    """ Class constructor.
    model: ggsession model.
    screen: screen handler.
    """
    isoview.IsoView.__init__(self, model, screen)
    self.__isoviewInventory = []
    self.__player = self.getModel().getPlayer()
    self.__isoviewRoom = self.__player.getRoom().defaultView(self.getScreen(), self)
    self.widgetContainer = ocempgui.widgets.Renderer()
    self.widgetContainer.set_screen(screen)
    self.textArea = None
    self.__textField = None
    self.windowInventory = None
    
    self.__fullScreen = False
    
    self.__img = pygame.sprite.Sprite()
    self.__img.image = pygame.image.load(GG.genteguada.GenteGuada.getInstance().getDataPath(GG.utils.INTERFACE_LOWER)).convert_alpha()
    self.__img.rect = self.__img.image.get_rect()
    self.__img.rect.topleft = GG.utils.HUD_OR
    
    model.subscribeEvent('chatAdded', self.chatAdded)
    self.__player.subscribeEvent('room', self.roomChanged)
    #elf.__player.subscribeEvent('addInventory', self.inventoryAdded)
    self.__player.subscribeEvent('addToInventory', self.addItemToInventory)
    self.__player.subscribeEvent('removeFromInventory', self.inventoryRemoved)
    self.__player.subscribeEvent('selectedItem', self.itemSelected)
    self.__player.subscribeEvent('unselectedItem', self.itemUnselected)
    self.__selectedItem = None
    self.buttonActions = {
        "inventory":{"image":"guardar.png", "action": self.itemToInventory},
        "clone":{"image":"guardar.png", "action": self.itemToClone},
        "push":{"image":"empujar.png", "action": self.itemToPush},
        "up":{"image":"levantar.png", "action": self.itemToUp},
        "talk":{"image":"sonido.png", "action": self.itemToTalk},
        "exchange":{"image":"empujar.png", "action": self.exchangeItemPlayer},
        "open":{"image":"sonido.png", "action": self.itemToOpen},
        "url":{"image":"derecha.png", "action": self.itemToUrl}
    }
    self.winWardrobe = None
    self.wardrobe = None

  def processEvent(self, events):
    for event in events:
      event_type = event.type
      if event_type == QUIT:
        GG.genteguada.GenteGuada.getInstance().finish()
      elif event_type == KEYDOWN:
        if event.key == K_ESCAPE:
          GG.genteguada.GenteGuada.getInstance().finish()
        elif event.key == K_RETURN: 
          self.chatMessageEntered()
      elif event_type == MOUSEBUTTONDOWN:
        cordX, cordY = pygame.mouse.get_pos()
        if 0 <= cordY <= GG.utils.HUD_OR[1]:
          dest = self.getIsoviewRoom().findTile([cordX, cordY])
          if not dest == [-1, -1]:
            self.__isoviewRoom.getModel().clickedByPlayer(self.__player, [dest[0], 0, dest[1]])
    self.widgetContainer.distribute_events(*events)

  def getPlayer(self):
    return self.__player
  
  def findIVItem(self, item):
    for ivItem in self.__isoviewRoom.getIsoViewItems():
      if ivItem.getModel() == item:
        return ivItem
    return None

  def findIVInventoryItem(self, item):
    for ivItem in self.__isoviewInventory:
      if ivItem.getModel() == item:
        return ivItem
    return None
  
  def inventoryRemoved(self, event):
    item = event.getParams()["item"]  
    ivInventItem = self.findIVInventoryItem(item)
    self.__isoviewInventory.remove(ivInventItem)
    self.paintItemsInventory()
      
  def addItemToInventory(self, event):
    """ Adds a new isoview inventory item.
    """
    item = event.getParams()["item"]
    posOrigin = event.getParams()["position"]
    posX = len(self.__isoviewInventory)%GG.utils.INV_ITEM_COUNT[0]
    posY = len(self.__isoviewInventory)/GG.utils.INV_ITEM_COUNT[1]
    pos = [GG.utils.INV_OR[0] + (posX * GG.utils.INV_ITEM_SZ[0]), GG.utils.INV_OR[1] + (posY * GG.utils.INV_ITEM_SZ[1])]
    ivItem = self.findIVItem(item)
    invItem = isoview_inventoryitem.IsoViewInventoryItem(item, self.getScreen(), self, pos)
    if ivItem != None:
      positionAnim = animation.ScreenPositionAnimation(GG.utils.ANIM_INVENTORY_TIME, ivItem, \
                            GG.utils.p3dToP2d(posOrigin, item.offset), pos, True)
      positionAnim.setOnStop(item.getRoom().removeItem, item)
    else:
      ivItem = item.defaultView(self.getScreen(), self.__isoviewRoom, self)
      self.__isoviewRoom.addIsoViewItem(ivItem)  
      positionAnim = animation.ScreenPositionAnimation(GG.utils.ANIM_INVENTORY_TIME, ivItem, \
                            GG.utils.p3dToP2d(posOrigin, [0, 0]), pos, True)
    positionAnim.setOnStop(self.__isoviewRoom.removeSprite, ivItem.getImg())
    positionAnim.setOnStop(self.__isoviewInventory.append, invItem)
    positionAnim.setOnStop(self.paintItemsInventory, None)
    ivItem.setAnimation(positionAnim)
    
  def addItemToRoomFromInventory(self, ivItem):
    """ Removes an item from the inventory item list and creates an animation to the room.
    event: event info.
    """
    item = ivItem.getModel()
    ivInventItem = self.findIVInventoryItem(item)
    if ivItem:    
      posX = len(self.__isoviewInventory)%GG.utils.INV_ITEM_COUNT[0]
      posY = len(self.__isoviewInventory)/GG.utils.INV_ITEM_COUNT[1]
      pos = [GG.utils.INV_OR[0] + (posX * GG.utils.INV_ITEM_SZ[0]), GG.utils.INV_OR[1] + (posY * GG.utils.INV_ITEM_SZ[1])]
      positionAnim = animation.ScreenPositionAnimation(GG.utils.ANIM_INVENTORY_TIME, ivItem, \
                            pos, GG.utils.p3dToP2d(item.getPosition(), item.offset), True)
      ivItem.setAnimation(positionAnim)
      if ivInventItem != None:
        self.__isoviewInventory.remove(ivInventItem)
        self.paintItemsInventory()
      GG.utils.playSound(GG.utils.SOUND_DROPITEM)
      
  def draw(self):
    """ Updates the changed zones on the room view and draws the hud.
    """
    #self.paintBackground()
    self.paintInventory()
    self.paintChat()
    self.paintTextBox()
    self.paintActionButtons()

  def updateFrame(self, ellapsedTime):
    """ Updates all sprites for a new frame.
    """
    #hay que dibujar la habitacion DESPUES del hud, para que las animaciones de los items 
    #se vean sobre el HUD y no debajo como ahora.

    self.paintBackground()
    self.buttonBar.update()
    self.textArea.update()
    self.__textField.update()
    self.windowInventory.update()

    if self.__isoviewRoom:
      self.__isoviewRoom.updateFrame(ellapsedTime)
    #for item in self.__isoviewInventory:
    #  item.updateFrame(ellapsedTime)
    pygame.display.update()

  def roomChanged(self, event):
    """ Triggers after receiving a change room event.
    event: event info.
    """
    if self.__isoviewRoom:
      self.__isoviewRoom.stopAnimations()
      self.__isoviewRoom.unsubscribeAllEvents()
      GG.utils.playSound(GG.utils.SOUND_OPENDOOR)
      self.__isoviewRoom = None
      rect = pygame.Rect(0, 0, GG.utils.GAMEZONE_SZ[0], GG.utils.GAMEZONE_SZ[1])
      self.getScreen().fill((0, 0, 0), rect)
      self.buttonBar.update()
    if not event.getParams()["room"] is None:
      self.__isoviewRoom = event.getParams()["room"].defaultView(self.getScreen(), self)
      
  def getIsoviewRoom(self):
    """ Returns the isometric view room.
    """
    return self.__isoviewRoom
           
  # Paint methods
    
  def paintBackground(self):
    """ Paints the HUD background on screen.
    """
    self.getScreen().blit(self.__img.image, GG.utils.HUD_OR)
    #pygame.display.update()

  def paintChat(self):
    """ Paints the chat window on screen.
    """
    self.textArea = ocempgui.widgets.ScrolledWindow(GG.utils.CHAT_SZ[0], GG.utils.CHAT_SZ[1])
    self.textArea.set_scrolling(1)
    self.textArea.border = 1
    self.textArea.topleft = GG.utils.CHAT_OR[0], GG.utils.CHAT_OR[1]
    self.__layoutTextArea= ocempgui.widgets.VFrame()
    self.__layoutTextArea.border = 0
    self.__layoutTextArea.set_align(ocempgui.widgets.Constants.ALIGN_LEFT)
    self.textArea.child = self.__layoutTextArea
    self.widgetContainer.add_widget(self.textArea)
  
  def paintTextBox(self):
    """ Paints the editable text box on screen.
    """
    self.__textField = ocempgui.widgets.Entry()
    self.__textField.set_style(ocempgui.widgets.WidgetStyle(GG.utils.STYLES["textFieldChat"]))
    self.__textField.border = 1
    self.__textField.topleft = GG.utils.TEXT_BOX_OR[0], GG.utils.TEXT_BOX_OR[1]
    self.__textField.set_minimum_size(GG.utils.TEXT_BOX_SZ[0], GG.utils.TEXT_BOX_SZ[1])
    self.widgetContainer.add_widget(self.__textField)

  def paintInventory(self):
    """ Paints the inventory box and its items on it.    
    """
    self.windowInventory = ocempgui.widgets.ScrolledWindow(GG.utils.INV_SZ[0], GG.utils.INV_SZ[1])
    self.windowInventory.border = 1
    self.windowInventory.topleft = GG.utils.INV_OR[0], GG.utils.INV_OR[1] - 15
    self.widgetContainer.add_widget(self.windowInventory)
    self.paintItemsInventory()

  def paintItemsInventory(self):
    """ Paints the inventory items.
    """
    self.windowInventory.child = None
    self.__frameInventory = ocempgui.widgets.VFrame()
    self.__frameInventory.border = 0
    self.__frameInventory.set_align(ocempgui.widgets.Constants.ALIGN_LEFT)
    self.windowInventory.child = self.__frameInventory
    position = 0
    for inventoryitem in self.__isoviewInventory:
      self.paintItemOnInventory(inventoryitem, position)
      position += 1

  def itemInventorySelected(self,invIsoItem):
    """ Selects an item from the player's inventory.
    invIsoItem: selected item.
    """
    if invIsoItem.getModel().inventoryOnly():
      self.__player.removeFromInventory(invIsoItem.getModel())  
      #self.__isoviewInventory.remove(invIsoItem)
      self.paintItemsInventory()
    else:    
      self.__player.addToRoomFromInventory(invIsoItem.getModel())

  def paintItemOnInventory(self, invItem, position):
    """ Paints an item on the hud inventory.
    spriteName: sprite name.
    position: position in the inventory that the item will be painted into.
    """
    if position % GG.utils.INV_ITEM_COUNT[0] == 0:
      self.hframe =  ocempgui.widgets.HFrame()
      self.hframe.border = 0
      self.hframe.add_child(invItem.draw(self.widgetContainer))
      self.__frameInventory.add_child(self.hframe)
    else:
      self.hframe.add_child(invItem.draw(self.widgetContainer))
  
  def printChatMessage(self, chatMessage):
    self.__layoutTextArea.add_child(chatMessage.draw())
    self.textArea.vscrollbar.value = self.textArea.vscrollbar.maximum
  
  def getStyleMessageChat(self):
    """ Returns the chat current style.
    """
    #TODO entiendo que el color del chat depende de cada usuario 
    listStyle = ["chatEntryBlack","chatEntryRed","chatEntryGreen","chatEntryBlue"]
    return GG.utils.STYLES[listStyle[random.randint(0,len(listStyle)-1)]]
    
  def chatMessageEntered(self):
    """ Prints a new message on chat window.
    """
    self.__player.getRoom().newChatMessage(self.__textField.text, self.__player, 0)
    self.__textField.text = ""

  def chatAdded(self, event):
    """ Triggers after receiving a new chat message event.
    event: event info.
    """
    messageChat = event.getParams()['message']
    ivMessageChat = messageChat.chatView(self.getScreen(), self)
    cad = messageChat.getHour()+" [" + messageChat.getSender() + "]: " + messageChat.getMessage()

    animTime = (len(messageChat.getMessage()) / 12) * 1000
    if animTime < 2000:
      animTime = 2000 
    
    idleAnim = animation.IdleAnimation(animTime, ivMessageChat)
    positionAnim = animation.ScreenPositionAnimation(GG.utils.ANIM_CHAT_TIME2, ivMessageChat, \
                            ivMessageChat.getScreenPosition(), GG.utils.TEXT_BOX_OR, True)
    secAnim = animation.SecuenceAnimation()
    secAnim.addAnimation(idleAnim)
    secAnim.addAnimation(positionAnim)
    secAnim.setOnStop(self.printChatMessage, ivMessageChat)
    secAnim.setOnStop(self.__isoviewRoom.removeIsoViewItem, ivMessageChat)
    secAnim.setOnStop(self.__isoviewRoom.removeTopSprite, ivMessageChat.getImg())
    ivMessageChat.setAnimation(secAnim)
    self.__isoviewRoom.addIsoViewItem(ivMessageChat)
        
  def itemSelected(self,event):
    """ Triggers after receiving an item selected event.
    event: event info.
    """
    self.__selectedItem = event.getParams()['item'] 
    self.__isoviewRoom.itemSelected(self.__selectedItem)
    options = self.__selectedItem.getOptions()
    self.buttonBarActions = ocempgui.widgets.HFrame()
    if len(options) == 1:
      offset = 0
    else:
      offset = 3 + len(options) 
    self.buttonBarActions.topleft = [GG.utils.SCREEN_SZ[0] - (GG.utils.ACTION_BUTTON_SZ[0]*len(options) - offset), \
                                     GG.utils.HUD_OR[1] - GG.utils.ACTION_BUTTON_SZ[1]]
    #self.buttonBarActions.topleft = 0,0
    print "********************", options
    for action in options:
      button = ocempgui.widgets.ImageButton(GG.genteguada.GenteGuada.getInstance().getDataPath(self.buttonActions[action]['image']))
      button.border = 0
      button.connect_signal(ocempgui.widgets.Constants.SIG_CLICKED, self.buttonActions[action]['action'])
      self.buttonBarActions.add_child(button)
    self.widgetContainer.add_widget(self.buttonBarActions)
  
  def itemUnselected(self,event=None):
    if self.__selectedItem:
      if self.__isoviewRoom:  
        self.__isoviewRoom.itemUnselected(self.__selectedItem)
      self.dropActionsItembuttons()

  #Defincion de la buttonBar y sus acciones permanentes

  def paintActionButtons(self):
    """ Paints the general action buttons.
    """
    ACTIONS = [
                {"image":"vestidor.png", "action": self.showDresser},
                {"image":"derecha.png", "action": self.turnRight},
                {"image":"izquierda.png", "action": self.turnLeft},
                {"image":"herramientas.png", "action": self.showTools},
                {"image":"sonido.png", "action": self.showSoundControl},
                {"image":"ayuda.png", "action": self.showHelp},
              ]

    self.buttonBar = ocempgui.widgets.HFrame()
    self.buttonBar.topleft = [0,GG.utils.HUD_OR[1] - 80]
    self.widgetContainer.add_widget(self.buttonBar)
    for buttonData in ACTIONS:
      button = ocempgui.widgets.ImageButton(GG.genteguada.GenteGuada.getInstance().getDataPath(buttonData['image']))
      button.border = 0
      button.connect_signal(ocempgui.widgets.Constants.SIG_CLICKED, buttonData['action'])
      self.buttonBar.add_child(button)
  
  def getPlayerConfiguration(self):
    dict = {}
    dict["gender"] = "boy"
    dict["headSize"] = "S"
    dict["mask"] = "mask"
    dict["hairStyle"] = "1"
    dict["hairColor"] = "1"
    dict["skin"] = "1"
    dict["bodySize"] = "S"
    dict["typeShirt"] = "short"
    dict["shirt"] = "3"
    dict["typeTrousers"] = "short"
    dict["trousers"] = "5"
    dict["skirt"] = "3"
    dict["shoes"] = "9"
    return dict

  def showDresser(self):
    playerConfiguration = self.getPlayerConfiguration()
    self.wardrobe = avatareditor.AvatarEditor(self.widgetContainer, self, playerConfiguration)
    self.winWardrobe = self.wardrobe.draw()
    self.widgetContainer.add_widget(self.winWardrobe)
    GG.genteguada.GenteGuada.getInstance().activeScreen = self.wardrobe

  def closeDresser(self, configuration = None):
    if configuration:
      self.setPlayerConfiguration(configuration)
    GG.genteguada.GenteGuada.getInstance().activeScreen = self
    self.winWardrobe.destroy()
    self.winWardrobe = None

  def setPlayerConfiguration(self,configuration):
    print configuration

  def turnRight(self):
    print "turn right"
    self.__player.jump()
    """
    ivPlayer = self.findIVItem(self.__player)
    if ivPlayer == None:
      return
    ivPlayer.jump()
    """
    
  def turnLeft(self):
    print "turn left"

  def showTools(self):
    print "show tools"

  def showSoundControl(self):
    print "show sound control"
    
  def showHelp(self):
    """ Show help menu. (At the moment, It doesn't. It just toggles the full screen mode)
    """
    print "show help"
    #TODO solo funciona en linux con las X, para e
    self.__fullScreen = not self.__fullScreen
    pygame.display.toggle_fullscreen()

  #definicion de las acciones y botones en funcion del item seleccionado
  
  def dropActionsItembuttons(self):
    """ Removes the action buttons from the screen.
    """
    self.__selectedItem = None
    children = copy.copy(self.buttonBarActions.children)
    for child in children:
      self.buttonBarActions.remove_child(child)
      child.destroy()
    self.widgetContainer.remove_widget(self.buttonBarActions)
    self.buttonBarActions.destroy()

  def itemToInventory(self):
    """ Brings an item from the room to the player's inventory.
    """
    self.__player.addToInventoryFromRoom(self.__selectedItem)
    #self.__isoviewRoom.setItemOnTile(None, self.__selectedItem.getPosition())
    #self.__selectedItem.getRoom().removeItem(self.__selectedItem)
    self.dropActionsItembuttons()
 
  def itemToClone(self):
    """ Clones an item from the room and inserts it on the player's inventory
    """
    clone = self.__selectedItem.getClone()
    self.__player.addInventory(clone)
    self.itemUnselected()

  def itemToPush(self):
    print "push"
    self.itemUnselected()

  def itemToUp(self):
    print "lift"
    self.itemUnselected()

  def itemToTalk(self):
    """ Talks to an item.
    """
    #print "talk"
    self.__player.talkTo(self.__selectedItem)
    self.itemUnselected()

  def exchangeItemPlayer(self):
    """ Shows the trade window.
    """
    #print "intercambio"
    self.showExchangeWindow()

  def showExchangeWindow(self):
    """ Shows the exchange items window.
    """
    window = ocempgui.widgets.VFrame()
    window.set_minimum_size(GG.utils.INV_SZ[0], GG.utils.INV_SZ[1])
    window.topleft = GG.utils.SCREEN_SZ[0] - 200, GG.utils.HUD_OR[1] - 200
    window.border = 1
    #self.buttonBarActions.topleft = [GG.utils.SCREEN_SZ[0] - (GG.utils.ACTION_BUTTON_SZ[0]*len(options) - offset), \
    #                                 GG.utils.HUD_OR[1] - GG.utils.ACTION_BUTTON_SZ[1]]
    self.widgetContainer.add_widget(window)

  def itemToOpen(self):
    """ Attempts to open a teleporter item.
    """
    print "open"
    self.__player.open(self.__selectedItem)
    self.itemUnselected()

  def itemToUrl(self):
    """ Attempts to open a teleporter item.
    """
    print "url"
    import webbrowser
    if self.__fullScreen:
      self.showHelp()
    webbrowser.open(self.__selectedItem.url)
    self.itemUnselected()
