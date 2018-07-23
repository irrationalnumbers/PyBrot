#Python GUI for Creating and Saving Mandelbrot Fractals
#Author: S. Tootle
#Course: Methods for the Study of Complex Systems
#Date: Winter Semester, 2018
#
#OpenCL code was utilized directly from:
#https://github.com/inducer/pyopencl/blob/master/examples/demo_mandelbrot.py
#
#This program is designed around an external mouse.  The wheel is used
#to zoom in and out, left mouse buton - as defined by the OS - is used
#to drag the scene, and a double click of the left mouse button will
#	a) recent the scene to the point that was double clicked on
#	b) determine a new scale for the mandelbrot calculation based on
#		the current zoom level
#	c) recalculate the mandelbrot set
#	d) display new image of the mandelbrot set
#
#Images can be saved, but only to the current working directory with
#a filename based on the current parameters of the fractal.
#See method "saveCurrentFractal" for more information

from PyQt4 import QtCore, QtGui
import sys, math
import numpy as np
import pyopencl as cl
from PIL import Image, ImageTk
import StringIO

#----------------------------------------------------------------------
#QT4 Design Code
#----------------------------------------------------------------------
try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(2000, 1500)
        MainWindow.setMinimumSize(QtCore.QSize(640, 480))
        MainWindow.setMaximumSize(QtCore.QSize(2000, 1500))
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout_8 = QtGui.QHBoxLayout()
        self.horizontalLayout_8.setObjectName(_fromUtf8("horizontalLayout_8"))
        self.horizontalLayout_6 = QtGui.QHBoxLayout()
        self.horizontalLayout_6.setObjectName(_fromUtf8("horizontalLayout_6"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.iterationsLabel = QtGui.QLabel(self.centralwidget)
        self.iterationsLabel.setObjectName(_fromUtf8("iterationsLabel"))
        self.horizontalLayout.addWidget(self.iterationsLabel)
        self.iterationsPTE = QtGui.QPlainTextEdit(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.iterationsPTE.sizePolicy().hasHeightForWidth())
        self.iterationsPTE.setSizePolicy(sizePolicy)
        self.iterationsPTE.setMinimumSize(QtCore.QSize(100, 20))
        self.iterationsPTE.setMaximumSize(QtCore.QSize(20, 30))
        self.iterationsPTE.setObjectName(_fromUtf8("iterationsPTE"))
        self.horizontalLayout.addWidget(self.iterationsPTE)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.horizontalLayout_6.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.xminLabel = QtGui.QLabel(self.centralwidget)
        self.xminLabel.setObjectName(_fromUtf8("xminLabel"))
        self.horizontalLayout_2.addWidget(self.xminLabel)
        self.xminPTE = QtGui.QPlainTextEdit(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.xminPTE.sizePolicy().hasHeightForWidth())
        self.xminPTE.setSizePolicy(sizePolicy)
        self.xminPTE.setMinimumSize(QtCore.QSize(100, 20))
        self.xminPTE.setMaximumSize(QtCore.QSize(20, 30))
        self.xminPTE.setObjectName(_fromUtf8("xminPTE"))
        self.horizontalLayout_2.addWidget(self.xminPTE)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.horizontalLayout_6.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.xmaxLabel = QtGui.QLabel(self.centralwidget)
        self.xmaxLabel.setObjectName(_fromUtf8("xmaxLabel"))
        self.horizontalLayout_3.addWidget(self.xmaxLabel)
        self.xmaxPTE = QtGui.QPlainTextEdit(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.xmaxPTE.sizePolicy().hasHeightForWidth())
        self.xmaxPTE.setSizePolicy(sizePolicy)
        self.xmaxPTE.setMinimumSize(QtCore.QSize(100, 20))
        self.xmaxPTE.setMaximumSize(QtCore.QSize(20, 30))
        self.xmaxPTE.setObjectName(_fromUtf8("xmaxPTE"))
        self.horizontalLayout_3.addWidget(self.xmaxPTE)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem2)
        self.horizontalLayout_6.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.yminLabel = QtGui.QLabel(self.centralwidget)
        self.yminLabel.setObjectName(_fromUtf8("yminLabel"))
        self.horizontalLayout_4.addWidget(self.yminLabel)
        self.yminPTE = QtGui.QPlainTextEdit(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.yminPTE.sizePolicy().hasHeightForWidth())
        self.yminPTE.setSizePolicy(sizePolicy)
        self.yminPTE.setMinimumSize(QtCore.QSize(100, 20))
        self.yminPTE.setMaximumSize(QtCore.QSize(20, 30))
        self.yminPTE.setObjectName(_fromUtf8("yminPTE"))
        self.horizontalLayout_4.addWidget(self.yminPTE)
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem3)
        self.horizontalLayout_6.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.ymax_Label = QtGui.QLabel(self.centralwidget)
        self.ymax_Label.setObjectName(_fromUtf8("ymax_Label"))
        self.horizontalLayout_5.addWidget(self.ymax_Label)
        self.ymaxPTE = QtGui.QPlainTextEdit(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ymaxPTE.sizePolicy().hasHeightForWidth())
        self.ymaxPTE.setSizePolicy(sizePolicy)
        self.ymaxPTE.setMinimumSize(QtCore.QSize(100, 20))
        self.ymaxPTE.setMaximumSize(QtCore.QSize(20, 30))
        self.ymaxPTE.setObjectName(_fromUtf8("ymaxPTE"))
        self.horizontalLayout_5.addWidget(self.ymaxPTE)
        spacerItem4 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem4)
        self.horizontalLayout_6.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_8.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_7 = QtGui.QHBoxLayout()
        self.horizontalLayout_7.setContentsMargins(0, -1, 0, -1)
        self.horizontalLayout_7.setObjectName(_fromUtf8("horizontalLayout_7"))
        self.plotButton = QtGui.QPushButton(self.centralwidget)
        self.plotButton.setMaximumSize(QtCore.QSize(190, 25))
        self.plotButton.setFlat(False)
        self.plotButton.setObjectName(_fromUtf8("plotButton"))
        self.horizontalLayout_7.addWidget(self.plotButton)
        self.defaultsButton = QtGui.QPushButton(self.centralwidget)
        self.defaultsButton.setMaximumSize(QtCore.QSize(190, 25))
        self.defaultsButton.setObjectName(_fromUtf8("defaultsButton"))
        self.horizontalLayout_7.addWidget(self.defaultsButton)
        self.saveButton = QtGui.QPushButton(self.centralwidget)
        self.saveButton.setMaximumSize(QtCore.QSize(190, 25))
        self.saveButton.setObjectName(_fromUtf8("saveButton"))
        self.horizontalLayout_7.addWidget(self.saveButton)
        self.exitButton = QtGui.QPushButton(self.centralwidget)
        self.exitButton.setMaximumSize(QtCore.QSize(190, 25))
        self.exitButton.setObjectName(_fromUtf8("exitButton"))
        self.horizontalLayout_7.addWidget(self.exitButton)
        self.horizontalLayout_8.addLayout(self.horizontalLayout_7)
        self.verticalLayout.addLayout(self.horizontalLayout_8)
        self.fractalView = fractalView(self.centralwidget)
        self.fractalView.setEnabled(True)
        self.fractalView.setMinimumSize(QtCore.QSize(1280, 1024))
        self.fractalView.setMaximumSize(QtCore.QSize(2000, 1500))
        self.fractalView.setObjectName(_fromUtf8("fractalView"))
        self.verticalLayout.addWidget(self.fractalView)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.actionExit = QtGui.QAction(MainWindow)
        self.actionExit.setObjectName(_fromUtf8("actionExit"))
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "PyBrot", None))
        self.iterationsLabel.setText(_translate("MainWindow", "Iterations:", None))
        self.xminLabel.setText(_translate("MainWindow", "Xmin: ", None))
        self.xmaxLabel.setText(_translate("MainWindow", "Xmax:", None))
        self.yminLabel.setText(_translate("MainWindow", "Ymin:", None))
        self.ymax_Label.setText(_translate("MainWindow", "Ymax:", None))
        self.plotButton.setText(_translate("MainWindow", "Plot", None))
        self.defaultsButton.setText(_translate("MainWindow", "Defaults", None))
        self.saveButton.setText(_translate("MainWindow", "Save", None))
        self.exitButton.setText(_translate("MainWindow", "Exit", None))
        self.actionExit.setText(_translate("MainWindow", "Exit", None))
#----------------------------------------------------------------------

#Child Class extension to capture mouse wheel events
class fractalView(QtGui.QGraphicsView):
	
	def wheelEvent(self, event):
        
		moose = event.delta()/120
		if moose > 0:
			form.zoomIn()
		elif moose < 0:
			form.zoomOut()
	
#Child Class extension of QGraphicsScene to capture mouse double click
#events which will determine new center position and range to calculate
#mandelbrot set
class fractalScene(QtGui.QGraphicsScene):
		
	#The most important event!
	def mouseDoubleClickEvent(self, event):	
		#current middle x coord		
		tx = form.x[1]-(form.xrng/2)
		
		#current middle y coord 
		ty = form.y[1]-(form.yrng/2) 
		
		#double click point in the scene (x value)		
		xpp = form.x[1]-(form.xrng/form.imgw)*event.scenePos().x()
		
		#xnc is required due to how the GraphicsView is anchored
		#points are drawn from top left to buttom right, so the X 
		#coordinates are unintentionally mirrored.  This is resolved
		#here albeit manually
		xnc = tx-(xpp-tx)
		
		#double click point in the scene (y value)
		ypp = form.y[1]-(form.yrng/form.imgh)*event.scenePos().y()
				
		#NOTE: new center point (xpp, ypp)
		
		#determine new max and min ranges based on new middle point
		#and reset the current level of zoom
		form.xrng = form.xrng/form.zoom
		form.x[1] = xnc+(form.xrng/2)
		form.x[0] = form.x[1]-form.xrng
		form.yrng = form.yrng/form.zoom
		form.y[1] = ypp+(form.yrng/2)
		form.y[0] = form.y[1]-form.yrng
		form.zoom=1
		
		#Redraw
		form.fractalRedraw()
		form.updateView()

#Child class extension of QDesigner generated QMainWindow
#and it holds all the nuts and bolts
class FractalsApp(QtGui.QMainWindow, Ui_MainWindow):
	#default conditions - can be changed if desired as program will not
	#"zoom out" further than these values. 
	#Note: maxiter is just the default value to reset to.  Name max was
	#more of a naming convention
	maxiter = 40
	minx = -2.13
	maxx = 0.77
	miny = -1.3
	maxy = 1.3
	maxyr = maxy-miny
	maxxr = maxx-minx
	
	def __init__(self):
		super(self.__class__, self).__init__()
		self.setupUi(self)
		self.getScreenRes()		#Program always starts full screen
		self.imgw = self.fractalView.width()
		self.imgh = self.fractalView.height()
		
		self.scene = fractalScene(self)
		self.fractalView.setScene(self.scene)
		
		#Make the view more immersive by removing scroll bars
		self.fractalView.setDragMode(QtGui.QGraphicsView.ScrollHandDrag)
		self.fractalView.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
		self.fractalView.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
		
		#Initialize a new fractal image based on default values
		self.view_reset()
		
		#Give buttons some functionality
		self.defaultsButton.clicked.connect(self.view_reset)
		self.saveButton.clicked.connect(self.saveCurrentFractal)
		self.plotButton.clicked.connect(self.nplot)
		self.exitButton.clicked.connect(self.close)		
	
	#default is to open the window as full screen and set the 
	#image viewer to the same resolution as the desktop.  This allows
	#some added scrolling area left and right from the start and
	#ensures the user will save a fractal image the size of their
	#desktop resolution.
	#Note: If a max resolution is required, this method can be replaced
	#or modified with one that allows for custom resolutions
	def getScreenRes(self):
		self.screen_res = app.desktop().availableGeometry()
		self.screenw = self.screen_res.width()
		self.screenh = self.screen_res.height()
		self.setMaximumSize(QtCore.QSize(self.screenw, self.screenh))
		self.fractalView.setMaximumSize(QtCore.QSize(self.screenw, self.screenh))
		self.resize(QtCore.QSize(self.screenw, self.screenh))
		self.fractalView.resize(QtCore.QSize(self.screenw, self.screenh))
		
	
	#New plot based on values in the PlainText input boxes
	def nplot(self):
		self.x=[float(self.xminPTE.toPlainText()),float(self.xmaxPTE.toPlainText())]
		self.y=[float(self.yminPTE.toPlainText()),float(self.ymaxPTE.toPlainText())]
		self.citer = int(self.iterationsPTE.toPlainText())
		self.fractalRedraw()
		self.updateView()
	
	#Save to file
	#Filename is defaulted to a text string of the values of
	#Iterations, xmin, xmax, ymin, and ymax should a user want to
	#recreate the area in the image.  However, this can be changed here
	#or added as a dialog box to give more customization
	def saveCurrentFractal(self):
		fname = "./Fractal_iter-"+str(self.citer)
		fname = fname+"_xmin-"+str("%.6f" % self.x[0])
		fname = fname+"_xmax-"+str("%.6f" % self.x[0])
		fname = fname+"_ymin-"+str("%.6f" % self.x[0])
		fname = fname+"_ymax-"+str("%.6f" % self.x[0])
		fname = fname+".tiff"
		self.img.save(fname,format="tiff")
	
	#Reset the fractal to the default values defined at the start
	#of the class
	def view_reset(self):
		self.x=[self.minx,self.maxx]
		self.y=[self.miny,self.maxy]
		self.citer = self.maxiter
		self.zoom = 1.0
		self.xrng = self.maxxr
		self.yrng = self.maxyr		
		self.resetScroll()
		self.fractalRedraw()
		self.updateView()		
		
	def resetScroll(self):
		self.fractalView.verticalScrollBar().setValue(0)
		self.fractalView.horizontalScrollBar().setValue(0)
        
	#duh
	def zoomReset(self):
		self.zoom = 1
		self.x=[self.minx,self.maxx]
		self.y=[self.miny,self.maxy]
		self.updateView()
	
	#duh
	def zoomIn(self):
		self.zoom *= 1.05
		self.updateView()
    
    	#duh, however, allows one to zoom out further than the image, but
    	#not to exceed the default values
    	#one must double click in order to recalculate otherwise the image
   	 #will remain surrounded by whitespace    
	def zoomOut(self):
		self.zoom /= 1.05
		if self.x[0] < self.minx or self.x[1] > self.maxx or self.y[1] > self.maxy or self.y[0] < self.miny: 
			self.zoom = 1
			self.x=[self.minx,self.maxx]
			self.y=[self.miny,self.maxy]
		self.updateView()	
   
   	#Used to transform the QGraphicsView when zooming
	def updateView(self):
		
		self.fractalView.setTransform(QtGui.QTransform().scale(self.zoom, self.zoom))
    
    	#fractalRedraw controls the creation of a fractal image by creating
    	#"drawing" a new fractal, creating an image from the array
    	#containing said fractal, and applying a palette to it.
    	#Finally, this method also updates the text boxes with the current
    	#values should the method be called from a doubleclick event
	def fractalRedraw(self):
		self.draw(self.x[0], self.x[1], self.y[0], self.y[1])
		self.img = Image.fromarray(self.mandel)
		palette = [i for rgb in ((j, 0, 0) for j in range(255)) for i in rgb]
		self.img.putpalette(palette)
		self.image = QtGui.QImage()
		output=StringIO.StringIO()
		self.img.save(output, format="tiff")		
		self.image.loadFromData(output.getvalue())
		self.pix = QtGui.QPixmap.fromImage(self.image)
		self.scene.addPixmap(self.pix)	
		output.close()
		self.iterationsPTE.setPlainText(str(self.citer))
		self.xminPTE.setPlainText(str("%.6f" % self.x[0]))
		self.xmaxPTE.setPlainText(str("%.6f" % self.x[1]))
		self.yminPTE.setPlainText(str("%.6f" % self.y[0]))
		self.ymaxPTE.setPlainText(str("%.6f" % self.y[1]))		
        
		
	#OpenCL code to calculate mandelbrot set
	def calc_fractal_opencl(self,q, maxiter):
		ctx = cl.create_some_context(interactive=False)
		queue = cl.CommandQueue(ctx)

		output = np.empty(q.shape, dtype=np.uint16)

		mf = cl.mem_flags
		q_opencl = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=q)
		output_opencl = cl.Buffer(ctx, mf.WRITE_ONLY, output.nbytes)

		prg = cl.Program(ctx, """
		#pragma OPENCL EXTENSION cl_khr_byte_addressable_store : enable
		__kernel void mandelbrot(__global float2 *q,
						__global ushort *output, ushort const maxiter)
		{
			int gid = get_global_id(0);
			float nreal, real = 0;
			float imag = 0;
			output[gid] = 0;
			for(int curiter = 0; curiter < maxiter; curiter++) {
				nreal = real*real - imag*imag + q[gid].x;
				imag = 2* real*imag + q[gid].y;
				real = nreal;
				if (real*real + imag*imag > 4.0f)
					output[gid] = curiter;
			}
		}
		""").build()

		prg.mandelbrot(queue, output.shape, None, q_opencl, 
		output_opencl, np.uint16(maxiter))

		cl.enqueue_copy(queue, output, output_opencl).wait()

		return output
	
	#Draw creates the array that stores the fractal.  One can think of
	#it as a stencil that has yet to be colored.
	def draw(self, x1, x2, y1, y2):
		# Generate complex array q for calculation in OpenCL
		xx = np.arange(x1, x2, (x2-x1)/self.imgw)
		yy = np.arange(y2, y1, (y1-y2)/self.imgh) * 1j
		
		#Generate a 1D array of complex numbers
		q = np.ravel(xx+yy[:, np.newaxis]).astype(np.complex64)

		output = self.calc_fractal_opencl(q, self.citer)
		
		#make sure array is not larger than scene dimensions.
		#If it is, shrink it
		size = self.imgw*self.imgh
		if(size < output.shape[0]):
			diff = size-output.shape[0]
			output=output[:diff]
			 
		#take output from OpenCL and reshape it into a array of the form (height, width)
		#note: values here are saved as uint8, however, this can be altered to float values
		#for more advanced color palette designs
		self.mandel = (output.reshape((self.imgh, self.imgw)) / float(output.max()) * 255.).astype(np.uint8)
    
#Start app
app = QtGui.QApplication(sys.argv)
form = FractalsApp()
form.show()
app.exec_()
