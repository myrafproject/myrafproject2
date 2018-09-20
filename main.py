# -*- coding: utf-8 -*-
"""
Created:--------------------------------------------------------------------------------------------
        By:
            Muhammed SHEMUNI        Developer
            Yücel KILIÇ             Developer
        at:
            Begin                   04.12.2013
            Last update             17.02.2017
Importing things:-----------------------------------------------------------------------------------
        Must have as installed:
            python-2.7
            pyqt4-dev-tools
            iraf                    http://www.astro.uson.mx/~favilac/downloads/ubuntu-iraf/iso/
            pyraf                   ^
            sextractor              http://www.astromatic.net/software/sextractor/
            alipy                   http://obswww.unige.ch/~tewes/alipy/
            astroasciidata          http://www.stecf.org/software/PYTHONtools/astroasciidata/
            f2n                     http://obswww.unige.ch/~tewes/f2n_dot_py/
            Ginga                   http://ginga.readthedocs.org/en/latest/
            matplotlib              http://matplotlib.org/
            astropy                 http://www.astropy.org/
----------------------------------------------------------------------------------------------------
"""
import sys, time, string, math, signal, datetime, ntpath, numpy, subprocess

try:
    # force Qt4 API v2
    import sip
    apis = ["QDate",
            "QDateTime",
            "QString",
            "QTextStream",
            "QTime",
            "QUrl",
            "QVariant"]

    for api in apis:
        sip.setapi(api, 2)
    
    import os
    os.environ['QT_API'] = 'pyqt'
    # force matplotlib to use Qt4 backend
    import matplotlib
    matplotlib.use('Qt4Agg')
    
    from PyQt4 import QtGui, QtCore
    from PyQt4.QtGui import *
    from PyQt4.QtCore import *
except:
    print("Can not load PyQT4")
    os.system("echo \"- " + str(datetime.datetime.utcnow()) + " - Did you install PyQT4?.\" >>$HOME/.MYRaf2/log.my")
    raise SystemExit

from matplotlib.patches import Circle
os.system("mkdir -p $HOME/.MYRaf2")
os.system("echo \"- " + str(datetime.datetime.utcnow()) + " - MYRaf started.\" >>$HOME/.MYRaf2/log.my")

try:
    from myraf import Ui_Form
    from mainErr import MyForm2
    import function, gui
except:
    print("Can not load MYRaf.")
    os.system("echo \"-- " + str(datetime.datetime.utcnow()) + " - MYRaf is not installed properly.\">>$HOME/.MYRaf2/log.my")
    raise SystemExit

try:
    from fPlot import *
    from sexCat import *
except:
    print("Where is fPlot?")
    raise SystemExit

try:
    from pyraf import iraf
    from pyraf.iraf import noao, imred, ccdred, darkcombine, flatcombine, ccdproc ,astutil, setjd, setairmass, asthedit, digiphot, apphot, phot, ptools, txdump, artdata, imgeom
    from astropy.stats import sigma_clip
    from numpy import mean
    import numpy as np
except:
    print("Can not load PyRAF, iraf")
    os.system("echo \"-- " + str(datetime.datetime.utcnow()) + " - Did you install PyRAF, iraf?\">>$HOME/.MYRaf2/log.my")
    raise SystemExit

try:
    import lco_alipy as alipy
    import glob
except:
    print("Did you install 'alipy'? To furter information:\nhttp://obswww.unige.ch/~tewes/alipy/")
    os.system("echo \"-- " + str(datetime.datetime.utcnow()) + " - Where is alipy & glob?\">>$HOME/.MYRaf2/log.my")
    raise SystemExit

from astropy.table import Table
from astropy import table


class MyForm(QtGui.QWidget, Ui_Form):
  def __init__(self):
    super(MyForm, self).__init__()
    self.ui = Ui_Form()
    self.ui.setupUi(self)
    
    ud = os.popen("echo $HOME")
    self.HOME = "%s/.MYRaf2" %(ud.read().replace("\n",""))
    if not os.path.isdir("%s/obsdat" %(self.HOME)):
        os.popen("mkdir -p %s/obsdat/" %(self.HOME))
        os.popen("cp -rf /usr/share/myraf/obsdat/* %s/obsdat/" %(self.HOME))
        
    if not os.path.isdir("%s/set" %(self.HOME)):
        os.popen("mkdir -p %s/set/" %(self.HOME))
        os.popen("cp -rf /usr/share/myraf/set/* %s/set/" %(self.HOME))

#    try:
#		frev = open("%s/set/rev" %(self.HOME), "r")
#		for r in frev:
#			irev = r
#		rev = os.popen("svn info http://myrafproject.googlecode.com/svn/trunk/ |grep Revision")
#		rev = rev.read().replace("\n","")
#		self.ui.label_12.setText(QtGui.QApplication.translate("Form", "%s is available, you have %s" %(rev, irev), None, QtGui.QApplication.UnicodeUTF8))
#    except:
#		rev = os.popen("svn info http://myrafproject.googlecode.com/svn/trunk/ |grep Revision")
#		rev = rev.read().replace("\n","")
#		self.ui.label_12.setText(QtGui.QApplication.translate("Form", "%s is available, you have an unknown revision. Please update MYRaf." %(rev), None, QtGui.QApplication.UnicodeUTF8))

    os.system("rm -rf $HOME/.MYRaf2/tmp/*")
    os.system("rm -rf $HOME/.MYRaf2/alipy_visu")
    os.system("rm -rf $HOME/.MYRaf2/alipy_out")
    os.system("mkdir -p $HOME/.MYRaf2/tmp/alipy/")
    os.system("mkdir -p $HOME/.MYRaf2/tmp/analyzed/")
    
    f = open('%s/log.my' %(self.HOME), 'r')
    it = self.ui.listWidget_10.count()-1
    for line in f:
        li=line.strip()
        li = str(li)
        it = it+1
        item = QtGui.QListWidgetItem()
        self.ui.listWidget_10.addItem(item)
        item = self.ui.listWidget_10.item(it)
        item.setText(QtGui.QApplication.translate("Form", str(li), None, QtGui.QApplication.UnicodeUTF8))

    it = self.ui.listWidget_12.count()-1
    for files in glob.glob("%s/obsdat/*" %(self.HOME)):
        fn = ntpath.basename(str(files))
        it = it+1
        item = QtGui.QListWidgetItem()
        self.ui.listWidget_12.addItem(item)
        item = self.ui.listWidget_12.item(it)
        item.setText(QtGui.QApplication.translate("Form", str(fn), None, QtGui.QApplication.UnicodeUTF8))
    self.ui.listWidget_12.sortItems()
      
    self.ui.tabWidget_2.setTabEnabled(1,False)
    self.ui.tabWidget_2.setTabEnabled(2,False)
    self.ui.tabWidget_2.setTabEnabled(3,False)
    
    self.ui.tabWidget_8.setTabEnabled(1,False)
    self.ui.tabWidget_8.setTabEnabled(2,False)
    self.ui.tabWidget_8.setTabEnabled(3,False)
    
    self.ui.tabWidget_6.setTabEnabled(3,False)
    self.ui.tabWidget_4.setTabEnabled(3,False)
    
    self.ui.checkBox.clicked.connect(self.unlockBias)
    self.ui.checkBox_2.clicked.connect(self.unlockDark)
    self.ui.checkBox_3.clicked.connect(self.unlockFlat)
    
    self.ui.checkBox_8.clicked.connect(self.unlockSBias)
    self.ui.checkBox_9.clicked.connect(self.unlockSDark)
    self.ui.checkBox_10.clicked.connect(self.unlockSFlat)
    
    self.ui.pushButton_18.clicked.connect(self.displayCoords)
    
    #self.ui.pushButton_34.clicked.connect(self.saveSettings)
    
    self.ui.pushButton_3.clicked.connect(lambda: gui.add(self, self.ui.listWidget))
    self.ui.pushButton_4.clicked.connect(lambda: gui.rm(self, self.ui.listWidget))
    self.ui.pushButton_5.clicked.connect(lambda: gui.add(self, self.ui.listWidget_2))
    self.ui.pushButton_6.clicked.connect(lambda: gui.rm(self, self.ui.listWidget_2))
    self.ui.pushButton_10.clicked.connect(lambda: gui.add(self, self.ui.listWidget_3))
    self.ui.pushButton_8.clicked.connect(lambda: gui.rm(self, self.ui.listWidget_3))
    self.ui.pushButton_13.clicked.connect(lambda: gui.add(self, self.ui.listWidget_4))
    self.ui.pushButton_11.clicked.connect(lambda: gui.rm(self, self.ui.listWidget_4))
    self.ui.pushButton_15.clicked.connect(lambda: gui.add(self, self.ui.listWidget_5))
    self.ui.pushButton_16.clicked.connect(lambda: gui.rm(self, self.ui.listWidget_5))
    self.ui.pushButton_22.clicked.connect(lambda: gui.add(self, self.ui.listWidget_6))
    self.ui.pushButton_21.clicked.connect(lambda: gui.rm(self, self.ui.listWidget_6))
    self.ui.pushButton_33.clicked.connect(lambda: gui.add(self, self.ui.listWidget_7))
    self.ui.pushButton_32.clicked.connect(lambda: gui.rm(self, self.ui.listWidget_7))
    self.ui.pushButton_36.clicked.connect(lambda: gui.add(self, self.ui.listWidget_9))
    self.ui.pushButton_37.clicked.connect(lambda: gui.rm(self, self.ui.listWidget_9))
    
    self.ui.pushButton_20.clicked.connect(lambda: gui.add(self, self.ui.listWidget_13))
    self.ui.pushButton_23.clicked.connect(lambda: gui.rm(self, self.ui.listWidget_13))
    self.ui.pushButton_26.clicked.connect(lambda: gui.add(self, self.ui.listWidget_14))
    self.ui.pushButton_25.clicked.connect(lambda: gui.rm(self, self.ui.listWidget_14))
    self.ui.pushButton_30.clicked.connect(lambda: gui.add(self, self.ui.listWidget_15))
    self.ui.pushButton_29.clicked.connect(lambda: gui.rm(self, self.ui.listWidget_15))
    self.ui.pushButton_43.clicked.connect(lambda: gui.add(self, self.ui.listWidget_16))
    self.ui.pushButton_42.clicked.connect(lambda: gui.rm(self, self.ui.listWidget_16))
    
    self.ui.pushButton_3.clicked.connect(self.displayCalibLabel)
    self.ui.pushButton_4.clicked.connect(self.displayCalibLabel)
    self.ui.pushButton_5.clicked.connect(self.displayCalibLabel)
    self.ui.pushButton_6.clicked.connect(self.displayCalibLabel)
    self.ui.pushButton_10.clicked.connect(self.displayCalibLabel)
    self.ui.pushButton_8.clicked.connect(self.displayCalibLabel)
    self.ui.pushButton_13.clicked.connect(self.displayCalibLabel)
    self.ui.pushButton_11.clicked.connect(self.displayCalibLabel)
    
    self.ui.listWidget_5.clicked.connect(self.displayAutAlign)
    self.ui.pushButton_14.clicked.connect(self.goAutAlign)
    
    self.ui.listWidget_6.clicked.connect(self.displayManAlign)
    self.ui.pushButton_27.clicked.connect(self.goManAlign)
    
    self.ui.listWidget_7.clicked.connect(self.displayPhot)
    self.ui.pushButton_45.clicked.connect(self.coorDel)
    self.ui.pushButton_35.clicked.connect(self.goPhot)
    
    self.ui.listWidget_9.clicked.connect(self.getHeader)
    self.ui.listWidget_11.clicked.connect(self.getVlueFromHeader)
    self.ui.checkBox_5.clicked.connect(self.unlockGetHeaderFromValue)
    self.ui.pushButton_39.clicked.connect(self.goHeaderAdd)
    self.ui.pushButton_38.clicked.connect(self.goHeaderDel)
    
    self.ui.listWidget_12.clicked.connect(self.getObservat)
    self.ui.pushButton_41.clicked.connect(self.rmObservatory)
    self.ui.pushButton_40.clicked.connect(self.addObservatory)
    
    self.ui.pushButton_7.clicked.connect(self.masterZero)
    self.ui.pushButton_9.clicked.connect(self.masterDark)
    self.ui.pushButton_12.clicked.connect(self.masterFlat)
    self.ui.pushButton_2.clicked.connect(self.choosePointCol)
    
    self.ui.pushButton.clicked.connect(self.calib)
    
    self.ui.pushButton_44.clicked.connect(self.readStars)
    self.ui.pushButton_46.clicked.connect(self.plotChart)
    
    self.ui.pushButton_17.clicked.connect(self.findStars)
    
    self.ui.checkBox_4.clicked.connect(self.epochUnlock)
    self.ui.checkBox_12.clicked.connect(self.timeobsUnlock)
    # self.ui.checkBox_12.clicked.connect(self.timeStampUnlock)
    
    self.ui.pushButton_19.clicked.connect(self.chartClear)
  
    self.ui.pushButton_34.clicked.connect(self.saveSettings)
    self.applySettings()
    
    self.ui.dispManual.canvas.fig.canvas.mpl_connect('button_press_event',self.mouseClick)
    self.ui.dispPhoto.canvas.fig.canvas.mpl_connect('button_press_event',self.mouseClick)
    
    self.ui.disp_chart.canvas.fig.canvas.mpl_connect('pick_event', self.onpick)

    self.ui.listWidget_13.clicked.connect(self.displayScheduler)
    self.ui.dispSched.canvas.fig.canvas.mpl_connect('button_press_event',self.mouseClick)
    self.ui.pushButton_47.clicked.connect(lambda: gui.rm(self, self.ui.listWidget_17))
    self.ui.pushButton_47.clicked.connect(self.displayCoords)
    self.ui.pushButton_28.clicked.connect(lambda: self.uaSched("add"))
    self.ui.pushButton_31.clicked.connect(self.rmSched)
    self.ui.listWidget_18.clicked.connect(self.getSched)
    self.ui.pushButton_48.clicked.connect(lambda: self.uaSched("upd"))
    self.ui.pushButton_24.clicked.connect(self.goSched)
    
    self.ui.pushButton_51.clicked.connect(self.getHeaderExtra)
    self.ui.pushButton_49.clicked.connect(self.extraAdd)
    self.ui.pushButton_50.clicked.connect(lambda: gui.rm(self, self.ui.listWidget_20))
    
    self.ui.listWidget_8.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
    self.connect(self.ui.listWidget_8, QtCore.SIGNAL('customContextMenuRequested(const QPoint&)'), self.on_context_menu)
    
    self.popMenu = QtGui.QMenu(self)
    self.popMenu.addAction('Import', self.impCooPhot)
    self.popMenu.addAction('Export', self.expCooPhot)
    
    self.ui.listWidget_17.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
    self.connect(self.ui.listWidget_17, QtCore.SIGNAL('customContextMenuRequested(const QPoint&)'), self.on_context_menu2)
    self.popMenu2 = QtGui.QMenu(self)
    self.popMenu2.addAction('Import', self.impSchPhot)
    self.popMenu2.addAction('Export', self.expSchPhot)
    
    self.plotFdA = FitsPlot(self.ui.dispAuto.canvas)
    self.plotFdM = FitsPlot(self.ui.dispManual.canvas)
    self.plotFdP = FitsPlot(self.ui.dispPhoto.canvas)
    self.plotFdS = FitsPlot(self.ui.dispSched.canvas)
    self.plotFdCC = FitsPlot(self.ui.dispCC.canvas)
    self.plotFdWCS = FitsPlot(self.ui.dispWCS.canvas)
    
    self.ui.listWidget_22.clicked.connect(self.displayCC)
    self.ui.pushButton_55.clicked.connect(self.goCC)
    
    self.ui.listWidget_24.clicked.connect(self.displayWCS)
    self.ui.pushButton_58.clicked.connect(self.goWCS)

    self.ui.pushButton_52.clicked.connect(self.updateMe)
    
    self.ui.checkBox_13.clicked.connect(lambda: gui.unlocDiv(self, self.ui.checkBox_13, self.ui.doubleSpinBox_8))
    self.ui.checkBox_14.clicked.connect(lambda: gui.unlocDiv(self, self.ui.checkBox_14, self.ui.doubleSpinBox_9))
    self.ui.checkBox_15.clicked.connect(lambda: gui.unlocDiv(self, self.ui.checkBox_15, self.ui.doubleSpinBox_15))
    
    self.ui.pushButton_57.clicked.connect(lambda: gui.add(self, self.ui.listWidget_22))
    self.ui.pushButton_56.clicked.connect(lambda: gui.rm(self, self.ui.listWidget_22))
    self.ui.pushButton_60.clicked.connect(lambda: gui.add(self, self.ui.listWidget_24))
    self.ui.pushButton_59.clicked.connect(lambda: gui.rm(self, self.ui.listWidget_24))
###############################################
  def displayWCS(self):
    gui.logging(self, "-- %s - image conversion started." %(datetime.datetime.utcnow()))
    img = self.ui.listWidget_24.currentItem()
    img = img.text()
    self.plotFdWCS.load(str(img))

  def goWCS(self):
    if self.ui.listWidget_24.count() != 0:
		if self.ui.checkBox_18.checkState() == QtCore.Qt.Checked:
			if self.ui.checkBox_19.checkState() == QtCore.Qt.Checked:
				print "Hizala baslik gom"
			else:
				print "Hizala baslik gomme"
		else:
			if self.ui.checkBox_19.checkState() == QtCore.Qt.Checked:
				print "Hizalama baslik gom"
			else:
				print "Hizalama baslik gomme"
    else:
		QtGui.QMessageBox.critical( self,  ("MYRaf Error"), ("Please add some images"))
#############################################
  def displayCC(self):
    gui.logging(self, "-- %s - image conversion started." %(datetime.datetime.utcnow()))
    img = self.ui.listWidget_22.currentItem()
    img = img.text()
    self.plotFdCC.load(str(img))

  def goCC(self):
    if self.ui.listWidget_22.count() != 0:
		odir = QtGui.QFileDialog.getExistingDirectory( self, 'Select Directory to Save Cleaned File(s)')
		if os.path.exists(odir):
			it = 0
			if self.ui.checkBox_16.checkState() == QtCore.Qt.Checked:
				ccMask = "yes"
			else:
				ccMask = "no"
			ccGaing = float(self.ui.doubleSpinBox_10.value())
			ccRN = float(self.ui.doubleSpinBox_11.value())
			ccSC = float(self.ui.doubleSpinBox_12.value())
			ccSF = float(self.ui.doubleSpinBox_13.value())
			ccOL = float(self.ui.doubleSpinBox_14.value())
			
			errCC = ""
			
			for x in xrange(self.ui.listWidget_22.count()):
				 it = it + 1
				 img = self.ui.listWidget_22.item(x)
				 img = str(img.text())
				 if not function.cosmicsClean(img, "%s/%s" %(odir, ntpath.basename(str(img))), mask = ccMask, Gain=ccGaing, Readnoise=ccRN, Sigclip = ccSC, Sigfrac = ccSF, Objlim = ccOL):
					 errCC = "%s/%s" %(errCC, ntpath.basename(str(img)))
				 self.ui.label_58.setText(QtGui.QApplication.translate("Form", "Cleaning %s" %(ntpath.basename(str(img))), None, QtGui.QApplication.UnicodeUTF8))
				 self.ui.progressBar_9.setProperty("value", math.ceil(100*(float(float(it)/float(self.ui.listWidget_22.count())))))
			if errCC != "":
				errCC = "Cosmic Cleaner can't handle images below\n%s" %(errCC)
				self.dispErr(errCC)
    else:
		QtGui.QMessageBox.critical( self,  ("MYRaf Error"), ("Please add some images"))
############################################
  def restart(self):
    subprocess.Popen("myraf2")
    sys.exit(0)
##########################################

  def updateMe(self):
    print "Started to Download"
    self.ui.label_12.setText(QtGui.QApplication.translate("Form", "Started to Download", None, QtGui.QApplication.UnicodeUTF8))
    os.popen("svn checkout http://myrafproject.googlecode.com/svn/trunk/ /tmp/myraf")
    self.ui.progressBar_8.setProperty("value", 33)
    print "copying files"
    os.popen("cp -rf /tmp/myraf/* /usr/share/myraf/")
    self.ui.progressBar_8.setProperty("value", 66)
    self.ui.label_12.setText(QtGui.QApplication.translate("Form", "Copying files", None, QtGui.QApplication.UnicodeUTF8))
    rev = os.popen("svn info http://myrafproject.googlecode.com/svn/trunk/ |grep Revision")
    rev = rev.read().replace("\n","")
    self.ui.progressBar_8.setProperty("value", 100)
    self.ui.label_12.setText(QtGui.QApplication.translate("Form", "Finished...", None, QtGui.QApplication.UnicodeUTF8))
    print "Finished..."
    rev = os.popen("svn info http://myrafproject.googlecode.com/svn/trunk/ |grep Revision")
    rev = rev.read().replace("\n","")
    f = open("%s/set/rev" %(self.HOME), "w")
    f.write(rev)
    f.close()
    self.ui.label_12.setText(QtGui.QApplication.translate("Form", "%s is available" %(rev), None, QtGui.QApplication.UnicodeUTF8))
    reply = QtGui.QMessageBox.question(self, 'Message', "If you want to apply changeds please restart MYRaf.\nDo you want to restart MYRaf?", QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
    if reply == QtGui.QMessageBox.Yes:
		self.restart()
	
##################################################
  def on_context_menu2(self, point):
    self.popMenu2.exec_(self.ui.listWidget_17.mapToGlobal(point))
    
  def impSchPhot(self):
    fname = QtGui.QFileDialog.getOpenFileName(self, 'Open MYRaf Coordinates file', '')
    if os.path.isfile(fname):
        f = open(fname, 'r')
        it = self.ui.listWidget_17.count()-1
        for i in f:
            try:
                den, den2 = float(i.replace("\n","").split("-")[0].strip()), float(i.replace("\n","").split("-")[1].strip())
                it = it + 1
                item = QtGui.QListWidgetItem()
                self.ui.listWidget_17.addItem(item)
                item = self.ui.listWidget_17.item(it)
                item.setText(QtGui.QApplication.translate("Form", "%s-%s" %(den, den2), None, QtGui.QApplication.UnicodeUTF8))
            except:
                print "Not Float"
            
  def expSchPhot(self):
    if self.ui.listWidget_17.count() == 0:
        QtGui.QMessageBox.critical( self,  ("MYRaf Error"), ("No Coordinates"))
    else:
        ofile = QtGui.QFileDialog.getSaveFileName( self, 'Save MYRaf Coordinates file', 'coo.my', 'my (*.my)')
        it = -1
        f = open(ofile, 'w')
        for i in xrange(self.ui.listWidget_17.count()):
            it = it + 1
            coo = self.ui.listWidget_17.item(i)
            coo = str(coo.text())
            f.write("%s\n" %(coo))
        f.close()

##########################################

  def impCooPhot(self):
    fname = QtGui.QFileDialog.getOpenFileName(self, 'Open MYRaf Coordinates file', '')
    if os.path.isfile(fname):
        f = open(fname, 'r')
        it = self.ui.listWidget_8.count()-1
        for i in f:
            try:
                den, den2 = float(i.replace("\n","").split("-")[0].strip()), float(i.replace("\n","").split("-")[1].strip())
                it = it + 1
                item = QtGui.QListWidgetItem()
                self.ui.listWidget_8.addItem(item)
                item = self.ui.listWidget_8.item(it)
                item.setText(QtGui.QApplication.translate("Form", "%s-%s" %(den, den2), None, QtGui.QApplication.UnicodeUTF8))
            except:
                print "Not Float"
            
  def expCooPhot(self):
    if self.ui.listWidget_8.count() == 0:
        QtGui.QMessageBox.critical( self,  ("MYRaf Error"), ("No Coordinates"))
    else:
        ofile = QtGui.QFileDialog.getSaveFileName( self, 'Save MYRaf Coordinates file', 'coo.my', 'my (*.my)')
        it = -1
        f = open(ofile, 'w')
        for i in xrange(self.ui.listWidget_8.count()):
            it = it + 1
            coo = self.ui.listWidget_8.item(i)
            coo = str(coo.text())
            f.write("%s\n" %(coo))
        f.close()

  def on_context_menu(self, point):
    self.popMenu.exec_(self.ui.listWidget_8.mapToGlobal(point))
#########################################################

  def extraAdd(self):
    if self.ui.listWidget_19.selectedItems() == []:
        QtGui.QMessageBox.critical( self,  ("MYRaf Error"), ("Please at least select one header."))
    else:
            
        for i in self.ui.listWidget_19.selectedItems():
            if self.ui.listWidget_20.findItems(str(i.text()), Qt.MatchExactly) == []:
                item = QtGui.QListWidgetItem()
                self.ui.listWidget_20.addItem(item)
                item = self.ui.listWidget_20.item(self.ui.listWidget_20.count()-1)
                item.setText(QtGui.QApplication.translate("Form", "%s" %(str(i.text())), None, QtGui.QApplication.UnicodeUTF8))

  def getHeaderExtra(self):
    
    ok = False
    if self.ui.listWidget_13.count() == 0:
        if self.ui.listWidget_7.count() == 0:
            QtGui.QMessageBox.critical( self,  ("MYRaf Error"), ("Please add some images to Photometry Image or Scheduler Image list."))
        else:
            ok = True
            lst = self.ui.listWidget_7
    else:
        ok = True
        lst = self.ui.listWidget_13
    
    if ok:
        lst.setCurrentRow(0)
        img = lst.currentItem()
        
        if os.path.isfile(str(img.text())):
            h = iraf.hedit(str(img.text()), "*", ".", Stdout=1)
            for x in xrange(self.ui.listWidget_19.count()):
                self.ui.listWidget_19.takeItem(0)
            
            it = -1
            for i in h:
                st = i.split(",")[1].split(" = ")[0]
                it = it + 1
                item = QtGui.QListWidgetItem()
                self.ui.listWidget_19.addItem(item)
                item = self.ui.listWidget_19.item(it)
                item.setText(QtGui.QApplication.translate("Form", "%s" %(st), None, QtGui.QApplication.UnicodeUTF8))
###########################################################

  def dispErr(self, er):
    if os.path.isfile("%s/tmp/error" %(self.HOME)):
        os.popen("rm -rf %s/tmp/error" %(self.HOME))
    fl = open("%s/tmp/error" %(self.HOME), "w")
    fl.write(er)
    fl.close()
    f2 = MyForm2()
    f2.setParent(f)
    flags = QtCore.Qt.Tool
    f2.setWindowFlags(flags)
    f2.show()

#Scheduler#########################
  def goSched(self):    
    if self.ui.listWidget_18.count() == 0:
        QtGui.QMessageBox.critical( self,  ("MYRaf Error"), ("Nothing to do."))
    else:
        it = 0
        rows = self.ui.listWidget_18.count()
        img = self.ui.listWidget_18.setCurrentRow(0)
        
        for x in xrange(rows):
            self.getSched()
            it = it + 1
            ofilename = self.ui.listWidget_18.currentItem()
            ofilename = str(ofilename.text())
            ofile = "%s/tmp/%s" %(self.HOME, ofilename)
            
            zC = com = self.ui.comboBox_2.currentText()
            zR = com = self.ui.comboBox_3.currentText()
            zCT = self.ui.lineEdit_9.text()
            
            dC = com = self.ui.comboBox_4.currentText()
            dR = com = self.ui.comboBox_5.currentText()
            dS = com = self.ui.comboBox_8.currentText()
            dCT = self.ui.lineEdit_10.text()
            
            fC = com = self.ui.comboBox_6.currentText()
            fR = com = self.ui.comboBox_7.currentText()
            fS = com = self.ui.comboBox_9.currentText()
            fCT = self.ui.lineEdit_11.text()
            
            cS = com = self.ui.comboBox_10.currentText()
            cCT = self.ui.lineEdit_12.text()
            
            sname = self.ui.lineEdit_14.text()
            subf = self.ui.comboBox_9.currentText()
            subc = self.ui.comboBox_10.currentText()
            
            biasFiles = ""
            darkFiles = ""
            flatFiles = ""
            
            fErr = ""
            cErr = ""
            
            if self.ui.groupBox_26.isChecked():
                if self.ui.checkBox_8.isChecked():
                    
                    gui.list2file(gui.lisFromLW(self, self.ui.listWidget_14), "%s/tmp/zeroList" %(self.HOME))
                    self.ui.label_71.setText("Zero Combine...")
                    if os.path.isfile("%s/tmp/zero.fit" %(self.HOME)):
                        os.popen("rm %s/tmp/zero.fit" %(self.HOME))
                    if function.zeroCombine("%s/tmp/zeroList" %(self.HOME), "%s/tmp/zero.fit" %(self.HOME), com=zC, rej=zR, cty=zCT):
                        biasFiles = "%s/tmp/zero.fit" %(self.HOME)
                        
                if self.ui.checkBox_9.isChecked():
                    gui.list2file(gui.lisFromLW(self, self.ui.listWidget_15), "%s/tmp/darkList" %(self.HOME))
                    self.ui.label_71.setText("Dark Combine...")
                    if os.path.isfile("%s/tmp/dark.fit" %(self.HOME)):
                        os.popen("rm %s/tmp/dark.fit" %(self.HOME))
                    if function.darkCombine("%s/tmp/darkList" %(self.HOME), "%s/tmp/dark.fit" %(self.HOME), com=dC, rej=dR, cty=dCT, scl=dS):
                        darkFiles = "%s/tmp/dark.fit" %(self.HOME)

                if self.ui.checkBox_10.isChecked():
                    gui.list2file(gui.lisFromLW(self, self.ui.listWidget_16), "%s/tmp/flatList" %(self.HOME))
                    self.ui.label_71.setText("Flat Combine...")
                    f = open("%s/tmp/flatList" %(self.HOME), "r")
                    itF = 0
                    for z in f:
                        fn = z.replace("\n","")
                        if function.headerRead(fn,sname) == "":
                            itF = itF + 1
                    f.close()
                    if subf == "yes" and itF != 0:
                        self.ui.label_71.setText("There is no %s header in some Flat files. Skipping" %(subf))
                    else:
                        if os.path.isfile("%s/tmp/flat_*.fit" %(self.HOME)):
                            os.popen("rm %s/tmp/flat_*.fit" %(self.HOME))
                        if function.flatCombine("%s/tmp/flatList" %(self.HOME), "%s/tmp/" %(self.HOME), com=fC, rej=fR, cty=fCT, sub=fS):
                            flatFiles = "%s/tmp/flat_*.fits" %(self.HOME)

            if self.ui.groupBox_29.isChecked():
                f = open("%s/tmp/pc" %(self.HOME), "w")
                for x in xrange(self.ui.listWidget_17.count()):
                    coo = self.ui.listWidget_17.item(x)
                    coo = str(coo.text())
                    coo = coo.replace("-", " ")
                    f.write("%s\n" %(coo))
                f.close()
                    
                exp = self.ui.lineEdit_13.text()
                fil = self.ui.lineEdit_14.text()
                dan = self.ui.doubleSpinBox.value()
                ann = self.ui.doubleSpinBox_2.value()
                cbo = self.ui.doubleSpinBox_3.value()
                ape = self.ui.lineEdit_15.text()
                zma = self.ui.lineEdit_16.text()
                obs = self.ui.lineEdit_18.text()
                obt = self.ui.lineEdit_17.text()
                obd = self.ui.lineEdit_24.text()
                ra = self.ui.lineEdit_22.text()
                dec = self.ui.lineEdit_23.text()
                epo = self.ui.lineEdit_25.text()
                gai = self.ui.lineEdit_26.text()
                
                apert = self.ui.lineEdit_15.text()
                staCount = self.ui.listWidget_17.count()
                
                if os.path.exists(ofile):
                    os.popen("rm %s" %(ofile))
                    
                extFie = ""
                itExt = 0
                for ext in xrange(self.ui.listWidget_20.count()):
                    itExt = itExt + 1
                    fie = self.ui.listWidget_20.item(ext)
                    fie = str(fie.text())
                    extFie = "%s\t%s" %(extFie, fie)
                
                f = open(ofile, "w")
                f.write("# STAR = %s\n" %(str(staCount)))
                f.write("# APERTURE = %s\n" %(str(apert)))
                f.write("# DO NOT EDIT PARAMETRES ABOVE. You can add comments starts with '#' below ths line.\n")
                f.write("# If you don't have any experience before, DO NOT EDIT THIS FILE!\n")
                f.write("# id\tTIME\tMAG%s\tMERR%s\tAIRMASS%s\n"%(self.ui.lineEdit_15.text().replace(",","\tMAG"), self.ui.lineEdit_15.text().replace(",","\tMERR"), extFie))
                f.close()
                
            err = ""
            errJD = ""
            errSid = ""
            errAir = ""
            errTM = ""
            errOB = ""
            errORA = ""
            errODEC = ""
            errdt = ""
            errOBSERVAT = ""
            errEpoch = ""
            obsOK = False

            iIt = 0

            for y in xrange(self.ui.listWidget_13.count()):
                iIt = iIt + 1
                iImg = self.ui.listWidget_13.item(y)
                iImg = str(iImg.text())
                if self.ui.groupBox_26.isChecked():
                    if function.headerRead(iImg, sname) == "" and subc == "yes":
                        self.ui.label_71.setText("There is no %s header in %s file. Skipping" %(subf, ntpath.basename(str(iImg))))
                    else:
                        function.headerWrite(iImg, "subset", str("'(@\"%s\")'" %sname))
                        if not function.calibration(iImg, biasFiles, darkFiles, flatFiles, "%s/tmp" %(self.HOME), cCT, sub=cS):
                            cErr = "%s, %s" %(iImg, cErr)
                        else:
                            os.popen("mv -f %s/tmp/%s %s" %(self.HOME, ntpath.basename(str(iImg)), iImg))
                            
                if self.ui.checkBox_11.isChecked():
                    refImage = self.ui.listWidget_13.currentItem()
                    refImage = str(refImage.text())
                    if not function.autoAlign(self, iImg, refImage, os.path.split(iImg)[0], visu=False):
                        self.ui.label_71.setText("Can not align %s" %(ntpath.basename(str(iImg))))
                
                if self.ui.groupBox_29.isChecked():
                    tm = function.headerRead(iImg, obt)
                    ob = function.headerRead(iImg, obs)
                    dt = function.headerRead(iImg, obd)
                    ora = function.headerRead(iImg, ra)
                    odec = function.headerRead(iImg, dec)
                    observatory = function.headerRead(img, obs)
                    
                    if self.ui.checkBox_4.checkState() == QtCore.Qt.Checked:
                        epo = function.epoch(iImg, obd, obt)
                        if epo == False:
                            errEpoch = "%sBad time-date header:%s\n" %(errEpoch, iImg)
                        else:
                            function.headerWrite(iImg, "epoch", epo)
                            
                    function.headerWrite(iImg, "epoch", epo)
                    if errEpoch == "":
                        obsFiles = glob.glob("%s/obsdat/*" %(self.HOME))
                        for i in obsFiles:
                            if i.replace("%s/obsdat/" %(self.HOME),"").lower() == ob.lower():
                                obsOK = True
                        if obsOK:
                            if dt !="":
                                if ob !="":
                                    if tm != "":
                                        if ora != "":
                                            if odec != "":
                                                if function.JD(iImg, str(obs), str(obd), str(obt), str(ra), str(dec), str("epoch"), str(exp)):
                                                    if function.sideReal(self, iImg, ob, obd, obt):
                                                        if function.airmass(iImg, observatory, ra, dec, epok, "st", obt, obd, exp):
                                                            if function.phot(self, iImg, "%s/tmp/analyzed/" %(self.HOME), "%s/tmp/pc" %(self.HOME), expTime = exp, Filter = fil, centerBOX = int(cbo), annulus = int(ann), dannulus = int(dan), apertur = ape, zmag = zma, gain = gai):
                                                                if function.txDump("%s/tmp/analyzed/%s.mag.1"  %(self.HOME, ntpath.basename(iImg)), "%s/tmp/analyzed/%s"  %(self.HOME, ntpath.basename(iImg))):
                                                                    os.popen("rm %s/tmp/analyzed/%s.mag.1" %(self.HOME, ntpath.basename(iImg)))
                                                                    #os.popen("cat %s/tmp/analyzed/%s >> %s"  %(self.HOME, ntpath.basename(iImg), ofile))
                                                                    #os.popen("rm %s/tmp/analyzed/%s" %(self.HOME, ntpath.basename(iImg)))
                                                                    
                                                                    itExt = 0
                                                                    val = ""
                                                                    for ext in xrange(self.ui.listWidget_20.count()):
                                                                        itExt = itExt + 1
                                                                        fie = self.ui.listWidget_20.item(ext)
                                                                        fie = str(fie.text())
                                                                        val = "%s\t%s" %(val, function.headerRead(iImg, fie))
                                                                    v = open("%s/tmp/analyzed/%s"  %(self.HOME, ntpath.basename(iImg)), 'r')
                                                                    res = open(ofile, 'a')
                                                                    for r in v:
                                                                        r = r.replace("\n","")
                                                                        res.write("%s%s\n" %(r, val))
                                                                    res.close()
                                                                    v.close()
                                                                    os.popen("rm %s/tmp/analyzed/%s" %(self.HOME, ntpath.basename(iImg)))
                                                            else:
                                                                err = "PhotErr=%s, %s" %(err, ntpath.basename(iImg))
                                                        else:
                                                            errAir = "AiMaErr=%s, %s" %(errAir, ntpath.basename(iImg))
                                                    else:
                                                        errSid = "SiReErr%s, %s" %(errSid, ntpath.basename(iImg))
                                                else:
                                                    errJD = "JDErr%s, %s" %(errJD, ntpath.basename(iImg))
                                            else:
                                                errODEC = "EpoErr%s, %s" %(errODEC, ntpath.basename(iImg))
                                        else:
                                            errORA = "RAErr%s, %s" %(errORA, ntpath.basename(iImg))
                                    else:
                                        errTM = "No %s header=%s, %s" %(obt, errTM, ntpath.basename(iImg))
                                else:
                                    errOB = "No %s header=%s, %s" %(obs, errOB, ntpath.basename(iImg))
                            else:
                                errdt = "No %s header=%s, %s" %(obd, errdt, ntpath.basename(iImg))
                        else:
                            errOBSERVAT = "No obervat %s=%s, %s" %(ob, errOBSERVAT, ntpath.basename(iImg))
                        
                self.ui.progressBar_7.setProperty("value", math.ceil(100*(float(float(iIt)/float(self.ui.listWidget_13.count())))))
            
            self.ui.progressBar_6.setProperty("value", math.ceil(100*(float(float(it)/float(self.ui.listWidget_18.count())))))
            row = self.ui.listWidget_18.currentRow()
            if row < rows-1:
                self.ui.listWidget_18.setCurrentRow(row+1)
        if self.ui.groupBox_29.isChecked():
            os.popen("cp %s %s" %(ofile, os.path.dirname(iImg)))
    
    e=""
    if err != "":
        e = ("%s%s" %(e, err))
    if errAir != "":
        e = ("%s%s" %(e, errAir))
    if errSid != "":
        e = ("%s%s" %(e, errSid))
    if errJD != "":
        e = ("%s%s" %(e, errJD))
    if errODEC != "":
        e = ("%s%s" %(e, errODEC))
    if errORA != "":
        e = ("%s%s" %(e, errORA))
    if errTM != "":
        e = ("%s%s" %(e, errTM))
    if errOB != "":
        e = ("%s%s" %(e, errOB))
    if errdt != "":
        e = ("%s%s" %(e, errdt))
    if errOBSERVAT != "":
        e = ("%s%s" %(e, errOBSERVAT))
    if errEpoch != "":
        e = ("%s%s" %(e, errEpoch))
        
    if err != "" or errAir != "" or errSid != "" or errJD != "" or errODEC != "" or errORA != "" or errTM != "" or errOB != "" or errdt != "" or errOBSERVAT != "" or errEpoch != "":
        self.dispErr(e)
        
        
  def getSched(self):
    sFile = self.ui.listWidget_18.currentItem()
    sFile = "%s/tmp/sf%s" %(self.HOME, sFile.text())
    f = open(sFile, "r")
    itImg = -1
    itBia = -1
    itDar = -1
    itFla = -1
    itPhot = -1
    
    for x in xrange(self.ui.listWidget_13.count()):
        self.ui.listWidget_13.takeItem(0)
        
    for x in xrange(self.ui.listWidget_14.count()):
        self.ui.listWidget_14.takeItem(0)
        
    for x in xrange(self.ui.listWidget_15.count()):
        self.ui.listWidget_15.takeItem(0)
        
    for x in xrange(self.ui.listWidget_16.count()):
        self.ui.listWidget_16.takeItem(0)
        
    for x in xrange(self.ui.listWidget_17.count()):
        self.ui.listWidget_17.takeItem(0)
        
    self.ui.groupBox_26.setChecked(False)
    self.ui.groupBox_29.setChecked(False)
    self.ui.checkBox_8.setChecked(False)
    self.ui.checkBox_9.setChecked(False)
    self.ui.checkBox_10.setChecked(False)
    self.ui.checkBox_11.setChecked(False)
    
    for i in f:
        if i.startswith("isBia"):
            if i.split(" = ")[1].replace("\n","") == "True":
                self.ui.groupBox_26.setChecked(True)
                self.ui.checkBox_8.setChecked(True)
                self.unlockSBias()
            else:
                self.ui.checkBox_8.setChecked(False)
                self.unlockSBias()

        if i.startswith("isDar"):
            if i.split(" = ")[1].replace("\n","") == "True":
                self.ui.groupBox_26.setChecked(True)
                self.ui.checkBox_9.setChecked(True)
                self.unlockSDark()
            else:
                self.ui.checkBox_9.setChecked(False)
                self.unlockSDark()

        if i.startswith("isFla"):
            if i.split(" = ")[1].replace("\n","") == "True":
                self.ui.groupBox_26.setChecked(True)
                self.ui.checkBox_10.setChecked(True)
                self.unlockSFlat()
            else:
                self.ui.checkBox_10.setChecked(False)
                self.unlockSFlat()
                
        if i.startswith("isAli"):
            if i.split(" = ")[1].replace("\n","") == "True":
                self.ui.checkBox_11.setChecked(True)
            else:
                self.ui.checkBox_11.setChecked(False)

        if i.startswith("isPhot"):
            if i.split(" = ")[1].replace("\n","") == "True":
                self.ui.groupBox_29.setChecked(True)
            else:
                self.ui.groupBox_29.setChecked(False)
                
        if(i.startswith("img")):
            itImg = itImg +1
            item = QtGui.QListWidgetItem()
            self.ui.listWidget_13.addItem(item)
            item = self.ui.listWidget_13.item(itImg)
            item.setText(QtGui.QApplication.translate("Form", "%s" %(i.split(" = ")[1].replace("\n","")), None, QtGui.QApplication.UnicodeUTF8))

        if(i.startswith("bia")):
            itBia = itBia +1
            item = QtGui.QListWidgetItem()
            self.ui.listWidget_14.addItem(item)
            item = self.ui.listWidget_14.item(itBia)
            item.setText(QtGui.QApplication.translate("Form", "%s" %(i.split(" = ")[1].replace("\n","")), None, QtGui.QApplication.UnicodeUTF8))

        if(i.startswith("dar")):
            itDar = itDar +1
            item = QtGui.QListWidgetItem()
            self.ui.listWidget_15.addItem(item)
            item = self.ui.listWidget_15.item(itDar)
            item.setText(QtGui.QApplication.translate("Form", "%s" %(i.split(" = ")[1].replace("\n","")), None, QtGui.QApplication.UnicodeUTF8))

        if(i.startswith("fla")):
            itFla = itFla +1
            item = QtGui.QListWidgetItem()
            self.ui.listWidget_16.addItem(item)
            item = self.ui.listWidget_16.item(itFla)
            item.setText(QtGui.QApplication.translate("Form", "%s" %(i.split(" = ")[1].replace("\n","")), None, QtGui.QApplication.UnicodeUTF8))

        if(i.startswith("ref")):
            ind = i.split(" = ")[1].replace("\n","")
            print ind
            self.ui.listWidget_13.setCurrentRow(int(ind))

        if(i.startswith("coo")):
            for m in i.split(" = ")[1].replace("\n","").split(","):
                if m != "":
                    itPhot = itPhot +1
                    item = QtGui.QListWidgetItem()
                    self.ui.listWidget_17.addItem(item)
                    item = self.ui.listWidget_17.item(itPhot)
                    item.setText(QtGui.QApplication.translate("Form", "%s" %(m), None, QtGui.QApplication.UnicodeUTF8))

  def rmSched(self):
    for x in self.ui.listWidget_18.selectedItems():
        self.ui.listWidget_18.takeItem(self.ui.listWidget_18.row(x))
        os.popen("rm -rf %s/tmp/sf%s" %(self.HOME, x.text()))
        
  def uaSched(self, st):    
    if self.ui.listWidget_13.count() == 0:
        QtGui.QMessageBox.critical( self,  ("MYRaf Error"), ("No Image to process."))
    else:
        if (self.ui.groupBox_26.isChecked() and self.ui.checkBox_8.checkState() == QtCore.Qt.Checked) or (self.ui.groupBox_26.isChecked() and self.ui.checkBox_9.checkState() == QtCore.Qt.Checked) or (self.ui.groupBox_26.isChecked() and self.ui.checkBox_10.checkState() == QtCore.Qt.Checked):
            std = True
        elif self.ui.checkBox_11.checkState() == QtCore.Qt.Checked:
            std = True
        elif self.ui.groupBox_29.isChecked():
            std = True
        else:
            std = False
    
        if std:
            isBia = False
            isDar = False
            isFla = False
            isAli = False
            isPho = False
            
            fImg = []
            fBia = []
            fDar = []
            fFla = []
            fCoo = ""
            
            err = True
            
            if st == "add":
                ts = time.time()
                sFl = datetime.datetime.fromtimestamp(ts).strftime('%Y%m%d_%H%M%S')
            elif st == "upd":
                sFl = self.ui.listWidget_18.currentItem()
                sFl = sFl.text()
            
            
            if self.ui.groupBox_26.isChecked():
                if self.ui.checkBox_8.checkState() == QtCore.Qt.Checked:
                    if self.ui.listWidget_14.count() != 0:
                        isBia = True
                    else:
                        QtGui.QMessageBox.critical( self,  ("MYRaf Error"), ("Add some Bias images."))
                        err = False

                if self.ui.checkBox_9.checkState() == QtCore.Qt.Checked:
                    if self.ui.listWidget_15.count() != 0:
                        isDar = True
                    else:
                        QtGui.QMessageBox.critical( self,  ("MYRaf Error"), ("Add some Dark images."))
                        err = False

                if self.ui.checkBox_10.checkState() == QtCore.Qt.Checked:
                    if self.ui.listWidget_16.count() != 0:
                        isFla = True
                    else:
                        QtGui.QMessageBox.critical( self,  ("MYRaf Error"), ("Add some Flat images."))
                        err = False
                    
            if self.ui.checkBox_11.checkState() == QtCore.Qt.Checked:
                if self.ui.listWidget_13.currentItem() != None:
                    isAli = True
                else:
                    QtGui.QMessageBox.critical( self,  ("MYRaf Error"), ("Please select a reference image."))
                    err = False

            if self.ui.groupBox_29.isChecked():
                if self.ui.listWidget_17.count() != 0:
                    isPho = True
                else:
                    QtGui.QMessageBox.critical( self,  ("MYRaf Error"), ("Select coordinates for Photometry."))
                    err = False
            
            if err:
                f = open("%s/tmp/sf%s" %(self.HOME, sFl), "w")
                for i in xrange(self.ui.listWidget_13.count()):
                    img = self.ui.listWidget_13.item(i)
                    img = str(img.text())
                    fImg.append(img)
                
                if isBia:
                    f.write("isBia = True\n")
                    for i in xrange(self.ui.listWidget_14.count()):
                        img = self.ui.listWidget_14.item(i)
                        img = str(img.text())
                        fBia.append(img)
                else:
                    f.write("isBia = False\n")

                if isDar:
                    f.write("isDar = True\n")
                    for i in xrange(self.ui.listWidget_15.count()):
                        img = self.ui.listWidget_15.item(i)
                        img = str(img.text())
                        fDar.append(img)
                else:
                    f.write("isDar = False\n")

                if isFla:
                    f.write("isFla = True\n")
                    for i in xrange(self.ui.listWidget_16.count()):
                        img = self.ui.listWidget_16.item(i)
                        img = str(img.text())
                        fFla.append(img)
                else:
                    f.write("isFla = False\n")

                if isAli:
                    f.write("isAli = True\n")
                else:
                    f.write("isAli = False\n")

                if isPho:
                    f.write("isPhot = True\n")
                    for i in xrange(self.ui.listWidget_17.count()):
                        coo = self.ui.listWidget_17.item(i)
                        coo = str(coo.text())
                        fCoo = "%s,%s" %(fCoo, coo)
                else:
                    f.write("isPhot = False\n")
                    
                for i in fImg:
                    f.write("img = %s\n" %(i))
                    
                for i in fBia:
                    f.write("bia = %s\n" %(i))
                
                for i in fDar:
                    f.write("dar = %s\n" %(i))
                    
                for i in fFla:
                    f.write("fla = %s\n" %(i))
                    
                if isAli:
                    reImg = self.ui.listWidget_13.currentRow()
                    f.write("ref = %s\n" %(reImg))
                    
                if isPho:
                    f.write("coo = %s\n" %(fCoo))
                    
                    
                if st == "add":
                    it = self.ui.listWidget_18.count()
                    item = QtGui.QListWidgetItem()
                    self.ui.listWidget_18.addItem(item)
                    item = self.ui.listWidget_18.item(it)
                    item.setText(QtGui.QApplication.translate("Form", "%s" %(sFl), None, QtGui.QApplication.UnicodeUTF8))
                f.close()

        else:
            QtGui.QMessageBox.critical( self,  ("MYRaf Error"), ("Nothing to do."))
    
  def displayScheduler(self):
    img = self.ui.listWidget_13.currentItem()
    img = img.text()
    self.plotFdS.load(str(img))

# Chart point picker
  def onpick(self, event):
    thisline = event.artist
    xdata = thisline.get_xdata()
    ydata = thisline.get_ydata()
    ind = event.ind
    self.ui.label_9.setText("x=" + str(format(xdata[ind][0], '.3f')) + " y=" + str(format(ydata[ind][0], '.3f')))

  #Chart area clear
  def chartClear(self):
    data = []
    self.ui.disp_chart.canvas.axlc1.hold(False)
    self.ui.disp_chart.canvas.axlc1.plot(data)
    self.ui.disp_chart.canvas.axlc2.hold(False)
    self.ui.disp_chart.canvas.axlc2.plot(data)
    self.ui.disp_chart.canvas.draw()
     
#Choose Point Color of Chart###################################
  def choosePointCol(self):
      col = QtGui.QColorDialog.getColor()
      if col:
          if col.isValid():
              pcol = self.ui.label_55.setText(QtGui.QApplication.translate("Form", "%s" %(str(col.name())), None, QtGui.QApplication.UnicodeUTF8))
              return pcol

#other###################################
  def displayCalibLabel(self):
    imC = self.ui.listWidget.count()
    biC = self.ui.listWidget_2.count()
    daC = self.ui.listWidget_3.count()
    flC = self.ui.listWidget_4.count()
    self.ui.label_3.setText(QtGui.QApplication.translate("Form", "<b>%s</b> image(s) will be calibrated by using <b>%s</b> Bias(es), <b>%s</b> Dark(s) and <b>%s</b> Flat(s)." %(imC, biC, daC, flC), None, QtGui.QApplication.UnicodeUTF8))
    self.ui.label_4.setText(QtGui.QApplication.translate("Form", "<b>%s</b> image(s) will be calibrated by using <b>%s</b> Bias(es), <b>%s</b> Dark(s) and <b>%s</b> Flat(s)." %(imC, biC, daC, flC), None, QtGui.QApplication.UnicodeUTF8))
    self.ui.label_5.setText(QtGui.QApplication.translate("Form", "<b>%s</b> image(s) will be calibrated by using <b>%s</b> Bias(es), <b>%s</b> Dark(s) and <b>%s</b> Flat(s)." %(imC, biC, daC, flC), None, QtGui.QApplication.UnicodeUTF8))
    self.ui.label_6.setText(QtGui.QApplication.translate("Form", "<b>%s</b> image(s) will be calibrated by using <b>%s</b> Bias(es), <b>%s</b> Dark(s) and <b>%s</b> Flat(s)." %(imC, biC, daC, flC), None, QtGui.QApplication.UnicodeUTF8))
    

#Read Stars ID to Graph Tab###################################
  def readStars(self):
    filename = QtGui.QFileDialog.getOpenFileName(self ,"MYRaf Result File...","",("My Files (*.my *.myf)"))
    if filename:

        self.ui.label_43.setText(QtGui.QApplication.translate("Form", "File location: %s" %(filename), None, QtGui.QApplication.UnicodeUTF8))
        # counting stars in result file
        with open(filename) as resultFile:
            head=[resultFile.next() for x in xrange(3)]
        capStar, starCount = head[0].split(" = ")
        capStar, apertures = head[1].split(" = ")

        result_file = Table.read(filename,
                                 format='ascii.commented_header', header_start=-1)

        result_unique_by_keys = table.unique(result_file, keys='FILTER')

        result_unique_by_keys.colnames.index('FILTER')

        #clearing comboxBoxs
        self.ui.comboBox_11.clear()
        self.ui.comboBox_12.clear()
        self.ui.comboBox_13.clear()

        for ifilter in result_unique_by_keys['FILTER']:
            self.ui.comboBox_filter.addItem(str(ifilter))

        for i in range(1, int(starCount.replace("\n",""))+1):
            self.ui.comboBox_11.addItem(str(i))
            self.ui.comboBox_12.addItem(str(i))
            self.ui.comboBox_13.addItem(str(i))
        self.ui.comboBox_14.clear()
        #getting apertures
        apertures = apertures.replace("\n","")
        for aperture in apertures.split(","):
            self.ui.comboBox_14.addItem(aperture.replace("\n", ""))
        """except:
            QtGui.QMessageBox.critical( self,  ("MYRaf Error"), ("Error reading MYRaf <b>result file</b>!"))
            gui.logging(self, "--- %s - Error reading MYRaf result file!" %(datetime.datetime.utcnow()))    """

#Plot Chart#############################################
  def plotChart(self):
    # reading form
    if self.ui.label_43.text():
        #Checking result file
        if self.ui.lineEdit_19.text() and self.ui.lineEdit_20.text() and self.ui.lineEdit_21.text() and self.ui.label_55.text() and self.ui.comboBox_11.currentText() and self.ui.comboBox_12.currentText() and self.ui.comboBox_13.currentText() and self.ui.comboBox_14.currentText():
            varStarID = self.ui.comboBox_11.currentText()
            compStarID = self.ui.comboBox_12.currentText()
            checkStarID = self.ui.comboBox_13.currentText()
            ifilter = self.ui.comboBox_filter.currentText()
            apertureIndex = self.ui.comboBox_14.currentIndex() + 3
            legendName = self.ui.lineEdit_21.text().replace(" ",  "")
            t0 = float(self.ui.lineEdit_19.text())
            period = float(self.ui.lineEdit_20.text())
            
            # reading result file
            neednt,  filename = self.ui.label_43.text().split(":")
            filename = filename.replace("\n", "")
            filename = filename.replace(" ", "")
            variable_star = function.readResultFile(self, filename, varStarID, ifilter, apertureIndex)
            comp_star = function.readResultFile(self, filename, compStarID, ifilter, apertureIndex)
            check_star = function.readResultFile(self, filename, checkStarID, ifilter, apertureIndex)

            # aperture colomn names
            mag_column = variable_star.colnames[apertureIndex - 1]

            variable_star['diffMag'] = variable_star[mag_column].astype(float) - comp_star[mag_column].astype(float)
            variable_star['residuMag'] = comp_star[mag_column].astype(float) - check_star[mag_column].astype(float)

            variable_star['phase'] = ((variable_star['TIME'].astype(float) - t0) / period) - ((variable_star['TIME'].astype(float) - t0) / period).astype(int)
            print(variable_star['phase'])
            
            #Plot
            pointColor = self.ui.label_55.text()
            sp = str(self.ui.comboBox_15.currentText()).split(" ")[0]
            gui.PlotFunc(self, self.ui.disp_chart.canvas, variable_star['phase'], (variable_star['diffMag']*(-1)), variable_star['residuMag'], pointColor,  legendName, sp)
            head, tail = os.path.split(filename)
            self.ui.disp_chart.canvas.axlc1.title.set_fontsize(10)
            self.ui.disp_chart.canvas.axlc1.set_title(tail.replace(".my", " Light Curve"))
            self.ui.disp_chart.canvas.axlc2.set_xlabel("Phase", fontsize = 9)
            self.ui.disp_chart.canvas.axlc1.set_ylabel("V - C", fontsize = 9)
            self.ui.disp_chart.canvas.axlc2.set_ylabel("C - R", fontsize = 9)

            labels_x1 = self.ui.disp_chart.canvas.axlc1.get_xticklabels()
            labels_y1 = self.ui.disp_chart.canvas.axlc1.get_yticklabels()

            labels_x2 = self.ui.disp_chart.canvas.axlc2.get_xticklabels()
            labels_y2 = self.ui.disp_chart.canvas.axlc2.get_yticklabels()

            for xlabel in labels_x1:
                xlabel.set_fontsize(8)
                xlabel.set_color('b')
            for ylabel in labels_y1:
                ylabel.set_fontsize(8)
                ylabel.set_color('b')

            for xlabel in labels_x2:
                xlabel.set_fontsize(8)
                xlabel.set_color('b')
            for ylabel in labels_y2:
                ylabel.set_fontsize(8)
                ylabel.set_color('b')

            self.ui.disp_chart.canvas.draw()
        else:
            QtGui.QMessageBox.critical( self,  ("MYRaf Error"), ("Please <b>fill/select</b> the required informations!"))
            gui.logging(self, "--- %s - Please fill/select the required informations!" %(datetime.datetime.utcnow()))
    else:
        QtGui.QMessageBox.critical( self,  ("MYRaf Error"), ("Please select MYRaf <b>result file</b>!"))
        gui.logging(self, "--- %s - Please select MYRaf result file!" %(datetime.datetime.utcnow()))
########################################################

#Pohtometry#############################################
  def getObservat(self):
    fl = self.ui.listWidget_12.currentItem()
    fl = fl.text()
    
    self.ui.lineEdit_3.setText(QtGui.QApplication.translate("Form", "", None, QtGui.QApplication.UnicodeUTF8))
    self.ui.lineEdit_4.setText(QtGui.QApplication.translate("Form", "", None, QtGui.QApplication.UnicodeUTF8))
    self.ui.lineEdit_5.setText(QtGui.QApplication.translate("Form", "", None, QtGui.QApplication.UnicodeUTF8))
    self.ui.lineEdit_6.setText(QtGui.QApplication.translate("Form", "", None, QtGui.QApplication.UnicodeUTF8))
    self.ui.lineEdit_7.setText(QtGui.QApplication.translate("Form", "", None, QtGui.QApplication.UnicodeUTF8))
    self.ui.lineEdit_8.setText(QtGui.QApplication.translate("Form", "", None, QtGui.QApplication.UnicodeUTF8))
    self.ui.plainTextEdit.setPlainText(QtGui.QApplication.translate("Form", "", None, QtGui.QApplication.UnicodeUTF8))
    
    f = open("%s/obsdat/%s" %(self.HOME, str(fl)), "r")
    for i in f:
        ln = i.replace("\n","")
        if ln.replace(" ","").startswith("observatory"):
            self.ui.lineEdit_3.setText(QtGui.QApplication.translate("Form", str(ln).split(" = ")[1].replace("\"",""), None, QtGui.QApplication.UnicodeUTF8))

        if ln.replace("\t","").startswith("name"):
            self.ui.lineEdit_4.setText(QtGui.QApplication.translate("Form", str(ln).split(" = ")[1].replace("\"",""), None, QtGui.QApplication.UnicodeUTF8))

        if ln.replace("\t","").startswith("longitude"):
            self.ui.lineEdit_5.setText(QtGui.QApplication.translate("Form", str(ln).split(" = ")[1].replace("\"",""), None, QtGui.QApplication.UnicodeUTF8))

        if ln.replace("\t","").startswith("latitude"):
            self.ui.lineEdit_6.setText(QtGui.QApplication.translate("Form", str(ln).split(" = ")[1].replace("\"",""), None, QtGui.QApplication.UnicodeUTF8))

        if ln.replace("\t","").startswith("altitude"):
            self.ui.lineEdit_7.setText(QtGui.QApplication.translate("Form", str(ln).split(" = ")[1].replace("\"",""), None, QtGui.QApplication.UnicodeUTF8))

        if ln.replace("\t","").startswith("timezone"):
            self.ui.lineEdit_8.setText(QtGui.QApplication.translate("Form", str(ln).split(" = ")[1].replace("\"",""), None, QtGui.QApplication.UnicodeUTF8))
            
        if ln.replace("\t","").startswith("#"):
            self.ui.plainTextEdit.setPlainText(QtGui.QApplication.translate("Form", "%s" %(ln.replace("#","")), None, QtGui.QApplication.UnicodeUTF8))
            
  def rmObservatory(self):
    fl = self.ui.listWidget_12.currentItem()
    fl = fl.text()
    os.popen("rm -rf %s/obsdat/%s" %(self.HOME, str(fl)))
    c=self.ui.listWidget_12.count()
    for i in xrange(c):
        self.ui.listWidget_12.takeItem(0)
    
    it = self.ui.listWidget_12.count()-1
    for files in glob.glob("%s/obsdat/*" %(self.HOME)):
        fn = ntpath.basename(str(files))
        it = it+1
        item = QtGui.QListWidgetItem()
        self.ui.listWidget_12.addItem(item)
        item = self.ui.listWidget_12.item(it)
        item.setText(QtGui.QApplication.translate("Form", str(fn), None, QtGui.QApplication.UnicodeUTF8))
    self.ui.listWidget_12.sortItems()
    os.popen("cat %s/obsdat/* > /iraf/iraf/noao/lib/obsdb.dat" %(self.HOME))

  def addObservatory(self):
    fl = self.ui.listWidget_12.currentItem()
    
    observatory = self.ui.lineEdit_3.text()
    name = self.ui.lineEdit_4.text()
    longitude = self.ui.lineEdit_5.text()
    latitude = self.ui.lineEdit_6.text()
    altitude = self.ui.lineEdit_7.text()
    timeZone = self.ui.lineEdit_8.text()
    other = str(self.ui.plainTextEdit.toPlainText())
    
    f = open("%s/obsdat/%s" %(self.HOME, observatory), "w")
    f.write("#%s\n" %(other.replace("\n"," ")))
    f.write("observatory = \"%s\"\n" %(observatory))
    f.write("\tname = \"%s\"\n" %(name))
    f.write("\tlongitude = %s\n" %(longitude))
    f.write("\tlatitude = %s\n" %(latitude))
    f.write("\taltitude = %s\n" %(altitude))
    f.write("\ttimezone = %s\n" %(timeZone))
    f.close()
    
    c=self.ui.listWidget_12.count()
    for i in xrange(c):
        self.ui.listWidget_12.takeItem(0)
    
    it = self.ui.listWidget_12.count()-1
    for files in glob.glob("%s/obsdat/*" %(self.HOME)):
        fn = ntpath.basename(str(files))
        it = it+1
        item = QtGui.QListWidgetItem()
        self.ui.listWidget_12.addItem(item)
        item = self.ui.listWidget_12.item(it)
        item.setText(QtGui.QApplication.translate("Form", str(fn), None, QtGui.QApplication.UnicodeUTF8))
    self.ui.listWidget_12.sortItems()
    
    os.popen("cat %s/obsdat/* > /iraf/iraf/noao/lib/obsdb.dat" %(self.HOME))
        
########################################################
#Header Editor##########################################
  def getHeader(self):
    
    img = self.ui.listWidget_9.currentItem()
    img = img.text()
    h = iraf.hedit(img, "*", ".", Stdout=1)
    
    c=self.ui.listWidget_11.count()
    for i in xrange(c):
        self.ui.listWidget_11.takeItem(0)
        
    it = self.ui.listWidget_11.count()-1
    for i in h:
        it = it+1
        item = QtGui.QListWidgetItem()
        self.ui.listWidget_11.addItem(item)
        item = self.ui.listWidget_11.item(it)
        item.setText(QtGui.QApplication.translate("Form", i.split(",")[1], None, QtGui.QApplication.UnicodeUTF8))
        self.ui.comboBox.addItem(i.split(",")[1])
        
  def getVlueFromHeader(self):
    hed = self.ui.listWidget_11.currentItem()
    hed = hed.text()
    field, val = hed.split(" = ")
    self.ui.lineEdit.setText(QtGui.QApplication.translate("Form", str(field), None, QtGui.QApplication.UnicodeUTF8))
    self.ui.lineEdit_2.setText(QtGui.QApplication.translate("Form", str(val), None, QtGui.QApplication.UnicodeUTF8))
    
  def unlockGetHeaderFromValue(self):
    if self.ui.checkBox_5.checkState() == QtCore.Qt.Checked:
        self.ui.lineEdit_2.setEnabled(False)
        self.ui.comboBox.setEnabled(True)
    else:
        self.ui.lineEdit_2.setEnabled(True)
        self.ui.comboBox.setEnabled(False)

  def epochUnlock(self):
    if self.ui.checkBox_4.checkState() == QtCore.Qt.Checked:
        self.ui.lineEdit_25.setEnabled(False)
    else:
        self.ui.lineEdit_25.setEnabled(True)
        
  def timeobsUnlock(self):
    if self.ui.checkBox_12.checkState() == QtCore.Qt.Checked:
        self.ui.lineEdit_17.setEnabled(False)
    else:
        self.ui.lineEdit_17.setEnabled(True)
        
  def unlockSBias(self):
    if self.ui.checkBox_8.checkState() == QtCore.Qt.Checked:
        self.ui.tabWidget_8.setTabEnabled(1,True)
    else:
        self.ui.tabWidget_8.setTabEnabled(1,False)

  def unlockSDark(self):
    if self.ui.checkBox_9.checkState() == QtCore.Qt.Checked:
        self.ui.tabWidget_8.setTabEnabled(2,True)
    else:
        self.ui.tabWidget_8.setTabEnabled(2,False)

  def unlockSFlat(self):
    if self.ui.checkBox_10.checkState() == QtCore.Qt.Checked:
        self.ui.tabWidget_8.setTabEnabled(3,True)
    else:
        self.ui.tabWidget_8.setTabEnabled(3,False)


  def goHeaderAdd(self):
    if self.ui.listWidget_9.count() != 0:
        f = self.ui.lineEdit.text()
        if str(f).strip():
            headErr = ""
            it = 0
            for x in xrange(self.ui.listWidget_9.count()):
                it = it + 1
                img = self.ui.listWidget_9.item(x)
                img = str(img.text())
                field = self.ui.lineEdit.text()
                field = str(field).strip()
                    
                if self.ui.checkBox_5.checkState() != QtCore.Qt.Checked:
                    val = self.ui.lineEdit_2.text()
                else:
                    h = self.ui.comboBox.currentText()
                    selectedField = h.split(" = ")[0]
                    val = str("'(@\"%s\")'" %selectedField)
                
                self.ui.progressBar_4.setProperty("value", math.ceil(100*(float(float(it)/float(self.ui.listWidget_9.count())))))
                self.ui.label_41.setText(QtGui.QApplication.translate("Form", "Header: %s." %(ntpath.basename(str(img))), None, QtGui.QApplication.UnicodeUTF8))
                    
                if not function.headerWrite(img, field, val):
                    headErr = "%s\n%s" %(headErr, ntpath.basename(str(img)))
                        
            if self.ui.listWidget_9.currentIndex():
                self.getHeader()
            if headErr != "" :
                QtGui.QMessageBox.critical( self,  ("MYRaf Error"), ("Due to an error <b>hedit</b> can not handle this job for images below\n%s" %(headErr)))
        else:
            QtGui.QMessageBox.critical( self,  ("MYRaf Error"), ("Please fill the \"Field\" section!"))         
    else:
        QtGui.QMessageBox.critical( self,  ("MYRaf Error"), ("Please select some <b>images</b>."))
    
  def goHeaderDel(self):
    if self.ui.listWidget_9.count() != 0:
        f = self.ui.listWidget_11.currentItem()
        f = f.text()
        field = f.split(" = ")[0]
        heErr = ""
        it = 0
        for x in xrange(self.ui.listWidget_9.count()):
            it = it + 1
            img = self.ui.listWidget_9.item(x)
            img = str(img.text())
            if function.headerDel(img, field):
                self.getHeader()
            else:
                heErr = "%s\n%s" %(heErr, ntpath.basename(str(img)))                    
                
            self.ui.progressBar_4.setProperty("value", math.ceil(100*(float(float(it)/float(self.ui.listWidget_9.count())))))
            self.ui.label_41.setText(QtGui.QApplication.translate("Form", "Header: %s." %(ntpath.basename(str(img))), None, QtGui.QApplication.UnicodeUTF8))

        if heErr != "":
            QtGui.QMessageBox.critical( self,  ("MYRaf Error"), ("Due to an error <b>hedit</b> can not handle this job for images below\n%s" %(heErr)))
            
    else:
        QtGui.QMessageBox.critical( self,  ("MYRaf Error"), ("Please select some <b>images</b>."))
########################################################
#Pohtometry#############################################
  def displayPhot(self):

    img = self.ui.listWidget_7.currentItem()
    img = img.text()
    self.plotFdP.load(str(img))

  def coorDel(self):
    gui.rm(self, self.ui.listWidget_8)
        
  def displayCoords(self):
    if self.ui.tabWidget.currentIndex() == 2:
        if self.ui.listWidget_8.count() != 0:
            self.displayPhot()
            lNumber = 0 
            for x in self.ui.listWidget_8.selectedItems():
                lNumber = lNumber +1
                coo = str(x.text())
                print coo
                x, y = coo.split("-")
                mean = 0
                ap = str(self.ui.lineEdit_15.text())
                for ape in ap.split(","):
                    mean = mean + int(ape)
                Aperture = mean/len(ap.split(","))
                Aperture = mean/len(ap.split(","))
                circAperture = Circle((Aperture, Aperture), Aperture, edgecolor="#00FF00", facecolor="none")                
                circAnnulus = Circle((self.ui.doubleSpinBox_2.value(), self.ui.doubleSpinBox_2.value()), self.ui.doubleSpinBox_2.value(), edgecolor="#00FFFF", facecolor="none")
                circDannulus = Circle((self.ui.doubleSpinBox_2.value() + self.ui.doubleSpinBox.value(), self.ui.doubleSpinBox_2.value() + self.ui.doubleSpinBox.value()), self.ui.doubleSpinBox_2.value() + self.ui.doubleSpinBox.value(), edgecolor="red", facecolor="none")
                self.ui.dispPhoto.canvas.fig.gca().add_artist(circAnnulus)
                self.ui.dispPhoto.canvas.fig.gca().add_artist(circDannulus)
                self.ui.dispPhoto.canvas.fig.gca().add_artist(circAperture)
                circAperture.center = x, y
                circAnnulus.center = x, y
                circDannulus.center = x, y
                self.ui.dispPhoto.canvas.fig.gca().annotate(lNumber, xy = (x, y), xytext=(int(Aperture/3),int(Aperture/3)), textcoords='offset points', color = "blue", fontsize = 10)
            self.ui.dispPhoto.canvas.draw()
    #hela vela vel vela
    elif self.ui.tabWidget.currentIndex() == 5:
        if self.ui.listWidget_17.count() != 0:
            self.displayScheduler()
            lNumber = 0 
            for x in xrange(self.ui.listWidget_17.count()):
                lNumber = lNumber +1
                coo = self.ui.listWidget_17.item(x)
                coo = str(coo.text())
                print coo
                x, y = coo.split("-")
                mean = 0
                ap = str(self.ui.lineEdit_15.text())
                for ape in ap.split(","):
                    mean = mean + int(ape)
                Aperture = mean/len(ap.split(","))
                Aperture = mean/len(ap.split(","))
                circAperture = Circle((Aperture, Aperture), Aperture, edgecolor="#00FF00", facecolor="none")                
                circAnnulus = Circle((Aperture + self.ui.doubleSpinBox_2.value(), Aperture + self.ui.doubleSpinBox_2.value()), Aperture + self.ui.doubleSpinBox_2.value(), edgecolor="#00FFFF", facecolor="none")
                circDannulus = Circle((Aperture + self.ui.doubleSpinBox_2.value() + self.ui.doubleSpinBox.value(), Aperture + self.ui.doubleSpinBox_2.value() + self.ui.doubleSpinBox.value()), Aperture + self.ui.doubleSpinBox_2.value() + self.ui.doubleSpinBox.value(), edgecolor="red", facecolor="none")
                self.ui.dispSched.canvas.ax.add_artist(circAnnulus)
                self.ui.dispSched.canvas.ax.add_artist(circDannulus)
                self.ui.dispSched.canvas.ax.add_artist(circAperture)
                circAperture.center = x, y
                circAnnulus.center = x, y
                circDannulus.center = x, y
                self.ui.dispSched.canvas.ax.annotate(lNumber, xy = (x, y), xytext=(int(Aperture/3),int(Aperture/3)), textcoords='offset points', color = "blue", fontsize = 10)
            self.ui.dispSched.canvas.draw()
            
  def goPhot(self):
    if self.ui.listWidget_7.count() != 0:
        if self.ui.listWidget_8.count() != 0:
            gui.logging(self, "-- %s - phot started." %(datetime.datetime.utcnow()))

            f = open("%s/tmp/pc" %(self.HOME), "w")
            for x in xrange(self.ui.listWidget_8.count()):
                coo = self.ui.listWidget_8.item(x)
                coo = str(coo.text())
                coo = coo.replace("-", " ")
                f.write("%s\n" %(coo))
            f.close()
            
            exp = self.ui.lineEdit_13.text()
            fil = self.ui.lineEdit_14.text()
            ann = self.ui.doubleSpinBox_2.value()
            dan = self.ui.doubleSpinBox.value()
            cbo = self.ui.doubleSpinBox_3.value()
            ape = self.ui.lineEdit_15.text()
            zma = self.ui.lineEdit_16.text()
            obs = self.ui.lineEdit_18.text()
            obd = self.ui.lineEdit_24.text()
            obt = self.ui.lineEdit_17.text()
            ra = self.ui.lineEdit_22.text()
            dec = self.ui.lineEdit_23.text()
            epok = self.ui.lineEdit_25.text()
            gai = self.ui.lineEdit_26.text()
            
            apert = self.ui.lineEdit_15.text()
            staCount = self.ui.listWidget_8.count()
            
            ofile = QtGui.QFileDialog.getSaveFileName( self, 'Save MYRaf file', 'res.my', 'my (*.my)')
            itExt = 0
            extFie = ""
            for ext in xrange(self.ui.listWidget_20.count()):
                itExt = itExt + 1
                fie = self.ui.listWidget_20.item(ext)
                fie = str(fie.text())
                extFie = "%s\t%s" %(extFie, fie)
                
            if ofile != "":
                if os.path.exists(ofile):
                    os.popen("rm %s" %(ofile))
                f = open(ofile, "w")
                f.write("# STAR = %s\n" %(str(staCount)))
                f.write("# APERTURE = %s\n" %(str(apert)))
                f.write("# DO NOT EDIT PARAMETRES ABOVE. You can add comments starts with '#' below ths line.\n")
                f.write("# If you don't have any experience before, DO NOT EDIT THIS FILE!\n")
                f.write("# id\tTIME\tMAG%s\tMERR%s\tAIRMASS%s\n" %(self.ui.lineEdit_15.text().replace(",","\tMAG"), self.ui.lineEdit_15.text().replace(",","\tMERR"), extFie))
                f.close()
                it = 0
                err = ""
                errJD = ""
                errSid = ""
                errAir = ""
                errTM = ""
                errOB = ""
                errORA = ""
                errODEC = ""
                errdt = ""
                errOBSERVAT = ""
                errEpoch = ""
                obsOK = False
                for x in xrange(self.ui.listWidget_7.count()):
                    it = it + 1
                    img = self.ui.listWidget_7.item(x)
                    img = str(img.text())
                    
                    dt = function.headerRead(img, self.ui.lineEdit_24.text())
                    if "T" in dt:
                        dat, tm = dt.split("T")
                    else:
                        dat = function.headerRead(img, self.ui.lineEdit_24.text())
                        
                    function.headerWrite(img, "mydt-obs", dat)
                    
                    if self.ui.checkBox_12.checkState() == QtCore.Qt.Checked:
                        if "T" in dt:
                            dat, tm = dt.split("T")
                            function.headerWrite(img, "mytm-obs", tm)
                            function.headerWrite(img, "mytm-obs", tm)
                        else:
                            QtGui.QMessageBox.critical( self,  ("MYRaf Error"), ("Please provide YYYY-MM-DDTHH:MM:SS formatted keyword!"))
                            break
                            
                    else:
                        function.headerWrite(img, "mytm-obs", function.headerRead(img, self.ui.lineEdit_17.text()))
                        function.headerWrite(img, "mytm-obs", function.headerRead(img, self.ui.lineEdit_17.text()))

                    tm = function.headerRead(img, "mytm-obs")
                    ob = function.headerRead(img, obs)
                    ora = function.headerRead(img, ra)
                    odec = function.headerRead(img, dec)
                    if self.ui.checkBox_4.checkState() == QtCore.Qt.Checked:
                        epo = function.epoch(img, "mydt-obs", "mytm-obs")
                        if epo == False:
                            errEpoch = "%s\n%s" %(errEpoch, img)
                        else:
                            function.headerWrite(img, "epoch", epo)
                    
                    if errEpoch == "":
                        obsFiles = glob.glob("%s/obsdat/*" %(self.HOME))
                        for i in obsFiles:
                            if i.replace("%s/obsdat/" %(self.HOME),"").lower() == ob.lower():
                                obsOK = True
                        if obsOK:
                            if dt !="":
                                if ob !="":
                                    if tm != "":
                                        if ora != "":
                                            if odec != "":
                                                if function.JD(img, str(obs), str("mydt-obs"), str("mytm-obs"), str(ra), str(dec), str(epok), str(exp)):
                                                    if function.sideReal(self, img, ob):
                                                        if function.airmass(img, obs, ra, dec, epok, "st", exp):
                                                            if function.phot(self, img, "%s/tmp/analyzed/" %(self.HOME), "%s/tmp/pc" %(self.HOME), expTime = exp, Filter = fil, centerBOX = cbo, annulus = ann, dannulus = dan, apertur = ape, zmag = zma, gain = gai):
                                                                if function.txDump("%s/tmp/analyzed/%s.mag.1"  %(self.HOME, ntpath.basename(img)), "%s/tmp/analyzed/%s"  %(self.HOME, ntpath.basename(img))):
                                                                    #os.popen("echo '#ap=%s'"%(str()))
                                                                    itExt = 0
                                                                    val = ""
                                                                    for ext in xrange(self.ui.listWidget_20.count()):
                                                                        itExt = itExt + 1
                                                                        fie = self.ui.listWidget_20.item(ext)
                                                                        fie = str(fie.text())
                                                                        val = "%s\t%s" %(val, function.headerRead(img, fie))
                                                                    v = open("%s/tmp/analyzed/%s"  %(self.HOME, ntpath.basename(img)), 'r')
                                                                    res = open(ofile, 'a')
                                                                    for r in v:
                                                                        r = r.replace("\n","")
                                                                        res.write("%s%s\n" %(r, val))
                                                                    res.close()
                                                                    v.close()
                                                                    os.popen("rm %s/tmp/analyzed/%s" %(self.HOME, ntpath.basename(img)))
                                                            else:
                                                                err = "%s\n%s" %(err, ntpath.basename(img))
                                                        else:
                                                            errAir = "%s\n%s" %(errAir, ntpath.basename(img))
                                                    else:
                                                        errSid = "%s\n%s" %(errSid, ntpath.basename(img))
                                                else:
                                                    errJD = "%s\n%s" %(errJD, ntpath.basename(img))
                                            else:
                                                errODEC = "%s\n%s" %(errODEC, ntpath.basename(img))
                                        else:
                                            errORA = "%s\n%s" %(errORA, ntpath.basename(img))
                                    else:
                                        errTM = "%s\n%s" %(errTM, ntpath.basename(img))
                                else:
                                    errOB = "%s\n%s" %(errOB, ntpath.basename(img))
                            else:
                                errdt = "%s\n%s" %(errdt, ntpath.basename(img))
                        else:
                            errOBSERVAT = "%s\n%s" %(errOBSERVAT, ntpath.basename(img))
                    self.ui.progressBar_5.setProperty("value", math.ceil(100*(float(float(it)/float(self.ui.listWidget_7.count())))))
                    self.ui.label_14.setText(QtGui.QApplication.translate("Form", "Photometry: %s." %(ntpath.basename(str(img))), None, QtGui.QApplication.UnicodeUTF8))
                if errOBSERVAT != "":
                    errOBSERVAT = "Can't find Observatory in obsdb for images below:\nYou can add your observatory using editor.\n%s" %(errOBSERVAT)
                    self.dispErr(errOBSERVAT)
                    
                if errTM != "":
                    errTM = "No %s header on images below:\n%s" %(obt, errTM)
                    self.dispErr(errTM)
                if errEpoch != "":
                    errEpoch = "Time format is not correct for images below:\nYou can change value from header or choose manual epoch from setting tab.\n%s" %(errEpoch)
                    self.dispErr(errEpoch)
                if errOB != "":
                    errOB = "No %s header on images below:\n%s" %(obs, errOB)
                    self.dispErr(errOB)
                if errORA != "":
                    errORA = "No %s header on images below:\n%s" %(ra, errORA)
                    self.dispErr(errORA)
                if errODEC != "":
                    errODEC = "No %s header on images below:\n%s" %(dec, errODEC)
                    self.dispErr(errODEC)
                if errdt != "":
                    errdt = "No %s header on images below:\n%s" %(obd, errdt)
                    self.dispErr(errdt)
                if errJD != "":
                    errJD = "Due to an error setjd can not handle images below:\n%s." %(errJD)
                    self.dispErr(errJD)
                if errSid != "":
                    errSid = "Due to an error can not calculate sidereal time for images below:\n%s." %(errSid)
                    self.dispErr(errSid)
                if errAir != "":
                    errAir = "Due to an error setairmass can not handle images below:\n%s." %(errAir)
                    self.dispErr(errAir)
                if err != "":
                    err = "Due to an error phot can not handle images below:\n%s." %(err)
                    self.dispErr(err)
                
        else:
            QtGui.QMessageBox.critical( self,  ("MYRaf Error"), ("Please select some <b>sources</b>."))
    else:
        QtGui.QMessageBox.critical( self,  ("MYRaf Error"), ("No <b>image</b> for Photometry."))

    os.system("rm -rf $HOME/.MYRaf2/tmp/*")
    os.system("rm -rf $HOME/.MYRaf2/alipy_visu")
    os.system("rm -rf $HOME/.MYRaf2/alipy_out")
    os.system("mkdir -p $HOME/.MYRaf2/tmp/alipy/")
    os.system("mkdir -p $HOME/.MYRaf2/tmp/analyzed/")
        
########################################################
#Manual Align############################################
  def displayManAlign(self):
    img = self.ui.listWidget_6.currentItem()
    img = img.text()
    self.plotFdM.load(str(img))
    c = function.headerRead(img, "MYRAFCOR")
    print c
    coors = function.headerRead(img, "MYRafCor")
    self.ui.label_11.setText(QtGui.QApplication.translate("Form", "%s" %(coors), None, QtGui.QApplication.UnicodeUTF8))

  def goManAlign(self):
    if self.ui.listWidget_6.count() != 0:
        if self.ui.listWidget_6.currentItem() != None:
            img = self.ui.listWidget_6.currentItem()
            img = img.text()
            coorRef = function.headerRead(img, "MYRafCor").split("-")
            if str(coorRef) != "['']":
                xref = coorRef[0]
                yref = coorRef[1]
                odir = QtGui.QFileDialog.getExistingDirectory( self, 'Select Directory to Save Aligned File(s)')
                if os.path.exists(odir):
                    it = 0
                    err = ""
                    for x in xrange(self.ui.listWidget_6.count()):
                        it = it + 1
                        img = self.ui.listWidget_6.item(x)
                        img = str(img.text())
                        self.ui.label_10.setText(QtGui.QApplication.translate("Form", "Aligning: %s." %(ntpath.basename(str(img))), None, QtGui.QApplication.UnicodeUTF8))
                        ofile = "%s/%s" %(odir, ntpath.basename(str(img)))
                        coorImg = function.headerRead(img, "MYRafCor").split("-")
                        if str(coorImg) != "['']":
                            ximg = coorImg[0]
                            yimg = coorImg[1]
                            x = float(xref) - float(ximg)
                            y = float(yref) - float(yimg)
                            print x, y
                            if not function.manAlign(img, x, y, ofile):
                                err = "%s, %s" %(err, ntpath.basename(str(img)))
                                gui.logging(self, "--- %s - imshift failed." %(datetime.datetime.utcnow()))
                        self.ui.label_10.setText(QtGui.QApplication.translate("Form", "Aligning:%s" %(ntpath.basename(img)), None, QtGui.QApplication.UnicodeUTF8))
                        self.ui.progressBar_3.setProperty("value", math.ceil(100*(float(float(it)/float(self.ui.listWidget_6.count())))))
                    if err!="":
                        err = "Due to an error imshift can not align images below\n%s." %(err)
                        self.dispErr(err)
            else:
                QtGui.QMessageBox.critical( self,  ("MYRaf Error"), ("Please select coordinates for reference image."))
        else:
            QtGui.QMessageBox.critical( self,  ("MYRaf Error"), ("Please select a reference image first."))
    else:
        QtGui.QMessageBox.critical( self,  ("MYRaf Error"), ("Please add some <b>Image</b> files."))
    
########################################################
  def mouseClick(self, event):
    if self.ui.tabWidget.currentIndex() == 1:
        if self.ui.tabWidget_3.currentIndex() == 1:
            if self.ui.checkBox_6.isChecked():
                if event.ydata != None and event.xdata != None:
                    rows = self.ui.listWidget_6.count()
                    row = self.ui.listWidget_6.currentRow()
                    img = self.ui.listWidget_6.currentItem()
                    img = img.text()
                    height = function.headerRead(img, "i_naxis2")
                    x = event.xdata
                    y = event.ydata
                    function.headerWrite(img, "MYRafCor", "%s-%s" %(str(x), str(y)))
                    if row < rows-1:
                        self.ui.listWidget_6.setCurrentRow(row+1)
                    else:
                        self.ui.listWidget_6.setCurrentRow(0)
                    self.displayManAlign()
    elif self.ui.tabWidget.currentIndex() == 2:
        if self.ui.checkBox_7.isChecked():      
            #print event.ydata
            if event.ydata != None and event.xdata != None:
                self.ui.listWidget_8.addItem(str(format(event.xdata, '.4f')) + " - " + str(format(event.ydata, '.4f')))
    elif self.ui.tabWidget.currentIndex() == 5:
        if self.ui.groupBox_29.isChecked(): 
            #print event.ydata
            if event.ydata != None and event.xdata != None:
                self.ui.listWidget_17.addItem(str(format(event.xdata, '.4f')) + " - " + str(format(event.ydata, '.4f')))
                self.displayCoords()

#Auto Align#############################################
  def findStars(self):
    if self.ui.tabWidget.currentIndex() == 2:
        if self.ui.listWidget_7.currentItem():
            if self.ui.doubleSpinBox_5.value() > self.ui.doubleSpinBox_6.value():
                QtGui.QMessageBox.critical( self,  ("MYRaf Error"), ("<b>Min FWHM</b> can not be bigger than <b>Max FWHM</b>"))
            else:
                img = self.ui.listWidget_7.currentItem()
                img = str(img.text())
                
                minFWHM = self.ui.doubleSpinBox_5.value()
                maxFWHM = self.ui.doubleSpinBox_6.value()
                FluxRadi = self.ui.doubleSpinBox_4.value()
                maxStar = int(self.ui.doubleSpinBox_7.value())                
                
                sex = runSex(img)
                stars = sex.run(FluxRadi, minFWHM, maxFWHM, maxStar)
                
                c=self.ui.listWidget_8.count()
                for i in xrange(c):
                    self.ui.listWidget_8.takeItem(0)
                
                it = -1
                for x in stars:
                    it = it+1
                    coo = "%s-%s" %(x[0],x[1])
                    item = QtGui.QListWidgetItem()
                    self.ui.listWidget_8.addItem(item)
                    item = self.ui.listWidget_8.item(it)
                    item.setText(QtGui.QApplication.translate("Form", coo, None, QtGui.QApplication.UnicodeUTF8))

  def displayAutAlign(self):
    gui.logging(self, "-- %s - image conversion started." %(datetime.datetime.utcnow()))
    img = self.ui.listWidget_5.currentItem()
    img = img.text()
    self.plotFdA.load(str(img))

  def goAutAlign(self):
    if self.ui.listWidget_5.count() != 0:
        if self.ui.listWidget_5.currentItem() != None:
            gui.logging(self, "-- %s - AutoAlign started." %(datetime.datetime.utcnow()))
            ref = self.ui.listWidget_5.currentItem()
            ref = str(ref.text())
            it = 0
            odir = QtGui.QFileDialog.getExistingDirectory( self, 'Select Directory to Save Aligned File(s)')
            if os.path.exists(odir):
                aliErr = ""
                for x in xrange(self.ui.listWidget_5.count()):
                    it = it + 1
                    img = self.ui.listWidget_5.item(x)
                    img = str(img.text())
                    self.ui.label_7.setText(QtGui.QApplication.translate("Form", "Aligning: %s" %(ntpath.basename(str(img))), None, QtGui.QApplication.UnicodeUTF8))
                    if not function.autoAlign(self, img, ref, odir):
                        aliErr = "%s, %s" %(aliErr, ntpath.basename(str(img)))
                        gui.logging(self, "--- %s - alipy failed." %(datetime.datetime.utcnow()))
                    self.ui.progressBar_2.setProperty("value", math.ceil(100*(float(float(it)/float(self.ui.listWidget_5.count())))))
                    os.popen("rm -rf %s/alipy_cats/ %s/alipy_out/" %(self.HOME, self.HOME))
                gui.logging(self, "-- %s - AutoAlign finished aligning." %(datetime.datetime.utcnow()))
                if aliErr != "":
                    QtGui.QMessageBox.critical( self,  ("MYRaf Error"), ("Due to an error <b>alipy</b> can not align images below\n%s") %(aliErr))

        else:
            QtGui.QMessageBox.critical( self,  ("MYRaf Error"), ("Please select a <b>reference image</b> first."))
    else:
        QtGui.QMessageBox.critical( self,  ("MYRaf Error"), ("Please add some <b>Image</b> files."))
########################################################
#Calibration############################################
  def calib(self):
    if self.ui.listWidget.count() != 0:
        if self.ui.checkBox.checkState() != QtCore.Qt.Checked and self.ui.checkBox_2.checkState() != QtCore.Qt.Checked and self.ui.checkBox_3.checkState() != QtCore.Qt.Checked:
            QtGui.QMessageBox.critical( self,  ("MYRaf Error"), ("Nothing to do!"))
        else:
            gui.logging(self, "-- %s - Calibration started." %(datetime.datetime.utcnow()))
            go = True
            
            os.popen("rm -rf %s/tmp/dark.fits %s/tmp/dark.fits %s/tmp/flat_*.fits" %(self.HOME, self.HOME, self.HOME))
                
            b, d, f="","",""
            if self.ui.checkBox.checkState() == QtCore.Qt.Checked and self.ui.listWidget_2.count() == 0: b = "Bias\n"
            if self.ui.checkBox_2.checkState() == QtCore.Qt.Checked and self.ui.listWidget_3.count() == 0: d = "Dark\n"
            if self.ui.checkBox_3.checkState() == QtCore.Qt.Checked and self.ui.listWidget_4.count() == 0: f = "Flat\n"
            
            sname = self.ui.lineEdit_14.text()
            
            if b != "" or d != "" or f != "":
                QtGui.QMessageBox.critical( self,  ("MYRaf Error"), ("Add file(s) to\n%s%s%s" %(b,d,f)))
            else:
                print "basla"
                zeroFilePath, darkFilePath, flatFilePath = "", "", ""
                
                if self.ui.checkBox.checkState() == QtCore.Qt.Checked:
                    self.ui.label.setText(QtGui.QApplication.translate("Form", "Creating Masster Bias.", None, QtGui.QApplication.UnicodeUTF8))
                    gui.logging(self, "--- %s - zerocombine started for calibration." %(datetime.datetime.utcnow()))
                    lst = gui.lisFromLW(self, self.ui.listWidget_2)
                    gui.list2file(lst, "%s/tmp/zeroLST" %(self.HOME))
                    comb = self.ui.comboBox_4.currentText()
                    rejb = self.ui.comboBox_5.currentText()
                    ctyb = self.ui.lineEdit_10.text()
                    if not function.zeroCombine("%s/tmp/zeroLST" %(self.HOME), "%s/tmp/zero.fits" %(self.HOME), com=comb, rej=rejb, cty=ctyb):
                        QtGui.QMessageBox.critical( self,  ("MYRaf Error"), ("Due to an error <b>zerocombine</b> can not handle this job."))
                        gui.logging(self, "--- %s - zerocombine failed." %(datetime.datetime.utcnow()))
                    else:
                        gui.logging(self, "--- %s - zerocombine succeed." %(datetime.datetime.utcnow()))
                        zeroFilePath = "%s/tmp/zero.fits"  %(self.HOME)
                    os.popen("rm -rf %s/tmp/zeroLST"  %(self.HOME))
                
                if self.ui.checkBox_2.checkState() == QtCore.Qt.Checked:
                    self.ui.label.setText(QtGui.QApplication.translate("Form", "Creating Masster Dark.", None, QtGui.QApplication.UnicodeUTF8))
                    gui.logging(self, "--- %s - darkcombine started for calibration." %(datetime.datetime.utcnow()))
                    lst = gui.lisFromLW(self, self.ui.listWidget_3)
                    gui.list2file(lst, "%s/tmp/darkLST" %(self.HOME))
                    comd = self.ui.comboBox_4.currentText()
                    rejd = self.ui.comboBox_5.currentText()
                    scld = self.ui.comboBox_8.currentText()
                    ctyd = self.ui.lineEdit_10.text()
                    if not function.darkCombine("%s/tmp/darkLST" %(self.HOME), "%s/tmp/dark.fits" %(self.HOME), com=comd, rej=rejd, cty=ctyd, scl=scld):
                        QtGui.QMessageBox.critical( self,  ("MYRaf Error"), ("Due to an error <b>darkcombine</b> can not handle this job."))
                        gui.logging(self, "--- %s - darkcombine failed." %(datetime.datetime.utcnow()))
                    else:
                        gui.logging(self, "--- %s - darkcombine succeed." %(datetime.datetime.utcnow()))
                        darkFilePath = "%s/tmp/dark.fits" %(self.HOME)
                    os.popen("rm -rf %s/tmp/darkLST" %(self.HOME))
            
                if self.ui.checkBox_3.checkState() == QtCore.Qt.Checked:
                    self.ui.label.setText(QtGui.QApplication.translate("Form", "Creating Masster Flat.", None, QtGui.QApplication.UnicodeUTF8))
                    gui.logging(self, "--- %s - flatcombine started for calibration." %(datetime.datetime.utcnow()))
                    lst = gui.lisFromLW(self, self.ui.listWidget_4)
                    gui.list2file(lst, "%s/tmp/flatLST" %(self.HOME))
                    comf = self.ui.comboBox_6.currentText()
                    rejf = self.ui.comboBox_7.currentText()
                    subf = self.ui.comboBox_10.currentText()
                    ctyf = self.ui.lineEdit_11.text()
                    
                    f = open("%s/tmp/flatLST" %(self.HOME), "r")
                    it = 0
                    
                    for i in f:
                        fn = i.replace("\n","")
                        if function.headerRead(fn,sname) == "":
                            it = it + 1
                    f.close()
                    
                    if subf == "yes" and it != 0:
                        QtGui.QMessageBox.critical( self,  ("MYRaf Error"), ("Subset classification is enabled but one or more images have no <b>%s</b> field in header.\nAdd <b>%s</b> field to headers." %(sname, sname)))
                        go = False
                    else:
                        function.headerWrite("@%s/tmp/flatLST" %(self.HOME), "subset", str("'(@\"%s\")'" %sname))
                        if not function.flatCombine("%s/tmp/flatLST" %(self.HOME), "%s/tmp" %(self.HOME), com=comf, rej=rejf, cty=ctyf, sub=subf):
                            QtGui.QMessageBox.critical( self,  ("MYRaf Error"), ("Due to an error <b>flatcombine</b> can not handle this job."))
                            gui.logging(self, "--- %s - flatcombine failed." %(datetime.datetime.utcnow()))
                        else:
                            gui.logging(self, "--- %s - flatcombine succeed." %(datetime.datetime.utcnow()))
                            flatFilePath = "%s/tmp/flat_*.fits" %(self.HOME)
                        os.popen("rm -rf %s/tmp/flatLST" %(self.HOME))
                
                if go:  
                    odir = QtGui.QFileDialog.getExistingDirectory(self, 'Select Directory to Save calibrated files')
                    err = ""
                    errs = ""
                    subc = self.ui.comboBox_10.currentText()
                    ctyc = self.ui.lineEdit_12.text()
                    if os.path.isdir(odir):
                        pit = 0
                        gui.logging(self, "--- %s - ccdproc started for calibration." %(datetime.datetime.utcnow()))
                        for x in xrange(self.ui.listWidget.count()):
                            pit = pit + 1
                            ln = self.ui.listWidget.item(x)
                            img = ln.text()
                            if function.headerRead(img, sname) == "" and subc == "yes":
                                errs = "%s, %s" %(errs, ntpath.basename(str(img)))
                            else:
                                function.headerWrite(img, "subset", str("'(@\"%s\")'" %sname))
                                if not function.calibration(img, zeroFilePath, darkFilePath, flatFilePath, odir, sub=subc, cty=ctyc):
                                    err = "%s, %s" %(err, ntpath.basename(str(img)))
                            self.ui.label.setText(QtGui.QApplication.translate("Form", "Calibration: %s." %(ntpath.basename(str(img))), None, QtGui.QApplication.UnicodeUTF8))
                            self.ui.progressBar.setProperty("value", math.ceil(100*(float(float(pit)/float(self.ui.listWidget.count())))))
                        
                        if err != "":
                            err = "ccdproc failed on:\n%s" %(err)
                            self.dispErr(err)
                        if errs:
                            errs = "Images below have no %s field in header:\n%s" %(sname, errs)
                            self.dispErr(errs)
                        
                        gui.logging(self, "--- %s - ccdproc finished calibration." %(datetime.datetime.utcnow()))
                        os.popen("rm -rf %s/tmp/flatLS %s/tmp/zeroLST %s/tmp/darkLST %s %s %s" %(self.HOME, self.HOME, self.HOME, zeroFilePath, darkFilePath, flatFilePath))
    else:
        QtGui.QMessageBox.critical( self,  ("MYRaf Error"), ("No <b>image</b> to calibrate."))
########################################################
#Create master files####################################
  def masterZero(self):
    gui.logging(self, "-- %s - zerocombine started." %(datetime.datetime.utcnow()))
    lst = gui.lisFromLW(self, self.ui.listWidget_2)
    gui.list2file(lst, "%s/tmp/zeroLST" %(self.HOME))
    ofile = QtGui.QFileDialog.getSaveFileName( self, 'Save Master Bias file', 'zero.fits', 'Fit or Fits (*.fits *.fit)')
    if ofile != "":
        com = self.ui.comboBox_2.currentText()
        rej = self.ui.comboBox_3.currentText()
        cty = self.ui.lineEdit_9.text()
        if not function.zeroCombine("%s/tmp/zeroLST" %(self.HOME), ofile, com=com, rej=rej, cty=cty):
            QtGui.QMessageBox.critical( self,  ("MYRaf Error"), ("Due to an error <b>zerocombine</b> can not handle this job."))
            gui.logging(self, "-- %s - zerocombine failed." %(datetime.datetime.utcnow()))
        else:
            gui.logging(self, "-- %s - zerocombine succeed." %(datetime.datetime.utcnow()))
    os.popen("rm -rf %s/tmp/zeroLST" %(self.HOME))

  def masterDark(self):
    gui.logging(self, "-- %s - darkcombine started." %(datetime.datetime.utcnow()))
    lst = gui.lisFromLW(self, self.ui.listWidget_3)
    gui.list2file(lst, "%s/tmp/darkLST" %(self.HOME))
    ofile = QtGui.QFileDialog.getSaveFileName( self, 'Save Master Dark file', 'dark.fits', 'Fit or Fits (*.fits *.fit)')
    if ofile != "":
        com = self.ui.comboBox_4.currentText()
        rej = self.ui.comboBox_5.currentText()
        scl = self.ui.comboBox_8.currentText()
        cty = self.ui.lineEdit_10.text()
        if not function.darkCombine("%s/tmp/darkLST" %(self.HOME), ofile, com=com, rej=rej, cty=cty, scl=scl):
            QtGui.QMessageBox.critical( self,  ("MYRaf Error"), ("Due to an error <b>darkcombine</b> can not handle this job."))
            gui.logging(self, "-- %s - darkcombine failed." %(datetime.datetime.utcnow()))
        else:
            gui.logging(self, "-- %s - darkcombine succeed." %(datetime.datetime.utcnow()))
    os.popen("rm -rf %s/tmp/darkLST" %(self.HOME))
        
  def masterFlat(self):
    gui.logging(self, "-- %s - flatcombine started." %(datetime.datetime.utcnow()))
    lst = gui.lisFromLW(self, self.ui.listWidget_4)
    gui.list2file(lst, "%s/tmp/flatLST" %(self.HOME))
    odir = QtGui.QFileDialog.getExistingDirectory( self, 'Select Directory to Save Flat(s)')
    f = open("%s/tmp/flatLST" %(self.HOME), "r")
    it = 0
    sname = self.ui.lineEdit_14.text()
    
    for i in f:
        fn = i.replace("\n","")
        if function.headerRead(fn,sname) == "":
            it = it + 1
    f.close()
    
    com = self.ui.comboBox_6.currentText()
    rej = self.ui.comboBox_7.currentText()
    sub = self.ui.comboBox_9.currentText()
    cty = self.ui.lineEdit_11.text()
    
    if os.path.isdir(odir):
        if sub == "yes" and it != 0:
            QtGui.QMessageBox.critical( self,  ("MYRaf Error"), ("Subset classification is enabled but one or more images have no <b>%s</b> field in header.\nAdd <b>%s</b> field to headers." %(sname, sname)))
        else:
            
            function.headerWrite("@%s/tmp/flatLST" %(self.HOME), "subset", str("'(@\"%s\")'" %sname))
            if not function.flatCombine("%s/tmp/flatLST" %(self.HOME), odir, com=com, rej=rej, cty=cty, sub=sub):
                QtGui.QMessageBox.critical( self,  ("MYRaf Error"), ("Due to an error <b>flatcombine</b> can not handle this job."))
                gui.logging(self, "-- %s - flatcombine failed." %(datetime.datetime.utcnow()))
            else:
                gui.logging(self, "-- %s - flatcombine succeed." %(datetime.datetime.utcnow()))
    os.popen("rm -rf %s/tmp/flatLST" %(self.HOME))
    
########################################################
#Load and set set########################################
  def applySettings(self):
      
      f = open("%s/set/setting" %(self.HOME), "r")
      for l in f:
          #print(l.replace("\n",""))
          
          if l.startswith("zCombine"):
              zCombine = int(l.split(":")[1].replace("\n",""))
              self.ui.comboBox_2.setCurrentIndex(zCombine)

          if l.startswith("zReject"):
              zReject = int(l.split(":")[1].replace("\n",""))
              self.ui.comboBox_3.setCurrentIndex(zReject)
              
          if l.startswith("zccdtype"):
              zccdtype = l.split(":")[1].replace("\n","")
              self.ui.lineEdit_9.setText(QtGui.QApplication.translate("Form", str(zccdtype), None, QtGui.QApplication.UnicodeUTF8))

          if l.startswith("dCombine"):
              dCombine = int(l.split(":")[1].replace("\n",""))
              self.ui.comboBox_4.setCurrentIndex(dCombine)

          if l.startswith("dReject"):
              dReject = int(l.split(":")[1].replace("\n",""))
              self.ui.comboBox_5.setCurrentIndex(dReject)

          if l.startswith("dScale"):
              dScale = int(l.split(":")[1].replace("\n",""))
              self.ui.comboBox_8.setCurrentIndex(dScale)

          if l.startswith("dccdtype"):
              dccdtype = l.split(":")[1].replace("\n","")
              self.ui.lineEdit_10.setText(QtGui.QApplication.translate("Form", str(dccdtype), None, QtGui.QApplication.UnicodeUTF8))

          if l.startswith("fCombine"):
              fCombine = int(l.split(":")[1].replace("\n",""))
              self.ui.comboBox_6.setCurrentIndex(dCombine)

          if l.startswith("fReject"):
              fReject = int(l.split(":")[1].replace("\n",""))
              self.ui.comboBox_7.setCurrentIndex(fReject)

          if l.startswith("fSubset"):
              fSubset = int(l.split(":")[1].replace("\n",""))
              self.ui.comboBox_9.setCurrentIndex(fSubset)

          if l.startswith("fccdtype"):
              fccdtype = l.split(":")[1].replace("\n","")
              self.ui.lineEdit_11.setText(QtGui.QApplication.translate("Form", str(fccdtype), None, QtGui.QApplication.UnicodeUTF8))
              
          if l.startswith("cSubset"):
              cSubset = int(l.split(":")[1].replace("\n",""))
              self.ui.comboBox_10.setCurrentIndex(cSubset)
              
          if l.startswith("cccdtype"):
              cccdtype = l.split(":")[1].replace("\n","")
              self.ui.lineEdit_12.setText(QtGui.QApplication.translate("Form", str(cccdtype), None, QtGui.QApplication.UnicodeUTF8))
              
          if l.startswith("dpExpTime"):
              dpExpTime = l.split(":")[1].replace("\n","")
              self.ui.lineEdit_13.setText(QtGui.QApplication.translate("Form", str(dpExpTime), None, QtGui.QApplication.UnicodeUTF8))
              
          if l.startswith("dpFilter"):
              dpFilter = l.split(":")[1].replace("\n","")
              self.ui.lineEdit_14.setText(QtGui.QApplication.translate("Form", str(dpFilter), None, QtGui.QApplication.UnicodeUTF8))
          
          if l.startswith("fspAnnulus"):
              fspAnnulus = int(l.split(":")[1].replace("\n",""))
              self.ui.doubleSpinBox_2.setValue(fspAnnulus)
              
          if l.startswith("fspDannulus"):
              fspDannulus = int(l.split(":")[1].replace("\n",""))
              self.ui.doubleSpinBox.setValue(fspDannulus)
              
          if l.startswith("fspCBox"):
              fspCBox = int(l.split(":")[1].replace("\n",""))
              self.ui.doubleSpinBox_3.setValue(fspCBox)
              
          if l.startswith("ppApertur"):
              ppApertur = l.split(":")[1].replace("\n","")
              self.ui.lineEdit_15.setText(QtGui.QApplication.translate("Form", str(ppApertur), None, QtGui.QApplication.UnicodeUTF8))
              
          if l.startswith("ppZMag"):
              ppZMag = l.split(":")[1].replace("\n","")
              self.ui.lineEdit_16.setText(QtGui.QApplication.translate("Form", str(ppZMag), None, QtGui.QApplication.UnicodeUTF8))        
              
          if l.startswith("oRa"):
              oRa = l.split(":")[1].replace("\n","")
              self.ui.lineEdit_22.setText(QtGui.QApplication.translate("Form", str(oRa), None, QtGui.QApplication.UnicodeUTF8))
        
          if l.startswith("oDec"):
              oDec = l.split(":")[1].replace("\n","")
              self.ui.lineEdit_23.setText(QtGui.QApplication.translate("Form", str(oDec), None, QtGui.QApplication.UnicodeUTF8))

          if l.startswith("obser"):
              obser = l.split(":")[1].replace("\n","")
              self.ui.lineEdit_18.setText(QtGui.QApplication.translate("Form", str(obser), None, QtGui.QApplication.UnicodeUTF8))
        
          if l.startswith("obsti"):
              obsti = l.split(":")[1].replace("\n","")
              self.ui.lineEdit_17.setText(QtGui.QApplication.translate("Form", str(obsti), None, QtGui.QApplication.UnicodeUTF8))

          if l.startswith("obsda"):
              obsda = l.split(":")[1].replace("\n","")
              self.ui.lineEdit_24.setText(QtGui.QApplication.translate("Form", str(obsda), None, QtGui.QApplication.UnicodeUTF8))

          if l.startswith("gain"):
              gain = l.split(":")[1].replace("\n","")
              self.ui.lineEdit_26.setText(QtGui.QApplication.translate("Form", str(gain), None, QtGui.QApplication.UnicodeUTF8))
              
          if l.startswith("epoc"):
              epoc = l.split(":")[1].replace("\n","")
              self.ui.lineEdit_25.setText(QtGui.QApplication.translate("Form", str(epoc), None, QtGui.QApplication.UnicodeUTF8))

          if l.startswith("WCSServer"):
              WCSServer = l.split(":")[1].replace("\n","").replace(";",":")
              self.ui.lineEdit_27.setText(QtGui.QApplication.translate("Form", str(WCSServer), None, QtGui.QApplication.UnicodeUTF8))

          if l.startswith("WCSApiKey"):
              WCSApiKey = l.split(":")[1].replace("\n","")
              self.ui.lineEdit_28.setText(QtGui.QApplication.translate("Form", str(WCSApiKey), None, QtGui.QApplication.UnicodeUTF8))

          if l.startswith("WCSDonNothing"):
              chepoc = l.split(":")[1].replace("\n","")
              if chepoc == "t":
                  self.ui.radioButton.setChecked(True)
              else:
                  self.ui.radioButton.setChecked(False)

          if l.startswith("WCSComp"):
              chepoc = l.split(":")[1].replace("\n","")
              if chepoc == "t":
                  self.ui.radioButton_2.setChecked(True)
              else:
                  self.ui.radioButton_2.setChecked(False)

          if l.startswith("WCSCon2Bin"):
              chepoc = l.split(":")[1].replace("\n","")
              if chepoc == "t":
                  self.ui.radioButton_3.setChecked(True)
              else:
                  self.ui.radioButton_3.setChecked(False)

          if l.startswith("WCSSWCS"):
              chepoc = l.split(":")[1].replace("\n","")
              if chepoc == "t":
                  self.ui.checkBox_19.setChecked(True)
              else:
                  self.ui.checkBox_19.setChecked(False)

          if l.startswith("chepoc"):
              chepoc = l.split(":")[1].replace("\n","")
              if chepoc == "t":
                  self.ui.checkBox_4.setChecked(True)
                  self.ui.lineEdit_25.setEnabled(False)
              else:
                  self.ui.checkBox_4.setChecked(False)
                  self.ui.lineEdit_25.setEnabled(True)

          if l.startswith("sfMaxStar"):
              sfMaxStar = int(l.split(":")[1].replace("\n",""))
              self.ui.doubleSpinBox_7.setValue(sfMaxStar)

          if l.startswith("sMaxFWHM"):
              sMaxFWHM = int(l.split(":")[1].replace("\n",""))
              self.ui.doubleSpinBox_6.setValue(sMaxFWHM)

          if l.startswith("sMinFWHM"):
              sMinFWHM = int(l.split(":")[1].replace("\n",""))
              self.ui.doubleSpinBox_5.setValue(sMinFWHM)

          if l.startswith("sFluxradi"):
              sFluxradi = int(l.split(":")[1].replace("\n",""))
              self.ui.doubleSpinBox_4.setValue(sFluxradi)

          if l.startswith("CCMask"):
              chepoc = l.split(":")[1].replace("\n","")
              if chepoc == "t":
                  self.ui.checkBox_16.setChecked(True)
              else:
                  self.ui.checkBox_16.setChecked(False)

          if l.startswith("CCGain"):
              CCGain = float(l.split(":")[1].replace("\n",""))
              self.ui.doubleSpinBox_10.setValue(CCGain)

          if l.startswith("CCReadNoise"):
              CCReadNoise = float(l.split(":")[1].replace("\n",""))
              self.ui.doubleSpinBox_11.setValue(CCReadNoise)

          if l.startswith("CCSigclip"):
              CCSigclip = float(l.split(":")[1].replace("\n",""))
              self.ui.doubleSpinBox_12.setValue(CCSigclip)

          if l.startswith("CCsigfrac"):
              CCsigfrac = float(l.split(":")[1].replace("\n",""))
              self.ui.doubleSpinBox_13.setValue(CCsigfrac)

          if l.startswith("CCobjlim"):
              CCobjlim = float(l.split(":")[1].replace("\n",""))
              self.ui.doubleSpinBox_14.setValue(CCobjlim)

          if l.startswith("timeobs"):
              chepoc = l.split(":")[1].replace("\n","")
              if chepoc == "t":
                  self.ui.checkBox_12.setChecked(True)
              else:
                  self.ui.checkBox_12.setChecked(False)

          if l.startswith("extraVal"):
              extraVal = l.split(":")[1].replace("\n","")
              extraVals = extraVal.split(',')
              it = -1
              for i in extraVals:
                  if i != "":
                      it = it +1
                      item = QtGui.QListWidgetItem()
                      self.ui.listWidget_20.addItem(item)
                      item = self.ui.listWidget_20.item(it)
                      item.setText(QtGui.QApplication.translate("Form", i, None, QtGui.QApplication.UnicodeUTF8))

      f.close()
      
  def saveSettings(self):
    
    f = open("%s/set/setting" %(self.HOME), "w")
    
    f.write("zCombine:%s\n" %self.ui.comboBox_2.currentIndex())
    f.write("zReject:%s\n" %self.ui.comboBox_3.currentIndex())
    f.write("zccdtype:%s\n" %self.ui.lineEdit_9.text())
    
    f.write("dCombine:%s\n" %self.ui.comboBox_4.currentIndex())
    f.write("dReject:%s\n" %self.ui.comboBox_5.currentIndex())
    f.write("dScale:%s\n" %self.ui.comboBox_8.currentIndex())
    f.write("dccdtype:%s\n" %self.ui.lineEdit_10.text())
    
    f.write("fCombine:%s\n" %self.ui.comboBox_6.currentIndex())
    f.write("fReject:%s\n" %self.ui.comboBox_7.currentIndex())
    f.write("fSubset:%s\n" %self.ui.comboBox_9.currentIndex())
    f.write("fccdtype:%s\n" %self.ui.lineEdit_11.text())
    
    f.write("cSubset:%s\n" %self.ui.comboBox_10.currentIndex())
    f.write("ccdtype:%s\n" %self.ui.lineEdit_12.text())

    f.write("dpExpTime:%s\n" %self.ui.lineEdit_13.text())
    f.write("dpFilter:%s\n" %self.ui.lineEdit_14.text())

    f.write("fspAnnulus:%s\n" %int(self.ui.doubleSpinBox_2.value()))
    f.write("fspDannulus:%s\n" %int(self.ui.doubleSpinBox.value()))
    f.write("fspCBox:%s\n" %int(self.ui.doubleSpinBox_3.value()))
    
    f.write("CCGain:%s\n" %float(self.ui.doubleSpinBox_10.value()))
    f.write("CCReadNoise:%s\n" %float(self.ui.doubleSpinBox_11.value()))
    f.write("CCSigclip:%s\n" %float(self.ui.doubleSpinBox_12.value()))
    f.write("CCsigfrac:%s\n" %float(self.ui.doubleSpinBox_13.value()))
    f.write("CCobjlim:%s\n" %float(self.ui.doubleSpinBox_14.value()))
    
    
    f.write("ppApertur:%s\n" %self.ui.lineEdit_15.text())
    f.write("ppZMag:%s\n" %self.ui.lineEdit_16.text())
    
    f.write("oRa:%s\n" %self.ui.lineEdit_22.text())
    f.write("oDec:%s\n" %self.ui.lineEdit_23.text())
    
    f.write("obser:%s\n" %self.ui.lineEdit_18.text())
    f.write("obsti:%s\n" %self.ui.lineEdit_17.text())
    f.write("obsda:%s\n" %self.ui.lineEdit_24.text())

    f.write("WCSServer:%s\n" %self.ui.lineEdit_27.text().replace(":",";"))
    f.write("WCSApiKey:%s\n" %self.ui.lineEdit_28.text())
    
    f.write("epoc:%s\n" %self.ui.lineEdit_25.text())
    if self.ui.checkBox_4.checkState() == QtCore.Qt.Checked:
        f.write("chepoc:t\n")
    else:
        f.write("chepoc:f\n")
        
    if self.ui.radioButton.isChecked():
        f.write("WCSDonNothing:t\n")
    else:
        f.write("WCSDonNothing:f\n")  

    if self.ui.radioButton_2.isChecked():
        f.write("WCSComp:t\n")
    else:
        f.write("WCSComp:f\n")    

    if self.ui.radioButton_3.isChecked():
        f.write("WCSCon2Bin:t\n")
    else:
        f.write("WCSCon2Bin:f\n")
        
    if self.ui.checkBox_19.checkState() == QtCore.Qt.Checked:
        f.write("WCSSWCS:t\n")
    else:
        f.write("WCSSWCS:f\n")

    if self.ui.checkBox_16.checkState() == QtCore.Qt.Checked:
        f.write("CCMask:t\n")
    else:
        f.write("CCMask:f\n")

    if self.ui.checkBox_12.checkState() == QtCore.Qt.Checked:
        f.write("timeobs:t\n")
    else:
        f.write("timeobs:f\n")

    f.write("sfMaxStar:%s\n" %int(self.ui.doubleSpinBox_7.value()))
    f.write("sMaxFWHM:%s\n" %int(self.ui.doubleSpinBox_6.value()))
    f.write("sMinFWHM:%s\n" %int(self.ui.doubleSpinBox_5.value()))
    f.write("sFluxradi:%s\n" %int(self.ui.doubleSpinBox_4.value()))
    f.write("gain:%s\n" %self.ui.lineEdit_26.text())
    
    vv = ""
    for i in xrange(self.ui.listWidget_20.count()):
        val = self.ui.listWidget_20.item(i)
        val = str(val.text())
        vv = "%s,%s" %(val, vv)
    f.write("extraVal:%s\n" %(vv[:-1]))
    f.close()
#########################################################
#Unlock calibration tabs.################################
  def unlockBias(self):
    gui.unlocCali(self, self.ui.checkBox, 1)
  def unlockDark(self):
    gui.unlocCali(self, self.ui.checkBox_2, 2)
  def unlockFlat(self):
    gui.unlocCali(self, self.ui.checkBox_3, 3)
########################################################
  def closeEvent(self, event):
    gui.logging(self, "- %s - MYRaf closed." %(datetime.datetime.utcnow()))
    exit(0)
########################################################
app = QtGui.QApplication(sys.argv)
f = MyForm()
f.show()

app.exec_()
