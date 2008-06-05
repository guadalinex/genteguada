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
import Queue


class RClient(synchronized.Synchronized): 

  def __init__(self, serverIP, port=8000, autoEvents=True): #{{{
    utils.logger.debug("RClient.__init__")
    synchronized.Synchronized.__init__(self)

    dMVC.setRClient(self)

    self.__serverIP   = serverIP
    self.__serverPort = port

    self.__rootModel = None
    self.__sessionID = None
    self.__initialDataSemaphore = threading.Semaphore(0)

    self.__answersCommandsList = []

    self.__remoteSuscriptions = {}  ## TODO: Use weak references

    self.__socket = None
    self.__connect()

    self.__commandQueue = Queue.Queue()

    self.__autoEvents = autoEvents
    if self.__autoEvents:
      threadProcessCommand = threading.Thread(target=self.processCommandQueue)
      threadProcessCommand.setDaemon(True)
      threadProcessCommand.start()

    thread.start_new(self.__start, ())
  #}}}

  def processEvents(self):
    try:
      while True:
        command = self.__commandQueue.get_nowait()
        try:
          command.do()
        except:
          utils.logger.exception('exception in process_command')
    except Queue.Empty:
      pass

  def processCommandQueue(self):
    while True:
      command = self.__commandQueue.get()
      try:
        command.do()
      except:
        utils.logger.exception('exception in process_command')

  def __connect(self): #{{{
    utils.logger.debug("connecting to server")
    self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.__socket.connect((self.__serverIP, self.__serverPort))
    utils.logger.debug("connected to server")
  #}}}

  @synchronized.synchronized(lockName='commandsList')
  def __addAnswererCommand(self, command): #{{{
    self.__answersCommandsList.append(command)
    #print "ponemos ",command
  #}}}


  def __setInitialData(self, initialData): #{{{
    utils.logger.debug("RClient.__setInitialData: "+str(initialData))

    if self.__rootModel != None:
      utils.logger.error("The receiver already has a rootModel")
      raise Exception('The receiver already has a rootModel')

    self.__rootModel = dMVC.clientMaterialize(initialData['rootModel'], self)
    self.__sessionID = dMVC.clientMaterialize(initialData['sessionID'], self)

    self.__initialDataSemaphore.release()
  #}}}


  def getRootModel(self): #{{{
    self.__initialDataSemaphore.acquire()
    result = self.__rootModel
    self.__initialDataSemaphore.release()   
    return result
  #}}}

  def getSessionID(self): #{{{
    self.__initialDataSemaphore.acquire()
    result = self.__sessionID
    self.__initialDataSemaphore.release()   
    return result
  #}}}


  def sendCommand(self, command): #{{{
    serializedCommand = pickle.dumps(command)
    sizeCommand = len(serializedCommand)
    size = struct.pack("i", sizeCommand)
    utils.logger.debug("Sending command: " + str(command) + ' (' + str(sizeCommand) + 'b)')
    self.__socket.send(size)
    self.__socket.send(serializedCommand)
  #}}}


  @synchronized.synchronized(lockName='commandsList')
  def __getAnswer(self, executerCommand):
    found = None
    for each in self.__answersCommandsList:
      if executerCommand.isYourAnswer(each):
        found = each
        #print "encontramos ",each
        break
    if found:
      self.__answersCommandsList.remove(found)
    return found


  def waitForExecutionAnswerer(self, executerCommand): #{{{
    utils.logger.debug("RClient.waitForExecutionAnswerer executerCommand: "+str(executerCommand))
    #print "RClient.waitForExecutionAnswerer executerCommand: "+str(executerCommand)
    found = None
    while not found:
      found = self.__getAnswer(executerCommand)
      if not found:
        if not self.__autoEvents:
          self.processEvents()
        time.sleep(0.001) # tiny sleep to avoid burning the CPU
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
  def unsubscribeEventObserver(self, observer, eventType): #{{{
    utils.logger.debug("RClient.unsubscribeEventObserver observer: "+str(observer)+" , event type: "+str(eventType))
    toRemove = []
    for key, value in self.__remoteSuscriptions.iteritems():
      subscriptionEventType = value[0]
      subscriptionMethod = value[1]
      if subscriptionMethod.im_self is observer:
        if eventType == None or eventType == subscriptionEventType: 
          toRemove.append(key)
    for key in toRemove:
      del self.__remoteSuscriptions[key]
    return toRemove
  #}}}

  @synchronized.synchronized(lockName='remoteSuscriptions')
  def unsubscribeEventMethod(self, method, eventType): #{{{
    utils.logger.debug("RClient.unsubscribeEventMethod method: "+str(method)+" , event type: "+str(eventType))
    toRemove = []
    for key, value in self.__remoteSuscriptions.iteritems():
      subscriptionMethod = value[1]
      subscriptionEventType = value[0]
      if subscriptionMethod == method:
        if eventType == None or eventType == subscriptionEventType: 
          toRemove.append(key)
    for key in toRemove:
      del self.__remoteSuscriptions[key]
  #}}}


  @synchronized.synchronized(lockName='remoteSuscriptions')
  def getRemoteSuscriptionByID(self, suscriptionID): #{{{
    utils.logger.debug("RClient.getRemoteSuscriptionByID suscriptionID: "+str(suscriptionID))
    if suscriptionID in self.__remoteSuscriptions:
      return self.__remoteSuscriptions[suscriptionID]
    else:
      return False
  #}}}


  def __receiveInitialData(self): #{{{
    utils.logger.debug("RClient.receiveRootModel")
    size = self.__socket.recv(struct.calcsize("i"))
    if len(size):
      size = struct.unpack("i", size)[0]
      data = ""
      while len(data) < size:
        data = self.__socket.recv(size - len(data))
      initialData = pickle.loads(data)
      self.__setInitialData(initialData)
  #}}}


  def __start(self): #{{{
    utils.logger.debug("Starting connection thread")
    try:
      self.__receiveInitialData()
      sizeInt = struct.calcsize("i")
      while True:
        size = self.__socket.recv(sizeInt)
        if len(size):
          size = struct.unpack("i", size)[0]
          commandData = ""
          utils.logger.debug("Receive from the server the size: " + str(size)  +"b)")
          #print "recibimos ",size
          while len(commandData) < size:
            commandData += self.__socket.recv(size - len(commandData))
            #print "==============================================>  ",len(commandData)
          command = pickle.loads(commandData)
          #print "recibimos ",size , command
          #print "Al siguiente"
          utils.logger.debug("Receive from the server the command: " + str(command) + " (" + str(size) + "b)")
          if isinstance(command, remotecommand.RExecutionAnswerer):
            self.__addAnswererCommand(command)
          else:
            self.__commandQueue.put(command)
        else:
          self.__socket.close()
    except:
      utils.logger.exception('exception in __start')
  #}}}
