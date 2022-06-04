import time
from PyQt5 import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import mysql.connector
from LoginUi import *
from movableLabel import *
from MainChatRoom import *

db = mysql.connector.connect(user='ChatApp',
                             password='Chatapp_project123',
                             host='192.168.1.70',
                             database='chat',
                             auth_plugin='mysql_native_password')
myCursor = db.cursor()

class LoginWin(Ui_LoginUi):

    """ Abdalla Login Page Class"""
    filepath = r'Icons\RegisterPhoto.png'
    with open(filepath , 'rb') as file:
        defaultphoto = file.read()
    def __init__(self):

        self.RegisterData = {
            'firstName':'',
            'lastName':'',
            'phone':'',
            'password':'',
            'photoLink':'',
        }
        self.ProfileDescription = {
            'photoBinary': LoginWin.defaultphoto,
            'about':'',
            'visibility':1
        }
        self.LoginData = {
            'phone':'',
            'password':''
        }
        self.log = QWidget()     # empty window
        super().setupUi(self.log)    # to initialize widgets

        """ Buttons Assignment """
        self.loginButton.clicked.connect(self.login)     # attach login method to the button
        self.close.clicked.connect(sys.exit)    # Close Button
        self.min.clicked.connect(self.log.showMinimized)    # Minimize Button
        self.max.clicked.connect(self.MaxButton)
        self.registerButton.clicked.connect(self.Slide)
        self.backToLogin.clicked.connect(self.Slide)
        self.SubmitButton.clicked.connect(self.Register)
        self.BrowseImage.clicked.connect(self.BrowsePhoto)

        MovableLabel.mainWindow = self.log

        """ Remove Background and Windows Title Bar """
        self.log.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.log.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        QSizeGrip(self.frame)


    def MaxButton(self):
        if self.log.isMaximized():
            self.log.showNormal()
        else:
            self.log.showMaximized()

    def Slide(self):
        value = self.LoginSide.maximumSize()
        self.registerAnime = QPropertyAnimation(self.RegisterSide, b'maximumSize')
        self.loginAnime = QPropertyAnimation(self.LoginSide, b'maximumSize')
        self.loginAnime.setEasingCurve(QEasingCurve.OutQuart)
        self.registerAnime.setEasingCurve(QEasingCurve.OutQuart)
        self.registerAnime.setDuration(750)
        self.loginAnime.setDuration(750)
        newValue = int((self.log.width()/5)*3)
        if value.width() == 0:
            self.registerAnime.setStartValue(self.RegisterSide.size())
            self.registerAnime.setEndValue(QSize(0, value.height()))
            self.registerAnime.start()
            # print(self.RegisterSide.width())
            self.loginAnime.setStartValue(value)
            self.loginAnime.setEndValue(QSize(newValue, value.height()))
            self.loginAnime.start()
        else:
            self.loginAnime.setStartValue(value)
            self.loginAnime.setEndValue(QSize(0, value.height()))
            self.loginAnime.start()
            # print(self.RegisterSide.width())
            self.registerAnime.setStartValue(QSize(0, value.height()))
            self.registerAnime.setEndValue(QSize(newValue,value.height()))
            self.registerAnime.start()

    def login(self):
        # Store Input
        phone = self.phoneLine.text()
        passw = self.passwLine.text()

        # Checking for missing data
        if not phone and passw:
            self.errorLabel.setText('no phone number entered')
            print('please enter your phone number')
            return
        elif not passw and phone:
            self.errorLabel.setText('no password entered')
            print ('plase enter your password')
            return
        elif not phone and not passw:
            self.errorLabel.setText('no data entered')
            return
        else :
            self.errorLabel.clear()     # Clear Error message if all data entered

        # Clear Lines after insertion
        self.phoneLine.clear()
        self.passwLine.clear()


        # Get from Database
        myCursor.execute(f"select * from chat_user where mobile_number = '{phone}' and user_password = '{passw}'")
        user = myCursor.fetchall()  # Store Data found
        print(user)

        # Check for users found
        if not user:
            self.errorLabel.setText('no users found')
            return

        downloadPath = f'Icons/{user[0][0]}.jpg'
        with open(downloadPath,'wb') as file:
            file.write(self.ProfileDescription['photoBinary'])
            file.close()
        print('user ',user[0][0],'logging in')
        goNuts = myChatRoomWin(user[0][0])
        self.log.hide()
        goNuts.win.show()

    def BrowsePhoto(self):
        Photo = QFileDialog.getOpenFileName(caption='Choose Profile Photo',filter='*.jpg;;*.png')
        photoPath = Photo[0]
        photoExtenstion = Photo[1]
        print(photoPath)

        if photoPath:
            self.RegisterData['photoLink'] = photoPath
            self.registerProfileImage.setStyleSheet(f"""
            QLabel#registerProfileImage{{
            border-image: url({photoPath});
            border-radius : 70px;
            }}
            """)
            with open(photoPath , 'rb') as file:
                photoBinary = file.read()
                self.ProfileDescription['photoBinary'] = photoBinary


    def Register(self):
        if not (self.FirstName.text() and self.LastName.text() and self.SubmitPass.text() and self.SubmitPhone.text()) :
            self.registerErrorLabel.setText('Missing Data')
        else :
            self.RegisterData['firstName'] = self.FirstName.text()
            self.FirstName.clear()
            self.RegisterData['lastName'] = self.LastName.text()
            self.LastName.clear()
            self.RegisterData['phone'] = self.SubmitPhone.text()
            self.SubmitPhone.clear()
            self.RegisterData['password'] = self.SubmitPass.text()
            self.SubmitPass.clear()
            self.ProfileDescription['about'] = self.aboutRegister.text()
            self.aboutRegister.clear()

            myCursor.execute(f"select mobile_number from chat_user where mobile_number = {self.RegisterData['phone']}")
            if (myCursor.fetchall()):
                self.registerErrorLabel.setText("Phone Number is Already Used")
            if len(self.RegisterData['phone']) > 11:
                self.registerErrorLabel.setText("Phone Number out of Range")
            else:
                myCursor.execute(f"""
                insert into chat_user(mobile_number,user_password,first_name,Last_name)
                values ('{self.RegisterData['phone']}',
                        '{self.RegisterData['password']}',
                        '{self.RegisterData['firstName']}',
                        '{self.RegisterData['lastName']}');
                                                        """)
                db.commit()
                myCursor.execute(f"""select * from chat_user where mobile_number = '{self.RegisterData['phone']}';""")
                id = myCursor.fetchall()[0][0]
                print(type(id))

                myCursor.execute(f"""
                insert into user_profile_description(user_ID,visibilty,personal_photo,About_description)
                values({id},{self.ProfileDescription['visibility']},%s,'{self.ProfileDescription['about']}');
                """,(self.ProfileDescription['photoBinary'],))
                db.commit()

                print(self.ProfileDescription)
                print(self.RegisterData)

                # goNuts = myChatRoomWin(id)
                # self.log.hide()
                # goNuts.win.show()


if __name__ == "__main__":
    import sys
    print(LoginWin.__doc__)
    app = QtWidgets.QApplication(sys.argv)
    ui = LoginWin()
    ui.log.show()
    sys.exit(app.exec_())