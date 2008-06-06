import ocempgui
import pygame
import random
import GG.utils
import animation
import positioned_view

class IsoViewChatMessage(positioned_view.PositionedView):
  """ IsoViewChatMessage class.
  Defines a chat message view.
  """
  
  def __init__(self, model, screen, isohud):
    """ Class constructor.
    model: chat message model.
    screen: screen handler.
    """
    positioned_view.PositionedView.__init__(self, model, screen)
    imgPath = GG.genteguada.GenteGuada.getInstance().getDataPath("balloon.png")  
    self.__isohud = isohud
    self.__img = pygame.sprite.Sprite()
    self.__img.image = pygame.image.load(imgPath).convert_alpha()
    self.__img.rect = self.__img.image.get_rect()
    self.__img.rect.topleft = [model.getPosition()[0] + 80, model.getPosition()[1] - 10]
    self.__isohud.getIsoviewRoom().addTopSprite(self.__img)
    
  def getImg(self):
    return self.__img
  
  def getScreenPosition(self):
    return self.__img.rect.topleft

  def setScreenPosition(self, pos):
    self.__img.rect.topleft = pos
  
  #def setSprite(self, sprite):
  #  self.__img.image = sprite
    
  def getStyleMessageChat(self):
    """ Returns the chat current style.
    """
    #TODO entiendo que el color del chat depende de cada usuario 
    listStyle = ["chatEntryBlack","chatEntryRed","chatEntryGreen","chatEntryBlue"]
    return GG.utils.STYLES[listStyle[random.randint(0,len(listStyle)-1)]]
  
  def paintBalloon(self):
    self.getScreen().blit(self.__img.image, GG.utils.HUD_OR)
    pygame.display.update()
  
  def draw(self):
    hframe = ocempgui.widgets.HFrame()
    hframe.border = 0
    imgPath = GG.genteguada.GenteGuada.getInstance().getDataPath(GG.utils.IMAGE_CHAT_MESSAGE)
    image = ocempgui.widgets.ImageLabel(imgPath)
    image.buttom = 0
    hframe.add_child(image)
    string = self.getModel().getHour()+" [" + self.getModel().getSender() + "]: " + self.getModel().getMessage()
    label = ocempgui.widgets.Label(string)
    label.set_style(ocempgui.widgets.WidgetStyle(self.getStyleMessageChat()))
    hframe.add_child(label)
    return hframe