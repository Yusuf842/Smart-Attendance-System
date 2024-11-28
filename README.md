Smart Attendance System

## Application Overview
**EduTrack: Smart Attendance System** is a face-recognition-based attendance management tool, designed for educational environments such as schools and colleges. It features an intuitive interface for efficient attendance tracking.

### Features
1. **Face Recognition**: Marks attendance using a camera.
2. **Add/Remove Student**: Manage student records and face data.
3. **Clear Attendance**: Reset attendance records.
4. **Save Attendance**: Export attendance data to a CSV file.
5. **Real-Time Updates**: Status display and attendance summaries.

---

### Code Overview

- **`main.py`**: Initializes the application and handles core processes.
- **`gui.py`**: Manages the graphical user interface using PySide6.
- **`camera.py`**: Handles camera operations.
- **`data_manager.py`**: Manages student data and face encodings.
- **`face_recognition_handler.py`**: Detects and recognizes faces using the `face_recognition` library.
- **`attendance_manager.py`**: Updates attendance records and table views.
- **`ui_manager.py`**: Handles UI updates and CSV exports.
- **`recognizer.py`**: Orchestrates face recognition processes.

---

### Setup Instructions

1. Use **Python 3.10** or above.
2. Install the required dependencies:
   ```bash
   pip install PySide6 opencv-python face_recognition numpy
   ```
3. Run the application:
   ```bash
   python main.py
   ```