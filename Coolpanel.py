import sys
import subprocess

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction, QKeySequence
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QTabWidget,
    QVBoxLayout, QHBoxLayout, QGridLayout, QFormLayout,
    QLabel, QPushButton, QLineEdit, QCheckBox, QRadioButton, QButtonGroup,
    QComboBox, QTableWidget, QTableWidgetItem, QHeaderView,
    QMessageBox, QDialog, QStatusBar, QToolBar
)

class BaseWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        canvas = QWidget()
        # 1. Set the basic window details
        self.button = QPushButton("whoami",canvas)
        self.button.move(0,50)
        self.button.resize(100,75)
        self.button.clicked.connect(self.run)

        self.button1 = QPushButton("ping",canvas)
        self.button1.move(100,50)
        self.button1.resize(100,75)
        self.button1.clicked.connect(self.run2)

        self.button2 = QPushButton("trace route",canvas)
        self.button2.move(200,50)
        self.button2.resize(100,75)
        self.button2.clicked.connect(self.run3)

        self.button2 = QPushButton("dns lookup",canvas)
        self.button2.move(300,50)
        self.button2.resize(100,75)
        self.button2.clicked.connect(self.run4)

        self.button2 = QPushButton("arp table",canvas)
        self.button2.move(0,125)
        self.button2.resize(100,75)
        self.button2.clicked.connect(self.run5)
        self.textbox =  QLineEdit(canvas)

        self.textbox.setPlaceholderText("ip goes here")
        self.textbox.resize(400,50)

        self.setWindowTitle("Super epic ddos tool 5000😎😎😎😎😎")
        self.resize(400, 300)
        self.setCentralWidget(canvas)
        self.setMaximumSize(400,300)
        self.setMinimumSize(400,300)
 
    def run(self):
        QMessageBox.information(None, "Result", subprocess.getoutput("whoami"))
    def run2(self):
        ip = self.textbox.text()
        if ip:
            QMessageBox.information(None, "Result", subprocess.getoutput(f"ping {ip} -n 1"))
    def run3(self):
        ip = self.textbox.text()
        if ip:
            QMessageBox.information(None, "Result",subprocess.getoutput(f"tracert -d {ip}"))
    def run4(self):
        ip = self.textbox.text()
        if ip:
            QMessageBox.information(None, "Result",subprocess.getoutput(f"nslookup {ip}"))
    def run5(self):
        QMessageBox.information(None, "Result",subprocess.getoutput(f"arp -a"))
if __name__ == "__main__":
    # 2. Initialize the application infrastructure
    app = QApplication(sys.argv)
    
    # 3. Create and display the window object
    window = BaseWindow()
    window.show()
    
    # 4. Start the main event loop and wait for the user to close it
    sys.exit(app.exec())
