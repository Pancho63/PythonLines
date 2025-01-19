import logging

import PyQt5.QtGui
#import packet
from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtWidgets import QGraphicsEllipseItem, QGraphicsRectItem, QApplication, QGraphicsView, QGraphicsScene, \
     QGraphicsPixmapItem

import sacn
import threading

logging.basicConfig(
    level=logging.DEBUG,  # Set logging level to debug
    format='%(asctime)s - %(levelname)s - %(message)s',  # Include timestamp for clarity
)



iarg = 0
iarg2 = 0
sarg = ""
master = [255, 255, 0, 0, 0]
X1 = [3000, 3000, 0, 0, 0]
X2 = [3000, 3000, 0, 0, 0]
Y1 = [3000, 3000, 0, 0, 0]
Y2 = [3000, 3000, 0, 0, 0]
R = [0, 0, 0, 0, 0]
rouge = [255, 255, 0, 0, 0]
vert = [255, 255, 0, 0, 0]
bleu = [255, 255, 0, 0, 0]
thick = [10, 10, 0, 0, 0]
base_channel = {0, 14, 28, 42, 56}
dmx_data = [0] * 71

app = QApplication([])
view = QGraphicsView()
scene = QGraphicsScene()
view.setScene(scene)
view.showFullScreen()

# fetch screen definition
screen = app.primaryScreen()
screenGeometry = screen.geometry()
view.setSceneRect(QRectF(screenGeometry))  # Define scene size
screenWidth = screenGeometry.width()
screenHeight = screenGeometry.height()
logging.debug(f"Definition : {screenWidth}x{screenHeight}")
# y adapter la vue
view.setFixedWidth(screenWidth)
view.setFixedHeight(screenHeight)
# black background et better quality
view.setBackgroundBrush(PyQt5.QtGui.QBrush(Qt.black, Qt.SolidPattern))
view.setAutoFillBackground(True)
view.setRenderHints(PyQt5.QtGui.QPainter.Antialiasing)
view.setRenderHints(PyQt5.QtGui.QPainter.SmoothPixmapTransform)
# Remove the border and frame
view.setFrameShape(QGraphicsView.NoFrame)
# Hide the cursor
view.setCursor(Qt.BlankCursor)
# no scrollBars
view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

# Add items to the scene
#rect1 = QGraphicsRectItem()
#rect2 = QGraphicsRectItem()
#ellipse1 = QGraphicsEllipseItem()
#ellipse2 = QGraphicsEllipseItem()
#pix = QGraphicsPixmapItem()

def lineupdate():
     global scene, X1, Y1, X2, Y2, screenWidth, screenHeight, rouge, vert, bleu, master, thick, R

     rect1 = QGraphicsRectItem()
     scene.addItem(rect1)
     rect1.setRect(QRectF((X1[0] * screenWidth / 65535), (Y1[0] * screenHeight / 65535), (X2[0] * screenWidth / 65535), (Y2[0] * screenHeight / 65535)))
     rect1.setPen(PyQt5.QtGui.QPen(PyQt5.QtGui.QColor(rouge[0], vert[0], bleu[0], master[0]), thick[0], Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
     rect1.setTransformOriginPoint(rect1.boundingRect().center())
     rect1.setRotation(R[0])


     rect2 = QGraphicsRectItem()
     scene.addItem(rect2)
     rect2.setRect(QRectF(((screenWidth - X1[1] * screenWidth / 65535) - X2[1] * screenWidth / 65535),((screenHeight - Y1[1] * screenHeight / 65535) - Y2[1] * screenHeight / 65535), (X2[1] * screenWidth / 65535), (Y2[1] * screenHeight / 65535)))
     rect2.setPen(PyQt5.QtGui.QPen(PyQt5.QtGui.QColor(rouge[1], vert[1], bleu[1], master[1]), thick[1], Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
     rect2.setTransformOriginPoint(rect2.boundingRect().center())
     rect2.setRotation(R[1])

     ellipse1 = QGraphicsEllipseItem()
     scene.addItem(ellipse1)
     ellipse1.setRect(QRectF((X1[2] * screenWidth / 65535), ((screenHeight - Y1[2] * screenHeight / 65535) - Y2[2] * screenHeight / 65535), (2 * X2[2] * screenWidth / 65535), (2 * Y2[2] * screenHeight / 65535)))
     ellipse1.setPen(PyQt5.QtGui.QPen(PyQt5.QtGui.QColor(rouge[2], vert[2], bleu[2], master[2]), thick[2], Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
     ellipse1.setTransformOriginPoint(ellipse1.boundingRect().center())
     ellipse1.setRotation(R[2])

     ellipse2 = QGraphicsEllipseItem()
     scene.addItem(ellipse2)
     ellipse2.setRect(QRectF((X1[3] * screenWidth / 65535), ((screenHeight - Y1[3] * screenHeight / 65535) - Y2[3] * screenHeight / 65535), (X2[3] * screenWidth / 65535), (Y2[3] * screenHeight / 65535)))
     ellipse2.setPen(PyQt5.QtGui.QPen(PyQt5.QtGui.QColor(rouge[3], vert[3], bleu[3], master[3]), thick[3], Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
     ellipse2.setTransformOriginPoint(ellipse2.boundingRect().center())
     ellipse2.setRotation(R[3])

     pix = QGraphicsPixmapItem()
     scene.addItem(pix)
     pix.setTransformationMode(Qt.SmoothTransformation)
     xpix = X1[4] * screenWidth
     ypix = Y1[4] * screenHeight
     hpix = X2[4] * screenWidth / 127
     vpix = Y2[4] * screenHeight / 127
     pix.setOpacity(master[4] / 255)
     trans = PyQt5.QtGui.QTransform()
     trans.setMatrix(hpix / 65535, 0, 0, 0, vpix / 65535, 0, xpix / 65535, ypix / 65535, 1)
     pix.setTransform(trans)
     pix.setTransformOriginPoint(pix.boundingRect().center())
     pix.setRotation(R[4])


def on_levels_changed(dmxDataIn) :
     for  cha in range (99, 170, 1) :
          dmx_data[cha - 99] = dmxDataIn[cha]
     processDMXData(dmx_data)


def master_level(ch, value):
    pass  # Implement masterLevel functionality

def red_sacn(ch, value):
    pass  # Implement redSacn functionality

def green_sacn(ch, value):
    pass  # Implement greenSacn functionality

def blue_sacn(ch, value):
    pass  # Implement blueSacn functionality

def thickness(ch, value):
    pass  # Implement thickness functionality

def rotate(ch, value):
    pass  # Implement rotate functionality

def pan(ch, value):
    pass  # Implement pan functionality

def tilt(ch, value):
    pass  # Implement tilt functionality

def largeur(ch, value):
    pass  # Implement largeur functionality

def hauteur(ch, value):
    pass  # Implement hauteur functionality

def picture_sacn(level):
    pass  # Implement pictureSacn functionality


def processDMXData(dmx_data) :
     for base_ch in range(0,57,14):
          for i in range(6):
               current_value = dmx_data[base_ch + i]
               if i == 0:
                    master_level(base_ch, current_value)
               elif i == 1:
                    red_sacn(base_ch, current_value)
               elif i == 2:
                    green_sacn(base_ch, current_value)
               elif i == 3:
                    blue_sacn(base_ch, current_value)
               elif i == 4:
                    thickness(base_ch, current_value * 256)
               elif i == 5:
                    rotate(base_ch, current_value * 256)

          for i in range(6, 14, 2):
               combined_value = (dmx_data[base_ch + i] << 8) | dmx_data[base_ch + i + 1]
               if i == 6:
                    pan(base_ch, combined_value)
               elif i == 8:
                    tilt(base_ch, combined_value)
               elif i == 10:
                    largeur(base_ch, combined_value)
               elif i == 12:
                    hauteur(base_ch, combined_value)

     level = dmx_data[70]
     if level >= 0:
          picture_sacn(level)
     lineupdate()

#sACN :
# Initialize the sACN receiver
receiver = sacn.sACNreceiver()
# optional: if multicast is desired, join with the universe number as parameter
receiver.join_multicast(7)
# Define a callback function
@receiver.listen_on('universe', universe=7)  # listens on universe 7
def callback(packet):  # packet type: sacn.DataPacket
#   logging.debug("callback() called")
    if packet.dmxStartCode == 0x00:  # ignore non-DMX-data packets
        #print(packet.dmxData)
        on_levels_changed(packet.dmxData)
# Start the receiver in a separate thread
def start_receiver():
    receiver.start()  # start the receiving thread

receiver_thread = threading.Thread(target=start_receiver)
receiver_thread.daemon = True
receiver_thread.start()

app.exec_()
