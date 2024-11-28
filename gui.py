import sys
from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, 
                               QPushButton, QLabel, QTableWidget, 
                               QTableWidgetItem, QHeaderView, 
                               QPlainTextEdit, QGridLayout, QLineEdit, QHBoxLayout)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

class AttendanceSystem(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        mainLayout = QGridLayout()
        self.setLayout(mainLayout)

        self.attendanceTable = QTableWidget()
        self.attendanceTable.setColumnCount(3)
        self.attendanceTable.setHorizontalHeaderLabels(['Roll Number', 'Name', 'Absent/Present'])
        self.attendanceTable.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.attendanceTable.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.attendanceTable.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)

        self.attendanceTable.setStyleSheet(
            """
            QTableWidget {background-color: #FFFFFF; border: none; font: 15px 'Helvetica Neue'; color: #333333;}
            QHeaderView::section {background-color: #F0F0F0; border: none; font: bold 15px 'Helvetica Neue'; color: #333333;}
            QTableWidget::item {border: 1px solid #E0E0E0;}
            """
        )
        
        mainLayout.addWidget(self.attendanceTable, 0, 0, 3, 1)

        self.cameraLabel = QLabel("")
        self.cameraLabel.setAlignment(Qt.AlignCenter)
        self.cameraLabel.setStyleSheet("background-color: #F9F9F9; border: 1px solid #CCCCCC; min-height: 300px; min-width: 300px;")
        mainLayout.addWidget(self.cameraLabel, 0, 1, 1, 1)

        self.connectCameraButton = QPushButton("Connect/Disconnect Camera")
        self.addStudentButton = QPushButton("Add New Student")
        self.removeStudentButton = QPushButton("Remove Student")
        self.studentNameInput = QLineEdit()
        self.studentNameInput.setPlaceholderText("Enter Student Name")
        self.rollNumberInput = QLineEdit()
        self.rollNumberInput.setPlaceholderText("Enter Roll Number")
        self.saveAttendanceButton = QPushButton("Save Attendance")
        self.clearAttendanceButton = QPushButton("Clear Attendance")

        buttonStyle = """
            QPushButton {
                background-color: #3A3A3A; 
                color: white; 
                font: bold 15px 'Helvetica Neue'; 
                border: none; 
                padding: 10px; 
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #555555;
            }
            """
        self.connectCameraButton.setStyleSheet(buttonStyle)
        self.addStudentButton.setStyleSheet(buttonStyle)
        self.removeStudentButton.setStyleSheet(buttonStyle)
        self.saveAttendanceButton.setStyleSheet(buttonStyle)
        self.clearAttendanceButton.setStyleSheet(buttonStyle)
        
        inputStyle = """
            QLineEdit {
                background-color: #FFFFFF; 
                font: 15px 'Helvetica Neue'; 
                border: 1px solid #CCCCCC; 
                padding: 5px; 
                color: #333333;
                border-radius: 8px;
            }
            """
        self.studentNameInput.setStyleSheet(inputStyle)
        self.rollNumberInput.setStyleSheet(inputStyle)
        
        buttonLayout = QVBoxLayout()
        buttonLayout.addWidget(self.connectCameraButton)
        buttonLayout.addWidget(self.studentNameInput)
        buttonLayout.addWidget(self.rollNumberInput)
        buttonLayout.addWidget(self.addStudentButton)
        buttonLayout.addWidget(self.removeStudentButton)
        buttonLayout.addWidget(self.saveAttendanceButton)
        buttonLayout.addWidget(self.clearAttendanceButton)
        buttonContainer = QWidget()
        buttonContainer.setLayout(buttonLayout)
        mainLayout.addWidget(buttonContainer, 1, 1, 1, 1)

        self.statusDisplay = QPlainTextEdit()
        self.statusDisplay.setReadOnly(True)
        self.statusDisplay.setPlainText("Status/Message Area")
        self.statusDisplay.setStyleSheet(
            """
            background-color: #F9F9F9; 
            font: 15px 'Helvetica Neue'; 
            border: 1px solid #CCCCCC; 
            padding: 10px; 
            color: #333333; 
            border-radius: 8px;
            """
        )
        mainLayout.addWidget(self.statusDisplay, 2, 0, 1, 2)

        summaryLayout = QHBoxLayout()
        self.totalPresentLabel = QLabel("Total Present: 0")
        self.totalAbsentLabel = QLabel("Total Absent: 0")
        summaryStyle = "font: bold 15px 'Helvetica Neue'; color: #333333;"
        self.totalPresentLabel.setStyleSheet(summaryStyle)
        self.totalAbsentLabel.setStyleSheet(summaryStyle)
        summaryLayout.addWidget(self.totalPresentLabel)
        summaryLayout.addWidget(self.totalAbsentLabel)
        summaryContainer = QWidget()
        summaryContainer.setLayout(summaryLayout)
        mainLayout.addWidget(summaryContainer, 3, 0, 1, 2, alignment=Qt.AlignRight)

        mainLayout.setColumnStretch(0, 2)
        mainLayout.setColumnStretch(1, 1)
        mainLayout.setRowStretch(0, 5)
        mainLayout.setRowStretch(1, 3)
        mainLayout.setRowStretch(2, 1)
        mainLayout.setRowStretch(3, 0)

        self.setWindowTitle('Smart Attendance System')
        self.setGeometry(100, 100, 1400, 800)
        self.setStyleSheet("background-color: #F0F0F0;")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = AttendanceSystem()
    ex.show()
    sys.exit(app.exec())
