import GG.model.room_item
import GG.isoview.isoview_item
import dMVC.model

class GGDoorLobby(GG.model.room_item.GGRoomItem):
  """ GGDoorLobby class.
  Defines a teleporter object behaviour.
  """
 
  def __init__(self, sprite, position, offset, entryPosition, exitPosition, destinationRoom):
    """ Class builder.
    sprite: sprite used to paint the teleporter.
    entryPosition: teleporter entrance position.
    exitPosition: teleporter exit position on the new room.
    position: teleporter position.
    offset: image offset on screen.
    destinationRoom: room the teleporter will carry players to.
    """
    GG.model.room_item.GGRoomItem.__init__(self, sprite, position, offset)
    self.__entryPosition = entryPosition
    self.__exitPosition = exitPosition
    self.__destinationRoom = destinationRoom
    
  def getOptions(self):
    """ Returns the item's available options.
    """
    return ["open"]    
    
  # self.__entryPosition
  
  def getEntryPosition(self):
    """ Returns the teleporter entrance position.
    """
    return self.__entryPosition
  
  def setEntryPosition(self, entryPosition):
    """ Sets a new teleporter entrance position:
    entryPosition: new teleporter entrance position.
    """
    if self.__entryPosition != entryPosition:
      self.__entryPosition = entryPosition
      #self.triggerEvent('entryPositon', entryPosition=entryPosition)
    
  # self.__exitPosition
  
  def getExitPosition(self):
    """ Returns the teleporter exit position.
    """
    return self.__exitPosition
  
  def setExitPosition(self, exitPosition):
    """ Sets a new teleporter exit position:
    entryPosition: new teleporter exit position.
    """
    if self.__exitPosition != exitPosition:
      self.__exitPosition = exitPosition
      #self.triggerEvent('exitPosition', exitPosition=exitPosition)
  
  # self.__destinationRoom
  
  def getDestinationRoom(self):
    """ Returns the room that the teleporter connects to.
    """
    return self.__destinationRoom
  
  def setDestinationRoom(self, destinationRoom):
    """ Sets a new room connected to the teleporter.
    """
    if not self.__destinationRoom == destinationRoom:
      self.__destinationRoom = destinationRoom
      self.triggerEvent('destinationRoom', destinationRoom=destinationRoom)

  # self.__condition
  
  def setCondition(self, condition):
    """ Sets a new condition for teleporter activation.
    condition: new condition list.
    """
    self.__condition = condition
    
  @dMVC.model.localMethod 
  def defaultView(self, screen, room, parent):
    """ Creates an isometric view object for the item.
    screen: screen handler.
    parent: isoview hud handler.
    """
    return GG.isoview.isoview_item.IsoViewItem(self, screen, room, parent)
  
  def clickedBy(self, clicker):
    """ Triggers an event when the teleporter receives a click by a player.
    clicker: player who clicks.
    """
    GG.model.room_item.GGRoomItem.clickedBy(self, clicker)
    if GG.utils.checkNeighbour(clicker.getPosition(), self.getPosition()):
      clicker.setSelectedItem(self)
    else:
      return False    

  def openedBy(self, clicker):
    """ Teleports a player to another location.
    clicker: player to teleport.
    """
    if clicker.getPosition() == self.__entryPosition:
      if not clicker.hasItemLabeledInInventory('llave dorada'):
        self.newChatMessage('Necesitas la llave dorada')  
        return False
      clicker.changeRoom(self.__destinationRoom, self.__exitPosition)
    else:
      return False    
    
  def newChatMessage(self, message):
    """ Triggers a new event after receiving a new chat message.
    message: new chat message.
    """
    self.getRoom().triggerEvent('chatAdded', message=GG.model.chat_message.ChatMessage(message, 'Teleporter', \
                    GG.utils.TEXT_COLOR["black"], self.getPosition()))
