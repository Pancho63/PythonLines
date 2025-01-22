import logging
import queue
import PyQt6.QtGui
from PyQt6.QtGui import QShortcut
from PyQt6.QtCore import Qt, QRectF, QThread, pyqtSignal, QTimer
from PyQt6.QtWidgets import (QApplication, QGraphicsView, QGraphicsScene,
                             QGraphicsRectItem, QGraphicsEllipseItem, QGraphicsPixmapItem)
import ola.ClientWrapper

logging.basicConfig(
    level=logging.DEBUG,  # Set logging level to debug
    format='%(asctime)s - %(levelname)s - %(message)s',)  # Include timestamp for clarity

gobo = 0
app = QApplication([])
view = QGraphicsView()
scene = QGraphicsScene()
view.setScene(scene)
view.showFullScreen()

# Fetch screen definition
screen = app.primaryScreen()
screenGeometry = screen.geometry()
view.setSceneRect(QRectF(screenGeometry))  # Define scene size
logging.debug(f"Definition : {screenGeometry.width()}x{screenGeometry.height()}")
# Adapt the view
view.setFixedWidth(screenGeometry.width())
view.setFixedHeight(screenGeometry.height())
# Black background and better quality
view.setBackgroundBrush(PyQt6.QtGui.QBrush(Qt.GlobalColor.black, Qt.BrushStyle.SolidPattern))
view.setAutoFillBackground(True)
view.setRenderHints(PyQt6.QtGui.QPainter.RenderHint.Antialiasing)
view.setRenderHints(PyQt6.QtGui.QPainter.RenderHint.SmoothPixmapTransform)
# Remove the border and frame
view.setFrameShape(PyQt6.QtWidgets.QFrame.Shape.NoFrame)
# Hide the cursor
view.setCursor(Qt.CursorShape.BlankCursor)
# No scrollbars
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

# Add Ctrl+Q shortcut to quit the application
quit_sc = QShortcut(PyQt6.QtGui.QKeySequence('Ctrl+Q'), view)
quit_sc.activated.connect(app.quit)

# Precompute ratios
width_ratio = view.width() / 65535
height_ratio = view.height() / 65535

# Preload and cache images
image_cache = {}
for i in range(1, 11):
    image = PyQt6.QtGui.QPixmap(f"imageLine/{i}.png")
    if not image.isNull():
        image_cache[i] = image.scaled(view.width(), view.height())
    else:
        logging.debug(f"Failed to load image: imageLine/{i}.png")

class OLAReceiverThread(QThread):
    dmx_signal = pyqtSignal(list)  # Signal to communicate with the main thread

    def __init__(self, universe):
        super().__init__()
        self.universe = universe
        self.wrapper = ola.ClientWrapper.ClientWrapper()
        self.client = self.wrapper.Client()

    def run(self):
        self.client.RegisterUniverse(
            self.universe, self.client.REGISTER, self.dmx_callback
        )
        print(f"Listening for DMX data on universe {self.universe}...")

    def dmx_callback(self, data):
        self.dmx_signal.emit(list(data))  # Emit the data to the main thread

# Create the OLAReceiverThread
receiver_thread = OLAReceiverThread(universe=7)
receiver_thread.start()

def valeur16b(value, data):
    return (data[value] << 8) | data[value + 1]

def line_update(data):
    global view, pix, ellipse1, ellipse2, rect1, rect2, gobo, width_ratio, height_ratio

    # Update rect1
    new_rect1 = QRectF((valeur16b(7, data) * width_ratio),
                       (valeur16b(9, data) * height_ratio),
                       (valeur16b(11, data) * width_ratio),
                       (valeur16b(13, data) * height_ratio))
    if rect1.rect() != new_rect1:
        rect1.setRect(new_rect1)
    new_pen1 = PyQt6.QtGui.QPen(PyQt6.QtGui.QColor(data[1], data[2], data[3], data[0]), data[4],
                                Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin)
    if rect1.pen() != new_pen1:
        rect1.setPen(new_pen1)
    rect1.setTransformOriginPoint(rect1.boundingRect().center())
    rect1.setRotation(360 * (valeur16b(5, data)) / 65535)

    # Update rect2
    new_rect2 = QRectF((valeur16b(22, data) * width_ratio),
                       ((view.height() - (valeur16b(24, data)) * height_ratio) - (valeur16b(28, data)) * height_ratio),
                       ((valeur16b(26, data)) * width_ratio),
                       ((valeur16b(28, data)) * height_ratio))
    if rect2.rect() != new_rect2:
        rect2.setRect(new_rect2)
    new_pen2 = PyQt6.QtGui.QPen(PyQt6.QtGui.QColor(data[16], data[17], data[18], data[15]), data[19],
                                Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin)
    if rect2.pen() != new_pen2:
        rect2.setPen(new_pen2)
    rect2.setTransformOriginPoint(rect2.boundingRect().center())
    rect2.setRotation(360 * (valeur16b(20, data)) / 65535)

    # Update ellipse1
    new_ellipse1 = QRectF((valeur16b(37, data) * width_ratio),
                          ((view.height() - (valeur16b(39, data)) * height_ratio) - (valeur16b(43, data)) * height_ratio),
                          (2 * (valeur16b(41, data)) * width_ratio),
                          (2 * (valeur16b(43, data)) * height_ratio))
    if ellipse1.rect() != new_ellipse1:
        ellipse1.setRect(new_ellipse1)
    new_pen3 = PyQt6.QtGui.QPen(PyQt6.QtGui.QColor(data[31], data[32], data[33], data[30]), data[34],
                                Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin)
    if ellipse1.pen() != new_pen3:
        ellipse1.setPen(new_pen3)
    ellipse1.setTransformOriginPoint(ellipse1.boundingRect().center())
    ellipse1.setRotation(360 * (valeur16b(35, data)) / 65535)

    # Update ellipse2
    new_ellipse2 = QRectF((valeur16b(52, data) * width_ratio),
                          ((view.height() - (valeur16b(54, data)) * height_ratio) - (valeur16b(58, data)) * height_ratio),
                          ((valeur16b(56, data)) * width_ratio),
                          ((valeur16b(58, data)) * height_ratio))
    if ellipse2.rect() != new_ellipse2:
        ellipse2.setRect(new_ellipse2)
    new_pen4 = PyQt6.QtGui.QPen(PyQt6.QtGui.QColor(data[46], data[47], data[48], data[45]), data[49],
                                Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin)
    if ellipse2.pen() != new_pen4:
        ellipse2.setPen(new_pen4)
    ellipse2.setTransformOriginPoint(ellipse2.boundingRect().center())
    ellipse2.setRotation(360 * (valeur16b(50, data)) / 65535)

    # Update pixmap
    if data[75] != gobo:
        picture_sacn(data[75])
        gobo = data[75]

    pix.setTransformationMode(Qt.TransformationMode.SmoothTransformation)
    pix_pan = (valeur16b(67, data)) * view.width()
    pix_tilt = (valeur16b(69, data)) * view.height()
    pix_width = (valeur16b(71, data)) * view.width() / 1700
    pix_height = (valeur16b(73, data)) * view.height() / 1000
    pix.setOpacity(data[60] / 255)
    trans = PyQt6.QtGui.QTransform()
    trans.setMatrix(pix_width / 65535, 0, 0, 0, pix_height / 65535, 0, pix_pan / 65535, pix_tilt / 65535, 1)
    pix.setTransform(trans)
    pix.setTransformOriginPoint(pix.boundingRect().center())
    pix.setRotation(360 * (valeur16b(65, data)) / 65535)

def picture_sacn(level):
    global pix
    # Map the level to the correct image index
    if level < 23:
        # No picture for levels 0 to 22
        pix.setPixmap(PyQt6.QtGui.QPixmap())  # Set an empty pixmap
    else:
        # Calculate the image index for levels 23 to 255
        image_index = ((level - 23) // 23) + 1  # Map to range 1-10
        image_index = min(image_index, 10)  # Ensure it doesn't exceed 10

        if image_index in image_cache:
            pix.setPixmap(image_cache[image_index])

# Function to process DMX data from the queue
def process_dmx_data(data):
    line_update(data)

# Connect the DMX signal to the processing function
receiver_thread.dmx_signal.connect(process_dmx_data)

# Start the OLA wrapper in the main thread
receiver_thread.wrapper.Run()

app.exec()