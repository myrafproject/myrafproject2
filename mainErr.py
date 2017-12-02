# -*- coding: utf-8 -*-
"""
Created:--------------------------------------------------------------------------------------------
		By:
			Muhammed SHEMUNI		Developer
			Yücel KILIÇ				Developer
		at:
			Begin					04.12.2013
			Last update				04.06.2014
Importing things:-----------------------------------------------------------------------------------
		Must have as installed:
			python-2.7
			pyqt4-dev-tools
			imagemagick(convert)
			iraf					http://www.astro.uson.mx/~favilac/downloads/ubuntu-iraf/iso/
			pyraf					^
			sextractor				http://www.astromatic.net/software/sextractor/
			alipy					http://obswww.unige.ch/~tewes/alipy/
			astroasciidata			http://www.stecf.org/software/PYTHONtools/astroasciidata/
			f2n						http://obswww.unige.ch/~tewes/f2n_dot_py/
----------------------------------------------------------------------------------------------------
"""
import sys , os, time, string, math, signal, datetime, ntpath, numpy


from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from error import Ui_Form2



class MyForm2(QtGui.QWidget, Ui_Form2):
  def __init__(self):
    super(MyForm2, self).__init__()
    self.ui2 = Ui_Form2()
    self.ui2.setupUi(self)

    self.ui2.pushButton.clicked.connect(self.sav)
    
    ud = os.popen("echo $HOME")
    self.HOME = "%s/.MYRaf2" %(ud.read().replace("\n",""))
    if not os.path.isdir("%s/obsdat" %(self.HOME)):
		os.popen("mkdir -p %s/obsdat/" %(self.HOME))
		os.popen("cp -rf /usr/share/myraf/obsdat/* %s/obsdat/" %(self.HOME))
    
    if os.path.isfile("%s/tmp/error" %(self.HOME)):
		fl = open("%s/tmp/error" %(self.HOME), "r")
		it = self.ui2.listWidget.count()-1
		for i in fl:
			i=i.replace("\n","")
			it = it+1
			item = QtGui.QListWidgetItem()
			self.ui2.listWidget.addItem(item)
			item = self.ui2.listWidget.item(it)
			item.setText(QtGui.QApplication.translate("Form", i, None, QtGui.QApplication.UnicodeUTF8))
			
  def sav(self):
	if os.path.isfile("%s/tmp/error" %(self.HOME)):
		ofile = QtGui.QFileDialog.getSaveFileName( self, 'MYRaf Error', 'myErr.my', 'log or my (*.my *.log)')
		os.popen("cp %s/tmp/error %s" %(self.HOME, ofile))
