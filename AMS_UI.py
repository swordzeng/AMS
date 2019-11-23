from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget
import sys

class Ui_MainWindow(QtWidgets.QMainWindow):
	def __init__(self, parent=None):

		QtWidgets.QWidget.__init__(self, parent=None)
		self.setWindowTitle('AMS')

if __name__ == '__main__':
	#字体大小自适应分辨率
	QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
	app = QtWidgets.QApplication(sys.argv)
	ui = Ui_MainWindow()
	ui.show()
	sys.exit(app.exec_())