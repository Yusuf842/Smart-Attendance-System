import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QTimer
from gui import AttendanceSystem
from camera import Camera
from data_manager import DataManager
from face_recognition_handler import FaceRecognitionHandler
from attendance_manager import AttendanceManager
from ui_manager import UIManager
from recognizer import Recognizer

class MainApp:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.attendance_system = AttendanceSystem()
        self.camera = Camera(self.attendance_system.cameraLabel)
        self.data_manager = DataManager('data.json')
        self.face_recognition_handler = FaceRecognitionHandler(
            self.data_manager.known_face_encodings,
            self.data_manager.known_face_names
        )
        self.attendance_manager = AttendanceManager(self.data_manager, self.attendance_system)
        self.ui_manager = UIManager(self.attendance_system, self.data_manager, self.attendance_manager)
        self.recognizer = Recognizer(self.face_recognition_handler, self.data_manager, self.attendance_manager, self.camera, self.ui_manager)
        self.timer = QTimer()
        self.check_data_timer = QTimer()
        self.setup_connections()
        self.attendance_system.show()
        self.ui_manager.populate_table()
        self.setup_check_data_timer()

    def setup_connections(self):
        self.attendance_system.connectCameraButton.clicked.connect(self.toggle_camera)
        self.attendance_system.addStudentButton.clicked.connect(self.add_new_student)
        self.attendance_system.removeStudentButton.clicked.connect(self.remove_student)
        self.attendance_system.clearAttendanceButton.clicked.connect(self.clear_attendance)
        self.attendance_system.refreshButton.clicked.connect(self.refresh_data)

    def refresh_data(self):
        for roll_number, details in self.data_manager.get_students().items():
            details['arrival_time'] = None  
        self.data_manager.save_data() 
        self.ui_manager.populate_table()  

    def setup_check_data_timer(self):
        self.check_data_timer.timeout.connect(self.check_data_file)
        self.check_data_timer.start(1000) 

    def check_data_file(self):
        if self.data_manager.get_students() and self.data_manager.known_face_encodings:
            if not self.timer.isActive():
                self.start_face_recognition()
        else:
            if self.timer.isActive():
                self.timer.stop()
            print("No known face encodings available.")

    def toggle_camera(self):
        if self.camera.camera_connected:
            self.camera.disconnect_camera()
            self.ui_manager.append_status("Camera disconnected.")
        else:
            if self.camera.connect_camera():
                self.ui_manager.append_status("Camera connected.")
            else:
                self.ui_manager.append_status("Failed to connect to camera.")

    def add_new_student(self):
        print("Adding new student")
        name = self.attendance_system.studentNameInput.text()
        roll_number = self.attendance_system.rollNumberInput.text()
        if name and roll_number:
            if roll_number in self.data_manager.get_students():
                self.ui_manager.append_status("Student data already exists.")
                return

            if self.camera.camera_connected:
                ret, frame = self.camera.capture_image()
                if ret:
                    print("Captured image for new student")
                    if self.data_manager.add_student(roll_number, name, frame):
                        self.ui_manager.populate_table()  
                        self.ui_manager.append_status(f"Student added and image saved as {roll_number}_{name}.png")
                        self.face_recognition_handler.known_face_encodings = self.data_manager.known_face_encodings
                        self.face_recognition_handler.known_face_names = self.data_manager.known_face_names
                        print("Updated face recognition handler with new encodings")
                        self.check_data_file()
                    else:
                        self.ui_manager.append_status("Failed to capture image from camera.")
            else:
                self.ui_manager.append_status("Camera is not connected.")
        else:
            self.ui_manager.append_status("Please enter both name and roll number.")


    def remove_student(self):
        print("Removing student")
        self.ui_manager.remove_student()
        self.ui_manager.append_status("Student removed.")
        self.face_recognition_handler.known_face_encodings = self.data_manager.known_face_encodings
        self.face_recognition_handler.known_face_names = self.data_manager.known_face_names
        self.check_data_file()  

    def clear_attendance(self):
        print("Clearing attendance")
        self.ui_manager.clear_attendance()
        self.ui_manager.append_status("Attendance cleared.")
        self.face_recognition_handler.known_face_encodings = self.data_manager.known_face_encodings
        self.face_recognition_handler.known_face_names = self.data_manager.known_face_names
        self.check_data_file()  

    def start_face_recognition(self):
        print("Starting face recognition")
        self.timer.timeout.connect(self.recognizer.recognize_faces)
        self.timer.start(1000)

    def run(self):
        sys.exit(self.app.exec())

if __name__ == '__main__':
    main_app = MainApp()
    main_app.run()