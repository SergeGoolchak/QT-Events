from PySide2.QtWidgets import *
from PySide2.QtGui import QMouseEvent, Qt, QKeyEvent
from PySide2.QtCore import QObject, QEvent







class Widget(QWidget):

	def __init__(self, parent=None):
		super().__init__(parent)
		self.setWindowTitle(self.tr('Lab 3. Signal and Slot'))
		self.cnt = 0

		layout = QHBoxLayout()

		slider = QSlider(Qt.Horizontal, self)
		slider.setMinimum(0)
		slider.setMaximum(100)
		slider.setPageStep(1)
		spinBox = QSpinBox(self)
		spinBox.setMinimum(0)
		spinBox.setMaximum(100)
		progressBar = QProgressBar(self)

		layout.addWidget(slider)
		layout.addWidget(spinBox)
		layout.addWidget(progressBar)

		self.setLayout(layout)
		slider.valueChanged.connect(spinBox.setValue)
		slider.valueChanged.connect(progressBar.setValue)
		spinBox.valueChanged.connect(slider.setValue)






