# -*- coding: utf-8 -*-

import os
import dMVC.model
import ggmodel
import GG.model.teleport
import GG.model.giver_npc
import GG.model.penguin
import GG.model.pickable_item
import GG.model.web_item
import GG.utils

import giver_npc
import room_item
import box_heavy
import pickable_item
import teleport
import web_item
import GG.utils

    
# ======================= CONSTANTS ===========================    
    
IMAGES_DICT = {}
IMAGES_DICT["BoxHeavy"] = {"heavy_box.png": [[26, -10], [0, -12]]}
IMAGES_DICT["Door"] = {}
IMAGES_DICT["Door"]["wooden_door.png"] = [[28, 23], [0, 0]]
IMAGES_DICT["Door"]["wooden_door_a.png"] = [[24, 37], [0, 0]]
IMAGES_DICT["Door"]["wooden_door_b.png"] = [[24, 55], [0, 0]]
IMAGES_DICT["Door"]["armored_door_left.png"] = [[17, 15], [0, 0]]
IMAGES_DICT["Door"]["downArrow.png"] = [GG.utils.FLOOR_SHIFT, [0, 0]]
IMAGES_DICT["Door"]["leftArrow.png"] = [GG.utils.FLOOR_SHIFT, [0, 0]]
IMAGES_DICT["Door"]["rightArrow.png"] = [GG.utils.FLOOR_SHIFT, [0, 0]]
IMAGES_DICT["Door"]["upArrow.png"] = [GG.utils.FLOOR_SHIFT, [0, 0]]
IMAGES_DICT["DoorWithKey"] = IMAGES_DICT["Door"]
IMAGES_DICT["DoorOpenedByPoints"] = IMAGES_DICT["Door"]
IMAGES_DICT["DoorPressedTiles"] = IMAGES_DICT["Door"]
IMAGES_DICT["RoomItem"] = {}
IMAGES_DICT["RoomItem"]["hedge.png"] = [[55, 13], [0, -26]]
IMAGES_DICT["RoomItem"]["fence_up.png"] = [[55, 15], [0, 0]]
IMAGES_DICT["RoomItem"]["fence_left.png"] = [[55, 15], [0, 0]]
IMAGES_DICT["RoomItem"]["tree.png"] = [[100, 150], [0, -26]]
IMAGES_DICT["RoomItem"]["stone_column.png"] = [[13, 15], [0, 0]]
IMAGES_DICT["RoomItem"]["wooden_beam.png"] = [[57, 142], [0, 0]]
IMAGES_DICT["RoomItem"]["wall_left.png"] = [[55, 0], [0, 0]]
IMAGES_DICT["RoomItem"]["wall_up.png"] = [[35, 10], [0, 0]]
IMAGES_DICT["RoomItem"]["yard_up.png"] = [[25, 50], [0, 0]]
IMAGES_DICT["RoomItem"]["yard_left.png"] = [[45, 50], [0, 0]]
IMAGES_DICT["RoomItem"]["yard_lamp_up.png"] = [[25, 50], [0, 0]]
IMAGES_DICT["RoomItem"]["yard_lamp_left.png"] = [[45, 50], [0, 0]]
IMAGES_DICT["RoomItem"]["yard_corner.png"] = [[55, 45], [0, 0]]
IMAGES_DICT["RoomItem"]["warehouseWallUp01.png"] = [[35, 33], [0, 0]]
IMAGES_DICT["RoomItem"]["warehouseWallUp02.png"] = [[35, 33], [0, 0]]
IMAGES_DICT["RoomItem"]["warehouseWallLeft01.png"] = [[35, 33], [0, 0]]
IMAGES_DICT["RoomItem"]["warehouseWallLeft02.png"] = [[35, 33], [0, 0]]
IMAGES_DICT["RoomItem"]["warehouseWallCorner.png"] = [[35, 33], [0, 0]]
IMAGES_DICT["RoomItem"]["skylineWallUp01.png"] = [[35, 40], [0, 0]]
IMAGES_DICT["RoomItem"]["skylineWallUp02.png"] = [[35, 40], [0, 0]]
IMAGES_DICT["RoomItem"]["skylineWallUp03.png"] = [[35, 40], [0, 0]]
IMAGES_DICT["RoomItem"]["skylineWallUp04.png"] = [[35, 40], [0, 0]]
IMAGES_DICT["RoomItem"]["skylineWallLeft01.png"] = [[35, 40], [0, 0]]
IMAGES_DICT["RoomItem"]["skylineWallLeft02.png"] = [[35, 40], [0, 0]]
IMAGES_DICT["RoomItem"]["skylineCorner.png"] = [[35, 40], [0, 0]]
IMAGES_DICT["PenguinTalker"] = {}
IMAGES_DICT["PenguinTalker"]["andatuz_right.png"] = [[30, 0], [0, 0]]
IMAGES_DICT["PenguinTalker"]["andatuz_down.png"] = [[30, 0], [0, 0]]
IMAGES_DICT["PenguinTalker"]["andatuz_bottomright.png"] = [[30, 0], [0, 0]]
IMAGES_DICT["PenguinTrade"] = IMAGES_DICT["PenguinTalker"]
IMAGES_DICT["PenguinQuiz"] = IMAGES_DICT["PenguinTalker"]
IMAGES_DICT["GiverNpc"] = {}
IMAGES_DICT["GiverNpc"]["gift.png"] = [[15, -30], [0, 0]]
IMAGES_DICT["GiverNpc"]["golden_key.png"] = [[15, -30], [0, 0]]
IMAGES_DICT["PickableItem"] = {}
IMAGES_DICT["PickableItem"]["gift.png"] = [[15, -30], [0, 0]]
IMAGES_DICT["PickableItem"]["golden_key.png"] = [[15, -30], [0, 0]]
IMAGES_DICT["PaperMoney"] = {}
IMAGES_DICT["PaperMoney"]["5Guadapuntos.png"] = [[14, -25], [0, -10]]
IMAGES_DICT["PaperMoney"]["10Guadapuntos.png"] = [[14, -25], [0, -10]]
IMAGES_DICT["PaperMoney"]["50Guadapuntos.png"] = [[14, -25], [0, -10]]
IMAGES_DICT["WebGift"] = {}
IMAGES_DICT["WebGift"]["gift.png"] = [[15, -30], [0, 0]]
IMAGES_DICT["WebItem"] = IMAGES_DICT["RoomItem"]
IMAGES_DICT["WebItem"]["heavy_box.png"] = [[26, -10], [0, -12]]
IMAGES_DICT["WebItem"]["andatuz_right.png"] = [[30, 0], [0, 0]]
IMAGES_DICT["WebItem"]["andatuz_down.png"] = [[30, 0], [0, 0]]
IMAGES_DICT["WebItem"]["andatuz_bottomright.png"] = [[30, 0], [0, 0]]
IMAGES_DICT["WebItem"]["gift.png"] = [[15, -30], [0, 0]]
IMAGES_DICT["WebItem"]["golden_key.png"] = [[15, -30], [0, 0]]

IMAGES_GIFT_PATH = os.path.join(GG.utils.DATA_PATH, GG.utils.IMAGES_GIFT)

# ====================================================================
class GGSession(ggmodel.GGModel):
  """ GGSession class.
  Includes room and player objects, and some procedures to manage data.
  """
    
  def __init__(self, player, system):
    """ Initializes session attributes.
    player: session user.
    system: system object
    """
    ggmodel.GGModel.__init__(self)
    self.__player = player
    self.__system = system
    player.subscribeEvent('chatAdded', self.chatAdded)
    player.getRoom().subscribeEvent('chatAdded', self.chatAdded)
    player.subscribeEvent('roomChanged', self.roomChanged)
      
  def setStartRoom(self, room, startRoom):
    """ Adds a new startRoom.
    startRoom: new start room.
    """  
    self.__system.setStartRoom(room, startRoom)
      
  def getPlayer(self):
    """ Returns the active player.
    """
    return self.__player
   
  def roomChanged(self, event):
    """ Triggers after receiving a change room event.
    event: event info.
    """
    oldRoom = event.getParams()['oldRoom']
    if oldRoom:
      oldRoom.unsubscribeEventMethod(self.chatAdded)
    newRoom = self.__player.getRoom()
    if newRoom: 
      newRoom.subscribeEvent('chatAdded', self.chatAdded)
      
  @dMVC.model.localMethod
  def defaultView(self, screen, fullscreen, user, accesMode):
    """ Creates the isoview hud.
    screen: screen handler.
    fullscreen: sets view as fullscreen or windowed mode.
    """
    import GG.isoview.isoview_hud
    return GG.isoview.isoview_hud.IsoViewHud(self, screen, fullscreen, user, accesMode)
    
  def chatAdded(self, event):
    """ Triggers after receiving a chat added event.
    event: event info.
    """
    self.triggerEvent('chatAdded', message=event.getParams()['message'], text=event.getParams()['text'], 
                      header=event.getParams()['header'])
  
  def quizAdded(self, event):
    """ Triggers after receiving a chat added event.
    event: event info.
    """
    self.triggerEvent('quizAdded', message=event.getParams()['message'])

  def unsubscribeEvents(self):
    """ Unsubscribes itself from all events.
    """
    self.__player.getRoom().unsubscribeEventObserver(self)
    self.__player.unsubscribeEventObserver(self)

  def logout(self):
    """ Logs out and ends session.
    """  
    if self.__system:
      self.__system.logout(self)
      self.__system = None
    self.__player = None
    
  def getRoomLabels(self):
    """ Returns rooms labels.
    """  
    return self.__system.getRoomLabels()  

  def getRooms(self):
    """ Returns the room list.
    """  
    return self.__system.getRooms()  

  def getRoom(self, roomLabel):
    """ Returns one specific room.
    roomLabel: room label.
    """  
    return self.__system.existsRoom(roomLabel)

  def getPlayersList(self):
    """ Returns the player's list.
    """  
    return self.__system.getPlayersList()    

  def getSpecificPlayer(self, name):
    """ Returns a specific player.
    name: player name.
    """  
    return self.__system.getSpecificPlayer(name)  

  def getSystem(self):
    """ Returns the system object.
    """  
    return self.__system  
    
  def newBroadcastMessage(self, line):
    """ Sends a new broadcast message.
    line: new message.
    """  
    self.__system.newBroadcastMessage(line, self.__player)  
    
  def labelChange(self, oldLabel, newLabel):
    """ Changes an item label and all its references on all items.
    oldLabel: old label.
    newLabel: new label.
    """  
    self.__system.labelChange(oldLabel, newLabel)
    
  def getObjectsData(self):
    """ Returns the objects data.
    """  
    if not self.__player.getAccessMode():
      return None  
    pos = self.__player.getRoom().getNearestEmptyCell(self.__player.getPosition())
    """           
    "PenguinQuiz": {"position": pos, "label": [""], "filePath": [GG.utils.QUESTIONS_PATH], "images": IMAGES_DICT["PenguinTalker"].keys() },  
    "PenguinTalker": {"position": pos, "label": [""], "message": [""], "images": IMAGES_DICT["PenguinTalker"].keys() },
    "PenguinTrade": { "position": pos, "label": [""], "gift": [""], "message": [""], "images": IMAGES_DICT["PenguinTrade"].keys()},
    """
    self.objectsDict = {
      "Muros":{ "position": pos, "images": GG.utils.WALLS },
      "Decorativos":{ "position": pos, "images": GG.utils.DECORATORS },
      "Apilables":{ "position": pos, "label": "", "images": GG.utils.STACKS },
      "Llaves":{ "position": pos, "label": "", "images": GG.utils.KEYS },
      "Rios":{ "position": pos, "images": GG.utils.RIVERS },
      "Inventario": { "position": pos, "label": "", "images": GG.utils.INVENTORYS },
      "Dinero": { "position": pos, "images": GG.utils.MONEYS },
      "Puertas":{ "position": pos, "destinationRoom": "", "exitPosition": [1, 1], "label": "", "images": GG.utils.DOORS },
      "Puertas con llave":{ "position": pos, "destinationRoom": "", "exitPosition": [1, 1], "label": "",  "key": "", "images": GG.utils.DOORS },
      "Puertas con puntos": { "position": pos, "destinationRoom": "", "exitPosition": [1, 1], "label": "", "pointsGiver": "", "images": GG.utils.DOORS},
      "Puertas con celdas": { "position": pos, "destinationRoom": "", "exitPosition": [1, 1], "label": "", "pressedTile1": [0, 0], 
          "pressedTile2": [0, 0], "images": GG.utils.DOORS},
      "Enlaces web": { "position": pos, "label": "", "url": "", "images": GG.utils.WEBS },
      "Regalos":{ "position": pos, "label": "", "imagesGift": self.getImagesGift()}
    }
    return self.objectsDict
    
  def __getImageCreateObject(self, img, name):
    if not img:
      self.__player.newChatMessage("Debe seleccionar una imagen para el objeto.", 1)
      return None
    if name == "Regalos":
      return os.path.join(GG.utils.IMAGES_GIFT, img)
    else:
      return os.path.join(GG.utils.FURNITURE_PATH, img)
    
  def __getPositionCreateObject(self, value, room, key):
    if not room:
      return None
    try: 
      posX = int(value[0])    
      posY = int(value[1])
    except ValueError: 
      self.__player.newChatMessage("El valor "+ key +" debe ser un entero", 1) 
      return None
    if not (0 <= posX < room.size[0] and 0 <= posY < room.size[1]):
      self.__player.newChatMessage("Las coordenadas para la "+ key +" no son correctas.", 1)
      return None
    if key == "posicion":
      if not room.getTile([posX, posY]).stepOn():
        self.__player.newChatMessage('No se puede colocar un objeto en esa posicion', 1) 
        return None
    return [posX, posY]

  def __getLabelCreateObject(self, label):
    if label[0] == "":
      self.__player.newChatMessage("Debe introducir un nombre para el objeto.", 1)
      return None
    return str(label[0])

  def __getDestinationRoomCreateObject(self, roomLabel):
    room = self.__system.getRoom(str(roomLabel[0])) 
    if not room:
      self.__player.newChatMessage("La habitación destino no existe", 1)
      return None
    return room

  def __getKeyCreateObject(self, key, text):
    if key[0] == "":
      self.__player.newChatMessage("Debe introducir la eiqueta " + text + "la puerta.", 1)
      return None
    return str(key[0])

  def __getUrlCreateObject(self, url):
    if url[0] == "":
      self.__player.newChatMessage("Debe introducir una direccion web para el objeto.", 1)
      return None
    return str(url[0])

  def __createObjectImagesPosition(self, data, room, objectLabel):
    images = self.__getImageCreateObject(data["images"], objectLabel)
    position = self.__getPositionCreateObject(data["position"], room, "posicion")
    if images and position:
      if objectLabel in ["Muros","Decoradores"]:
        object = room_item.GGRoomItem(images)
      elif objectLabel == "Rios":
        object = room_item.GGRiver(images)
      elif objectLabel == "Dinero":
        object = pickable_item.PaperMoney(images)
      room.addItemFromVoid(object, position)

  def __createObjectImagesPositionLabel(self, data, room, objectLabel):
    images = self.__getImageCreateObject(data["images"], objectLabel)
    position = self.__getPositionCreateObject(data["position"], room, "posicion")
    label = self.__getLabelCreateObject(data["label"])
    if images and position and label:
      print objectLabel
      if objectLabel == "Apilables":
        object = box_heavy.GGBoxHeavy(images, label)
      elif objectLabel == "Llaves":
        object = giver_npc.GGGiverNpc(images, images, label)
      elif objectLabel == "Inventario":
        object = pickable_item.GGPickableItem(images, images, label)
      room.addItemFromVoid(object, position)

  def __createObjectTeleport(self, data, room):
    images = self.__getImageCreateObject(data["images"], "noRegalo")
    position = self.__getPositionCreateObject(data["position"], room, "posicion")
    destinationRoom = self.__getDestinationRoomCreateObject(data["destinationRoom"])
    exitPosition = self.__getPositionCreateObject(data["exitPosition"], destinationRoom, "posicionSalida")
    label = self.__getLabelCreateObject(data["label"])
    if images and position and destinationRoom and exitPosition:
      door = teleport.GGTeleport(images, exitPosition, destinationRoom.getName(), label)
      room.addItemFromVoid(door, position)

  def __createObjectTeleportKeyPoints(self, data, room, objectName):
    images = self.__getImageCreateObject(data["images"], objectName)
    position = self.__getPositionCreateObject(data["position"], room, "posicion")
    destinationRoom = self.__getDestinationRoomCreateObject(data["destinationRoom"])
    exitPosition = self.__getPositionCreateObject(data["exitPosition"], destinationRoom, "posicionSalida")
    label = self.__getLabelCreateObject(data["label"])
    if objectName == "Puertas con llave":
      key = self.__getKeyCreateObject(data["key"], " de la llave que abre ")
    elif objectName == "Puertas con puntos":
      key = self.__getKeyCreateObject(data["pointsGiver"], " del objeto que da los puntos para abrir ")
    else:
      key = None
    if images and position and destinationRoom and exitPosition and key: 
      if objectName == "Puertas con llave":
        object = teleport.GGDoorWithKey(images, exitPosition, destinationRoom.getName(), label, key)
      else:
        object = teleport.GGDoorOpenedByPoints(images, exitPosition, destinationRoom.getName(), label, key)
      room.addItemFromVoid(object, position)

  def __createObjectTeleportPressed(self, data, room):
    images = self.__getImageCreateObject(data["images"], "noRegalo")
    position = self.__getPositionCreateObject(data["position"], room, "posicion")
    destinationRoom = self.__getDestinationRoomCreateObject(data["destinationRoom"])
    exitPosition = self.__getPositionCreateObject(data["exitPosition"], destinationRoom, "posicionSalida")
    label = self.__getLabelCreateObject(data["label"])
    pressedTile1 = self.__getPositionCreateObject(data["pressedTile1"], room, "pressedTile1")
    pressedTile2 = self.__getPositionCreateObject(data["pressedTile2"], room, "pressedTile2")
    if images and position and destinationRoom and exitPosition and pressedTile1 and pressedTile2: 
      door = teleport.GGDoorPressedTiles(images, exitPosition, destinationRoom.getName(), label, [pressedTile1, pressedTile2])
      room.addItemFromVoid(door, position)

  def __createObjectWeb(self, data, room):
    images = self.__getImageCreateObject(data["images"], "noRegalo")
    position = self.__getPositionCreateObject(data["position"], room, "posicion")
    label = self.__getLabelCreateObject(data["label"])
    url = self.__getUrlCreateObject(data["url"])
    if images and position and label and url:
      webobject = web_item.GGWebItem(images, url, label)
      room.addItemFromVoid(webobject, position)

  def __createObjectGift(self, data, room, objectName):
    images = self.__getImageCreateObject(data["imagesGift"], objectName)
    position = self.__getPositionCreateObject(data["position"], room, "posicion")
    label = self.__getLabelCreateObject(data["label"])
    if images and position and label:
      gift = giver_npc.WebGift(images, label, self.__player.username)
      room.addItemFromVoid(gift, position)

  def createObject(self, name, data):
    """ Creates a new object.
    name: object type.
    data: object data.
    """  
    room = self.__player.getRoom()
    if name in ["Muros", "Decorativos", "Rios", "Dinero"]:
      self.__createObjectImagesPosition(data, room, name)
    elif name in ["Apilables","Llaves","Inventario"]:
      self.__createObjectImagesPositionLabel(data, room, name)
    elif name == "Puertas":
      self.__createObjectTeleport(data, room)
    elif name in ["Puertas con llave", "Puertas con puntos"]:
      self.__createObjectTeleportKeyPoints(data, room, name)
    elif name == "Puertas con celdas":
      self.__createObjectTeleportPressed(data, room)
    elif name == "Enlaces web":
      self.__createObjectWeb(data, room)
    elif name == "Regalos":
      self.__createObjectGift(data, room, name)

  def getImagesGift(self):
    """ Returns all available images for an admin created gift.
    """  
    result = []
    for giftFile in os.listdir(IMAGES_GIFT_PATH):
      if os.path.isfile(os.path.join(IMAGES_GIFT_PATH, giftFile)):
        filepath, fileName = os.path.split(giftFile)
        name, ext = os.path.splitext(fileName)
        if ext in [".jpg", ".png", ".JPG", ".PNG"]:
          result.append(fileName)
    return result

  def getAdminInitData(self):
    package = {}
    package["objectsData"] = self.getObjectsData()
    package["playerList"] = self.getPlayersList()
    package["roomListInfo"] = self.getRoomsInfo()
    return package

  def getRoomsInfo(self):
    roomsDict = {}
    rooms = self.getRooms()
    for room in rooms:
      roomsDict[room.getName()] = room
    return roomsDict
