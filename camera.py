import cv2
from PySide6.QtCore import QTimer
from PySide6.QtGui import QImage, QPixmap

class Camera:
    def __init__(self, label):
        self.cap = None
        self.timer = QTimer()
        self.camera_connected = False
        self.label = label

    def connect_camera(self):
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            return False
        self.camera_connected = True
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(20)
        return True

    def disconnect_camera(self):
        self.timer.stop()
        if self.cap:
            self.cap.release()
        self.label.clear()
        self.camera_connected = False

    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            frame = self.resize_frame(frame)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            height, width, channel = frame.shape
            bytes_per_line = 3 * width
            q_img = QImage(frame.data, width, height, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(q_img)
            self.label.setPixmap(pixmap)

    def resize_frame(self, frame, size=(640, 480)):
        return cv2.resize(frame, size)

    def capture_image(self):
        ret, frame = self.cap.read()
        if ret:
            frame = self.resize_frame(frame)
        return ret, frame
