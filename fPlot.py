# -*- coding: utf-8 -*-
#
# fPlot.py -- Plotting function for embedded matplotlib widget with Ginga.
#
# Thanks for Eric Jeschke (eric@naoj.org), https://github.com/ejeschke/ginga
# Copyleft, Yücel Kılıç (yucelkilic@myrafproject.org) and Mohammad Niaei Shameoni (mshemuni@myrafproject.org).
# This is open-source software licensed under a GPLv3 license.
import sys
import logging

from ginga.mplw.ImageViewCanvasMpl import ImageViewCanvas
from ginga.mplw.FigureCanvasQt import setup_Qt
from ginga.AstroImage import AstroImage

class FitsPlot(object):
    def __init__(self, chartDev):

        self.chartDev = chartDev
        # use_logger = False
        # logger = log.get_logger(null=not use_logger, log_stderr=True)
        # self.logger = logger
        self.logger = None
        # create a ginga object and tell it about the figure
        self.chartDev.fig.clf()
        fi = ImageViewCanvas(logger=self.logger)
        # Two subplots, the axes array is 1-d

        fi.enable_autocuts('on')
        fi.set_autocut_params('zscale')
        fi.set_figure(self.chartDev.fig)
        fi.ui_setActive(True)
        self.fitsimage = fi
        setup_Qt(chartDev, fi)

        # enable all interactive features
        fi.get_bindings().enable_all(True)
        self.fitsimage = fi

    def load(self, fitspath):

        # clear plotting area
        self.chartDev.fig.gca().cla()
        # load an image
        image = AstroImage(self.logger)
        image.load_file(fitspath)
        self.fitsimage.set_image(image)
        self.fitsimage.add_axes()
