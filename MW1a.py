from PySide2.QtWidgets import *
from PySide2.QtGui import QMouseEvent, Qt, QKeyEvent
from PySide2.QtCore import QObject, QEvent
from datetime import datetime
from math import sqrt
from random import randint
from ru_to_us import ru_to_us





class MouseWidget_a(QWidget):
	def __init__(self, parent=None):
		super().__init__(parent)
		self.setMouseTracking(True)
		self.__label = QLabel(self)
		self.__label1 = QLabel(self)
		layout = QHBoxLayout(self)
		layout.addWidget(self.__label)
		layout.addWidget(self.__label1)
		self.__label.setText('A')
		self.__label1.setText('B')
		self.setLayout(layout)
		self.__label.setFixedSize(200, 40)
		self.__label1.setFixedSize(200, 40)
		self.resize(500, 400)
		self.__moved = False

		self.__press_cnt, self.__release_cnt = 0, 0
		self.__x, self.__y = 0, 0
		self.__t = datetime.now()
		self.__t1 = datetime.now()

	#1a
	# def mouseMoveEvent(self, event: QMouseEvent):
	# 	pos = event.pos()
	# 	x, y = pos.x(), pos.y()
	# 	text = f'(x, y) = ({x}, {y})'
	# 	self.__label.setText(text)

	#1b
	# def mousePressEvent(self, event: QMouseEvent):
	# 	if event.MouseButtonPress:
	# 		self.__press_cnt += 1
	# 		text = f'{self.__press_cnt}: MousePressed'
	# 		self.__label.setText(text)
	#
	# def mouseReleaseEvent(self, event:QMouseEvent):
	# 	if event.MouseButtonRelease:
	# 		self.__release_cnt += 1
	# 		text = f'{self.__release_cnt}: MouseReleased'
	# 		self.__label1.setText(text)

	# 1c
	# def mousePressEvent(self, event: QMouseEvent):
	# 	if event.button() == Qt.RightButton:
	# 		text = f'Right button pressed'
	# 		self.__label.setText(text)
	# 	if event.button() == Qt.LeftButton:
	# 		text = f'Left button pressed'
	# 		self.__label.setText(text)

	# 1d
	# def mousePressEvent(self, event: QMouseEvent):
	# 	if event.button() == Qt.LeftButton:
	# 		self.setCursor(Qt.WaitCursor)
	#
	# def mouseReleaseEvent(self, event: QMouseEvent):
	# 	self.setCursor(Qt.ArrowCursor)

	# 1e
	# def mouseMoveEvent(self, event: QMouseEvent):
	# 	if self.__moved:
	# 		x = event.globalX() - self.__x
	# 		y = event.globalY() - self.__y
	# 		self.move(x, y)
	#
	#
	# def mousePressEvent(self, event: QMouseEvent):
	# 	if event.button() == Qt.LeftButton:
	# 		self.setCursor(Qt.ClosedHandCursor)
	# 		self.__moved = True
	# 		self.__x = event.pos().x()
	# 		self.__y = event.pos().y()
	#
	# def mouseReleaseEvent(self, event: QMouseEvent):
	# 	if event.MouseButtonRelease:
	# 		self.setCursor(Qt.ArrowCursor)
	# 		self.__moved = False

	# 1f
	# def __f(self, event):
	# 	t = self.pos().x() < event.globalX() < self.pos().x()+self.size().width()
	# 	t = t or self.pos().y() < event.globalY() < self.pos().x()+self.size().height()
	# 	return t
	#
	# def mouseMoveEvent(self, event: QMouseEvent):
	# 	if self.__f(event):
	# 		x, y = event.globalX()+randint(-150, 150), event.globalY()+randint(-150, 150)
	# 		self.move(x, y)
	# 		self.repaint()



	# 1g
	# def mousePressEvent(self, event: QMouseEvent):
	# 	self.__t = datetime.now()
	#
	# def mouseReleaseEvent(self, event:QMouseEvent):
	# 	self.__t1 = datetime.now()
	# 	dt = (self.__t1 - self.__t).microseconds
	# 	self.__label.setText(str(dt))


	# 2a
	# def mouseMoveEvent(self, event: QMouseEvent):
	# 	t = datetime.now()
	# 	dt = (t - self.__t).microseconds
	# 	dx = (event.x() - self.__x)/dt
	# 	dy = (event.y() - self.__y)/dt
	# 	self.__x, self.y, self.__t = event.x(), event.y(), t
	# 	v = (10**6)*sqrt(dx**2+dy**2)
	#
	# 	self.__label.setText(str(v))

	# 2b
	# def keyReleaseEvent(self, event: QKeyEvent):
	# 	t = datetime.now()
	# 	dt = (t - self.__t1).microseconds/1000
	# 	self.__label.setText(str(dt))

	# 3
class FilterWidget(QWidget):

	def __init__(self, parent=None):
		super().__init__(parent)
		self.__lineEdit = QLineEdit(self)
		self.__lineEdit.installEventFilter(self)

	def eventFilter(self, target: QObject, event: QEvent):

		if event.type() == QEvent.KeyPress:
			if target is self.__lineEdit:
				if event.key() in ru_to_us:
					key = ru_to_us[event.key()]
					self.__lineEdit.setText(self.__lineEdit.text()+chr(key))
					return True
				self.__lineEdit.keyPressEvent(event)
				return True
		return super().eventFilter(target,event)