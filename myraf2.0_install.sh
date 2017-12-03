#!/bin/bash
# MYRaf 2.0 installation script
echo "Installation started..."
echo "Installing required dependencies..."
sudo apt install wget python-pip and subversion sextractor pyqt4-dev-tools python-matplotlib libx11-dev x11proto-core-dev
sudo ln -s /usr/bin/sextractor /usr/bin/sex
sudo pip install --upgrade numpy
sudo pip install --upgrade astropy
sudo pip install ginga
echo "Installing pyraf..."
sudo pip install pyraf
# wget http://stsdas.stsci.edu/download/pyraf/pyraf-dev-py3.tar.gz
# tar -xvf pyraf-dev-py3.tar.gz
# pyraf_dir=$(tar -ztf pyraf-dev-py3.tar.gz | egrep '^[^/]+/?$')
# cd $pyraf_dir
# sudo python setup.py install
# cd ..
echo "Installing f2n..."
git clone https://github.com/mtewes/f2n.git
cd f2n
sudo python setup.py install
cd ..
echo "Installing astroasciidata..."
wget https://www.stecf.org/software/PYTHONtools/astroasciidata/source/asciidata-1.1.1.tar.gz
tar -xvf asciidata-1.1.1.tar.gz
cd asciidata-1.1.1
sudo python setup.py install
cd ..
echo "Installing alipy..."
git clone https://github.com/LCOGT/alipy.git
cd alipy
sudo python setup.py install
cd ..
echo "Installing MYRaf 2.0..."
sudo python setup.py install
echo "Setting MYRaf 2.0..."
sudo cp -rv ccd.dat /iraf/iraf/noao/imred/quadred/src/quad/ccd.dat
sudo cp -rv camera.dat /iraf/iraf/noao/imred/ccdred/ccddb/kpno/camera.dat
cd
echo "Installation has been completed."
echo "Please give the 'myraf2' command to run MYRaf 2.0 from terminal."
