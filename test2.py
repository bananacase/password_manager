import sys
from PyQt5.QtWidgets import QWidget, QPushButton, QApplication, QLabel, QHBoxLayout, QVBoxLayout, QDesktopWidget
from PyQt5.QtCore import QCoreApplication
from PyQt5 import QtGui

class MyWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        q = QDesktopWidget().availableGeometry()
        print('width', q.width())
        print('height', q.height())

        #размеры окна
        HSWindow = 800
        VSWindow = 600

        #расположение
        XWindow = 300
        YWindow = 300

        #шрифт
        font = QtGui.QFont()
        font.setPointSize(14)

        #кнопка чтения
        qbtn = QPushButton('Прочитать пароли', self)
        qbtn.clicked.connect(QCoreApplication.instance().quit)
        qbtn.resize(130, 30)
        qbtn.move(HSWindow // 4, VSWindow // 2)

        #кнопка записывания
        qbtn = QPushButton('Записать пароли', self)
        qbtn.clicked.connect(QCoreApplication.instance().quit)
        qbtn.resize(130, 30)
        qbtn.move(HSWindow / 4 * 2.5, VSWindow // 2)

        qlbl = QLabel('Hello', self)
        qlbl.resize(100, 100)
        qlbl.move(HSWindow // 2, VSWindow // 10)
        qlbl.setFont(font)

        self.setGeometry(XWindow, YWindow, HSWindow, VSWindow)
        self.setWindowTitle('Main window')
        self.show()

if __name__ == '__main__':

    app = QApplication(sys.argv)
    mw = MyWindow()
    sys.exit(app.exec_())
