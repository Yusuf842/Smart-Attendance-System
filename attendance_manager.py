from PySide6.QtWidgets import QTableWidgetItem
from PySide6.QtGui import QColor

class AttendanceManager:
    def __init__(self, data_manager, attendance_system):
        self.data_manager = data_manager
        self.attendance_system = attendance_system

    def mark_present(self, roll_number, name):
        for i in range(self.attendance_system.attendanceTable.rowCount()):
            if self.attendance_system.attendanceTable.item(i, 0).text() == roll_number:
                item = QTableWidgetItem("Present")
                item.setForeground(QColor(0, 128, 0))  # Green for present
                self.attendance_system.attendanceTable.setItem(i, 2, item)
                arrival_time = self.data_manager.get_students()[roll_number]['arrival_time']
                arrival_time_item = QTableWidgetItem(arrival_time if arrival_time else "")
                self.attendance_system.attendanceTable.setItem(i, 3, arrival_time_item)
                break
