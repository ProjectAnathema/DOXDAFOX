import socket
import threading
import sys
import subprocess
from PyQt6.QtCore import Qt,pyqtSignal, QObject
from PyQt6.QtGui import QAction, QKeySequence
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QTabWidget,
    QVBoxLayout, QHBoxLayout, QGridLayout, QFormLayout,
    QLabel, QPushButton, QLineEdit,QTextEdit, QCheckBox, QRadioButton, QButtonGroup,
    QComboBox, QTableWidget, QTableWidgetItem, QHeaderView,
    QMessageBox, QDialog, QStatusBar, QToolBar
)
class ServerSignals(QObject):
    log_message = pyqtSignal(str)
signals = ServerSignals()
class BaseWindow(QMainWindow):
    def __init__(self,sock):
        super().__init__()
        self.sock = sock
        canvas = QWidget()
        # 1. Set the basic window details
        self.button = QPushButton("send",canvas)
        self.button.move(700,0)
        self.button.resize(100,50)
        self.button.clicked.connect(self.run)
        self.textbox = QLineEdit(canvas)
        self.textbox.setPlaceholderText("Message")
        self.textbox.resize(700,50)
        self.text = QTextEdit(canvas)
        self.text.setReadOnly(True)
        self.text.resize(800,250)
        self.text.move(0,50)
        self.setWindowTitle(f"Host: {HOST}, Port: {PORT}, Room: {room_id}, Nick: {nickname}, Have fun!")
        self.resize(800, 300)
        self.setCentralWidget(canvas)
        self.setMaximumSize(800,300)
        self.setMinimumSize(800,300)
        signals.log_message.connect(self.receive)
    def run(self):
        self.sock.sendall(self.textbox.text().encode())
    def receive(self,add=str):
        self.text.append(add)



HOST = input("Enter server IP (e.g., 127.0.0.1): ")
PORT = int(input("Enter server PORT (e.g., 12345): "))

def receive_messages(sock):
    while True:
        try:
            data = sock.recv(1024)
            if not data:
                break
            signals.log_message.emit(data.decode())
        except:
            break

def main():
    global s
    global room_id
    global nickname
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))

    # Room ID
    data = s.recv(1024).decode()
    room_id = input(data)
    s.sendall(room_id.encode())

    # Nickname
    data = s.recv(1024).decode()
    nickname = input(data)
    s.sendall(nickname.encode())

    threading.Thread(target=receive_messages, args=(s,), daemon=True).start()

            
if __name__ == "__main__":
    main()
    app = QApplication(sys.argv)
    window = BaseWindow(s)
    window.show()
    sys.exit(app.exec())
    