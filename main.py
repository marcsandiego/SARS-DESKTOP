import sys
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton, QMessageBox, QComboBox, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QPixmap
import mysql.connector as mc
from PyQt5.uic import loadUi
import datetime

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
        self.mainLogin.clicked.connect(self.adminLogin)

    def attendance(self):
        now = datetime.now()
        studentId = self.studID.text()

        if studentId == "":
            self.studentValid.setText("Please fill up the field")
        #error dito di ko makita
        '''
        else:
            mydb = mc.connect(
                host="localhost",
                user="root",
                password="",
                database="db_sars"
            )
            mycursor = mydb.cursor()
            query = "SELECT * FROM student WHERE '" + studentId + "' LIKE student_id"
            mycursor.execute(query)
            result = mycursor.fetchone()

            if result is None:
                self.studentValid.setText("You are not a student here...")
        
            else:
                mydb = mc.connect(
                    host="localhost",
                    user="root",
                    password="",
                    database="db_sars"
                )

                mycursor = mydb.cursor()
                query = "SELECT firstname FROM student WHERE '" + studentId + "' LIKE student_id"
                mycursor.execute(query)
                resultName = mycursor.fetchone()
                #nameTime = resultName+" at "+now.strftime("%H:%M:%S")
                self.beenLogin.setText("You have been login")
                self.nameTime.setText(resultName)
                '''
    def adminLogin(self):
        username = self.usernameln.text()
        password = self.passwordln.text()

        if username == "" or password == "":
            self.adminValid.setText("Please complete the required field")
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
            else:
                self.loadMain()

    def loadMain(self):
        self.mainWidget.setCurrentWidget(self.mainPage)
        self.stackedWidget_2.setCurrentWidget(self.homePage)
        #set all buttons
        self.homeButton.clicked.connect(lambda: self.stackedWidget_2.setCurrentWidget(self.homePage))
        self.recordButton.clicked.connect(lambda: self.stackedWidget_2.setCurrentWidget(self.recordPage))
        self.logoutButton.clicked.connect(self.logout)
        #add new buttons aaralin ko pa yung modal-window sa registration nung accounts

        #comboBox
        accountLevel = self.comboBox.currentText()
        print(accountLevel)
        #kailagan maging dynamic,
        # pag pinili si admin: stackedWidget_2 = accountPage and stackedWidget = adminAccounts
        #pag student: stackedWidget_2 = accountPage and stackedWidget = studentAccounts


    def logout(self):
        sys.exit()








app=QApplication(sys.argv)
loginWindow=mainPage()
loginWindow.show()
app.exec_() #-- window execution --#
