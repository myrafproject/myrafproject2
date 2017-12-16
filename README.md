# What’s New on MYRaf v2.0 Beta:
- Multi-subset calibration at once.
- You can create master Bias/Dark/Flat files with one click.
- Save your calibrated/aligned/reduced files anywhere you want.
- Manually align tab added.
- Auto star finder added with alipy and SExtractor.
- Multi-source photometry tab added.
- Multi-aperture photometry.
- Graphics tab added for result file (.my files) plotting.
- Editor tab revised and “Header editor” can delete any keyword.
- Observatory editor added.
- Settings tab added for user-defined keywords. So, there is no keyword restriction with calibration and photometry.
- Help tab added but not documented in this version. We are sorry about that!
- Cosmic Ray Cleaner added.

# Installation
- For the video tutorial click the picture below.
[![MYRaf v2.0 Beta Video Tutorial](https://img.youtube.com/vi/XVrDA8rA9hs/0.jpg)](https://www.youtube.com/watch?v=XVrDA8rA9hs)
- Install IRAF v2.16 and later. If you are using Ubuntu it is easy to install from this [link](http://www.astrosen.unam.mx/%7Efavilac/IRAF/16.04/IRAF_Ubuntu16.04.iso).
- Download MYRaf v2.0 Beta

```
$ git clone https://github.com/myrafproject/myrafproject2.git
```

- By installation script (Ubuntu);

```
$ cd myrafproject2
$ chmod +x myraf2.0_install.sh
$ sudo ./myraf2.0_install.sh
$ sudo chown -R $(whoami):$(whoami) /usr/share/myraf/
$ sudo chown -R $(whoami):$(whoami) /iraf/iraf/noao/lib/obsdb.dat
$ myraf2
```

And close MYRaf, proceed by;

```bash
$ cd ~/.MYRaf2
$ cl
vocl> noao
noao> imred
imred> ccdred
ccdred> setinst
```
then, "enter the ccdred epar menu" and change "instrum" section;

(instrum= ccddb$kpno/camera.dat) CCD instrument file.

Press ":wq" and ":wq" save settings.

```bash
logout
$ myraf2
```

- By manual installation (If you installed MYRaf 2.0 with the installation script, you do not need to continue further).

- Install dependencies

```
$ sudo apt install wget python-pip and subversion sextractor pyqt4-dev-tools python-matplotlib libx11-dev x11proto-core-dev$ sudo ln -s /usr/bin/sextractor /usr/bin/sex
$ sudo pip install --upgrade numpy
$ sudo pip install --upgrade astropy
$ sudo pip install ginga
$ sudo pip install pyraf
```
- Install f2n

```
$ svn export https://svn.epfl.ch/svn/mtewes-public/trunk/f2n ./f2n
$ cd f2n
$ sudo python setup.py install
$ cd ..
```
- Install astroasciidata

```
$ wget https://www.stecf.org/software/PYTHONtools/astroasciidata/source/asciidata-1.1.1.tar.gz
$ tar -xvf asciidata-1.1.1.tar.gz
$ cd asciidata-1.1.1
$ sudo python setup.py install
$ cd ..
```
- Install alipy

```
$ svn checkout https://svn.epfl.ch/svn/mtewes-public/trunk/alipy2 ./alipy
$ cd alipy
$ sudo python setup.py install
$ cd ..
```
- Install MYRaf v2.0 Beta

```
$ sudo python setup.py install
$ cd
$ sudo chown -R $(whoami):$(whoami) /usr/share/myraf/
$ myraf2
```

If you have any problems during installation, please contact us or create an [issue](https://github.com/myrafproject/myrafproject2/issues/new).

We tried to create a version that you enjoy it. We wish you clear skies and data with high SNR! :)

**MYRaf Project Team**
**Yücel KILIÇ** | yucelkilic@myrafproject.org
**Mohammad SHEMUNI** | m.shemuni@myrafproject.org

For academic use, please cite the paper:

> Kilic, Y.; Shameoni Niaei, M.; Özeren, F. F.; Yesilyaprak, C.,
> 2016,
> *MYRaf: A new Approach with IRAF for Astronomical Photometric Reduction*,
> **RevMexAA (Serie de Conferencias)**, 48, 38–39 (2016).

[Bibtex@ADS](http://adsabs.harvard.edu/cgi-bin/nph-bib_query?bibcode=2016RMxAC..48...38K&data_type=BIBTEX&db_key=AST&nocookieset=1)
| [RevMexAA](http://www.astroscu.unam.mx/rmaa/RMxAC..48/PDF/RMxAC..48_part-2.2.pdf)
