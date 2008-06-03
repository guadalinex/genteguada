import pygame
import GG.utils
import isoview

class IsoViewItem(isoview.IsoView):
  """ IsoViewItem class.
  Defines an item view.
  """
  
  def __init__(self, model, screen, room, parent):
    """ Class constructor.
    screen: screen handler.
    parent: isoview_hud handler.
    """
    isoview.IsoView.__init__(self, model, screen)
    self.__ivroom = room
    self.__parent = parent
    self.loadImage()
    #self.getModel().subscribeEvent('chat', parent.pruebaChat)
    #self.getModel().subscribeEvent('room', self.roomChanged)
        
  def loadImage(self):
    """ Loads the item's image.
    """
    imgPath = GG.genteguada.GenteGuada.getInstance().getDataPath(self.getModel().getImagePath()+self.getModel().spriteName)  
    self.__img = pygame.sprite.Sprite()
    self.__img.image = pygame.image.load(imgPath).convert_alpha()
    self.__img.rect = self.__img.image.get_rect()
    self.__img.rect.topleft = GG.utils.p3dToP2d(self.getModel().getPosition(), self.getModel().offset)
        
  def getParent(self):
    """ Returns the isoview hud handler.
    """
    return self.__parent
  
  def getIVRoom(self):
    """ Returns the isometric view room object.
    """
    return self.__ivroom
  
  def setIVRoom(self, ivroom):
    """ Sets a new isoview room for the item.
    ivroom: new isoview room.
    """
    self.__ivroom = ivroom
  
  def getImg(self):
    """ Returns a sprite.
    """
    return self.__img
  
  def setImg(self, img):
    """ Sets a new image for the item.
    img: image name.
    """
    imgPath = GG.genteguada.GenteGuada.getInstance().getDataPath(self.getModel().getImagePath()+img)
    self.__img.image = pygame.image.load(imgPath).convert_alpha()
    pygame.display.update()
    
  def setImgPosition(self, pos):
    """ Sets a new position for the item's image.
    pos: new position.
    """
    self.__img.rect.topleft = pos  
    
  def setSprite(self, sprite):
    """ Sets a new sprite for the item
    sprite: new sprite.
    """
    self.__img.image = sprite
    
  def selected(self):
    """ Changes the item's color and sets it as selected.
    """
    size = self.__img.rect
    color2 = [0, 0, 0]
    for x in range(0, size[2]):
      for y in range(0, size[3]):
        color = self.__img.image.get_at((x,y))
        if color[3] != 0:
          color2[0] = color[0] + GG.utils.COLOR_SHIFT
          if color2[0] > 255: color2[0] = 255
          color2[1] = color[1] + GG.utils.COLOR_SHIFT
          if color2[1] > 255: color2[1] = 255
          color2[2] = color[2] + GG.utils.COLOR_SHIFT
          if color2[2] > 255: color2[2] = 255
          self.__img.image.set_at((x,y), color2)
    pygame.display.update()

  def unselected(self):
    """ Restores the item's color and sets it as unselected.
    """
    imgPath = GG.genteguada.GenteGuada.getInstance().getDataPath(self.getModel().getImagePath()+self.getModel().spriteName)
    self.__img.image = pygame.image.load(imgPath).convert_alpha()
    
  
