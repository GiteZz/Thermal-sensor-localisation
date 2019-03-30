from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QGraphicsScene, QFileDialog, QCheckBox, QLabel, QHBoxLayout


class ZoomQGraphicsView(QtWidgets.QGraphicsView):
    def __init__ (self, parent=None):
        super(ZoomQGraphicsView, self).__init__ (parent)

    def wheelEvent(self, event):
        # Zoom Factor
        zoomInFactor = 1.25
        zoomOutFactor = 1 / zoomInFactor

        # Set Anchors
        self.setTransformationAnchor(QtWidgets.QGraphicsView.NoAnchor)
        self.setResizeAnchor(QtWidgets.QGraphicsView.NoAnchor)

        # Save the scene pos
        oldPos = self.mapToScene(event.pos())

        # Zoom
        print(event.angleDelta())
        if event.angleDelta().y() > 0:
            zoomFactor = zoomInFactor
        else:
            zoomFactor = zoomOutFactor
        self.scale(zoomFactor, zoomFactor)

        # Get the new position
        newPos = self.mapToScene(event.pos())

        # Move scene to old position
        delta = newPos - oldPos
        self.translate(delta.x(), delta.y())

class Sensor:
    def __init__(self, sensor_type, sensor_id=None, file_name=None, data=None):
        self.sensor_type = sensor_type
        self.data = data
        self.file_name = file_name
        self.sensor_id = sensor_id

        self.layout = None
        self.label = None
        self.checkbox = None

        self.checkbox_callback = None

    def checkbox_activate(self):
        self.checkbox_callback(self)

    def create_ui(self, callback):
        self.layout = QHBoxLayout()
        self.label = QLabel(f'{self.sensor_type}: {self.sensor_id if self.sensor_id is not None else self.file_name}')
        self.checkbox = QCheckBox()
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.checkbox)

        self.checkbox_callback = callback
        self.checkbox.stateChanged.connect(self.checkbox_activate)

        return

