import sys
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton, QMessageBox, QComboBox, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QPixmap
import mysql.connector as mc
from PyQt5.uic import loadUi
import datetime
import time

class mainPage(QMainWindow):
    def __init__(self):
        super(mainPage, self).__init__()
        # --- FROM THE IMPORT PYQT5.UIC IMPORT LOADUI---##
        loadUi("SARS.ui", self)
        self.setFixedSize(1145,713)
        # --- SET THE PROFILE PAGE AS A DEFAULT PAGE AFTER LOGGING IN --- #
        self.mainWidget.setCurrentWidget(self.StudentLoginPage)
        self.studentLoginButton.clicked.connect(self.attendance)
        self.adminLoginButton.clicked.connect(lambda: self.mainWidget.setCurrentWidget(self.AdminLoginPage))
        self.studentLogin.clicked.connect(lambda: self.mainWidget.setCurrentWidget(self.StudentLoginPage))
        self.mainLogin.clicked.connect(self.adminLogin)

    def attendance(self):
        studentNo = self.studNo.text()
        time = "time now"
        date = "date now"

        if studentNo == "":
            self.studentValid.setText("Please fill up the field")
            self.beenLogin.setText("")
            self.nameTime.setText("")
            self.studNo.clear()
        #error dito di ko makita

        else:
            mydb = mc.connect(
                host="localhost",
                user="root",
                password="",
                database="db_sars"
            )
            mycursor = mydb.cursor()
            query = "SELECT * FROM student WHERE '" + studentNo + "' LIKE student_no"
            mycursor.execute(query)
            result = mycursor.fetchone()

            if result is None:
                self.studentValid.setText("You are not a student here...")
                self.beenLogin.setText("")
                self.nameTime.setText("")
                self.studNo.clear()
            else:
                self.studentValid.clear()
                mydb = mc.connect(
                    host="localhost",
                    user="root",
                    password="",
                    database="db_sars"
                )

                mycursor = mydb.cursor()
                query = "SELECT * FROM student WHERE '" + studentNo + "' LIKE student_no"
                mycursor.execute(query)
                resultName = mycursor.fetchall()
                for row in resultName:
                    fname = row[2]
                    lname = row[4]
                    studNo = row [1]
                studentName = (fname+" "+lname)
                self.beenLogin.setText("You have been login:")
                self.nameTime.setText(studentName+" at {time now}")
                #should display time.now
                #also use setstylesheet, diff color for name and time
                self.studNo.clear()
                #clear after 5 secs
                #time.sleep(5)
                #-----
                #insert attendance in time table
                mydb = mc.connect(
                    host="localhost",
                    user="root",
                    password="",
                    database="db_sars"
                )

                mycursor = mydb.cursor()
                queryAttendance = "INSERT INTO time (time_id, student_no, student_name, time, date) VALUES (%s, %s, %s, %s, %s)"
                value = ('', studNo, studentName, time, date)
                mycursor.execute(queryAttendance, value)
                mydb.commit()

    def adminLogin(self):
        username = self.usernameln.text()
        password = self.passwordln.text()

        if username == "" or password == "":
            self.adminValid.setText("Please complete the required field")
            self.usernameln.clear()
            self.passwordln.clear()
        else:
            mydb = mc.connect(
                host="localhost",
                user="root",
                password="",
                database="db_sars"
            )
            mycursor = mydb.cursor()
            query = "SELECT * FROM admin WHERE '" + username + "' LIKE username AND '" + password + "' LIKE password"
            mycursor.execute(query)
            result = mycursor.fetchone()

            if result is None:
                self.adminValid.setText("Invalid username or password")
                self.usernameln.clear()
                self.passwordln.clear()
            else:
                self.usernameln.clear()
                self.passwordln.clear()
                self.loadMain()

    def loadMain(self):
        self.mainWidget.setCurrentWidget(self.mainPage)
        self.stackedWidget_2.setCurrentWidget(self.homePage)
        #set all buttons
        self.homeButton.clicked.connect(lambda: self.stackedWidget_2.setCurrentWidget(self.homePage))
        self.adminButton.clicked.connect(lambda: self.stackedWidget_2.setCurrentWidget(self.adminPage))
        self.studentButton.clicked.connect(lambda: self.stackedWidget_2.setCurrentWidget(self.studentPage))
        self.recordButton.clicked.connect(lambda: self.stackedWidget_2.setCurrentWidget(self.recordPage))
        self.logoutButton.clicked.connect(lambda: self.mainWidget.setCurrentWidget(self.AdminLoginPage))
        #add new buttons aaralin ko pa yung modal-window sa registration nung accounts







app=QApplication(sys.argv)
loginWindow=mainPage()
loginWindow.show()
app.exec_() #-- window execution --#
