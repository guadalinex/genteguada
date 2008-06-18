import GG.model.room_item
#import GG.model.temp_pickable_item
import GG.model.chat_message
import GG.isoview.isoview_player
import GG.utils
import dMVC.model

class GGPlayer(GG.model.room_item.GGRoomItem):
  """ Player class.
  Defines a player object behaviour.
  """
 
  def __init__(self, spritePath, position, anchor, username, password):
    """ Class builder.
    spriteList: sprite list used to paint the player.
    position: player position.
    anchor: image anchor on screen.
    username: user name.
    password: user password.
    """
    filename = GG.utils.getSpriteName(GG.utils.STATE[1], GG.utils.HEADING[2], 0)
    GG.model.room_item.GGRoomItem.__init__(self, filename, position, anchor)
    self.username = username
    self.imagePath = spritePath
    self.__password = password # Not used outside this class
    self.__visited = [] # Not used outside this class
    self.__heading = GG.utils.HEADING[2]
    self.__state = GG.utils.STATE[1]
    self.__destination = position
    self.__inventory = []
    self.__visited = []
    self.__selected = None
    
  def variablesToSerialize(self):
    """ Sets some vars to be used as locals.
    """
    parentVars = GG.model.room_item.GGRoomItem.variablesToSerialize(self)
    return parentVars + ['username']
  
    # self.__heading

  def getHeading(self):
    """ Returns the direction the player is heading to.
    """
    return self.__heading
  
  def setHeading(self, heading):
    """ Sets a new heading direction for the item.
    """
    if self.__heading != heading:
      self.__heading = heading
      self.triggerEvent('heading', heading=heading)

  # self.__state
  
  def getState(self):
    """ Returns the player's state.
    """
    return self.__state
  
  def setState(self, state):
    """ Sets a new state for the item.
    state: new state
    """
    if not self.__state == state:
      self.__state = state
      self.triggerEvent('state', state=state)

  # self.__destination
  
  def getDestination(self):
    """ Returns the player's movement destination.
    """
    return self.__destination
  
  def setDestination(self, destination):
    """ Sets a new destination for the player movement.
    heading: movement direction.
    destination: movement destination.
    """
    if not self.__destination == destination:
      for vis in self.__visited:
        self.__visited.remove(vis)
      self.__visited = []
      self.__destination = destination
      self.triggerEvent('destination', destination=destination)

  def setStartDestination(self, destination):
    """ Sets a new destination for the player movement without calling for a 'destination' event.
    heading: movement direction.
    destination: movement destination.
    """
    if self.__destination != destination:
      for vis in self.__visited:
        self.__visited.remove(vis)
      self.__visited = []
      self.__destination = destination
      
  # self.__inventory
  
  def setInventory(self, inventory):
    """ Sets a new player's inventory.
    inventory: new player's inventory.
    """
    if not self.__inventory == inventory:
      self.__inventory = inventory
      self.triggerEvent('inventory', inventory=inventory)
      return True
    return False
  
  @dMVC.model.localMethod
  def defaultView(self, screen, room, parent):
    """ Creates a view object associated with this player.
    screen: screen handler.
    room: room view object.
    parent: hud or session view object.
    """
    return GG.isoview.isoview_player.IsoViewPlayer(self, screen, room, parent)
  
  
  def addToInventoryFromRoom(self, item):
    self.__inventory.append(item)
    item.setPlayer(self)
    self.triggerEvent('addToInventory', item=item, position=item.getPosition())
    
  def addToInventoryFromVoid(self, item, position):
    self.__inventory.append(item)
    item.setPlayer(self)
    self.triggerEvent('addToInventory', item=item, position=position)
    
  def removeFromInventory(self, item):
    """ Removes an item from the player's inventory.
    item: item to be removed.
    """
    if item in self.__inventory:
      self.__inventory.remove(item)
      #item.setPlayer(None)
      self.triggerEvent('removeFromInventory', item=item)
      return True
    return False
  
  def addToRoomFromInventory(self, item):
    """ Removes an item from the inventory and drops it in front of the player.
    item: item to drop.
    """
    #self.lala()
    dropLocation = GG.utils.getFrontPosition(self.getPosition(), self.__heading)
    itemOnPosition = self.getRoom().getItemOnPosition(dropLocation)
    if dropLocation == [-1, -1, -1]: 
      return False
    if itemOnPosition != None:
      if not itemOnPosition.isStackable():
        return False
    self.__inventory.remove(item)
    item.setPlayer(None)
    self.getRoom().addItemFromInventory(item, dropLocation)
    self.triggerEvent('chat', actor=item, receiver=self, msg=item.label+" depositado en el suelo")
    
  def checkItemOnInventory(self, item):
    for it in self.__inventory:
      if it.checkSimilarity(item):
        return True
    return False      

  def checkUser(self, username, password):
    """ Searchs for an user by his user name and password.
    username: user name.
    password: user password.
    """
    if self.username == username and self.__password == password:
      return 1
    return 0
  
  def hasBeenVisited(self, pos):
    """ Checks if a tile has been visited by the player on the last movement.
    pos: tile position.
    """
    if pos in self.__visited:
      return True
    return False
  
  def clickedBy(self, clicker):
    """ Triggers an event when the player receives a click by another player.
    clicker: player who clicks.
    """
    GG.model.room_item.GGRoomItem.clickedBy(self, clicker)
    #if GG.utils.checkNeighbour(clicker.getPosition(), self.getPosition()):
    #  clicker.setSelectedItem(self)
    self.newChatMessage(clicker.username + ' ha pinchado en mi', 0)

  def getOptions(self):
    """ Returns the available item options.
    """
    return ["talk","exchange"]
      
  def tick(self, now):
    """ Calls for an update on player's position an movement direction.
    """
    for item in self.__inventory:
      item.tick(now)
    if self.getPosition() == self.__destination:
      self.setState(GG.utils.STATE[1])
      return
    direction = self.getRoom().getNextDirection(self, self.getPosition(), self.getDestination())
    if direction == GG.utils.HEADING[0]:
      self.setDestination(self.getPosition())
      return
    pos = self.getPosition()
    self.setState(GG.utils.STATE[2])
    self.setHeading(direction)
    if self.getHeading() == "up":
      next = [pos[0], pos[1], pos[2] - 1]
    if self.getHeading() == "down":
      next = [pos[0], pos[1], pos[2] + 1]
    if self.getHeading() == "left":
      next = [pos[0] - 1, pos[1], pos[2]]
    if self.getHeading() == "right":
      next = [pos[0] + 1, pos[1], pos[2]]
    if self.getHeading() == "topleft":
      next = [pos[0] - 1, pos[1], pos[2] - 1]
    if self.getHeading() == "bottomright": 
      next = [pos[0] + 1, pos[1], pos[2] + 1]
    if self.getHeading() == "bottomleft":
      next = [pos[0] - 1, pos[1], pos[2] + 1]
    if self.getHeading() == "topright":
      next = [pos[0] + 1, pos[1], pos[2] - 1]
    self.__visited.append(pos)
    self.setPosition(next)

  def changeRoom(self, room, pos):
    """ Changes the player's room.
    room: new room.
    pos: starting position on the new room.
    """
    oldRoom = self.getRoom()
    if oldRoom:
      oldRoom.removeItem(self)
    room.addItemFromVoid(self, pos)
    self.triggerEvent('roomChanged', oldRoom=oldRoom)
    
  def newChatMessage(self, message, type):
    """ Triggers a new event after receiving a new chat message.
    message: new chat message.
    """
    self.triggerEvent('chatAdded', message=GG.model.chat_message.ChatMessage(message, self.username, \
                    GG.utils.TEXT_COLOR["black"], self.getPosition(), type))

  def setSelectedItem(self, item):
    """ Sets an item as selected.
    """
    if self.__selected != item:
      self.__selected = item
      self.triggerEvent('selectedItem', item=item)
    
  def setUnselectedItem(self):
    """ Sets an item as unselected.
    """
    if self.__selected:
      self.__selected = None
      self.triggerEvent('unselectedItem')
    
  def talkTo(self, item):
    """ Talks to an item.
    item: item to talk to.
    """
    item.talkedBy(self)
    
  def open(self, item):
    """ Opens an item.
    open: item to open.
    """
    item.openedBy(self)
    
  def setStartPosition(self, pos):
    self.__destination = pos
    GG.model.room_item.GGRoomItem.setStartPosition(self, pos)
    
  def hasItemLabeledInInventory(self, label):
    for item in self.__inventory:
      if item.label == label:
        return True  
    return False    
      
  def jump(self):
    self.triggerEvent('jump', position=self.getPosition())
 
