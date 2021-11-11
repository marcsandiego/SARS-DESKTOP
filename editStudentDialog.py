# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'editStudentDialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
import mysql.connector as mc


class Ui_editStudentDialog(object):
    def setupUi(self, editStudentDialog, mainPage, student):
        self.editStudentDialog = editStudentDialog
        self.editStudentDialog.setObjectName("editStudentDialog")
        self.editStudentDialog.setEnabled(True)
        self.editStudentDialog.resize(485, 539)
        self.editStudentDialog.setModal(True)
        self.mainPage = mainPage
        self.student = student
        self.newStudentBtns = QtWidgets.QDialogButtonBox(editStudentDialog)
        self.newStudentBtns.setEnabled(True)
        self.newStudentBtns.setGeometry(QtCore.QRect(230, 470, 221, 41))
        self.newStudentBtns.setOrientation(QtCore.Qt.Horizontal)
        self.newStudentBtns.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.newStudentBtns.setObjectName("newStudentBtns")
        self.studentIdFld = QtWidgets.QLineEdit(editStudentDialog)
        self.studentIdFld.setGeometry(QtCore.QRect(30, 50, 421, 31))
        self.studentIdFld.setObjectName("studentIdFld")
        self.studentIdLbl = QtWidgets.QLabel(editStudentDialog)
        self.studentIdLbl.setGeometry(QtCore.QRect(30, 20, 421, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.studentIdLbl.setFont(font)
        self.studentIdLbl.setObjectName("studentIdLbl")
        self.firstNameFld = QtWidgets.QLineEdit(editStudentDialog)
        self.firstNameFld.setGeometry(QtCore.QRect(30, 120, 421, 31))
        self.firstNameFld.setObjectName("firstNameFld")
        self.firstNameLbl = QtWidgets.QLabel(editStudentDialog)
        self.firstNameLbl.setGeometry(QtCore.QRect(30, 90, 421, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.firstNameLbl.setFont(font)
        self.firstNameLbl.setObjectName("firstNameLbl")
        self.middleNameLbl = QtWidgets.QLabel(editStudentDialog)
        self.middleNameLbl.setGeometry(QtCore.QRect(30, 160, 421, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.middleNameLbl.setFont(font)
        self.middleNameLbl.setObjectName("middleNameLbl")
        self.middleNameFld = QtWidgets.QLineEdit(editStudentDialog)
        self.middleNameFld.setGeometry(QtCore.QRect(30, 190, 421, 31))
        self.middleNameFld.setObjectName("middleNameFld")
        self.lastNameLabel = QtWidgets.QLabel(editStudentDialog)
        self.lastNameLabel.setGeometry(QtCore.QRect(30, 230, 421, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.lastNameLabel.setFont(font)
        self.lastNameLabel.setObjectName("lastNameLabel")
        self.lastNameFld = QtWidgets.QLineEdit(editStudentDialog)
        self.lastNameFld.setGeometry(QtCore.QRect(30, 260, 421, 31))
        self.lastNameFld.setObjectName("lastNameFld")
        self.courseLbl = QtWidgets.QLabel(editStudentDialog)
        self.courseLbl.setGeometry(QtCore.QRect(30, 300, 421, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.courseLbl.setFont(font)
        self.courseLbl.setObjectName("courseLbl")
        self.courseFld = QtWidgets.QLineEdit(editStudentDialog)
        self.courseFld.setGeometry(QtCore.QRect(30, 330, 421, 31))
        self.courseFld.setObjectName("courseFld")
        self.yearLbl = QtWidgets.QLabel(editStudentDialog)
        self.yearLbl.setGeometry(QtCore.QRect(30, 370, 421, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.yearLbl.setFont(font)
        self.yearLbl.setObjectName("yearLbl")
        self.yrFld = QtWidgets.QLineEdit(editStudentDialog)
        self.yrFld.setGeometry(QtCore.QRect(30, 400, 421, 31))
        self.yrFld.setObjectName("yrFld")

        self.studentIdFld.setText(str(self.student.student_no))
        self.firstNameFld.setText(self.student.fName)
        self.middleNameFld.setText(self.student.mName)
        self.lastNameFld.setText(self.student.lName)
        self.courseFld.setText(self.student.course)
        self.yrFld.setText(self.student.section)

        self.retranslateUi(editStudentDialog)
        self.newStudentBtns.accepted.connect(self.okButton)
        self.newStudentBtns.rejected.connect(editStudentDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(editStudentDialog)

    def retranslateUi(self, editStudentDialog):
        _translate = QtCore.QCoreApplication.translate
        editStudentDialog.setWindowTitle(_translate("editStudentDialog", "Dialog"))
        self.studentIdLbl.setText(_translate("editStudentDialog", "Student ID:"))
        self.firstNameLbl.setText(_translate("editStudentDialog", "First Name:"))
        self.middleNameLbl.setText(_translate("editStudentDialog", "Middle Name:"))
        self.lastNameLabel.setText(_translate("editStudentDialog", "Last Name:"))
        self.courseLbl.setText(_translate("editStudentDialog", "Course:"))
        self.yearLbl.setText(_translate("editStudentDialog", "Year and Section:"))

    def okButton(self):
        studentNo = self.studentIdFld.text()
        fName = self.firstNameFld.text()
        mName = self.middleNameFld.text()
        lName = self.lastNameFld.text()
        course = self.courseFld.text()
        yrs = self.yrFld.text()

        if studentNo == "" or fName == "" or lName == "" or course == "" or yrs == "":
            print("ERROR")
        else:
            mydb = mc.connect(
                host="localhost",
                user="root",
                password="",
                database="db_sars"
            )
            mycursor = mydb.cursor()
            query = f"UPDATE student SET student_no = '{studentNo}', firstname = '{fName}', middlename = '{mName}', lastname = '{lName}', course = '{course}', section = '{yrs}' WHERE student_id LIKE {self.student.student_id}"
            mycursor.execute(query)
            mydb.commit()
            print("Aba ayos ah")
            self.mainPage.loadStudentTable()
            self.editStudentDialog.close()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    editStudentDialog = QtWidgets.QDialog()
    ui = Ui_editStudentDialog()
    ui.setupUi(editStudentDialog)
    editStudentDialog.show()
    sys.exit(app.exec_())