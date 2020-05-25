# -*- coding: UTF-8 -*-

import os, sys
from PySide2.QtWidgets import QApplication, QWidget
from widget import *


def main(argv):
    app = QApplication(argv)

    widget = Widget()
    widget.show()

    return app.exec_()

if '__main__' == __name__:
    os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = './platforms'
    exit_status = main(sys.argv)
    sys.exit(exit_status)