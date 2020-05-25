# -*- Coding: utf-8 -*-

import sys, os
from enum import IntEnum

from PySide2.QtCore import Qt, QRect, QRectF, QLine, QLineF, QPoint
from PySide2.QtGui import QPainter, QPen, QMouseEvent, QHoverEvent, QBrush, QPen, QPixmap, QColor
from PySide2.QtWidgets import QApplication, QWidget, QGraphicsLineItem, \
    QGraphicsItem, QGraphicsRectItem, QGraphicsView, QGraphicsScene, QGraphicsSceneMouseEvent, QGraphicsTextItem, \
    QGraphicsSceneHoverEvent


class RectItem(QGraphicsRectItem):

    def __init__(self, name, x, y, w, h):
        super().__init__(x, y, w, h)
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setAcceptHoverEvents(True)

        self.__name = name
        # self.__textItem = QGraphicsTextItem(self.__name, self)
        self.__line_end = None
        self.__line_point_end = None

        self.pt1_capture = False
        self.pt2_capture = False

        pen = QPen()
        pen.setWidth(5)
        pen.setStyle(Qt.DashDotLine)
        self.setPen(pen)

        self.__captureObject = None

        # self.__textItem.setPos(self.rect().width()/2, self.rect().height()/2)

    def __updateTextPos(self):
        x = self.rect().width()/2
        y = self.rect().height()/2
        #self.__textItem.setPos(self.rect().height()/2, self.rect().width()/2)

    # def setEndsText(self, bold: bool=False, color: QColor=Qt.black):
    #     color = 'red' if color == Qt.red else 'black'
    #     style = f'color="{color}"'
    #     text = f'<font {style}><b>{self.__name}</b></font>' if bold else f'<font {style}><p>{self.__name}</p></font>'
    #     self.__textItem.setHtml(text)

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent):
        self.setCursor(Qt.ClosedHandCursor)
        # self.setEndsText(True, Qt.red)
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event: QGraphicsSceneMouseEvent):
        if self.isSelected():
            self.setCursor(Qt.ClosedHandCursor)
            if self.__captureObject is not None:
                x = (2 * self.scenePos().x() + self.rect().width()) / 2
                y = (2 * self.scenePos().y() + self.rect().height()) / 2

                self.__captureObject.moveObject(self, QPoint(x, y))
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event: QGraphicsSceneMouseEvent):
        self.setSelected(False)
        # self.setEndsText()
        self.setCursor(Qt.ArrowCursor)
        super().mouseReleaseEvent(event)

    def hoverMoveEvent(self, event: QHoverEvent):
        if not self.isSelected():
            self.setCursor(Qt.OpenHandCursor)
            # self.setEndsText(True)
            super().hoverMoveEvent(event)

    def hoverLeaveEvent(self, event: QHoverEvent):
        self.setCursor(Qt.ArrowCursor)
        self.setSelected(False)
        # self.setEndsText()
        super().hoverLeaveEvent(event)

    def __repr__(self):
        return self.__name

    def tryCapture(self, object):
        if self.__captureObject is None:
            pen = self.pen()
            pen.setColor(Qt.red)
            self.setPen(pen)
            self.update()

    def unCapture(self, object):
        if self.__captureObject is None:
            pen = self.pen()
            pen.setColor(Qt.black)
            self.setPen(pen)
            self.update()

    def capture(self, object):
        if self.__captureObject is None:
            self.__captureObject = object
            pen = self.pen()
            pen.setColor(Qt.black)
            self.setPen(pen)
            self.update()


class MoveLineEnds(IntEnum):
    NONE = 0
    P1 = 1
    P2 = 2
    BOTH = 3


class ArrowItem(QGraphicsLineItem):

    MOUSE_MARGIN = 20
    ENDS_TEXT_SHIFT_X = 20
    ENDS_TEXT_SHIFT_Y = 0
    TEXT_SHIFT = QPoint(ENDS_TEXT_SHIFT_X, ENDS_TEXT_SHIFT_Y)

    def __init__(self, line: QLineF):
        super().__init__(line)
        self.setAcceptHoverEvents(True)
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        pen = QPen()
        pen.setWidth(5)
        self.setPen(pen)
        self.__p1Ends = QGraphicsTextItem('1', self)
        self.__p2Ends = QGraphicsTextItem('2', self)
        self.__updateTextLinePos()

        self.__currentEndsMove = MoveLineEnds.NONE
        self.__currentEndsHover = MoveLineEnds.NONE
        self.__endsCapture = [None, None]

        self.__tryCapture = None

        self.__blockMove = False

    def __updateTextLinePos(self):
        if self.line().p1().x() < self.line().p2().x():
            self.__p1Ends.setPos(self.line().p1()-self.TEXT_SHIFT)
            self.__p2Ends.setPos(self.line().p2()+self.TEXT_SHIFT)
        else:
            self.__p1Ends.setPos(self.line().p1()+self.TEXT_SHIFT)
            self.__p2Ends.setPos(self.line().p2()-self.TEXT_SHIFT)

    def setEndsText(self, moveLineEnds: MoveLineEnds, bold: bool=False, color: QColor=Qt.black):
        if moveLineEnds == MoveLineEnds.NONE:
            return

        if moveLineEnds == MoveLineEnds.BOTH:
            self.setEndsText(MoveLineEnds.P1, bold, color)
            self.setEndsText(MoveLineEnds.P2, bold, color)
            return

        color = 'red' if color == Qt.red else 'black'
        style = f'color="{color}"'
        index = int(moveLineEnds)
        text = f'<font {style}><b>{index}</b></font>' if bold else f'<font {style}><p>{index}</p></font>'
        if moveLineEnds == MoveLineEnds.P1:
            self.__p1Ends.setHtml(text)
            return
        if moveLineEnds == MoveLineEnds.P2:
            self.__p2Ends.setHtml(text)
            return

    @classmethod
    def isInBox(cls, mousePosition: QPoint, objectPosition: QPoint):
        x_ok = mousePosition.x() - cls.MOUSE_MARGIN <= objectPosition.x() <= mousePosition.x() + cls.MOUSE_MARGIN
        y_ok = mousePosition.y() - cls.MOUSE_MARGIN <= objectPosition.y() <= mousePosition.y() + cls.MOUSE_MARGIN
        return x_ok and y_ok

    def hoverEnterEvent(self, event: QGraphicsSceneHoverEvent):
        if self.__blockMove:
            return

        if self.__currentEndsMove != MoveLineEnds.NONE:
            return

        p1_ok = self.isInBox(event.pos(), self.line().p1())
        p2_ok = self.isInBox(event.pos(), self.line().p2())

        if p1_ok:
            self.setEndsText(MoveLineEnds.P1, True)
            self.setCursor(Qt.OpenHandCursor)
            self.setSelected(False)
            self.__currentEndsHover = MoveLineEnds.P1
            return

        if p2_ok:
            self.setEndsText(MoveLineEnds.P2, True)
            self.setCursor(Qt.OpenHandCursor)
            self.setSelected(False)
            self.__currentEndsHover = MoveLineEnds.P2
            return

        if not self.isSelected():
            self.setCursor(Qt.OpenHandCursor)
            self.__currentEndsHover = MoveLineEnds.BOTH
            self.setEndsText(MoveLineEnds.BOTH, True)
            super().hoverMoveEvent(event)

    def hoverLeaveEvent(self, event: QHoverEvent):

        if self.__blockMove:
            return

        if self.__currentEndsMove != MoveLineEnds.NONE:
            return

        self.setEndsText(MoveLineEnds.BOTH)
        self.setCursor(Qt.ArrowCursor)
        self.setSelected(False)
        super().hoverLeaveEvent(event)


    def mousePressEvent(self, event: QGraphicsSceneMouseEvent):
        if self.__blockMove:
            return

        if self.__currentEndsMove != MoveLineEnds.NONE:
            return

        if self.isInBox(event.pos(), self.line().p1()) and self.__endsCapture[0] is None:
            self.__currentEndsMove = MoveLineEnds.P1
            self.setEndsText(MoveLineEnds.P1, True, Qt.red)
            self.setCursor(Qt.ClosedHandCursor)
            return

        if self.isInBox(event.pos(), self.line().p2()) and self.__endsCapture[1] is None:
            self.__currentEndsMove = MoveLineEnds.P2
            self.setEndsText(MoveLineEnds.P2, True, Qt.red)
            self.setCursor(Qt.ClosedHandCursor)
            return

        if self.__endsCapture[0] is None and self.__endsCapture[1] is None:
            self.__currentEndsMove = MoveLineEnds.BOTH
            self.setEndsText(MoveLineEnds.BOTH, True, Qt.red)
            self.setCursor(Qt.ClosedHandCursor)
            super().mousePressEvent(event)

    def mouseReleaseEvent(self, event: QGraphicsSceneMouseEvent):
        if self.__blockMove:
            return

        self.setCursor(Qt.OpenHandCursor)
        self.setEndsText(self.__currentEndsMove, True)

        if self.__tryCapture is not None:
            print(type(self.__tryCapture))
            self.__tryCapture.capture(self)
            if self.__currentEndsMove == MoveLineEnds.P1:
                self.__endsCapture[0] = self.__tryCapture
            else:
                self.__endsCapture[1] = self.__tryCapture
        self.__tryCapture = None

        self.__currentEndsMove = MoveLineEnds.NONE

    def mouseMoveEvent(self, event: QGraphicsSceneMouseEvent):

        if self.__blockMove:
            return
        if self.__currentEndsMove == MoveLineEnds.NONE:
            return

        if self.__tryCapture is not None:
            self.__tryCapture.unCapture(self)

        if self.__currentEndsMove == MoveLineEnds.P1:
            line = QLineF(event.pos(), self.line().p2())
            self.setLine(line)
            self.__updateTextLinePos()
            rect = self.__filteredCapturedObject()
            print(rect)
            if 1 == len(rect):
                rect = rect[0]
                self.__tryCapture = rect
                self.__tryCapture.tryCapture(self)
            self.update()
            return

        if self.__currentEndsMove == MoveLineEnds.P2:
            line = QLineF(self.line().p1(), event.pos())
            self.setLine(line)
            self.__updateTextLinePos()
            rect = self.__filteredCapturedObject()
            print(rect)
            if 1 == len(rect):
                rect = rect[0]
                self.__tryCapture = rect
                self.__tryCapture.tryCapture(self)
            self.update()
            return

        if self.__currentEndsMove == MoveLineEnds.BOTH:
            super().mouseMoveEvent(event)
            self.__updateTextLinePos()
            self.update()
            return

    def moveObject(self, object, pos):

        if object is self.__endsCapture[0]:
            line = QLineF(pos, self.line().p2())
            self.__blockMove = True
            self.setLine(line)
            self.__updateTextLinePos()
            self.__blockMove = False
            return
        if object is self.__endsCapture[1]:
            line = QLineF(self.line().p1(), pos)
            self.__blockMove = True
            self.setLine(line)
            self.__updateTextLinePos()
            rect = self.collidingItems()
            self.__blockMove = False
            return

    def __filteredCapturedObject(self):
        rect = self.collidingItems()
        try:
            rect.remove(self.__endsCapture[0])
            for ch in self.__endsCapture[0].children():
                try:
                    rect.remove(ch)
                except:
                    ...
        except:
            ...
        try:
            rect.remove(self.__endsCapture[1])
            for ch in self.__endsCapture[1].children():
                try:
                    rect.remove(ch)
                except:
                    ...
        except:
            ...
        return rect





def main(argv):
    app = QApplication(argv)

    scene = QGraphicsScene(0, 0, 500, 500)
    scene.setItemIndexMethod(QGraphicsScene.NoIndex)

    brush = QBrush(Qt.red)

    brush_brics = QBrush(QPixmap('brick_texture.jpg'))
    brush_brics.setStyle(Qt.TexturePattern)

    pen = QPen()
    pen.setWidth(5)
    pen.setStyle(Qt.DashLine)

    rectItem = RectItem('r1', 20, 10, 200, 100)
    rectItem.setBrush(brush)

    rectItem2 = RectItem('r2', 20, 10, 150, 250)
    rectItem2.setPen(pen)
    rectItem2.setBrush(brush_brics)
    rectItem2.setOpacity(70)
    arrowItem = ArrowItem(QLine(50, 200, 300, 400))
    scene.addItem(arrowItem)
    scene.addItem(rectItem)
    scene.addItem(rectItem2)

    view = QGraphicsView(scene)
    view.show()

    return app.exec_()


if __name__ == '__main__':

    os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = './platforms'

    exit_status = main(sys.argv)
    sys.exit(exit_status)