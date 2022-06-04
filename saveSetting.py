import os
import sys
import types

from PyQt5 import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import mysql.connector
import movableLabel
from PyQt5.QtCore import *
from PyQt5 import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from ProfileSetting import *
import mysql.connector


db = mysql.connector.connect(user='ChatApp',
                             password='Chatapp_project123',
                             host='192.168.1.70',
                             database='chat',
                             auth_plugin='mysql_native_password')
myCursor = db.cursor()

class saveSetting(Ui_profileSetting):
    def __init__(self,id):
        self.Profile = {'photoBinary': ''}
        self.akm = QWidget()
        super().setupUi(self.akm)
        self.id = id


        # empty window
        # .setupUi(self.profileSetting)  # to initialize widgets
        self.editAbout()
        self.editAboutButton.clicked.connect(lambda: self.clickeedit())
        self.saveSetting_2.clicked.connect(lambda: self.savesetting())
        self.editPhotoButton.clicked.connect(lambda: self.changphoto())
        self.settingoutput()
        self.showphoto()



    def editAbout(self):
        print("1")
        myCursor.execute(f"select About_description from user_profile_description where user_ID = {self.id};")

        Yourabout = myCursor.fetchall()[0][0]
        print(Yourabout)
        self.about.setText(Yourabout)

    def clickeedit(self):
        abo = self.about.text()
        print(abo)
        # myCursor.execute(f"""UPDATE   SET = {abo} WHERE t. = {self.id};""")
        try:
            sql_update_query = """Update user_profile_description set  About_description = %s where user_ID = %s"""
            input = (abo, self.id)
            myCursor.execute(sql_update_query, input)
            db.commit()

        except mysql.connector.Error as error:
            print("Failed to update columns of table: {}".format(error))

    def settingoutput(self):
        myCursor.execute(f"select visibilty from user_profile_description where user_ID = {self.id};")
        visibilty = myCursor.fetchall()[0][0]
        print(type(visibilty))
        print(visibilty)
        if visibilty:
            self.myContact.setChecked(1)
        else:
            self. onlyMe.setChecked(1)

        myCursor.execute(f"select first_name , last_name from chat_user where user_ID={self.id} ;")

        selectContact = myCursor.fetchall()
        firstName = selectContact[0][0]
        lastName = selectContact[0][1]
        self.firstName.setText(firstName)
        self.lastName.setText(lastName)
        myCursor.execute(f"select user_password from chat_user where user_ID={self.id} ;")
        password = myCursor.fetchall()[0][0]
        self.password.setText(password)

    def showphoto (self):
        myCursor.execute(f"select personal_photo from user_profile_description where user_ID = {self.id}")
        img = myCursor.fetchall()[0][0]
        storepath = f'Icons/{self.id}.jpg'
        with open(storepath, 'wb') as file:
            file.write(img)
            file.close()
        # print(storepath)
        self.photo.setStyleSheet(f"border-image: url({storepath});\n"
                                 "border-radius : 100px;\n"
                                 "")

    def savesetting(self):
        self.clickeedit()

        if self.myContact.isChecked():
            print("mycontact")

            try:
                myCursor.execute(f"""Update user_profile_description set visibilty = {1} where user_ID = {self.id}""")
                db.commit()

            except mysql.connector.Error as error:
                print("Failed to update columns of table: {}".format(error))

        if self.onlyMe.isChecked():
            print("onlyme")
            try:
                myCursor.execute(f"""Update user_profile_description set visibilty = {0} where user_ID = {self.id}""")
                db.commit()

            except mysql.connector.Error as error:
                print("Failed to update columns of table: {}".format(error))

        firstnamee = self.firstName.text()
        lastname = self.lastName.text()
        password = self.password.text()
        try:
            sql_update_query = """Update chat_user set  first_name = %s where user_ID = %s"""
            input = (firstnamee, self.id)
            myCursor.execute(sql_update_query, input)
            db.commit()
            sql_update_query = """Update chat_user set  last_name = %s where user_ID = %s"""
            input = (lastname, self.id)
            myCursor.execute(sql_update_query, input)
            db.commit()
            sql_update_query = """Update chat_user set  user_password = %s where user_ID = %s"""
            input = (password, self.id)
            myCursor.execute(sql_update_query, input)
            db.commit()
        except mysql.connector.Error as error:
            print("Failed to update columns of table: {}".format(error))

    def changphoto(self):

        Photo = QFileDialog.getOpenFileName(caption='Choose Profile Photo', filter='*.jpg;;*.png')
        photoPath = Photo[0]
        photoExtenstion = Photo[1]

        if photoPath:

            with open(photoPath, 'rb') as file:
                photoBinary = file.read()
                self.Profile['photoBinary'] = photoBinary

        try:
            sql_photo = """update user_profile_description set personal_photo = %s where user_ID = %s """
            photo = self.Profile['photoBinary']
            input = (photo, self.id)
            myCursor.execute(sql_photo, input)
            db.commit()
            self.showphoto()
        except mysql.connector.Error as error:
            print("Failed to update columns of table: {}".format(error))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    # profileSetting = QtWidgets.QWidget()
    ui = saveSetting()
    # ui.setupUi(profileSetting)
    ui.akm.show()
    sys.exit(app.exec_())

