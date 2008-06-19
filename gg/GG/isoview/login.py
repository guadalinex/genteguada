import os
import pygame
import ocempgui.widgets
import GG.utils
import sys
import time

from pygame.locals import * # faster name resolution


class Login:
  """ Login class.
  Defines attributes and methods for a Login class.
  """
    
  def __init__(self, screen, parent):
    """ Class constructor.
    screen: screen handler.
    parent: 
    """
    self.__screen = screen
    self.__textFieldUsername = None
    self.__textFieldPassword = None
    self.__finish = False
    self.__parent = parent
    self.__session = None
  
  def draw(self, user=None, passw=None):
    if user and passw:
      return self.autoLogin(user, passw)

    self.widgetContainer = ocempgui.widgets.Renderer()
    self.widgetContainer.set_screen(self.__screen)
    self.window = ocempgui.widgets.Box(GG.utils.SCREEN_SZ[0],GG.utils.SCREEN_SZ[1])  
    self.__paintScreen()
    self.__paintTextEntrys()
    self.__paintButtons()
    self.widgetContainer.add_widget(self.window)
    self.__start()
  
  def __start(self):
    while not self.__finish:
      time.sleep(GG.utils.TICK_DELAY)
      events = pygame.event.get()
      for event in events:
        if event.type == QUIT:
          sys.exit(0)
      self.widgetContainer.distribute_events(*events)
    if self.__session:
      return self.__session
    self.cancelLogin()


  def __paintScreen(self):
    imgBackgroundRight = GG.utils.OcempImageMapTransparent(GG.genteguada.GenteGuada.getInstance().getDataPath("interface/backgrounds/startGG.png"))
    imgBackgroundRight.topleft = 0,0
    self.window.add_child(imgBackgroundRight)

  def __paintTextEntrys(self):
    self.__textFieldUsername = ocempgui.widgets.Entry("")
    self.__textFieldUsername.topleft = 700,460
    self.__textFieldUsername.set_style(ocempgui.widgets.WidgetStyle(GG.utils.STYLES["textFieldLogin"]))
    self.__textFieldUsername.set_minimum_size(230,40)
    self.window.add_child(self.__textFieldUsername)

    self.__textFieldPassword = ocempgui.widgets.Entry("")
    self.__textFieldPassword.topleft = 700,570
    self.__textFieldPassword.set_style(ocempgui.widgets.WidgetStyle(GG.utils.STYLES["textFieldLogin"]))
    self.__textFieldPassword.set_minimum_size(230,40)
    self.__textFieldPassword.set_password(True)
    self.window.add_child(self.__textFieldPassword)

  def __paintButtons(self):
    imgPath = "interface/editor/ok_button.png"
    buttonOK = GG.utils.OcempImageButtonTransparent(GG.genteguada.GenteGuada.getInstance().getDataPath(imgPath))
    buttonOK.topleft = [750, 690]
    buttonOK.connect_signal(ocempgui.widgets.Constants.SIG_CLICKED, self.acceptLogin)
    self.window.add_child(buttonOK)
     
    imgPath = "interface/editor/cancel_button.png"
    buttonCancel = GG.utils.OcempImageButtonTransparent(GG.genteguada.GenteGuada.getInstance().getDataPath(imgPath))
    buttonCancel.topleft = [870, 690]
    buttonCancel.connect_signal(ocempgui.widgets.Constants.SIG_CLICKED, self.cancelLogin)
    self.window.add_child(buttonCancel)

  def acceptLogin(self):
    user = self.__textFieldUsername.text 
    passw = self.__textFieldPassword.text
    loginData = self.__parent.system.login(user,passw)
    print loginData
    if loginData[0] == True:
      self.__session = loginData[1]
      self.finishLogin()
    else:
      self.__showError(loginData[1])
  
  def __showError(self,errorText):
    buttons = [ocempgui.widgets.Button ("#OK")]
    results = [ocempgui.widgets.Constants.DLGRESULT_OK]
    self.dialog = ocempgui.widgets.GenericDialog ("Error", buttons, results)
    lbl = ocempgui.widgets.Label (errorText)
    self.dialog.content.add_child (lbl)
    self.dialog.connect_signal (ocempgui.widgets.Constants.SIG_DIALOGRESPONSE, self.__closeDialog, self.dialog, lbl)
    self.dialog.topleft = 100, 100
    self.dialog.depth = 1
    self.widgetContainer.add_widget(self.dialog)
    
  def __closeDialog (self,result, dialog, label):
    if result == ocempgui.widgets.Constants.DLGRESULT_OK:
      self.dialog.destroy ()

  def cancelLogin(self):
    sys.exit(0)

  def finishLogin(self):
    self.__screen.fill((0, 0, 0))
    self.__finish = True
  
  def autoLogin(self,user,passw):
    loginData = self.__parent.system.login(user,passw)
    if loginData[0] == True:
      return loginData[1]
    else:
      print loginData[1]
      sys.exit(0)

