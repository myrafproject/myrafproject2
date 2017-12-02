from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import os, datetime,  dateutil,  time
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.dates as md

def PlotFunc(self,  chartDevice,  Phase,  diffMag,  residual,  pColor, legend, shape):
    print(chartDevice)
    chartDevice.ax.hold(True)
    chartDevice.ax.plot(Phase, diffMag, shape,  color = "%s" %(pColor),  label = "%s" %(legend), picker=5)
    chartDevice.ax.legend(shadow = True, loc = (1, 0.5), numpoints = 1,  prop={'size':10})
    chartDevice.draw()

def add(self, flist):
	filename = QtGui.QFileDialog.getOpenFileNames(self ,"Images...","",("Fit or Fits (*.fits *.fit)"))
	it = flist.count()-1
	for x in filename:
			it = it+1
			item = QtGui.QListWidgetItem()
			flist.addItem(item)
			item = flist.item(it)
			item.setText(QtGui.QApplication.translate("Form", x, None, QtGui.QApplication.UnicodeUTF8))
	return True

def rm(self, flist):
	for x in flist.selectedItems():
			flist.takeItem(flist.row(x))
	fnumber = flist.count()
	return True

def unlocDiv(self, chBox, div):
	if chBox.checkState() == QtCore.Qt.Checked:
		div.setEnabled(True)
	else:
		div.setEnabled(False)
	return True

def unlocCali(self, chBox, tab):
	if chBox.checkState() == QtCore.Qt.Checked:
		self.ui.tabWidget_2.setTabEnabled(tab,True)
	else:
		self.ui.tabWidget_2.setTabEnabled(tab,False)
	return True

def lisFromLW(self, listWidget):
	items = []
	for x in xrange(listWidget.count()):
		line = listWidget.item(x)
		filePath = line.text()
		items.append(filePath)
	return map(str, items)
	
def list2file(lst, fl):
	if os.path.isfile(fl):
		os.popen("rm %s" %fl)
	
	f = open(fl, "wb")
	for i in lst:
		f.write("%s\n" %(i))
	f.close()

def logging(self, txt):
	f = open("%s/log.my" %(self.HOME), "a")
	f.write("%s\n" %(str(txt)))
	f.close()

def pixelSelectManAlign(event):
	print(str(event.pos().x()) + " - " + str(event.pos().y()))
	
def display(self, FilePath, displayDevice):
	if os.path.isfile(FilePath):
			scene = QtGui.QGraphicsScene()
			scene.addPixmap(QtGui.QPixmap(FilePath))
			displayDevice.setScene(scene)

def zoom(self, display, val):
	display.scale(val, val)
        
def rot(self, display, val):
	display.rotate(val);
        
def flip(self, display, dire):
	if dire == "v":
		display.scale(-1,1);
	if dire == "h":
		display.scale(1,-1);
