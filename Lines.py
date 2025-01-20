import logging
import PyQt5.QtGui
from PyQt5.QtCore import Qt, QRectF, QThread,pyqtSignal
from PyQt5.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsRectItem, QGraphicsEllipseItem, QGraphicsPixmapItem
import sacn
logging.basicConfig(
    level=logging.DEBUG,  # Set logging level to debug
    format='%(asctime)s - %(levelname)s - %(message)s',  # Include timestamp for clarity
)



int_arg = 0
int_arg2 = 0
string_arg = ""
master = [0, 0, 0, 0, 0]
X1 = [0, 0, 0, 0, 0]
X2 = [0, 0, 0, 0, 0]
Y1 = [0, 0, 0, 0, 0]
Y2 = [0, 0, 0, 0, 0]
R = [0, 0, 0, 0, 0]
rouge = [0, 0, 0, 0]
vert = [0, 0, 0, 0]
bleu = [0, 0, 0, 0]
thick = [0, 0, 0, 0]
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
rect1 = QGraphicsRectItem()
rect2 = QGraphicsRectItem()
ellipse1 = QGraphicsEllipseItem()
ellipse2 = QGraphicsEllipseItem()
pix = QGraphicsPixmapItem()
scene.addItem(rect1)
scene.addItem(rect2)
scene.addItem(ellipse1)
scene.addItem(ellipse2)
scene.addItem(pix)

class SACNReceiverThread(QThread):
    dmx_data_received = pyqtSignal(list)  # Ensure signal is defined correctly

    def run(self):
        receiver = sacn.sACNreceiver()
        receiver.start()

        @receiver.listen_on('universe', universe=7)
        def callback(packet):  # packet type: sacn.DataPacket
            self.dmx_data_received.emit(list(packet.dmxData))  # Ensure data is a list

receiver_thread = SACNReceiverThread()
receiver_thread.dmx_data_received.connect(lambda data: on_levels_changed(data))
receiver_thread.start()


def line_update():
     global scene, X1, Y1, X2, Y2, screenWidth, screenHeight, rouge, vert, bleu, master, thick, R

     rect1.setRect(QRectF((X1[0] * screenWidth / 65535), (Y1[0] * screenHeight / 65535), (X2[0] * screenWidth / 65535), (Y2[0] * screenHeight / 65535)))
     rect1.setPen(PyQt5.QtGui.QPen(PyQt5.QtGui.QColor(rouge[0], vert[0], bleu[0], master[0]), thick[0], Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
     rect1.setTransformOriginPoint(rect1.boundingRect().center())
     rect1.setRotation(360*R[0]/255)

     rect2.setRect(QRectF(((screenWidth - X1[1] * screenWidth / 65535) - X2[1] * screenWidth / 65535),((screenHeight - Y1[1] * screenHeight / 65535) - Y2[1] * screenHeight / 65535), (X2[1] * screenWidth / 65535), (Y2[1] * screenHeight / 65535)))
     rect2.setPen(PyQt5.QtGui.QPen(PyQt5.QtGui.QColor(rouge[1], vert[1], bleu[1], master[1]), thick[1], Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
     rect2.setTransformOriginPoint(rect2.boundingRect().center())
     rect2.setRotation(360*R[1]/255)

     ellipse1.setRect(QRectF((X1[2] * screenWidth / 65535), ((screenHeight - Y1[2] * screenHeight / 65535) - Y2[2] * screenHeight / 65535), (2 * X2[2] * screenWidth / 65535), (2 * Y2[2] * screenHeight / 65535)))
     ellipse1.setPen(PyQt5.QtGui.QPen(PyQt5.QtGui.QColor(rouge[2], vert[2], bleu[2], master[2]), thick[2], Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
     ellipse1.setTransformOriginPoint(ellipse1.boundingRect().center())
     ellipse1.setRotation(360*R[2]/255)

     ellipse2.setRect(QRectF((X1[3] * screenWidth / 65535), ((screenHeight - Y1[3] * screenHeight / 65535) - Y2[3] * screenHeight / 65535), (X2[3] * screenWidth / 65535), (Y2[3] * screenHeight / 65535)))
     ellipse2.setPen(PyQt5.QtGui.QPen(PyQt5.QtGui.QColor(rouge[3], vert[3], bleu[3], master[3]), thick[3], Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
     ellipse2.setTransformOriginPoint(ellipse2.boundingRect().center())
     ellipse2.setRotation(360*R[3]/255)

     pix.setTransformationMode(Qt.SmoothTransformation)
     pix_pan = X1[4] * screenWidth
     pix_tilt = Y1[4] * screenHeight
     pix_width = X2[4] * screenWidth / 127
     pix_height = Y2[4] * screenHeight / 127
     pix.setOpacity(master[4] / 255)
     trans = PyQt5.QtGui.QTransform()
     trans.setMatrix(pix_width / 65535, 0, 0, 0, pix_height / 65535, 0, pix_pan / 65535, pix_tilt / 65535, 1)
     pix.setTransform(trans)
     pix.setTransformOriginPoint(pix.boundingRect().center())
     pix.setRotation(360*R[4]/255)


def on_levels_changed(dmx_data_in) :
     for  cha in range (0, 71, 1) :
          dmx_data[cha] = dmx_data_in[cha]
     process_dmx_data(dmx_data)


def picture_sacn(level, local_pix, local_view):
     #if 0 <= level < 23:
     pict = PyQt5.QtGui.QPixmap()

     if 23 <= level < 46:
          pict = PyQt5.QtGui.QPixmap( "imageLine/1.png")
          if pict.isNull():
            return
          pict = pict.scaled(local_view.width(), local_view.height())


     elif 46 <= level < 69:
          pict = PyQt5.QtGui.QPixmap( "imageLine/2.png")
          if pict.isNull():
            return
          pict = pict.scaled(local_view.width(), local_view.height())


     elif 69 <= level < 92:

          pict = PyQt5.QtGui.QPixmap("./imageLine/3.png")
          if pict.isNull():
               logging.debug("null")
               return
          pict = pict.scaled(local_view.width(), local_view.height())
          logging.debug("set")

     elif 92 <= level < 115:
          pict = PyQt5.QtGui.QPixmap("imageLine/4.png")
          if pict.isNull():
            return
          pict = pict.scaled(local_view.width(), local_view.height())

     elif 115 <= level < 138:
          pict = PyQt5.QtGui.QPixmap("imageLine/5.png")
          if pict.isNull():
               return
          pict = pict.scaled(local_view.width(), local_view.height())

     elif 138 <= level < 161:
          pict = PyQt5.QtGui.QPixmap("imageLine/6.png")
          if pict.isNull():
               return
          pict = pict.scaled(local_view.width(), local_view.height())

     elif 161 <= level < 184:
          pict = PyQt5.QtGui.QPixmap("imageLine/7.png")
          if pict.isNull():
               return
          pict = pict.scaled(local_view.width(), local_view.height())

     elif 184 <= level < 207:
          pict = PyQt5.QtGui.QPixmap("imageLine/8.png")
          if pict.isNull():
               return
          pict = pict.scaled(local_view.width(), local_view.height())

     elif 207 <= level < 230:
          pict = PyQt5.QtGui.QPixmap("imageLine/9.png")
          if pict.isNull():
               return
          pict = pict.scaled(local_view.width(), local_view.height())

     elif 230 <= level < 256:
          pict = PyQt5.QtGui.QPixmap("imageLine/10.png")
          if pict.isNull():
               return
          pict = pict.scaled(local_view.width(), local_view.height())
     local_pix.setPixmap(pict)


def process_dmx_data(data) :
     for premier_circuit in range(0,57,14):
          shape_number = premier_circuit // 14
          #logging.debug(f"ch : {ch}")
          for i in range(6):
               current_value = data[premier_circuit + i]
               if (current_value >= 0) & (current_value <= 255) & (shape_number <= 4) & (shape_number >= 0):
                   if i == 0:
                       #logging.debug(f"ch : {ch} value : {current_value}")
                       master[shape_number] = current_value
                   if shape_number < 4:
                        if i == 1:
                             rouge[shape_number] = current_value
                        elif i == 2:
                             vert[shape_number] = current_value
                        elif i == 3:
                             bleu[shape_number] = current_value
                        elif i == 4:
                             thick[shape_number] = current_value
                   elif i == 5:
                        R[shape_number] = current_value

          for i in range(6, 14, 2):
               combined_value = (data[premier_circuit + i] << 8) | data[premier_circuit + i + 1]
               if i == 6:
                    X1[shape_number] = combined_value
                    #logging.debug(f"ch : {ch} value : {combined_value}")
               elif i == 8:
                    Y1[shape_number] = combined_value
               elif i == 10:
                    X2[shape_number] = combined_value
               elif i == 12:
                    Y2[shape_number] = combined_value

     level = data[70]
     if level >= 0:
          picture_sacn(level, pix, view)
     line_update()
     #logging.debug("out")



app.exec_()
