from PySide6.QtWidgets import QTableWidgetItem
from PySide6.QtGui import QColor

class AttendanceManager:
    def __init__(self, data_manager, attendance_system):
        self.data_manager = data_manager
        self.attendance_system = attendance_system

    def mark_present(self, roll_number, name):
        print(f"Marking {name} (Roll Number: {roll_number}) as present")
        for i in range(self.attendance_system.attendanceTable.rowCount()):
            if self.attendance_system.attendanceTable.item(i, 0).text() == roll_number:
                item = QTableWidgetItem("Present")
                item.setForeground(QColor(0, 128, 0))  
                self.attendance_system.attendanceTable.setItem(i, 2, item)
                print(f"Marked {name} as present in the table")
                self.attendance_system.attendanceTable.viewport().update()  
                break
