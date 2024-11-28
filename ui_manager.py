from datetime import datetime
from PySide6.QtWidgets import QTableWidgetItem, QFileDialog
from PySide6.QtGui import QColor
import csv

class UIManager:
    def __init__(self, attendance_system, data_manager, attendance_manager):
        self.attendance_system = attendance_system
        self.data_manager = data_manager
        self.attendance_manager = attendance_manager

        self.attendance_system.saveAttendanceButton.clicked.connect(self.save_attendance)
        self.attendance_system.clearAttendanceButton.clicked.connect(self.clear_attendance)

    def append_status(self, message):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        current_text = self.attendance_system.statusDisplay.toPlainText()
        new_message = f"{current_text}\n[{timestamp}] {message}"
        self.attendance_system.statusDisplay.setPlainText(new_message)
        self.attendance_system.statusDisplay.verticalScrollBar().setValue(
            self.attendance_system.statusDisplay.verticalScrollBar().maximum()
        )

    def populate_table(self):
        self.attendance_system.attendanceTable.setRowCount(0)  
        for roll_number, details in self.data_manager.get_students().items():
            row_position = self.attendance_system.attendanceTable.rowCount()
            self.attendance_system.attendanceTable.insertRow(row_position)
            self.attendance_system.attendanceTable.setItem(row_position, 0, QTableWidgetItem(roll_number))
            self.attendance_system.attendanceTable.setItem(row_position, 1, QTableWidgetItem(details['name']))
            absent_item = QTableWidgetItem("Absent")
            absent_item.setForeground(QColor(255, 0, 0)) 
            self.attendance_system.attendanceTable.setItem(row_position, 2, absent_item)
        self.update_summary()

    def remove_student(self):
        current_row = self.attendance_system.attendanceTable.currentRow()
        if current_row >= 0:
            roll_number = self.attendance_system.attendanceTable.item(current_row, 0).text()
            if self.data_manager.remove_student(roll_number):
                self.attendance_system.attendanceTable.removeRow(current_row)
                self.update_summary()

    def clear_attendance(self):
        self.attendance_system.attendanceTable.setRowCount(0)
        self.data_manager.clear_data()
        self.append_status("Attendance cleared.")
        self.attendance_system.attendanceTable.viewport().update()
        self.update_summary()

    def save_attendance(self):
        path, _ = QFileDialog.getSaveFileName(self.attendance_system, "Save Attendance", "", "CSV Files (*.csv);;All Files (*)")
        if path:
            if not path.endswith('.csv'):
                path += '.csv'
            
            attendance_data = []
            for row in range(self.attendance_system.attendanceTable.rowCount()):
                roll_number = self.attendance_system.attendanceTable.item(row, 0).text()
                name = self.attendance_system.attendanceTable.item(row, 1).text()
                status = self.attendance_system.attendanceTable.item(row, 2).text()
                attendance_data.append([roll_number, name, status])

            with open(path, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Roll Number", "Name", "Status"])
                writer.writerows(attendance_data)
            self.append_status(f"Attendance saved to {path}")

    def update_attendance_table(self):
        for roll_number, details in self.data_manager.get_students().items():
            for i in range(self.attendance_system.attendanceTable.rowCount()):
                if self.attendance_system.attendanceTable.item(i, 0).text() == roll_number:
                    status = "Present" if roll_number in self.data_manager.known_face_names else "Absent"
                    item = QTableWidgetItem(status)
                    item.setForeground(QColor(0, 128, 0) if status == "Present" else QColor(255, 0, 0))  # Set text color based on status
                    self.attendance_system.attendanceTable.setItem(i, 2, item)
        self.attendance_system.attendanceTable.viewport().update() 
        self.update_summary()

    def update_summary(self):
        total_present = 0
        total_absent = 0
        for row in range(self.attendance_system.attendanceTable.rowCount()):
            status_item = self.attendance_system.attendanceTable.item(row, 2)
            if status_item.text() == "Present":
                total_present += 1
            else:
                total_absent += 1
        
        self.attendance_system.totalPresentLabel.setText(f"Total Present: {total_present}")
        self.attendance_system.totalAbsentLabel.setText(f"Total Absent: {total_absent}")
