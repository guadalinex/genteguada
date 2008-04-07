import sys
import unittest

sys.path.append("../client")
sys.path.append("../common")

import ggclient.remoteclient
import ggcommon.remotemodel
import time

class TestRemoteObject(unittest.TestCase):
 
  def testConnect(self):
    print "Ejecutando test de conexion"
    ipServer = "127.0.0.1"
    client = ggclient.remoteclient.RClient(ipServer)
    time.sleep(1)
    assert client._thread.socket.getpeername()[0] == ipServer 
    
    print "Ejecutando test de root model"
    model = client.getRootModel()
    assert isinstance(model,ggcommon.remotemodel.RemoteModel)
    
    print "Ejecutamos el metodo foo sin argumentos"
    result = model.foo()
    assert result.__class__ == ggcommon.remotecommand.RExecuteResult
    assert result.do() == "foo"

    print "Ejecutamos el metodo bar sin argumentos"
    result = model.bar()
    assert result.__class__ == ggcommon.remotecommand.RExecuteResult
    assert result.do() == "bar"

    print "Obtenemos un modelo a partir del root model"
    result = model.player()
    assert result.__class__ == ggcommon.remotecommand.RExecuteResult
    player = result.do()
    assert isinstance(player,ggcommon.remotemodel.RemoteModel)

    print "Ejecutamos un metodo del objeto obtenido a partir del root"
    result = player.name()
    assert result.__class__ == ggcommon.remotecommand.RExecuteResult
    assert result.do() == "maradona"

    print "Ejecutamos un metodo del rootModel pasando un parametro"
    param = "Antonio"
    result = model.saluda(param)
    assert result.__class__ == ggcommon.remotecommand.RExecuteResult
    assert result.do() == "Hola "+str(param)

    print "Ejecutamos un metodo del rootModel pasando dos parametros"
    param1 = "Luis"
    param2 = "Garcia"
    result = model.nombreApellidos(param1,param2)
    assert result.__class__ == ggcommon.remotecommand.RExecuteResult
    assert result.do() == param1+ "  "+ param2

if __name__ == "__main__":
  test = unittest.main()
