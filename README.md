## Smart Attendance System

### Application Overview
**Smart Attendance System** is a face-recognition-based attendance management tool, designed for educational environments such as schools and colleges. It features an intuitive interface for efficient attendance tracking.

### Features
1. **Face Recognition**: Marks attendance using a camera.
2. **Add/Remove Student**: Manage student records and face data.
3. **Clear Attendance**: Reset attendance records.
4. **Save Attendance**: Export attendance data to a CSV file.
5. **Real-Time Updates**: Status display and attendance summaries.

---

### Setup Instructions

#### Windows
1. Install [Visual Studio Build Tools 2022](https://visualstudio.microsoft.com/visual-cpp-build-tools/):
   - Look for the installer under "Tools for Visual Studio 2022".
   - Install the "Desktop development with C++" workload.
2. Install [Python 3.10](https://www.python.org/downloads/release/python-3100/):
   - Ensure you use this specific version of Python.
3. Open "Developer Command Prompt for Visual Studio" (search in the start menu).
4. Install the required packages:
   ```bash
   pip install PySide6 opencv-python face_recognition numpy
   ```
5. Run the application:
   ```bash
   python main.py
   ```

#### Linux (Ubuntu 22.04)
1. Install build essentials:
   ```bash
   sudo apt-get update
   sudo apt-get install build-essential
   ```
2. Install Python3 and venv:
   ```bash
   sudo apt-get install python3-venv
   ```
3. Create a virtual environment and activate it:
   ```bash
   python3 -m venv env
   source env/bin/activate
   ```
4. Install the required packages:
   ```bash
   pip install PySide6 opencv-python face_recognition numpy
   ```
5. Run the application:
   ```bash
   python main.py
   ```

---

### Code Overview

#### `main.py`
Initializes the application and handles core processes including the setup of connections and the main loop.

#### `gui.py`
Manages the graphical user interface using PySide6, including the layout and style of various UI elements such as buttons, labels, and the attendance table.

#### `camera.py`
Handles camera operations such as connecting, capturing images, and displaying the camera feed within the application.

#### `data_manager.py`
Manages student data and face encodings. It handles tasks like adding, removing, and clearing student data, as well as loading and saving this data from/to a JSON file.

#### `face_recognition_handler.py`
Detects and recognizes faces using the `face_recognition` library. It compares captured face encodings with known encodings to identify students.

#### `attendance_manager.py`
Updates attendance records and table views, marking students as present or absent based on face recognition results.

#### `ui_manager.py`
Handles UI updates, including populating the attendance table with current data, updating attendance status, and exporting attendance data to a CSV file.

#### `recognizer.py`
Orchestrates face recognition processes, capturing images, and updating the attendance status of recognized students.
