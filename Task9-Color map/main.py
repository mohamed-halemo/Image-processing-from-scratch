from matplotlib.backend_bases import MouseEvent
from scipy.fftpack import fft2, ifft2, fftshift, ifftshift
from PyQt5.QtWidgets import QFrame, QMainWindow, QMessageBox, QDesktopWidget
import math
from math import sqrt, floor, ceil
import numpy as np
from matplotlib.figure import Figure
import struct
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT as Navi
from pydicom.data import get_testdata_files
import matplotlib.animation as animation
from PyQt5 import QtWidgets, QtGui, QtCore
from matplotlib.colors import Normalize
from numpy.core.fromnumeric import shape, size
from GuiT9 import Ui_MainWindow
import sys
from PyQt5.QtGui import *
from PIL import Image, ImageColor, ExifTags
import os
import matplotlib
from numpy import asarray, number, sign, uint8,random
import cv2
import matplotlib.pyplot as plt
import pyqtgraph as pg
import pydicom
matplotlib.use('Qt5Agg')
import ROI as roi # ROI_class.py
from skimage.data import shepp_logan_phantom
from skimage.transform import radon, rescale,iradon
from matplotlib.widgets  import RectangleSelector
import matplotlib.image as mpimg
class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(ApplicationWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # self.center()
        self.Browser = self.ui.Browse
        self.OutputImage = self.ui.Image
        self.Info = self.ui.Info
        # self.Info.setFrameShape(QFrame.Panel)
        self.ShowBtn = self.ui.ShowPixels
        self.Tab2OutPut = self.ui.Tab2Label
        self.GenerateBTN = self.ui.GenerateBtn
        self.ShowBtn.clicked.connect(self.ShowPixels)
        self.Browser.clicked.connect(self.Browse)
        self.GenerateBTN.clicked.connect(self.Generate)
        self.fig2, self.ax2 = plt.subplots(1, 1)
        self.lay2 = QtWidgets.QVBoxLayout(self.Tab2OutPut)

        self.fig, self.ax1 = plt.subplots(1, 1)
        self.fig.subplots_adjust(
            left=0, bottom=0, right=1, top=1, wspace=None, hspace=None)

        self.lay = QtWidgets.QVBoxLayout(self.OutputImage)

        self.plotWidget2 = FigureCanvas(self.fig2)
        # self.lay2.addWidget(self.plotWidget2)

        self.msg = QMessageBox()
        self.msg.setWindowTitle("Error")
        self.Bool = 0
        self.Bool2 = 1
        self.filename = 'none'
        self.KNNBTN = self.ui.KNNBtn
        self.BilinearBTN = self.ui.BilinearBtn
        self.ZoomOutput = self.ui.ZoomLabel
        self.KNNBTN.clicked.connect(self.showKNN)
        self.GrayScaled = []
        self.fig3, self.ax3 = plt.subplots(1, 1)
        self.lay3 = QtWidgets.QVBoxLayout(self.ZoomOutput)
        self.plotWidget3 = FigureCanvas(self.fig3)
        self.lay3.addWidget(self.plotWidget3)
        # self.ax3.axis([0,1000,500,0])

        self.ZoomFactorInput = self.ui.ZoomFactor
        self.BilinearBTN.clicked.connect(self.ShowBilinear)
        self.fix_img = 0
        self.EqualizeHistogramBtn = self.ui.EqualizeHBtn
        self.EqualizedImage = self.ui.EqualizedImage
        self.NormalizedHistoGram = self.ui.NormalizedH
        self.NormalizationOfEqualized = self.ui.EqaulizedH_N
        self.imageUsedInNormalization = []

        self.EqualizeHistogramBtn.clicked.connect(self.EqualizedHistogram)
        self.fig4, self.ax4 = plt.subplots(1, 1)
        self.lay4 = QtWidgets.QVBoxLayout(self.NormalizedHistoGram)
        self.plotWidget4 = FigureCanvas(self.fig4)
        self.lay4.addWidget(self.plotWidget4)
        self.fig5, self.ax5 = plt.subplots(1, 1)
        self.lay5 = QtWidgets.QVBoxLayout(self.NormalizationOfEqualized)
        self.plotWidget5 = FigureCanvas(self.fig5)
        self.lay5.addWidget(self.plotWidget5)
        self.fig6, self.ax6 = plt.subplots(1, 1)
        self.lay6 = QtWidgets.QVBoxLayout(self.EqualizedImage)
        self.plotWidget6 = FigureCanvas(self.fig6)
        self.lay6.addWidget(self.plotWidget6)
        self.Histogram = []
        self.im = []

        self.Image_Enahnced = self.ui.Image_Enahnced
        self.figEnhanced, self.axEnhanced = plt.subplots(1, 1)
        self.figEnhanced.subplots_adjust(
            left=0, bottom=0, right=1, top=1, wspace=None, hspace=None)
        self.layEnhanced = QtWidgets.QVBoxLayout(self.Image_Enahnced)
        self.BoolEnhanced = 0
        self.KernelSize = self.ui.KernelSize
        self.EnhanceFactor = self.ui.FactorValue
        self.EnhanceBtn = self.ui.Enhance_BTN
        self.EnhanceBtn.clicked.connect(self.convolve2D)
        self.Magnitude = self.ui.Magnitude
        self.phase = self.ui.Phase
        self.Image_FourierTab = self.ui.Image_FourierTab
        self.figMagnitude, self.axMagnitude = plt.subplots(1, 1)
        self.layMagnitude = QtWidgets.QVBoxLayout(self.Magnitude)
        self.plotWidgetMagnitude = FigureCanvas(self.figMagnitude)
        self.layMagnitude.addWidget(self.plotWidgetMagnitude)
        self.figPhase, self.axPhase = plt.subplots(1, 1)
        self.layPhase = QtWidgets.QVBoxLayout(self.phase)
        self.plotWidgetPhase = FigureCanvas(self.figPhase)
        self.layPhase.addWidget(self.plotWidgetPhase)
        self.figImgFourierTab, self.axImgFourierTab = plt.subplots(1, 1)
        self.layImgFourierTab = QtWidgets.QVBoxLayout(self.Image_FourierTab)
        self.plotWidgetImgFourierTab = FigureCanvas(self.figImgFourierTab)
        self.layImgFourierTab.addWidget(self.plotWidgetImgFourierTab)
        self.FourierBtn = self.ui.Fourier
        self.FourierBtn.clicked.connect(self.Fourier)
        self.Image_FurierFilter = self.ui.Fourier_Filter_Image
        self.figFourierFilter, self.axFourierFilter = plt.subplots(1, 1)
        self.layFourierFilter = QtWidgets.QVBoxLayout(self.Image_FurierFilter)
        self.BoolFourierFiltered = 0
        self.Fourier_FilterBTN = self.ui.Fourier_FilterBTN
        self.Fourier_FilterBTN.clicked.connect(self.FourierLPF)
        self.BoolSubtraction = 0
        self.Subtraction_Image = self.ui.Foruier_Spacila
        self.figSubtraction, self.axSubtraction = plt.subplots(1, 1)
        self.laySubtraction = QtWidgets.QVBoxLayout(self.Subtraction_Image)
        self.BOOL_Blured = 0
        # self.figSubtraction.subplots_adjust(
        #     left=0, bottom=0, right=1, top=1, wspace=None, hspace=None)
        self.figFourierFilter.subplots_adjust(
            left=0, bottom=0, right=1, top=1, wspace=None, hspace=None)

        # self.figMagnitude.subplots_adjust(left=0,bottom=0,right=1,top=1,wspace=None,hspace=None)
        # self.figPhase.subplots_adjust(left=0,bottom=0,right=1,top=1,wspace=None,hspace=None)
        # self.figImgFourierTab.subplots_adjust(left=0,bottom=0,right=1,top=1,wspace=None,hspace=None)
        self.Created_Image=self.ui.Image_Created
        self.fig_C, self.ax_C = plt.subplots(1, 1)
        self.lay_C = QtWidgets.QVBoxLayout(self.Created_Image)
        self.plotWidget_C = FigureCanvas(self.fig_C)
        self.lay_C.addWidget(self.plotWidget_C)
        self.DrawImage()
        self.Noisy_Image=self.ui.Image_Noisy
        self.fig_N,self.ax_N=plt.subplots(1,1)
        self.lay_N = QtWidgets.QVBoxLayout(self.Noisy_Image)
        self.ui.Gausian_Noise_BTN.clicked.connect(self.GusianNoise)
        self.BoolNoise=0
        self.ui.Uniform_Noise_BTN_2.clicked.connect(self.UniformNoise)
        self.ui.Draw_Region_BTN.clicked.connect(self.draw_map_Callback)
        self.ui.Choose_Region_BTN.clicked.connect(self.choose_roi)
        self.ROI_Histogram=self.ui.ROI_Histogram
        self.fig_ROI,self.ax_ROI=plt.subplots(1,1)
        self.lay_ROI = QtWidgets.QVBoxLayout(self.ROI_Histogram)
        self.BoolROI=0
        self.ui.Salt_Pepper_BTN.clicked.connect(self.Salt_Pepper)
        # self.selection = QtGui.QDragMoveEvent(QtGui.QRubberBand.Rectangle, self)
        self.boolPepper=0
        self.fig_phantom,self.ax_phantom=plt.subplots(1,1)
        self.lay_phantom = QtWidgets.QVBoxLayout(self.ui.Image_Phantom)
        self.plotWidget_Phantom = FigureCanvas(self.fig_phantom)
        self.lay_phantom.addWidget(self.plotWidget_Phantom)

        self.fig_sinogram,self.ax_sinogram=plt.subplots(1,1)
        self.lay_sinogram = QtWidgets.QVBoxLayout(self.ui.Image_SinoGram)
        self.plotWidget_sinogram = FigureCanvas(self.fig_sinogram)
        self.lay_sinogram.addWidget(self.plotWidget_sinogram)
        # self.SinoGram()
        self.fig_laminogram,self.ax_laminogram=plt.subplots(1,1)
        self.lay_laminogram = QtWidgets.QVBoxLayout(self.ui.Image_LaminoGram)
        self.BoolLaminogram=0
        self.ui.Lamino_NoFilterBTN.clicked.connect(lambda:self.laminogram(0))
        self.ui.Lamino_4anglesBTN.clicked.connect(lambda:self.laminogram(1))
        self.ui.Lamino_HammingBTN.clicked.connect(lambda:self.laminogram(2))
        self.ui.Lamino_RamlakBTN.clicked.connect(lambda:self.laminogram(3))
        self.fig_UnColored,self.ax_UnColored=plt.subplots(1,1)
        self.lay_UnColored = QtWidgets.QVBoxLayout(self.ui.Image_BeforeColor)
        self.plotWidget_UnColored = FigureCanvas(self.fig_UnColored)
        self.lay_UnColored.addWidget(self.plotWidget_UnColored)
        # self.DrawUnColored()
        self.fig_Colored,self.ax_Colored=plt.subplots(1,1)
        self.lay_Colored = QtWidgets.QVBoxLayout(self.ui.Image_Colored)
        self.BoolColored=0
        
        self.rs = RectangleSelector( self.ax_UnColored, self.line_select_callback,
                       drawtype='box', useblit=False, button=[1], 
                       minspanx=5, minspany=5, spancoords='pixels', 
                       interactive=True)
        self.DrawUnColored()
    def Browse(self):
        FileName = QtWidgets.QFileDialog.getOpenFileName(self, "Open File", "E:\\Year3 Term1\\Image Processing\\Task7-Noise",
                                                         "All Files (*);;PNG Files (*.png);;Tif Files (*.tif);;Jpg Files(*.jpg);; Bmp Files(*.bmp)")
        self.filename = FileName
        filename, file_extension = os.path.splitext(FileName[0])

        if(file_extension == '.dcm' or file_extension == '.DCM'):
            try:

                if self.Bool == 0:
                    self.plotWidget = FigureCanvas(self.fig)
                self.Bool = 1
                self.OutputImage.clear()
                ds = pydicom.dcmread(FileName[0])
                dsInfo = pydicom.read_file(FileName[0])

                # print(dir(dsInfo))
                # print(str(ds))
                self.lay.addWidget(self.plotWidget)
                im = Image.fromarray(ds.pixel_array)

                numpydata = asarray(im)
                channels2 = len(numpydata.shape)
                print(str(channels2)+"pilo")

                depth = ds.pixel_array.dtype
    ########################################################
                depth2 = dsInfo.BitsStored
                maxval = ds.pixel_array.max()
                minval = ds.pixel_array.min()
                print(maxval)
                print("inbetween")
                print(minval)
                # for i in range(len(ds.pixel_array)):
                #     ds.pixel_array[i]=((maxval-ds.pixel_array[i])/(maxval-minval))*255
                array1 = ((ds.pixel_array-minval)/(maxval-minval))*255
                maxval1 = ds.pixel_array.max()
                minval1 = ds.pixel_array.min()
                print(maxval1)
                print("inbetween")
                print(minval1)
    ############################################################
                self.show()

                self.ax1.imshow(array1, cmap='gray')
                self.fig.canvas.draw()
                self.fig.canvas.flush_events()
                self.ax1.get_xaxis().set_visible(False)
                self.ax1.get_yaxis().set_visible(False)
                self.ax1.axis("off")

                try:
                    self.INFO1 = dsInfo.PatientName
                except:
                    self.INFO1 = "not Avialabe"
                try:
                    self.INFO2 = dsInfo.PatientAge
                except:
                    self.INFO2 = "not Avialabe"
                try:
                    self.INFO3 = dsInfo.Modality
                except:
                    self.INFO3 = "not Avialabe"
                try:
                    self.INFO4 = dsInfo.BodyPartExamined
                except:
                    self.INFO4 = "not Avialabe"

                self.Info.setText("Name :"+str(self.INFO1)+" \n AGE: "+str(self.INFO2)+"\n Modality: "+str(self.INFO3)+"\n PartExamined: "+str(self.INFO4)+",\n Size: "+str(
                    dsInfo.__sizeof__()) + "\n width:"+str(im.width)+"\n height:" + str(im.height)+"\n depth: "+str(depth2) + "\n Size: "+str(os.stat(FileName[0]).st_size*8)+"bit "+"\n Colors :Grey")

            except:
                self.msg.setText("That DCM Image is corrupted!")
                self.msg.exec_()
        ####
        elif(file_extension == '.jpg' or file_extension == '.bmp' or file_extension == '.png' or file_extension == '.jpeg'):
            # try:
            # self.Bool=0
            # self.fig.set_visible(False)
            # self.fig.canvas.draw()
            # self.fig.canvas.close()
            # self.OutputImage.clear()
            # ###################

            if self.Bool == 0:
                self.plotWidget = FigureCanvas(self.fig)
            self.Bool = 1
            self.lay.addWidget(self.plotWidget)

            self.pixmap = QPixmap(FileName[0])
            im = Image.open(FileName[0])
            pixels = im.width*im.height

            #task3#####################################################
            # self.GaussianBlurImage(im,4)
            self.im = im
            im = im.convert("L")  # Convert photo to gray scale
            im = np.asarray(im)  # Convert variable type to numpy array

            self.imageUsedInNormalization = im

            ############################################################
            img = cv2.imread(FileName[0])
            fix_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            self.fix_img = fix_img
            R, G, B = fix_img[:, :, 0], fix_img[:, :, 1], fix_img[:, :, 2]
            Y = 0.299 * R + 0.587 * G + 0.114 * B
            self.fig.canvas.draw()
            self.ax1.get_xaxis().set_visible(False)
            self.ax1.get_yaxis().set_visible(False)
            self.ax1.axis("off")
            self.ax1.imshow(Y, cmap='gray')

            self.show()
            self.GrayScaled = Y

            self.fig.canvas.draw()
######################################
            numpydata = asarray(im)
            channels2 = len(numpydata.shape)
            depth = numpydata.dtype
            H = self.OutputImage.height()
            w = self.OutputImage.width()
            self.pix1 = self.pixmap.scaled(H, w, QtCore.Qt.KeepAspectRatio)
            ####
            size = os.stat(FileName[0]).st_size*8
            bitsnum = len(im.tobytes())*8

            depthreal = bitsnum/pixels
            # # self.OutputImage.setPixmap(self.pix1)
            # if(channels2==3):
            #     InfoColor="RGB"
            # else:
            #     InfoColor="Grey Scaled"
            # if(depth!="bool"):
            #     self.Info.setText("width:"+str(im.width)+"\nheight:" +str(im.height)+"\ndepth:"+str(depthreal)+ "\nSize:"+str(os.stat(FileName[0]).st_size*8)+"bit "+"\nColors " +str(InfoColor)  )
            # else:
            #     self.Info.setText("width:"+str(im.width)+" \nheight:" +str(im.height)+" \ndepth: =1"+ "\nSize: "+str(os.stat(FileName[0]).st_size*8)+"bit "+"\nColors " +"Binary Scaled"  )
            # except:
            # self.msg.setText("That  Image is corrupted!")
            # self.msg.exec_()
        else:
            self.msg.setText("Please Pick an Image!")
            self.msg.exec_()


    def RGBTOGRAY(self,image):
        fix_img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        self.fix_img = fix_img
        R, G, B = fix_img[:, :, 0], fix_img[:, :, 1], fix_img[:, :, 2]
        Y = 0.299 * R + 0.587 * G + 0.114 * B
        return Y
    
    def DrawUnColored(self):
        self.Original1 = mpimg.imread('US Image.jpeg')
        self.img_US1= cv2.imread('US Image.jpeg')
        self.Original1=self.RGBTOGRAY(self.Original1)
       
        self.ax_UnColored.imshow(self.Original1,cmap='gray')
       
    def cleargraph(self):
        self.ax_Colored.clear()
        self.fig_Colored.canvas.close()
        self.BoolColored=0
    def line_select_callback(self,eclick, erelease):
        self.Original = mpimg.imread('US Image.jpeg')
        self.img_US= cv2.imread('US Image.jpeg')
        self.Original=self.RGBTOGRAY(self.Original)
       
        #getting region of interest 
        if self.BoolColored==0:
                self.plotWidget_Colored = FigureCanvas(self.fig_Colored)
        self.BoolColored=1
        self.lay_Colored.addWidget(self.plotWidget_Colored)

        x1, y1 = eclick.xdata, eclick.ydata
        x2, y2 = erelease.xdata, erelease.ydata

        rect = plt.Rectangle( (min(x1,x2),min(y1,y2)), np.abs(x1-x2), np.abs(y1-y2) )
        self.ax_UnColored.add_patch(rect)
        rect.remove()
        x1=round(x1)
        y1=round(y1)
        x2=round(x2)
        y2=round(y2)
        self.imgUnColored=self.Original
        imgpadded=np.zeros([744,984])
        imgpadded[(25//2):-(25//2),(25//2):-(25//2)]=self.imgUnColored
        imgpadded[y1:y2,x1:x2]=self.imgUnColored[y1:y2,x1:x2]
        for i in range(y1,y2):
            for j in range(x1,x2):
                kernel= imgpadded[int(i)-12:int(i+12),int(j)-12:int(12+j)]
                summation=np.sum(kernel)
                mean = summation /len(kernel)
                sqDiff=0
                sqDiff = ((kernel - mean)
                    * (kernel - mean))
                sqDiff=np.sum(sqDiff)
                Sigma=sqDiff/len(kernel)
                self.imgUnColored[i,j]=Sigma
        self.imgUnColored=255*((self.imgUnColored-self.imgUnColored.min())/(self.imgUnColored.max()-self.imgUnColored.min()))
        Colored=np.zeros((721, 961, 3))
        for i in range (self.imgUnColored.shape[0]):
            for j in range(self.imgUnColored.shape[1]):
                Colored[i,j,0]=self.imgUnColored[i,j]
                Colored[i,j,1]=self.imgUnColored[i,j]
                Colored[i,j,2]=self.imgUnColored[i,j]
        Colored=Colored.astype('uint8')
        self.img_US=self.img_US.astype('uint8')
        # self.imgUnColored2=self.imgUnColored.astype('uint8')
        self.img_UScopy=self.img_US
        self.imgUnColored2=Colored
        self.imgUnColored2=cv2.applyColorMap(self.imgUnColored2,cv2.COLORMAP_JET)
        self.imgUnColored2=cv2.cvtColor(self.imgUnColored2,cv2.COLOR_RGB2BGR)
        self.img_UScopy[y1:y2,x1:x2]=self.imgUnColored2[y1:y2,x1:x2]
        self.fig_Colored.canvas.draw()
        
        self.ax_Colored.imshow(self.img_UScopy)
        self.fig_Colored.canvas.draw()

    def SinoGram(self):
        

       
        image = shepp_logan_phantom() #400,400
        image = rescale(image, scale=0.68, mode='reflect')
        
        self.ax_phantom.set_title("Original")
        self.ax_phantom.imshow(image, cmap=plt.cm.Greys_r)

        theta = np.linspace(0., 180., max(image.shape), endpoint=False) # number of samples to be generated
        theta2 = np.arange(0,160,20)
        sinogram = radon(image, theta=theta)
        sinogram2 = radon(image, theta=theta2)
        dx, dy = 0.5 * 180.0 / max(image.shape), 0.5 / sinogram.shape[0]
        self.ax_sinogram.set_title("Radon transform\n(Sinogram)")
        self.ax_sinogram.set_xlabel("Projection angle (deg)")
        self.ax_sinogram.set_ylabel("Projection position (pixels)")
        self.ax_sinogram.imshow(sinogram, cmap=plt.cm.Greys_r,
                extent=(-dx, 180.0 + dx, -dy, sinogram.shape[0] + dy),
                aspect='auto')

        self.phantom=image
        self.sinogram=sinogram
        self.sinogram2=sinogram2
    def laminogram(self,choose):
        self.ax_laminogram.clear()
        if self.BoolLaminogram==0:
            self.plotWidget_laminogram = FigureCanvas(self.fig_laminogram)
        self.BoolLaminogram=1
        self.lay_laminogram.addWidget(self.plotWidget_laminogram)

        image=self.phantom
        sinogram=self.sinogram
        if choose==0:
            theta = np.linspace(0, 180, max(image.shape), endpoint=False,dtype=np.uint8) # number of samples to be generated
            reconstruction_fbp = iradon(sinogram, theta=theta, filter_name=None)

        elif choose==1:
            theta = np.arange(0,160,20) # number of samples to be generated
            sinogram=self.sinogram2
            reconstruction_fbp = iradon(sinogram, theta=theta, filter_name=None)

        elif choose==2:
            theta = np.linspace(0, 180, max(image.shape), endpoint=False,dtype=np.uint8) # number of samples to be generated
            reconstruction_fbp = iradon(sinogram, theta=theta, filter_name="hamming")

        elif choose==3:
            theta = np.linspace(0, 180, max(image.shape), endpoint=False,dtype=np.uint8) # number of samples to be generated
            reconstruction_fbp = iradon(sinogram, theta=theta, filter_name="ramp")

        imkwargs = dict(vmin=-0.2, vmax=0.2)

        self.fig_laminogram.canvas.draw()
        self.ax_laminogram.set_title("Reconstruction\nFiltered back projection")
        self.ax_laminogram.imshow(reconstruction_fbp, cmap=plt.cm.Greys_r)
        self.fig_laminogram.canvas.draw()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

   
    def draw_map_Callback(self):    
        try:    
            self.ax_ROI.clear()
            if self.BoolROI==0:
                self.plotWidget_ROI = FigureCanvas(self.fig_ROI)
            self.BoolROI=1
            self.lay_ROI.addWidget(self.plotWidget_ROI)

            self.y.disconnect()
            self.y.disconnect()
            self.y.remove()
            count=0
            self.mask=self.y.get_mask()
            self.mask=np.asarray(self.mask)
            self.mask.astype(uint8)
            self.coord=self.y.get_indices()
            Temp=[]
            Temp=self.NoisyImageDone
            for i in range(self.mask.shape[0]):
                for j in range(self.mask.shape[1]):
                    if self.mask[i,j]==False:
                        Temp[i,j]=False
                        count+=1
            # arr=np.where(self.NoisyImageDone!=0,self.NoisyImageDone,False)
            H,r=self.NormalizeHistogram(self.NoisyImageDone,3)
            H[0]-=count
            # if H[0]>1000 and self.boolPepper==0:
            #     H[0]=0
            summation=0
            for i in range(len(H)):
                summation+=H[i]*r[i]
            Number=sum(H)
            Mean=summation/Number
            Summation_Diff=0
            for i in range(len(H)):
                Summation_Diff+=H[i]*(r[i]-Mean)**2
            Sigma=np.sqrt(Summation_Diff/Number)
            self.ui.Mean_Sigma.setText("Mean="+str(round(Mean,2))+"\nSigma="+str(round(Sigma,2)))
            self.fig_ROI.canvas.draw()
            self.fig_ROI.canvas.draw()
            # self.ax_ROI.set_ylim(0,500)

            self.ax_ROI.bar(r, H)
            self.show()
            self.y.remove()
        except:
            self.msg.setText("Generate Noise and Choose Region first ")
            self.msg.exec_()

    def choose_roi(self):
        try:
            self.y = roi.new_ROI(self.con_img)
        except:
            self.msg.setText("Generate Noise First ")
            self.msg.exec_()

    def DrawRect(self,color,pixel):
        self.color = color
        self.pixel = pixel
        
        self.im = np.zeros((pixel,pixel,1))
        self.im[:] = color
        self.im[40:220,40:220]=color+100
        return self.im

    def add_disk(self, centroid,radius,color):
        x, y = np.meshgrid(np.arange(self.im.shape[0]), np.arange(self.im.shape[1]))
        circle_pixels = (x - centroid[0]) ** 2 + (y - centroid[1]) ** 2 <= radius ** 2
        self.im[circle_pixels] = color
        return self.im
    def DrawImage(self):
        purple = np.array([50])
        Square = self.DrawRect(purple, 256)
        white = np.array([250])
        Square=self.add_disk((128, 128), 64, white)

        self.fig_C.canvas.draw()
        self.ax_C.imshow(Square,cmap='gray')
        self.fig_C.canvas.draw()

        self.show()

   

    def Salt_Pepper(self,img):
        self.boolPepper=1
        self.ax_N.clear()
        if self.BoolNoise==0:
            self.plotWidget_N = FigureCanvas(self.fig_N)
        self.BoolNoise=1
        self.lay_N.addWidget(self.plotWidget_N)
        img=self.im
        # Getting the dimensions of the image
        row , col = img.shape[0],img.shape[1]
        
        # Randomly pick some pixels in the
        # image for coloring them white
        # Pick a random number between 300 and 10000
        number_of_pixels = random.randint(300, 10000)
        #number of pixels to be noised
        for i in range(number_of_pixels):
        
            # Pick a random y coordinate
            y_coord=random.randint(0, row - 1)
            
            # Pick a random x coordinate
            x_coord=random.randint(0, col - 1)
            
            # Color that pixel to white
            img[y_coord][x_coord] = 255
            
        # Randomly pick some pixels in
        # the image for coloring them black
        # Pick a random number between 300 and 10000
        number_of_pixels = random.randint(300 , 10000)
        for i in range(number_of_pixels):
        
            # Pick a random y coordinate
            y_coord=random.randint(0, row - 1)
            
            # Pick a random x coordinate
            x_coord=random.randint(0, col - 1)
            
            # Color that pixel to black
            img[y_coord][x_coord] = 0
        img=255*((img-img.min())/(img.max()-img.min()))
        self.fig_N.canvas.draw()
        self.NoisyImageDone=img
        self.con_img=self.ax_N.imshow(img,cmap='gray')
        self.fig_N.canvas.draw()

        self.show()

    def GusianNoise(self,image,mean=0,sigma=5):
        self.boolPepper=0

        self.ax_N.clear()
        if self.BoolNoise==0:
            self.plotWidget_N = FigureCanvas(self.fig_N)
        self.BoolNoise=1
        self.lay_N.addWidget(self.plotWidget_N)
        image=self.im
        size=image.shape
        Noise=np.random.normal(loc=mean,scale=sigma,size=size)
        Noise=255*((Noise-Noise.min())/(Noise.max()-Noise.min()))
        Noisy_Image=image+Noise
        Noisy_Image=255*((Noisy_Image-Noisy_Image.min())/(Noisy_Image.max()-Noisy_Image.min()))
        self.fig_N.canvas.draw()
        self.NoisyImageDone=Noisy_Image
        self.con_img=self.ax_N.imshow(Noisy_Image,cmap='gray')
        self.fig_N.canvas.draw()

        self.show()


    def UniformNoise(self,image,a=-10,b=10):
        self.boolPepper=0

        self.ax_N.clear()
        if self.BoolNoise==0:
            self.plotWidget_N = FigureCanvas(self.fig_N)
        self.BoolNoise=1
        self.lay_N.addWidget(self.plotWidget_N)

        image=self.im
        size=image.shape
        Noise=np.random.uniform(low=a,high=b,size=size)
        Noise=255*((Noise-Noise.min())/(Noise.max()-Noise.min()))

        NoisyImage=image+Noise
        NoisyImage=255*((NoisyImage-NoisyImage.min())/(NoisyImage.max()-NoisyImage.min()))
        self.fig_N.canvas.draw()
        self.NoisyImageDone=NoisyImage

        self.con_img=self.ax_N.imshow(NoisyImage,cmap='gray')
        self.fig_N.canvas.draw()

        self.show()


    def DrawFourierTab(self, Image, Magnitude, Phase):
        self.axMagnitude.get_xaxis().set_visible(False)
        self.axMagnitude.get_yaxis().set_visible(False)
        self.axMagnitude.axis("off")
        self.axPhase.get_xaxis().set_visible(False)
        self.axPhase.get_yaxis().set_visible(False)
        self.axPhase.axis("off")
        self.axImgFourierTab.get_xaxis().set_visible(False)
        self.axImgFourierTab.get_yaxis().set_visible(False)
        self.axImgFourierTab.axis("off")

        Image = self.GrayScaled
        self.figImgFourierTab.canvas.draw()
        self.figImgFourierTab.canvas.draw()
        self.axImgFourierTab.imshow(Image, cmap='gray')
        self.figImgFourierTab.canvas.draw()

        self.show()
        self.axMagnitude.imshow(Magnitude, cmap='gray')
        self.show()

        self.figMagnitude.canvas.draw()
        self.axPhase.imshow(Phase, cmap='gray')
        self.show()

        self.figPhase.canvas.draw()

    def Fourier(self):
        img = np.asarray(self.GrayScaled)
        dft = fft2(img)  # 2D fourier transform for the image
        FourierImg = dft
        for i in range(dft.shape[0]):
            for j in range(dft.shape[1]):
               if i<50 and j <50:
                   dft[i,j]=0
        dft = fftshift(dft)
        
        real = dft.real
        imaginary = dft.imag
        phase = np.arctan(imaginary/real)
        real = dft.real
        imaginary = dft.imag
        addition = real**2+imaginary**2
        squareroot = np.sqrt(addition)
        dft = squareroot
        magnitude = np.float32(dft)
        c = 255 / np.log(1 + np.max(magnitude))
        magnitude = c * np.log(1 + magnitude)
        magnitude = np.asarray(magnitude)
        self.axPhase.clear()
        self.axMagnitude.clear()
        self.DrawFourierTab(img, magnitude, phase)
        return FourierImg

    def FourierLPF(self):
        try:
            if self.Bool == 0:
                self.msg.setText("Browse first")
                self.msg.exec_()
            else:
                image = self.GrayScaled
                # Factor=float(self.EnhanceFactor.text())
                kernelsize = int(self.KernelSize.text())
                kernelsize2 = kernelsize*kernelsize
                print(kernelsize)
                if kernelsize % 2 == 0 or kernelsize == 1 or kernelsize2 > (image.shape[0]*image.shape[1]):
                    self.msg.setText(
                        "kernel size must be odd and greater than 1 and Factor cannot be neagtive")
                    self.msg.exec_()
                else:
                    count = 1
                    for i in range(2, kernelsize):
                        if(i % 2 != 0):
                            count += 1
                    padding = count
                    if self.BoolFourierFiltered == 0 and self.BoolSubtraction == 0:
                        self.plotWidgetFourierFilter = FigureCanvas(
                            self.figFourierFilter)
                        self.plotWidgetSubtraction = FigureCanvas(
                            self.figSubtraction)
                    self.BoolFourierFiltered
                    self.BoolSubtraction = 1
                    self.axFourierFilter.get_xaxis().set_visible(False)
                    self.axFourierFilter.get_yaxis().set_visible(False)
                    self.axFourierFilter.axis("off")
                    self.axSubtraction.get_xaxis().set_visible(False)
                    self.axSubtraction.get_yaxis().set_visible(False)
                    self.axSubtraction.axis("off")
                    self.layFourierFilter.addWidget(
                        self.plotWidgetFourierFilter)
                    self.laySubtraction.addWidget(self.plotWidgetSubtraction)
                    mag = kernelsize*kernelsize
                    kernel = np.ones((kernelsize, kernelsize))
                    kernel = kernel*1/mag

                    xImgShape, yImgShape = image.shape
                    if(yImgShape % 2 == 0):
                        image = np.vstack((image, image[xImgShape-1, :]))
                    if(xImgShape % 2 == 0):
                        image = np.c_[image, image[:, yImgShape-1]]

                    xOutput, yOutput = image.shape
                    print(image.shape)
                    xKernShape = kernel.shape[0]
                    yKernShape = kernel.shape[1]
                    imagePadded = np.zeros((xOutput, yOutput))

                    kernH = (yOutput-yKernShape+1)//2
                    kernW = (xOutput-xKernShape+1)//2
                    for i in range(kernW, kernW+xKernShape):
                        for j in range(kernH, kernH+yKernShape):
                            imagePadded[i, j] = (1/(xKernShape**2))

                    imgFourier = fft2(image)
                    kernFourier = fft2(imagePadded)
                    LPF = imgFourier*kernFourier
                    Filtered = ifft2(LPF)
                    Filtered = ifftshift(Filtered)
                    # Filtered=np.asarray(Filtered)
                    # Image.fromarray((Filtered).astype('uint8')).save('hi.png')
                    Filtered = np.abs(Filtered)
                    self.figFourierFilter.canvas.draw()
                    self.axFourierFilter.imshow(Filtered, cmap='gray')
                    self.show()
                    self.figFourierFilter.canvas.draw()
                    print(yImgShape)

                    if self.BOOL_Blured == 1:
                     
                        subtraction = self.Blured_Normal-Filtered
                        subtraction=((subtraction-subtraction.min())/(subtraction.max()-subtraction.min()))*255
                        print(subtraction)
                        self.figSubtraction.canvas.draw()
                        for i in range(subtraction.shape[0]):
                            for j in range(subtraction.shape[1]):
                                if subtraction[i,j]<=255 and subtraction[i,j] >200:
                                    subtraction[i,j]=0
                                else:
                                    subtraction[i,j]=255

                        self.axSubtraction.imshow(
                            subtraction, cmap='gray',vmin=0,vmax=256)
                        self.figSubtraction.canvas.draw()

                        self.show()
                    else:
                        self.msg.setText(
                            "Click Enhance Image First to get S Domain Filter")
                        self.msg.exec_()
        except:
            self.msg.setText("Enter Factor and kernel size first ")
            self.msg.exec_()

    def convolve2D(self, padding=1):
        try:
            if self.Bool == 0:
                self.msg.setText("Browse first")
                self.msg.exec_()
            else:
                image = self.GrayScaled
                # Factor=float(self.EnhanceFactor.text())
                kernelsize = int(self.KernelSize.text())
                kernelsize2 = kernelsize*kernelsize

                print(kernelsize)
                if kernelsize % 2 == 0 or kernelsize == 0 or kernelsize2 > (image.shape[0]*image.shape[1]):
                    self.msg.setText(
                        "kernel size must be odd and greater than 1 and Factor cannot be neagtive\n kernel size is bigger than image size")
                    self.msg.exec_()
                else:
                    count = 1
                    for i in range(2, kernelsize):
                        if(i % 2 != 0):
                            count += 1
                    padding = count
                    if self.BoolEnhanced == 0:
                        self.plotWidgetEnhanced = FigureCanvas(
                            self.figEnhanced)
                    self.BoolEnhanced = 1
                    self.axEnhanced.get_xaxis().set_visible(False)
                    self.axEnhanced.get_yaxis().set_visible(False)
                    self.axEnhanced.axis("off")
                    self.layEnhanced.addWidget(self.plotWidgetEnhanced)
                    mag = kernelsize*kernelsize
                    kernel = np.ones((kernelsize, kernelsize))
                    kernel = kernel*1/mag

                    xKernShape = kernel.shape[0]
                    yKernShape = kernel.shape[1]
                    xImgShape = image.shape[0]
                    yImgShape = image.shape[1]
                    if(yImgShape % 2 == 0):
                        image = np.vstack((image, image[xImgShape-1, :]))
                    if(xImgShape % 2 == 0):
                        image = np.c_[image, image[:, yImgShape-1]]

                    xOutput = image.shape[0]
                    yOutput = image.shape[1]
                    output = np.zeros((xOutput, yOutput))

                    imagePadded = np.zeros(
                        (image.shape[0] + padding*2, image.shape[1] + padding*2))
                    imagePadded[int(padding):int(-1 * padding),
                                int(padding):int(-1 * padding)] = image

                    for y in range(image.shape[1]):

                        for x in range(image.shape[0]):

                            try:
                                output[x, y] = (
                                    kernel * imagePadded[x: x + xKernShape, y: y + yKernShape]).sum()
                            except:

                                break
                    self.Blured_Normal = output
                    self.BOOL_Blured = 1
                    sharpen = image-output

                    # output=image+Factor*sharpen
                    for j in range(0, output.shape[0]):
                        for i in range(0, output.shape[1]):
                            if output[j, i] > 255:
                                output[j, i] = 255
                            elif output[j, i] < 0:
                                output[j, i] = 0

                    self.figEnhanced.canvas.draw()
                    self.axEnhanced.imshow(self.Blured_Normal, cmap='gray')
                    self.show()
                    self.figEnhanced.canvas.draw()

        except:
            self.msg.setText("Enter Factor and kernel size first ")
            self.msg.exec_()

    def EqualizedHistogram(self):
        try:
            self.fig6.canvas.draw()
            im = self.GrayScaled

            h = self.NormalizeHistogram(im, 2)
            im = np.asarray(im)
            im = np.round(im)
            im = im.astype(int)

            b = [sum(h[:i+1]) for i in range(len(h))]

            cumulative = np.array(b)
            cumsum = np.round(cumulative*255)
            cumsum = cumsum.astype(int)
            s1, s2 = im.shape

            NewIM = np.zeros_like(im)
            for i in range(0, s1):
                for j in range(0, s2):
                    NewIM[i, j] = cumsum[im[i, j]]

            self.ax6.imshow(NewIM, cmap='gray')

            self.show()
            self.fig6.canvas.draw()
            NewIM = np.uint8(NewIM)
            self.NormalizeHistogram(NewIM, 1)
        except:
            self.msg.setText("browse first")
            self.msg.exec_()

    def Draw(self, normalizedH, I, r, EqN):

        self.fig4.canvas.draw()
        self.fig4.canvas.draw()

        self.ax4.bar(r, normalizedH)
        self.show()
        self.ax5.bar(r, EqN)
        self.show()
        self.fig5.canvas.draw()

    def NormalizeHistogram(self, GrayScaled, n):
        r = []
        im = GrayScaled
        im = np.asarray(im)
        im = np.round(im)
        im = im.astype(int)
        h = [0]*256
        h=np.asarray(h)
        for x in range(im.shape[0]):
            for y in range(im.shape[1]):
                i = np.round(im[x, y])
                # specfic intensity
                if i <= 256:
                    # had 1 of a specfic intensity then add one and repeat
                    h[i] = h[i]+1
                else:
                    pass
        for i in range(len(h)):
            r.append(i)
        newh = np.asanyarray(h)
        normalizedH = newh/(im.shape[0]*im.shape[1])
        if n == 0:
            self.ax4.clear()
            self.Draw(normalizedH, 0, r, 0)
        elif n == 1:
            self.ax5.clear()
            self.Draw(0, 0, r, normalizedH)

        return h,r

    def showKNN(self):

        try:
            self.ax3.clear()
            Factor = float(self.ZoomFactorInput.text())
            print(Factor)

            if Factor <= 0.0:
                self.msg.setText("you cannot put zero or negative")
                self.msg.exec_()

            else:
                self.fig3.canvas.draw()
                newwidth = int(Factor*self.Y.shape[0])
                newheight = int(Factor*self.Y.shape[1])
                zoomed = np.zeros((newwidth, newheight), dtype=self.Y.dtype)
                for i in range(0, newwidth):
                    for j in range(0, newheight):
                        if i/Factor > self.Y.shape[0]-1 or j/Factor > self.Y.shape[1]-1:
                            zoomed[i, j] = self.Y[int(i/Factor), int(j/Factor)]
                        else:
                            zoomed[i, j] = self.Y[round(
                                i/Factor), round(j/Factor)]
                self.ax3.axis([0, 1200, 600, 0])

                self.ax3.imshow(zoomed, cmap='gray')
                self.fig3.canvas.draw()

                self.show()
        except:
            self.msg.setText(
                "browse first then put a zooming factor\n make sure zooming factor is a postive number only")
            self.msg.exec_()

    def ShowBilinear(self):
        try:
            self.ax3.clear()

            Factor = float(self.ZoomFactorInput.text())
            if Factor <= 0.0:
                self.msg.setText("you cannot put zero or negative")
                self.msg.exec_()
            else:
                self.fig3.canvas.draw()

                newwidth = int(Factor*self.Y.shape[0])
                newheight = int(Factor*self.Y.shape[1])
                # # ##################################################################
                # get dimensions of original image
                old_h, old_w, c = self.fix_img.shape
                # create an array of the desired shape.
                # We will fill-in the values later.
                resized = np.zeros((newheight, newwidth, c))
                # Calculate horizontal and vertical scaling factor
                w_scale_factor = (old_w) / (newwidth) if newheight != 0 else 0
                h_scale_factor = (old_h) / (newheight) if newwidth != 0 else 0
                for i in range(newheight):
                    for j in range(newwidth):
                        # map the coordinates back to the original image
                        x = i * h_scale_factor
                        y = j * w_scale_factor
                        # calculate the coordinate values for 4 surrounding pixels.
                        x_floor = math.floor(x)
                        x_ceil = min(old_h - 1, math.ceil(x))
                        y_floor = math.floor(y)
                        y_ceil = min(old_w - 1, math.ceil(y))
                # case 1 it has specfic pixel in old image so we assign it
                        if (x_ceil == x_floor) and (y_ceil == y_floor):
                            q = self.fix_img[int(x), int(y), :]
        # when one of them is specfic we do linear interpolation for one only
                        elif (x_ceil == x_floor):
                            q1 = self.fix_img[int(x), int(y_floor), :]
                            q2 = self.fix_img[int(x), int(y_ceil), :]
                            q = q1 * (y_ceil - y) + q2 * (y - y_floor)
                        elif (y_ceil == y_floor):
                            q1 = self.fix_img[int(x_floor), int(y), :]
                            q2 = self.fix_img[int(x_ceil), int(y), :]
                            q = (q1 * (x_ceil - x)) + (q2 * (x - x_floor))
                        else:
                            v1 = self.fix_img[x_floor, y_floor, :]
                            v2 = self.fix_img[x_ceil, y_floor, :]
                            v3 = self.fix_img[x_floor, y_ceil, :]
                            v4 = self.fix_img[x_ceil, y_ceil, :]

                            q1 = v1 * (x_ceil - x) + v2 * (x - x_floor)
                            q2 = v3 * (x_ceil - x) + v4 * (x - x_floor)
                            q = q1 * (y_ceil - y) + q2 * (y - y_floor)

                        resized[i, j, :] = q
                R2, G2, B2 = resized[:, :, 0], resized[:,
                                                       :, 1], resized[:, :, 2]
                self.ax3.axis([0, 1200, 600, 0])

                Y2 = 0.299 * R2 + 0.587 * G2 + 0.114 * B2
                self.ax3.imshow(Y2, cmap='gray')
                self.fig3.canvas.draw()

                self.show()
        except:
            self.msg.setText(
                "browse first then put a zooming factor\n make sure zooming factor is number only")
            self.msg.exec_()

    def Generate(self):
        self.lay2.addWidget(self.plotWidget2)

        self.fig2.canvas.draw()
        white = np.ones([50, 50, 3], dtype=np.uint8)
        white[:] = 255
        self.ax2.imshow(white, cmap='gray')
        self.fig2.canvas.draw()

        self.show()
        self.Bool2 = 0

    def ShowPixels(self):
        if self.Bool2 == 1:

            self.msg.setText("click on generate first")
            self.msg.exec_()

        white = np.ones([50, 50, 3], dtype=np.uint8)
        white[:] = 255
        for i in range(4):
            L = len(white[0])
            white[1][len(white)-i-1] = (200, 0, 0)
            white[L-i-1][1] = (0, 0, 200)
        self.fig2.canvas.draw()
        self.ax2.imshow(white, cmap='gray')
        self.fig2.canvas.draw()

        self.show()


def main():
    app = QtWidgets.QApplication(sys.argv)
    application = ApplicationWindow()
    application.show()

    app.exec_()


if __name__ == "__main__":
    main()
