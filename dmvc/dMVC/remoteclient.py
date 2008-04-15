import threading
import socket
import time
import pickle
import sys
import select
import remotecommand

import utils
import struct
import traceback


global _rClientSingleton
_rClientSingleton = None

def getRClient(): #{{{
  if _rClientSingleton == None:
    raise Exception("RClient has to be instanciated before calling getRClient()")
  return _rClientSingleton
#}}}

class RClient: #{{{ 

  def __init__(self, serverIP, port=8000): #{{{
    global _rClientSingleton
    if not (_rClientSingleton == None):
      raise Exception("Can't create more then one instance of RClient")
    _rClientSingleton = self

    self._serverIP = serverIP
    self._serverPort = port
    self._rootModel = None
    self._rootModelSemaphore = threading.Semaphore(0)
    self._thread = None

    self._commandsList      = []
    self._commandsListMutex = threading.Semaphore(1)

    self._remoteSuscriptions = {}  ## TODO: Use weak references
    self._remoteSuscriptionsMutex = threading.Semaphore(1)

    self._start()
  #}}}

  def _addCommand(self, command):
    self._commandsListMutex.acquire()
    self._commandsList.append(command)
    #print str(len(self._commandsList)) + " commands in the list (appended)"
    self._commandsListMutex.release()
    

  def hasRootModel(self): #{{{
    return not (self._rootModel == None)
  #}}}

  def setRootModel(self, model): #{{{
    if self._rootModel != None:
      raise Exception('The receiver already has a rootModel')
    self._rootModel = model
    self._rootModelSemaphore.release()
  #}}}

  def getRootModel(self): #{{{
    self._rootModelSemaphore.acquire()
    result = self._rootModel
    self._rootModelSemaphore.release()   
    return result
  #}}}

  def sendCommand(self, command): #{{{
    serializedCommand = pickle.dumps(command)

    sizeCommand = len(serializedCommand)
    size = struct.pack("i",sizeCommand)
    self._thread.getSocket().send(size)

    self._thread.getSocket().send(serializedCommand)
  #}}}


  def waitForExecutionAnswerer(self, executerCommand):
    found = None

    while not found:
      self._commandsListMutex.acquire()

      for each in self._commandsList:
        if executerCommand.isYourAnswer(each):
          found = each
          break

      if found:
        self._commandsList.remove(found)
        #print str(len(self._commandsList)) + " commands in the list (removed)"

      self._commandsListMutex.release()

      if not found:
        time.sleep(0.02)

    return found

  def registerRemoteSuscription(self, suscription):
    suscriptionID = utils.nextID()
    self._remoteSuscriptionsMutex.acquire()
    self._remoteSuscriptions[suscriptionID] = suscription
    self._remoteSuscriptionsMutex.release()
    return suscriptionID


  def getRemoteSuscriptionByID(self, suscriptionID):
    self._remoteSuscriptionsMutex.acquire()
    result = self._remoteSuscriptions[suscriptionID]
    self._remoteSuscriptionsMutex.release()
    return result

  def _start(self): #{{{
    self._thread = RClientThread(self)
    self._thread.start()
  #}}}

#}}}

class RClientThread(threading.Thread): #{{{

  def __init__(self, rClient): #{{{
    threading.Thread.__init__(self)
    self.rClient = rClient

    self._socket          = None
    self._socketSemaphore = threading.Semaphore(0)
  #}}}

  def _receiveRootModel(self): #{{{
    size = struct.calcsize("i")
    size = self.getSocket().recv(size)
    if len(size):
      size = struct.unpack("i", size)[0]
      data = ""
      while len(data) < size:
        data = self.getSocket().recv(size - len(data))
      rootModel = pickle.loads(data)
      self.rClient.setRootModel(rootModel)
  #}}}


  def getSocket(self):
    self._socketSemaphore.acquire()
    result = self._socket
    self._socketSemaphore.release()
    return result


  def _connect(self):
    self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self._socket.connect((self.rClient._serverIP, self.rClient._serverPort))
    self._socketSemaphore.release()


  def run(self): #{{{
    self._connect()

    self._receiveRootModel()

    while True:
      size = struct.calcsize("i")
      size = self.getSocket().recv(size)
      if len(size):
        size = struct.unpack("i", size)[0]
        commandData = ""
        while len(commandData) < size:
          commandData = self.getSocket().recv(size - len(commandData))
        command = pickle.loads(commandData)
        if isinstance(command, remotecommand.RExecutionAnswerer):
          self.rClient._addCommand(command)
        else:
          command.do()
      else:
        self.getSocket().close()

#}}}
