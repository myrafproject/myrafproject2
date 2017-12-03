#!/usr/bin/env python										
#-*- coding: utf-8 -*-										
 													
from setuptools import setup								
import glob											
setup(name = "myraf",									
	version = "2.0b2",									
	author = "Yücel Kılıç",							
	url = "http://myrafproject.org",					
	author_email ="yucelkilic[at]myrafproject.org",					
	description = "An easy GUI for IRAF Photometry",								
	long_description = "The MYRaf is a practicable astronomical image reduction and photometry software and interface for IRAF. For this purpose, MYRaf uses iraf, PyRAF and alipy via great programming language Python and Qt framework. Also MYRaf is a absolutely free software and distributed with GPLv3 license. You can use it without restrictive licenses, make copies for your friends, school or business.",						
	license = "GPLv3",									
	platforms = 'linux',									
	data_files = [ ("/usr/share/myraf/img",glob.glob('./img/*')),    
                             ("/usr/share/myraf/obsdat",glob.glob('./obsdat/*')),
							 ("/usr/share/myraf/set",glob.glob('./set/*')),
                             ("/usr/share/myraf",glob.glob('./error.py')),
                             ("/usr/share/myraf",glob.glob('./error.ui')),
                             ("/usr/share/myraf",glob.glob('./fPlot.py')),
                             ("/usr/share/myraf",glob.glob('./function.py')),
                             ("/usr/share/myraf",glob.glob('./gingawidgetFile.py')),
							 ("/usr/share/myraf",glob.glob('./gui.py')),
							 ("/usr/share/myraf",glob.glob('./main.py')),
							 ("/usr/share/myraf",glob.glob('./cosmics.py')),
							 ("/usr/share/myraf",glob.glob('./mainErr.py')),
							 ("/usr/share/myraf",glob.glob('./matplotlibwidgetFile.py')),
							 ("/usr/share/myraf",glob.glob('./myraf.py')),
							 ("/usr/share/myraf",glob.glob('./myraf.ui')),
							 ("/usr/share/myraf",glob.glob('./sexCat.py')),
 							 ("/usr/share/applications",glob.glob('./myraf2.desktop'))],
							 scripts = ['myraf2'])
