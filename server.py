import socket
import threading
import sys
import subprocess
from PyQt6.QtCore import Qt, pyqtSignal, QObject
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
    def __init__(self):
        super().__init__()
        canvas = QWidget()
        # 1. Set the basic window details
        self.text = QTextEdit(canvas)
        self.text.setReadOnly(True)
        self.text.resize(400,300)


        signals.log_message.connect(self.textedit)
        self.setWindowTitle("Server")
        self.resize(400, 300)
        self.setCentralWidget(canvas)
        self.setMaximumSize(400,300)
        self.setMinimumSize(400,300)
    def textedit(self,add=str):
        self.text.append(add)


HOST = '0.0.0.0'  # Listen on all interfaces
PORT = int(input("PORT: "))

clients = {}  # room_id: list of (conn, nickname)

def broadcast(room_id, message, sender_conn):
    for conn, _ in clients[room_id]:
        if conn != sender_conn:
            try:
                conn.sendall(message.encode())
            except:
                pass  # Client might be disconnected

def handle_client(conn, addr):
    try:
        conn.sendall("Enter room ID: ".encode())
        room_id = conn.recv(1024).decode().strip()

        conn.sendall("Enter your nickname: ".encode())
        nickname = conn.recv(1024).decode().strip()

        if room_id not in clients:
            clients[room_id] = []

        clients[room_id].append((conn, nickname))

        welcome = f"[{nickname} has joined room '{room_id}']"
        signals.log_message.emit(welcome)
        broadcast(room_id, welcome, conn)

        while True:
            data = conn.recv(1024)
            if not data:
                break
            message = f"{nickname}: {data.decode()}"
            signals.log_message.emit(f"Room: {room_id}, Nick: {nickname}: {data.decode()}")
            broadcast(room_id, message, conn)
    except:
        pass
    finally:
        # Remove client from room
        for rid in clients:
            clients[rid] = [c for c in clients[rid] if c[0] != conn]
        conn.close()

def start_server():
    signals.log_message.emit(f"Server starting on port {PORT}...\n")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen()

    while True:
        conn, addr = s.accept()
        threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BaseWindow()
    window.show()
    thread = threading.Thread(target=start_server,daemon=True,).start()
    
    sys.exit(app.exec())

