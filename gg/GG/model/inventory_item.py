import ggmodel
import GG.isoview.isoview_item
import dMVC.model

class GGInventoryItem(ggmodel.GGModel):
  """GGInventoryItem class.
  Defines item attributes and methods.
  """
  
  def __init__(self, spriteName):
    """ Class constructor.
    spriteName: image name.
    offset: offset for that position.
    """
    ggmodel.GGModel.__init__(self)
    self.__player = None
    self.spriteName = spriteName
    self.imagePath = ""
    
  def variablesToSerialize(self):
    """ Sets some vars to be used as locals.
    """
    return ['spriteName', 'imagePath']
  
  # self.__player
  
  def getPlayer(self):
    return self.__player

  def setPlayer(self, player):
    self.__player = player  

  def checkSimilarity(self, item):
    if item.spriteName == self.spriteName:
      return True
    return False   
    
  @dMVC.model.localMethod 
  def defaultView(self, screen, room, parent):
    """ Creates an isometric view object for the item.
    screen: screen handler.
    parent: isoview hud handler.
    """
    return GG.isoview.isoview_item.IsoViewItem(self, screen, room, parent)
  
  def clickedBy(self, clicker):
    """ Triggers an avent when the item receives a click by a player.
    clicker: player who clicks.
    """
    #clicker.setHeading(GG.utils.getNextDirection(clicker.getPosition(), self.__position))
    pass
    
  def tick(self, now):
    """ Call for an update on item.
    Not used at the moment.
    """
    pass