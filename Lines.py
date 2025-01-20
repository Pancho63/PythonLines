import logging
import PyQt6.QtGui
from PyQt6.QtCore import Qt, QRectF, QThread,pyqtSignal
from PyQt6.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QGraphicsRectItem, QGraphicsEllipseItem, QGraphicsPixmapItem
import sacn
logging.basicConfig(
    level=logging.DEBUG,  # Set logging level to debug
    format='%(asctime)s - %(levelname)s - %(message)s',)  # Include timestamp for clarity

gobo = 0
app = QApplication([])
view = QGraphicsView()
scene = QGraphicsScene()
view.setScene(scene)
view.showFullScreen()

# fetch screen definition
screen = app.primaryScreen()
screenGeometry = screen.geometry()
view.setSceneRect(QRectF(screenGeometry))  # Define scene size
logging.debug(f"Definition : {screenGeometry.width()}x{screenGeometry.height()}")
# y adapter la vue
view.setFixedWidth(screenGeometry.width())
view.setFixedHeight(screenGeometry.height())
# black background et better quality
view.setBackgroundBrush(PyQt6.QtGui.QBrush(Qt.GlobalColor.black, Qt.BrushStyle.SolidPattern))
view.setAutoFillBackground(True)
view.setRenderHints(PyQt6.QtGui.QPainter.RenderHint.Antialiasing)
view.setRenderHints(PyQt6.QtGui.QPainter.RenderHint.SmoothPixmapTransform)
# Remove the border and frame
view.setFrameShape(PyQt6.QtWidgets.QFrame.Shape.NoFrame)
# Hide the cursor
view.setCursor(Qt.CursorShape.BlankCursor)
# no scrollBars
view.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
view.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

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
receiver_thread.dmx_data_received.connect(lambda data: line_update(data))
receiver_thread.start()


def valeur16b(value, data):
     return (data[value] << 8) | data[value+ 1]


def line_update(data):
     global scene, view, pix, ellipse1, ellipse2, rect1, rect2, gobo

     rect1.setRect(QRectF((valeur16b(7, data) * view.width() / 65535), (valeur16b(9, data) * view.height() / 65535), (valeur16b(11, data) * view.width() / 65535), (valeur16b(13, data) * view.height() / 65535)))
     rect1.setPen(PyQt6.QtGui.QPen(PyQt6.QtGui.QColor(data[1], data[2], data[3], data[0]), data[4], Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin))
     rect1.setTransformOriginPoint(rect1.boundingRect().center())
     rect1.setRotation(360*(valeur16b(5, data))/65535)

     rect2.setRect(QRectF((valeur16b(22, data) * view.width() / 65535), ((view.height() - (valeur16b(24, data)) * view.height() / 65535) - (valeur16b(28, data)) * view.height() / 65535), ((valeur16b(26, data)) * view.width() / 65535), ((valeur16b(28, data)) * view.height() / 65535)))
     rect2.setPen(PyQt6.QtGui.QPen(PyQt6.QtGui.QColor(data[16], data[17], data[18], data[15]), data[19], Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin))
     rect2.setTransformOriginPoint(rect2.boundingRect().center())
     rect2.setRotation(360*(valeur16b(20, data))/65535)

     ellipse1.setRect(QRectF((valeur16b(37, data) * view.width() / 65535), ((view.height() - (valeur16b(39, data)) * view.height() / 65535) - (valeur16b(43, data)) * view.height() / 65535), (2 * (valeur16b(41, data)) * view.width() / 65535), (2 * (valeur16b(43, data)) * view.height() / 65535)))
     ellipse1.setPen(PyQt6.QtGui.QPen(PyQt6.QtGui.QColor(data[31], data[32], data[33], data[30]), data[34], Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin))
     ellipse1.setTransformOriginPoint(ellipse1.boundingRect().center())
     ellipse1.setRotation(360*(valeur16b(35, data))/65535)

     ellipse2.setRect(QRectF((valeur16b(52, data) * view.width() / 65535), ((view.height() - (valeur16b(54, data)) * view.height() / 65535) - (valeur16b(58, data)) * view.height() / 65535), ((valeur16b(56, data)) * view.width() / 65535), ((valeur16b(58, data)) * view.height() / 65535)))
     ellipse2.setPen(PyQt6.QtGui.QPen(PyQt6.QtGui.QColor(data[46], data[47], data[48], data[45]), data[49], Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin))
     ellipse2.setTransformOriginPoint(ellipse2.boundingRect().center())
     ellipse2.setRotation(360*(valeur16b(50, data))/65535)

     if data[75] != gobo:
          picture_sacn(data[75])
          gobo = data[75]
     pix.setTransformationMode(Qt.TransformationMode.SmoothTransformation)
     pix_pan = (valeur16b(67, data)) * view.width()
     pix_tilt = (valeur16b(69, data)) * view.height()
     pix_width = (valeur16b(71, data)) *  view.width()/ 1700
     pix_height = (valeur16b(73, data)) * view.height() / 1000
     pix.setOpacity(data[60] / 255)
     trans = PyQt6.QtGui.QTransform()
     trans.setMatrix(pix_width / 65535, 0, 0, 0, pix_height / 65535, 0, pix_pan / 65535, pix_tilt / 65535, 1)
     pix.setTransform(trans)
     pix.setTransformOriginPoint(pix.boundingRect().center())
     pix.setRotation(360*(valeur16b(65, data))/65535)

def picture_sacn(level):
     global pix, view
     #if 0 <= level < 23:
     pict = PyQt6.QtGui.QPixmap()

     if 23 <= level < 46:
          pict = PyQt6.QtGui.QPixmap( "imageLine/1.png")
          if pict.isNull():
            return
          pict = pict.scaled(view.width(), view.height())


     elif 46 <= level < 69:
          pict = PyQt6.QtGui.QPixmap( "imageLine/2.png")
          if pict.isNull():
            return
          pict = pict.scaled(view.width(), view.height())


     elif 69 <= level < 92:
          pict = PyQt6.QtGui.QPixmap("./imageLine/3.png")
          if pict.isNull():
               logging.debug("null")
               return
          pict = pict.scaled(view.width(), view.height())

     elif 92 <= level < 115:
          pict = PyQt6.QtGui.QPixmap("imageLine/4.png")
          if pict.isNull():
            return
          pict = pict.scaled(view.width(), view.height())

     elif 115 <= level < 138:
          pict = PyQt6.QtGui.QPixmap("imageLine/5.png")
          if pict.isNull():
               return
          pict = pict.scaled(view.width(), view.height())

     elif 138 <= level < 161:
          pict = PyQt6.QtGui.QPixmap("imageLine/6.png")
          if pict.isNull():
               return
          pict = pict.scaled(view.width(), view.height())

     elif 161 <= level < 184:
          pict = PyQt6.QtGui.QPixmap("imageLine/7.png")
          if pict.isNull():
               return
          pict = pict.scaled(view.width(), view.height())

     elif 184 <= level < 207:
          pict = PyQt6.QtGui.QPixmap("imageLine/8.png")
          if pict.isNull():
               return
          pict = pict.scaled(view.width(), view.height())

     elif 207 <= level < 230:
          pict = PyQt6.QtGui.QPixmap("imageLine/9.png")
          if pict.isNull():
               return
          pict = pict.scaled(view.width(), view.height())

     elif 230 <= level < 256:
          pict = PyQt6.QtGui.QPixmap("imageLine/10.png")
          if pict.isNull():
               return
          pict = pict.scaled(view.width(), view.height())
     pix.setPixmap(pict)


app.exec()
