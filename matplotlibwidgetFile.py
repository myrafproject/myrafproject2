from PyQt4 import QtGui 
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas 

from PyQt4 import QtGui
# from matplotlib.backends.backend_qt4 import FigureCanvasQT as FigureCanvas
from matplotlib.backends.backend_qt4 import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

class MplCanvas(FigureCanvas):

    def __init__(self):

        self.fig = Figure(facecolor = '#FFFFFF')
        self.ax = self.fig.add_subplot(111)
        self.fig.subplots_adjust(left=0.1, bottom=0.1, right=0.9, top=0.9)
        self.xtitle="Phase"
        self.ytitle="Diff. Mag."
        self.PlotTitle = "Phot Plot"
        self.grid_status = True
        self.xaxis_style = 'linear'
        self.yaxis_style = 'linear'
        self.format_labels()
        self.ax.hold(True)
        FigureCanvas.__init__(self, self.fig)
        FigureCanvas.setSizePolicy(self, QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def format_labels(self):
        self.ax.set_title(self.PlotTitle)
        self.ax.title.set_fontsize(10)
        self.ax.set_xlabel(self.xtitle, fontsize = 9)
        self.ax.set_ylabel(self.ytitle, fontsize = 9)
        labels_x = self.ax.get_xticklabels()
        labels_y = self.ax.get_yticklabels()

        for xlabel in labels_x:
            xlabel.set_fontsize(8)
            xlabel.set_color('b')
        for ylabel in labels_y:
            ylabel.set_fontsize(8)
            ylabel.set_color('b')


class matplotlibWidget(QtGui.QWidget):

    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.canvas = MplCanvas()
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.vbl = QtGui.QVBoxLayout()
        self.vbl.addWidget(self.canvas)
        self.vbl.addWidget(self.toolbar)
        self.setLayout(self.vbl)
        self.parent = parent
