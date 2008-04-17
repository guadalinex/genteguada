#!/usr/bin/python

from distutils.core import setup
import os
import sys
import setuptools

class doc(setuptools.Command):
  description = "Genera la documentacion del proyecto"
  user_options = []
  doc_src=  "dMVC"
  doc_dst="doc"
  excepciones=['__init__.py']# Estos no los quiero documentar
  
  def initialize_options(self):
    pass

  def finalize_options(self):
    pass

  def run(self):
    try:
      import pydoc
    except:
      print "No se encuentra pydoc. No puedo seguir"
      sys.exit(256)
    
    if not os.path.isdir(self.doc_dst):
      os.mkdir(self.doc_dst)
    os.chdir(self.doc_dst)
    print "Generando documentacion de %s..."%self.doc_src,
    pydoc.writedoc(self.doc_src)
    for file in os.listdir('../'+self.doc_src):
      if file.split('.')[-1] == 'py' and file not in self.excepciones:
          print "Generando documentacion de %s..."%file,
          pydoc.writedoc("%s.%s"%(self.doc_src,file.split('.')[0]))


setup (  
        cmdclass={"doc": doc},
        name = "dMVC",
        version = "0.1",
        description = "distributed model view controller",
        author = "Diego Gomez Deck,Joseba Mariscal",
        author_email = "DiegoGomezDeck@consultar.com,jmariscal@igosoftware.es",
        license='(c) Igo Software.',
        platforms= ["UNIX"],
        packages = ["dMVC"]
      )

