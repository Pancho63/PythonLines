import PyQt5.QtGui
from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtWidgets import QGraphicsEllipseItem, QGraphicsRectItem, QApplication, QGraphicsView, QGraphicsScene, \
     QGraphicsPixmapItem
import logging

logging.basicConfig(
    level=logging.DEBUG,  # Set logging level to debug
    format='%(asctime)s - %(levelname)s - %(message)s',  # Include timestamp for clarity
)

logging.debug("This is a debug message.")  # This should display in your console


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
thickness = [10, 10, 0, 0, 0]
channel = 61



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
     try:
          logging.debug("Starting lineUpdate function...")
          logging.debug("Création de rect1...")
          rect1 = QGraphicsRectItem()
          rect1X = (X1[0] * screenWidth / 65535)
          rect1Y = (Y1[0] * screenHeight / 65535)
          rect1Width = (X2[0] * screenWidth / 65535)
          rect1Height = (Y2[0] * screenHeight / 65535)
          logging.debug(f"rect1: x={rect1X}, y={rect1Y}, width={rect1Width}, height={rect1Height}")

          rect1 = QGraphicsRectItem()
          scene.addItem(rect1)
          rect1.setRect(QRectF((X1[0] * screenWidth / 65535), (Y1[0] * screenHeight / 65535), (X2[0] * screenWidth / 65535), (Y2[0] * screenHeight / 65535)))
          rect1.setPen(PyQt5.QtGui.QPen(PyQt5.QtGui.QColor(rouge[0], vert[0], bleu[0], master[0]), thickness[0], Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
          rect1.setTransformOriginPoint(rect1.boundingRect().center())
          rect1.setRotation(R[0])


          rect2 = QGraphicsRectItem()
          scene.addItem(rect2)
          rect2.setRect(QRectF(((screenWidth - X1[1] * screenWidth / 65535) - X2[1] * screenWidth / 65535),((screenHeight - Y1[1] * screenHeight / 65535) - Y2[1] * screenHeight / 65535), (X2[1] * screenWidth / 65535), (Y2[1] * screenHeight / 65535)))
          rect2.setPen(PyQt5.QtGui.QPen(PyQt5.QtGui.QColor(rouge[1], vert[1], bleu[1], master[1]), thickness[1], Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
          rect2.setTransformOriginPoint(rect2.boundingRect().center())
          rect2.setRotation(R[1])

          ellipse1 = QGraphicsEllipseItem()
          scene.addItem(ellipse1)
          ellipse1.setRect(QRectF((X1[2] * screenWidth / 65535), ((screenHeight - Y1[2] * screenHeight / 65535) - Y2[2] * screenHeight / 65535), (2 * X2[2] * screenWidth / 65535), (2 * Y2[2] * screenHeight / 65535)))
          ellipse1.setPen(PyQt5.QtGui.QPen(PyQt5.QtGui.QColor(rouge[2], vert[2], bleu[2], master[2]), thickness[2], Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
          ellipse1.setTransformOriginPoint(ellipse1.boundingRect().center())
          ellipse1.setRotation(R[2])

          ellipse2 = QGraphicsEllipseItem()
          scene.addItem(ellipse2)
          ellipse2.setRect(QRectF((X1[3] * screenWidth / 65535), ((screenHeight - Y1[3] * screenHeight / 65535) - Y2[3] * screenHeight / 65535), (X2[3] * screenWidth / 65535), (Y2[3] * screenHeight / 65535)))
          ellipse2.setPen(PyQt5.QtGui.QPen(PyQt5.QtGui.QColor(rouge[3], vert[3], bleu[3], master[3]), thickness[3], Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
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

     except Exception as e:
          logging.error("An error occurred in lineupdate: %s", e)

app.exec_()
lineupdate()