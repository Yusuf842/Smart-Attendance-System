from datetime import datetime

class Recognizer:
    def __init__(self, face_recognition_handler, data_manager, attendance_manager, camera, ui_manager):
        self.face_recognition_handler = face_recognition_handler
        self.data_manager = data_manager
        self.attendance_manager = attendance_manager
        self.camera = camera
        self.ui_manager = ui_manager

    def recognize_faces(self):
        if not self.camera.camera_connected:
            return

        ret, frame = self.camera.capture_image()
        if not ret:
            return

        rgb_frame = frame[:, :, ::-1]
        recognized_faces = self.face_recognition_handler.recognize_faces(rgb_frame)

        for roll_number, _ in recognized_faces:
            name = self.data_manager.get_students()[roll_number]['name']
            self.attendance_manager.mark_present(roll_number, name)
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.data_manager.update_arrival_time(roll_number, current_time)
            self.ui_manager.update_specific_row(roll_number)
        self.ui_manager.update_summary()
