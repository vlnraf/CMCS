import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import pyqtgraph as pg
import matplotlib.pyplot as plt
import numpy as np


colors =  {
            'lightest':"#eeeeee",
            'lighter':"#e5e5e5",
            'light':"#effffb",
            'himid':"#50d890",
            'midmid':"#1089ff",
            'lomid':"#4f98ca",
            'dark' :"#272727",
            'darker' :"#23374d",
}


def linear_interp(x, in_min, in_max, out_min, out_max, lim=True, dec=None):
    y = (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

    if dec is not None:
        y = round(y, dec)

    if not lim:
        return y

    else:
        y = max(out_min, y)
        y = min(out_max, y)

        return y

def model(pop, r, K):
    # return 1
    return r * pop * ( 1 - (pop / K))
    # return r * pop * ( 1 - pop )

def get_function_values(ipop, r, n, K):
    pop = ipop
    y = []
    y.append(pop)
    for i in range(n):
        pop = model(pop, r, K)
        y.append(pop)

    return y

def series_plot(plt, y_vals, idx=100, r=0, xall=False):

    plt.clear()
    plt.setTitle("Population vs Time, growth rate: {:4.2f}".format(r))

    t = np.arange(len(y_vals))
    y = y_vals[:idx]
    t = t[:idx]

    if len(t) < 20:
        plt.setXRange(*[0,20])
    else:
        if not xall:
            plt.setXRange(*[len(t)-20, len(t)])
        else:
            plt.setXRange(*[0, 30])

    plt.setYRange(*[0,100])
    plt.showGrid(x=True, y=True)

    s = 20/len(t)
    s = max(10,s)

    line = plt.plot(x=t, y=y)
    line.setPen(color=colors['lomid'], width=3.0)

    scat = pg.ScatterPlotItem(x=t, y=y, size=s, name='series')
    scat.setPen(color=(1,1,1,0), width=0.0)
    scat.setBrush(color=colors['himid'])
    plt.addItem(scat)

    xaxis = plt.getAxis("bottom")
    #xaxis.setTickSpacing(4,4)

    # xaxis.tickFont = numfont
    xaxis.setStyle(tickTextOffset = 20)

    yaxis = plt.getAxis("left")

class Color(QWidget):
    def __init__(self, color, *args, **kwargs):
        super(Color, self).__init__(*args, **kwargs)
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(color))
        self.setPalette(palette)

class Controls(QWidget):
    def __init__(self, variable='', parent=None):
        super(Controls, self).__init__(parent=parent)
        self.verticalLayout = QVBoxLayout(self)

        #---CheckBox---#

        self.l1 = QVBoxLayout()
        self.l1.setAlignment(Qt.AlignTop)

        self.series_box = QCheckBox("📈 Plot", parent=self)
        self.l1.addWidget(self.series_box)
        self.series_box.setChecked(1)

        self.verticalLayout.addLayout(self.l1)
        #-------------#

        #---Init Population---#
        self.l2 = QVBoxLayout()
        self.l2.setAlignment(Qt.AlignTop)

        self.sub1 = QHBoxLayout()
        self.sub1.setAlignment(Qt.AlignLeft)
        self.ipop_txt = QLabel("Init. Pop.", self)
        
        self.ipop_box = QDoubleSpinBox(self)
        self.ipop_box.setSingleStep(1)
        self.ipop_box.setDecimals(0)

        self.sub1.addWidget(self.ipop_txt)
        self.sub1.addWidget(self.ipop_box)

        self.l2.addLayout(self.sub1)

        self.ipop = QSlider(self)
        self.ipop.setOrientation(Qt.Horizontal)
        self.l2.addWidget(self.ipop)

        self.verticalLayout.addLayout(self.l2)

        self.setFixedWidth(self.ipop.width() + 50)
        #-------------#

        #---Rate---#
        self.sub1 = QHBoxLayout()
        self.sub1.setAlignment(Qt.AlignLeft)
        self.rate_txt = QLabel("rate", self)
        
        self.rate_box = QDoubleSpinBox(self)
        self.rate_box.setSingleStep(0.01)
        self.rate_box.setDecimals(2)

        self.sub1.addWidget(self.rate_txt)
        self.sub1.addWidget(self.rate_box)

        self.l2.addLayout(self.sub1)

        self.rate = QSlider(self)
        self.rate.setOrientation(Qt.Horizontal)
        self.l2.addWidget(self.rate)

        #-------------#

        #---K---#
        self.sub1 = QHBoxLayout()
        self.sub1.setAlignment(Qt.AlignLeft)
        self.K_txt = QLabel("K", self)

        self.K_box = QDoubleSpinBox(self)
        self.K_box.setMaximum(200)
        self.K_box.setMinimum(1)
        self.K_box.setSingleStep(10)
        self.K_box.setDecimals(0)

        self.sub1.addWidget(self.K_txt)
        self.sub1.addWidget(self.K_box)

        self.l2.addLayout(self.sub1)

        self.K = QSlider(self)
        self.K.setOrientation(Qt.Horizontal)
        self.K.setMaximum(200)
        self.K.setMinimum(1)
        self.l2.addWidget(self.K)

        #-------------#
        self.verticalLayout.addLayout(self.l2)

        self.ipop.valueChanged.connect(lambda: self.setValues('ipop_slider'))
        self.ipop_box.valueChanged.connect(lambda: self.setValues('ipop_box'))
        self.rate.valueChanged.connect(lambda: self.setValues('rate_slider'))
        self.rate_box.valueChanged.connect(lambda: self.setValues('rate_box'))
        self.K.valueChanged.connect(lambda: self.setValues('K_slider'))
        self.K_box.valueChanged.connect(lambda: self.setValues('K_box'))

        self.rateval = 0

        #---Buttons---#
        self.last =  QVBoxLayout()
        self.last.setAlignment(Qt.AlignTop)

        self.animb = QPushButton('Play', parent=self)
        self.last.addWidget(self.animb)
        self.animb.setFixedWidth(self.ipop.width())

        self.restore = QPushButton('Restore', parent=self)
        self.last.addWidget(self.restore)
        self.restore.setFixedWidth(self.ipop.width())

        self.clear = QPushButton('Clear', parent=self)
        self.clear.setCheckable(False)
        self.clear.setFixedWidth(self.ipop.width())
        self.last.addWidget(self.clear)

        self.verticalLayout.addLayout(self.last)
        #------------#



    def setValues(self, kind=''):

        if kind == 'rate_slider':
            self.rateval = linear_interp(self.rate.value(),
                                            0, 99, 0, 3.99, lim=1, dec=2)
            self.rate_box.blockSignals(True)
            self.rate_box.setValue(self.rateval)
            self.rate_box.blockSignals(False)

        elif kind == 'rate_box':
            self.rateval = linear_interp(self.rate_box.value(),
                                            0, 3.99, 0, 3.99, lim=1, dec=2)
            self.rate.blockSignals(True)
            self.rate.setValue( linear_interp(self.rateval,
                                            0, 3.99, 0, 99, lim=1, dec=2) )
            self.rate.blockSignals(False)

        elif kind == 'ipop_slider':
            self.ipopval = linear_interp(self.ipop.value(),
                                            0, 100, 0, 100, lim=1)
            self.ipop_box.blockSignals(True)
            self.ipop_box.setValue(self.ipopval)
            self.ipop_box.blockSignals(False)


        elif kind == 'ipop_box':
            self.ipopval = self.ipop_box.value()

            self.ipop.blockSignals(True)
            self.ipop.setValue( linear_interp(self.ipopval,
                                            1, 100, 1, 100, lim=1) )
            self.ipop.blockSignals(False)

        elif kind == 'K_slider':
            self.Kval = self.K.value()
            self.K_box.blockSignals(True)
            self.K_box.setValue(self.Kval)
            self.K_box.blockSignals(False)

        elif kind == 'K_box':
            self.Kval = self.K_box.value()

            self.K.blockSignals(True)
            self.K.setValue(self.Kval)
            self.K.blockSignals(False)

        else:
            # defaults
            self.rate_box.setValue(1.0)
            self.ipop_box.setValue(10)
            self.K_box.setValue(10)
            self.setValues('rate_box')
            self.setValues('ipop_box')
            self.setValues('K_box')


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.horizontalLayout = QHBoxLayout()
        self.controls = Controls(parent=self)

        self.controls.setValues()
        self.horizontalLayout.addWidget(self.controls)

        self.win = pg.GraphicsWindow()

        self.setWindowTitle("Logistic Model")
        self.horizontalLayout.addWidget(self.win)

        self.plots = [
                        self.win.addPlot(col=1, title="Population vs Time",
                                            labels={'left': "Population",
                                                    'bottom': "Time"}),

                        self.win.addPlot(col=2, title="To Decide",
                                            labels={'left': "To Decide",
                                                    'bottom': "To Decide"})
                ]
        self.timer = QTimer()
        self.timer.timeout.connect(self.animate_plot)
        self.animate = False
        self.f = 0

        self.update_plot()

        self.controls.animb.pressed.connect(self.play)
        self.controls.clear.pressed.connect(self.clear)
        self.controls.restore.pressed.connect(self.restore)

        widget = QWidget()
        widget.setLayout(self.horizontalLayout)
        self.setCentralWidget(widget)

    def clear(self):
        print('Clear')
        for p in self.plots:
            p.clear()

    def restore(self):
        print('Reset')
        self.animate = False
        self.timer.stop()
        self.f = 0
        self.update_plot()


#     def model(self):
#         x = np.arange(0, 100, 1)
#         y = np.sin(x)
#         return x,y
        

    def play(self):
        self.animate = not self.animate

        if self.animate:
            print('Animation Start')
            # x,y = self.model()
            # self.plots[0].plot(x,y)
            self.update_plot()
            self.controls.animb.setText("Pause")
        else:
            print("Animation pause")
            self.timer.stop()
            self.controls.animb.setText("Play")

    def update_plot(self):

        if self.animate and self.f == 0:
            # start animate
            self.animspeed = 10
            self.animspeed = max(1, self.animspeed)
            self.animspeed = 1000/self.animspeed # sec/frame -> frames/msec

            self.f = 0
            self.fmax = 100
            self.timer.start(self.animspeed)

            self.redraw_plots()

        elif self.animate and self.f != 0:

            # continue animate
            self.animspeed = 10
            self.animspeed = max(1, self.animspeed)
            self.animspeed = 1000/self.animspeed

            self.timer.start(self.animspeed)

        elif not self.animate and self.f == 0:

            self.redraw_plots()

    def redraw_plots(self, index=0):

        """ redraw plots ; controlled by checkmarks """

        rate = self.controls.rateval
        ipop = self.controls.ipopval
        K = self.controls.Kval

        y_vals = get_function_values(ipop, rate, 100, K)

        if self.controls.series_box.isChecked():
            self.plots[0].setVisible(True)
            series_plot(self.plots[0], y_vals, r=rate, xall=True)
        else:
            self.plots[0].setVisible(False)

    def animate_plot(self):

        rate = self.controls.rateval
        ipop = self.controls.ipopval
        K = self.controls.Kval

        y_vals = get_function_values(ipop, rate, 100, K)

        if self.controls.series_box.isChecked():
            self.plots[0].setVisible(True)
            series_plot(self.plots[0], y_vals, idx =1 + self.f, r=rate)
        else:
            self.plots[0].setVisible(False)

        self.f += 1

        if self.f >= self.fmax:
            self.timer.stop()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    app.exec_()
