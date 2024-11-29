from datetime import datetime
from PySide6.QtWidgets import QTableWidgetItem, QFileDialog
from PySide6.QtGui import QColor
from PySide6.QtCore import Qt
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
        student_data = self.data_manager.get_students()
        self.attendance_system.attendanceTable.setRowCount(0)  # Clear the table
        for roll_number, details in student_data.items():
            row_position = self.attendance_system.attendanceTable.rowCount()
            self.attendance_system.attendanceTable.insertRow(row_position)
            self.attendance_system.attendanceTable.setItem(row_position, 0, QTableWidgetItem(roll_number))
            self.attendance_system.attendanceTable.setItem(row_position, 1, QTableWidgetItem(details['name']))
            status = "Present" if details['arrival_time'] else "Absent"
            status_item = QTableWidgetItem(status)
            status_item.setForeground(QColor(0, 128, 0) if status == "Present" else QColor(255, 0, 0))
            self.attendance_system.attendanceTable.setItem(row_position, 2, status_item)
            time_item = QTableWidgetItem(details['arrival_time'] if details['arrival_time'] else "")
            self.attendance_system.attendanceTable.setItem(row_position, 3, time_item)
        self.sort_table_by_roll_number()
        self.update_summary()


    def update_attendance_table(self):
        student_data = self.data_manager.get_students()
        for roll_number, details in student_data.items():
            row_position = self.find_row_by_roll_number(roll_number)
            if row_position == -1:
                continue  

            current_status_item = self.attendance_system.attendanceTable.item(row_position, 2)
            current_status = current_status_item.text() if current_status_item else "Absent"

            new_status = "Absent"
            if roll_number in self.data_manager.known_face_names:
                new_status = "Present"

            if current_status != "Present" and new_status == "Present":
                item = QTableWidgetItem(new_status)
                item.setForeground(QColor(0, 128, 0))  
                self.attendance_system.attendanceTable.setItem(row_position, 2, item)
                arrival_time_item = QTableWidgetItem(details['arrival_time'] if details['arrival_time'] else "")
                self.attendance_system.attendanceTable.setItem(row_position, 3, arrival_time_item)
        
        self.attendance_system.attendanceTable.viewport().update()
        self.sort_table_by_roll_number()

    def update_specific_row(self, roll_number):
        row_position = self.find_row_by_roll_number(roll_number)
        if row_position != -1:
            details = self.data_manager.get_students()[roll_number]
            status_item = QTableWidgetItem("Present")
            status_item.setForeground(QColor(0, 128, 0))
            self.attendance_system.attendanceTable.setItem(row_position, 2, status_item)
            arrival_time_item = QTableWidgetItem(details['arrival_time'] if details['arrival_time'] else "")
            self.attendance_system.attendanceTable.setItem(row_position, 3, arrival_time_item)
            self.attendance_system.attendanceTable.viewport().update()
        self.sort_table_by_roll_number()

    def find_row_by_roll_number(self, roll_number):
        for row in range(self.attendance_system.attendanceTable.rowCount()):
            if self.attendance_system.attendanceTable.item(row, 0).text() == roll_number:
                return row
        return -1

    def sort_table_by_roll_number(self):
        self.attendance_system.attendanceTable.sortItems(0, Qt.SortOrder.AscendingOrder)

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
                time_of_arrival = self.attendance_system.attendanceTable.item(row, 3).text()
                attendance_data.append([roll_number, name, status, time_of_arrival])

            with open(path, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Roll Number", "Name", "Status", "Time of Arrival"])
                writer.writerows(attendance_data)
            self.append_status(f"Attendance saved to {path}")

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
