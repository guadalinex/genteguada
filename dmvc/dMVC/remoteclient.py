import dMVC
import utils
import threading
import socket
import time
import pickle
import remotecommand
import struct
import thread

import synchronized

class RClient(synchronized.Synchronized): 

  def __init__(self, serverIP, port=8000): #{{{
    utils.logger.debug("RClient.__init__")
    synchronized.Synchronized.__init__(self)

    dMVC.setRClient(self)

    self.__serverIP = serverIP
    self.__serverPort = port
    self.__rootModel = None
    self.__rootModelSemaphore = threading.Semaphore(0)
    self.__commandsList      = []
    self.__remoteSuscriptions = {}  ## TODO: Use weak references
    self.__socket = None
    self.__socketSemaphore = threading.Semaphore(0)
    thread.start_new(self.__start,())
  #}}}

  @synchronized.synchronized(lockName='commandsList')
  def __addCommand(self, command): #{{{
    #utils.logger.debug("RClient.addCommand command: "+str(command))
    self.__commandsList.append(command)
  #}}}

  def setRootModel(self, model): #{{{
    utils.logger.debug("RClient.setRootModel model: "+str(model))
    if self.__rootModel != None:
      utils.logger.error("The receiver already has a rootModel")
      raise Exception('The receiver already has a rootModel')
    self.__rootModel = dMVC.clientMaterialize(model, self)
    self.__rootModelSemaphore.release()
  #}}}

  def getRootModel(self): #{{{
    #utils.logger.debug("RClient.getRootModel")
    self.__rootModelSemaphore.acquire()
    result = self.__rootModel
    self.__rootModelSemaphore.release()   
    return result
  #}}}

  def sendCommand(self, command): #{{{
    utils.logger.debug("RClient.sendCommand command: "+str(command))
    serializedCommand = pickle.dumps(command)
    sizeCommand = len(serializedCommand)
    size = struct.pack("i",sizeCommand)
    self.__socket.send(size)
    self.__socket.send(serializedCommand)
  #}}}



  @synchronized.synchronized(lockName='commandsList')
  def __getAnswer(self, executerCommand):
    found = None
    for each in self.__commandsList:
      if executerCommand.isYourAnswer(each):
        found = each
        break
    if found:
      self.__commandsList.remove(found)
    return found


  def waitForExecutionAnswerer(self, executerCommand): #{{{
    utils.logger.debug("RClient.waitForExecutionAnswerer executerCommand: "+str(executerCommand))
    found = None
    while not found:
      found = self.__getAnswer(executerCommand)
      if not found:
        time.sleep(0.025)
    return found
  #}}}

  @synchronized.synchronized(lockName='remoteSuscriptions')
  def registerRemoteSuscription(self, suscription): #{{{
    utils.logger.debug("RClient.registerRemoteSuscription suscription: "+str(suscription))
    suscriptionID = utils.nextID()
    self.__remoteSuscriptions[suscriptionID] = suscription
    return suscriptionID
  #}}}

  @synchronized.synchronized(lockName='remoteSuscriptions')
  def getRemoteSuscriptionByID(self, suscriptionID): #{{{
    utils.logger.debug("RClient.getRemoteSuscriptionByID suscriptionID: "+str(suscriptionID))
    result = self.__remoteSuscriptions[suscriptionID]
    return result
  #}}}

  def __connect(self): #{{{
    utils.logger.debug("RClient.connect")
    self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.__socket.connect((self.__serverIP, self.__serverPort))
    utils.logger.info("the client connect to server")
    self.__socketSemaphore.release()
  #}}}

  def __receiveRootModel(self): #{{{
    utils.logger.debug("RClient.receiveRootModel")
    size = struct.calcsize("i")
    size = self.__socket.recv(size)
    if len(size):
      size = struct.unpack("i", size)[0]
      data = ""
      while len(data) < size:
        data = self.__socket.recv(size - len(data))
      rootModel = pickle.loads(data)
      self.setRootModel(rootModel)
  #}}}

  def __start(self): #{{{
    utils.logger.debug("RClient.start")
    self.__connect()
    self.__receiveRootModel()
    sizeInt = struct.calcsize("i")
    while True:
      size = self.__socket.recv(sizeInt)
      if len(size):
        size = struct.unpack("i", size)[0]
        commandData = ""
        while len(commandData) < size:
          commandData = self.__socket.recv(size - len(commandData))
        command = pickle.loads(commandData)
        utils.logger.debug("Receive from the server the command: " + str(command) + " (" + str(size) + "b)")
        if isinstance(command, remotecommand.RExecutionAnswerer):
          self.__addCommand(command)
        else:
          command.do()
      else:
        self.__socket.close()
  #}}}

