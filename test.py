import os
import sys
import threading
import time

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from ContactWindow import *
from Contact import *
import mysql.connector

db = mysql.connector.connect(user='ChatApp',
                             password='Chatapp_project123',
                             host='192.168.1.70',
                             database='chat',
                             auth_plugin='mysql_native_password')
myCursor = db.cursor()


class myContact(Ui_ContactWindow ):
    lastRoom = 0
    dead = False

    def __init__(self,id):
        self.id = id
        self.win = QWidget()
        self.listwid = ()
        super().setupUi(self.win)
        # self.createRoomButton.clicked.connect(lambda : self.CreateRoom())
        # self.addContact.clicked.connect(lambda : self.newcontact())
        # self.searchButton.clicked.connect(lambda : self.Search())
        # self.exitContact.clicked.connect(lambda : self.BackToChat())

        # self.constantContact(self.id )


    def Search(self):
        if (self.verticalLayout_4.count() > 0):
            for i in reversed(range(self.verticalLayout_4.count() - 1)):
                self.verticalLayout_4.itemAt(0).widget().setParent(None)
            self.verticalLayout_4.removeItem(self.spacerItem)
        # searching = self.searchLine.text()
        # self.constantContact(self.id, searching)


    # def usercontact(self, userIdNumber):
    #     myCursor.execute(f"select contact from contacts where user_ID = {userIdNumber} ;")
    #     select = myCursor.fetchall()
    #     print('select : ',select)
    #     return select

    # def newcontact(self):
    #     lst = []
    #     checksys = False
    #     checkcontact = False
    #     myContact.num = self.newContact.text()
    #
    #     print('type of num : ',type(myContact.num))
    #     print('num : ', myContact.num)
    #     list = myContact.contacts
    #     print(list)
    #     self.newContact.clear()
    #     # contact = Contact()
    #     contactwindow = self.textError
    #     for i in myContact.num:
    #         lst.append(i)
    #
    #     if len(lst) <= 11:
    #         lenslist = len(list)
    #         for n in range(0, lenslist):
    #             chekk = list[n]
    #
    #             if myContact.num == chekk[0]:
    #                 checkcontact = True
    #
    #         if checkcontact:
    #             print("The number is already there")
    #             contactwindow.setText('The number is already there')
    #             contactwindow.setStyleSheet('color:#00a884;')
    #
    #
    #         else:
    #             # myCursor.execute(f"select mobile_number from chat_user")
    #             # checksystem = myCursor.fetchall()
    #             print(myContact.checksystem)
    #             h = len(myContact.checksystem)
    #
    #             for l in range(0, h):
    #                 # print(num)
    #                 # print(l)
    #                 che = myContact.checksystem[l]
    #                 # print(che[0])
    #                 if myContact.num == che[0]:
    #                     checksys = True
    #                 # else:
    #                 #     checksys = False
    #
    #             if checksys:
    #                 # myCursor.execute(f"select user_ID from chat_user where mobile_number = '{num}'")
    #                 # idContact = myCursor.fetchall()[0][0]
    #                 print(myContact.idContact)
    #                 if myContact.idContact == self.id:
    #                     print("You use this number!")
    #                     contactwindow.setText('You use this number!')
    #                     contactwindow.setStyleSheet('color:#00a884;')
    #
    #                 else:
    #                     # myCursor.execute(f"select first_name , last_name from chat_user where user_ID={idContact} ;")
    #                     # selectContact = myCursor.fetchall()
    #                     firstName = myContact.selectContact[0][0]
    #                     lastName = myContact.selectContact[0][1]
    #                     fullName = firstName + ' ' + lastName
    #                     print(fullName)
    #
    #                     # myCursor.execute(f"select About_description from user_profile_description where user_ID = {idContact};")
    #                     # Myabout = myCursor.fetchall()[0][0]
    #
    #                     if (self.verticalLayout_4.count() > 0):
    #                         self.verticalLayout_4.removeItem(self.spacerItem)
    #
    #
    #                     # myCursor.execute(f"select personal_photo from user_profile_description where user_ID = {myContact.idContact};")
    #                     # img = myCursor.fetchall()[0][0]
    #
    #                     storepath = f'C:/Users/nemo/Desktop/Studing/ChatApp/Icons/{myContact.idContact}.jpg'
    #                     with open(storepath, 'wb') as file:
    #                         file.write(myContact.img)
    #                         file.close()
    #
    #                     contact = Contact(fullname= fullName , photo=storepath , id=myContact.idContact , about=myContact.Myabout)
    #                     self.verticalLayout_4.addWidget(contact.win)
    #
    #                     self.spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
    #
    #                     self.verticalLayout_4.addItem(self.spacerItem)
    #                     idddd = self.id
    #
    #                     myContact.dead = True
    #                     self.thread.join()
    #                     mySql_insert_query = """INSERT INTO contacts(user_ID, contact)
    #                                                    VALUES (%s, %s) """
    #
    #                     record = (idddd, myContact.num)
    #                     myCursor.execute(mySql_insert_query, record)
    #                     db.commit()
    #
    #                     myContact.dead = False
    #                     self.thread.start()
    #
    #             else:
    #                 print("please check your number !")
    #                 contactwindow.setText('please check your number !')
    #                 contactwindow.setStyleSheet('color:#b62916;')
    #
    #
    #     else:
    #         print("This number out of range!!")
    #         contactwindow.setText('This number out of range!')
    #         contactwindow.setStyleSheet('color:#b62916;')


    def constantContact(self, userIdNumber , searching = ''):

        myCursor.execute(f"select contact from contacts where user_ID = {userIdNumber} ;")
        select = myCursor.fetchall()
        for i in select:
            print('i :' ,i)
            number = i[0]
            myCursor.execute(f"select user_ID from chat_user where mobile_number = {number}")
            Id = myCursor.fetchall()[0][0]

            print(Id)
            myCursor.execute(f"select first_name , last_name from chat_user where user_ID={Id} ;")
            selectContact = myCursor.fetchall()
            print(selectContact)
            firstName = selectContact[0][0]
            lastName = selectContact[0][1]
            fullName = firstName + ' ' + lastName
            print(fullName)

            myCursor.execute(f"select About_description from user_profile_description where user_ID = {Id}")
            Myabout = myCursor.fetchall()[0][0]



            myCursor.execute(f"select personal_photo from user_profile_description where user_ID = {Id}")
            img = myCursor.fetchall()[0][0]
            storepath = f'C:/Users/nemo/Desktop/Studing/ChatApp/Icons/{Id}.jpg'
            with open(storepath, 'wb') as file:
                file.write(img)
                file.close()

            contact = Contact(fullname= 'fullName' , about= 'Myabout' , photo= r'C:\Users\nemo\Desktop\Studing\ChatApp\Icons\9.jpg' , id= 9)

            if searching in contact.Data['fullname']:
                self.verticalLayout_4.addWidget(contact.win)

        self.spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(self.spacerItem)



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = myContact(9)
    ui.win.show()

    def update():
        # global myCursor , db
        while True:
            ui.constantContact(ui.id)
            # ui.Search()
            time.sleep(2)

    thread = threading.Thread(target=update )
    thread.start()

    sys.exit(app.exec_())

