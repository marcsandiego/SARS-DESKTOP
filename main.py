import sys
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton, QMessageBox, QComboBox, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QPixmap
import mysql.connector as mc
from PyQt5.uic import loadUi
import datetime
import time
from newAdminDialog import Ui_newAdminDialog
from editAdminDialog import Ui_editAdminDialog
from newStudentDialog import Ui_newStudentDialog
from editStudentDialog import Ui_editStudentDialog

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
        self.addNewAdminBtn.clicked.connect(self.addAdmin)
        self.addNewStudentBtn.clicked.connect(self.addStudent)
        self.adminSearchFld.textChanged.connect(self.searchAdmin)
        self.studentSearchFld.textChanged.connect(self.searchStudent)
        self.recordSearchFld.textChanged.connect(self.searchRecord)

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
                self.nameTime.setText(f"{studentName} at {datetime.datetime.now()}")
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
        self.loadAdminTable()
        self.loadStudentTable()
        self.loadRecordTable()
        #add new buttons aaralin ko pa yung modal-window sa registration nung accounts

    def loadAdminTable(self, search=""):
        searchString = ""
        if search != "":
            searchString = f"WHERE admin_id LIKE '%{search}%' OR username LIKE '%{search}%' OR firstname LIKE '%{search}%' OR middlename LIKE '%{search}%' OR lastname LIKE '%{search}%'"
        mydb = mc.connect(
                host="localhost",
                user="root",
                password="",
                database="db_sars"
            )
        mycursor = mydb.cursor()
        query = f"SELECT * FROM admin {searchString}"
        mycursor.execute(query)
        result = mycursor.fetchall()

        rowNum = 0

        self.adminTable.setRowCount(len(result))
        # print(result)

        for row in result:
            if row is not None:
                print("Meron")
            tempAdmin = admin(row[0], row[1], row[2], row[3], row[4], row[5])
            self.adminTable.setItem(rowNum, 0, QtWidgets.QTableWidgetItem(str(tempAdmin.username)))
            self.adminTable.setItem(rowNum, 1, QtWidgets.QTableWidgetItem(str(tempAdmin.password)))
            self.adminTable.setItem(rowNum, 2, QtWidgets.QTableWidgetItem(str(tempAdmin.fName)))
            self.adminTable.setItem(rowNum, 3, QtWidgets.QTableWidgetItem(str(tempAdmin.mName)))
            self.adminTable.setItem(rowNum, 4, QtWidgets.QTableWidgetItem(str(tempAdmin.lName)))
            self.adminTable.setCellWidget(rowNum,5 , AdminButtonsWidget(window=None, admin=tempAdmin, mainWindow=self)) #LAST ROW CONTAINS CUSTOM LAYOUT WITH 2 WIDGETS
            rowNum += 1

        print("Loaded")

    def loadStudentTable(self, search=""):
        searchString = ""
        if search != "":
            searchString = f"WHERE student_no LIKE '%{search}%'  OR firstname LIKE '%{search}%' OR middlename LIKE '%{search}%' OR lastname LIKE '%{search}%' OR course LIKE '%{search}%' OR section LIKE '%{search}%'"


        mydb = mc.connect(
                host="localhost",
                user="root",
                password="",
                database="db_sars"
            )
        mycursor = mydb.cursor()
        query = f"SELECT * FROM student {searchString}"
        mycursor.execute(query)
        result = mycursor.fetchall()

        rowNum = 0

        self.studentTable.setRowCount(len(result))
        # print(result)

        for row in result:
            if row is not None:
                print("Meron")
            tempStudent = student(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
            self.studentTable.setItem(rowNum, 0, QtWidgets.QTableWidgetItem(str(tempStudent.student_no)))
            self.studentTable.setItem(rowNum, 1, QtWidgets.QTableWidgetItem(str(tempStudent.fName)))
            self.studentTable.setItem(rowNum, 2, QtWidgets.QTableWidgetItem(str(tempStudent.mName)))
            self.studentTable.setItem(rowNum, 3, QtWidgets.QTableWidgetItem(str(tempStudent.lName)))
            self.studentTable.setItem(rowNum, 4, QtWidgets.QTableWidgetItem(str(tempStudent.course)))
            self.studentTable.setItem(rowNum, 5, QtWidgets.QTableWidgetItem(str(tempStudent.section)))
            self.studentTable.setCellWidget(rowNum,6 , StudentButtonsWidget(window=None, student=tempStudent, mainWindow=self)) #LAST ROW CONTAINS CUSTOM LAYOUT WITH 2 WIDGETS
            rowNum += 1

        print("Loaded")

    def loadRecordTable(self, search=""):
        searchString = ""
        if search != "":
            searchString = f"WHERE student_no LIKE '%{search}%' OR student_name LIKE '%{search}%' OR time LIKE '%{search}%' OR date LIKE '%{search}%'"

        mydb = mc.connect(
                host="localhost",
                user="root",
                password="",
                database="db_sars"
            )
        mycursor = mydb.cursor()
        query = f"SELECT * FROM time {searchString}"
        mycursor.execute(query)
        result = mycursor.fetchall()

        rowNum = 0

        self.recordTable.setRowCount(len(result))
        # print(result)

        for row in result:
            if row is not None:
                print("Meron")
            tempRecord = record(row[0], row[1], row[2], row[3], row[4])
            self.recordTable.setItem(rowNum, 0, QtWidgets.QTableWidgetItem(str(tempRecord.student_id)))
            self.recordTable.setItem(rowNum, 1, QtWidgets.QTableWidgetItem(str(tempRecord.studentName)))
            self.recordTable.setItem(rowNum, 2, QtWidgets.QTableWidgetItem(str(tempRecord.time)))
            self.recordTable.setItem(rowNum, 3, QtWidgets.QTableWidgetItem(str(tempRecord.date)))
            self.recordTable.setCellWidget(rowNum,4 , RecordButtonsWidget(window=None, record=tempRecord, mainWindow=self)) #LAST ROW CONTAINS CUSTOM LAYOUT WITH 2 WIDGETS
            rowNum += 1

        print("Loaded")

    def addAdmin(self):
        self.window = QtWidgets.QDialog()
        self.ui = Ui_newAdminDialog()
        self.ui.setupUi(self.window, self)
        self.window.show()
        self.loadAdminTable()

    def addStudent(self):
        self.window = QtWidgets.QDialog()
        self.ui = Ui_newStudentDialog()
        self.ui.setupUi(self.window, self)
        self.window.show()

    def searchAdmin(self):
        self.loadAdminTable(self.adminSearchFld.text())

    def searchStudent(self):
        self.loadStudentTable(self.studentSearchFld.text())

    def searchRecord(self):
        self.loadRecordTable(self.recordSearchFld.text())

#CUSTOM LAYOUT WHICH CONTAINS 2 WIDGETS FOR EDIT AND DELETE
class AdminButtonsWidget(QWidget):

    def __init__(self, window=None, admin=None, mainWindow=mainPage):
        super(AdminButtonsWidget,self).__init__(window)
        self.window = window
        self.mainWindow = mainWindow
        # add your buttons
        self.layout = QHBoxLayout()

        # adjust spacings to your needs
        self.layout.setContentsMargins(0,0,0,0)
        self.layout.setSpacing(0)

        self.editBtn = QPushButton('Edit')
        self.deleteBtn = QPushButton('Delete')
        # add your buttons
        self.layout.addWidget(self.editBtn)
        self.layout.addWidget(self.deleteBtn)
        self.setLayout(self.layout)
        self.editBtn.clicked.connect(self.editButton)
        self.deleteBtn.clicked.connect(self.deleteButton)
        self.admin = admin

    def editButton(self):
        self.window = QtWidgets.QDialog()
        self.ui = Ui_editAdminDialog()
        self.ui.setupUi(self.window, self.mainWindow, self.admin)
        self.window.show()
    
    def deleteButton(self):
        qm = QMessageBox
        ret = qm.question(self,'', "Do you want to delete this row?", qm.Yes | qm.No)
        if ret == qm.Yes:
            print("Deleted")
            mydb = mc.connect(
                host="localhost",
                user="root",
                password="",
                database="db_sars"
            )
            mycursor = mydb.cursor()
            query = f"DELETE FROM admin WHERE admin_id = {self.admin.userId}"
            mycursor.execute(query)
            mydb.commit()
            self.mainWindow.loadAdminTable()

class StudentButtonsWidget(QWidget):

    def __init__(self, window=None, student=None, mainWindow=mainPage):
        super(StudentButtonsWidget,self).__init__(window)
        self.window = window
        self.mainWindow = mainWindow
        # add your buttons
        self.layout = QHBoxLayout()

        # adjust spacings to your needs
        self.layout.setContentsMargins(0,0,0,0)
        self.layout.setSpacing(0)

        self.editBtn = QPushButton('Edit')
        self.deleteBtn = QPushButton('Delete')
        # add your buttons
        self.layout.addWidget(self.editBtn)
        self.layout.addWidget(self.deleteBtn)
        self.setLayout(self.layout)
        self.editBtn.clicked.connect(self.editButton)
        self.deleteBtn.clicked.connect(self.deleteButton)
        self.student = student

    def editButton(self):
        self.window = QtWidgets.QDialog()
        self.ui = Ui_editStudentDialog()
        self.ui.setupUi(self.window, self.mainWindow, self.student)
        self.window.show()
    
    def deleteButton(self):
        qm = QMessageBox
        ret = qm.question(self,'', "Do you want to delete this row?", qm.Yes | qm.No)
        if ret == qm.Yes:
            print("Deleted")
            mydb = mc.connect(
                host="localhost",
                user="root",
                password="",
                database="db_sars"
            )
            mycursor = mydb.cursor()
            query = f"DELETE FROM student WHERE student_id = {self.student.student_id}"
            mycursor.execute(query)
            mydb.commit()
            self.mainWindow.loadStudentTable()

class RecordButtonsWidget(QWidget):

    def __init__(self, window=None, record=None, mainWindow=mainPage):
        super(RecordButtonsWidget,self).__init__(window)
        self.window = window
        self.mainWindow = mainWindow
        # add your buttons
        self.layout = QHBoxLayout()

        # adjust spacings to your needs
        self.layout.setContentsMargins(0,0,0,0)
        self.layout.setSpacing(0)

        # self.editBtn = QPushButton('Edit')
        self.deleteBtn = QPushButton('Delete')
        # add your buttons
        # self.layout.addWidget(self.editBtn)
        self.layout.addWidget(self.deleteBtn)
        self.setLayout(self.layout)
        # self.editBtn.clicked.connect(self.editButton)
        self.deleteBtn.clicked.connect(self.deleteButton)
        self.record = record

    # def editButton(self):
    #     self.window = QtWidgets.QDialog()
    #     self.ui = Ui_editStudentDialog()
    #     self.ui.setupUi(self.window, self.mainWindow, self.student)
    #     self.window.show()
    
    def deleteButton(self):
        qm = QMessageBox
        ret = qm.question(self,'', "Do you want to delete this row?", qm.Yes | qm.No)
        if ret == qm.Yes:
            print("Deleted")
            mydb = mc.connect(
                host="localhost",
                user="root",
                password="",
                database="db_sars"
            )
            mycursor = mydb.cursor()
            query = f"DELETE FROM time WHERE time_id = {self.record.record_id}"
            mycursor.execute(query)
            mydb.commit()
            self.mainWindow.loadRecordTable()

class admin:
    def __init__(self, userId="", username="", password="", fName="", mName="", lName=""):
        self.userId = userId
        self.username = username
        self.password = password
        self.fName = fName
        self.mName = mName
        self.lName = lName

class student:
    def __init__(self, student_id, student_no, fName, mName, lName, course, section):
        self.student_id = student_id
        self.student_no = student_no
        self.fName = fName
        self.mName = mName
        self.lName = lName
        self.course = course
        self.section = section

class record:
    def __init__(self,record_id, student_id, studentName, time, date):
        self.record_id = record_id
        self.student_id = student_id
        self.studentName = studentName
        self.time = time
        self.date = date

app=QApplication(sys.argv)
loginWindow=mainPage()
loginWindow.show()
app.exec_() #-- window execution --#


        
