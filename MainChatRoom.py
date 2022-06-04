
import sys
from PyQt5 import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QThread , pyqtSignal
from PyQt5.QtCore import *
import MessageMain
from ChatRoom import ChatRoom
from Mycontact import *
from ChatRoomWin import *
from movableLabel import *
from ChatRoomUi import *
from MessageMain import *
from saveSetting import saveSetting
from CreateGroup import *
from MainStory import *

db = mysql.connector.connect(user='ChatApp',
                             password='Chatapp_project123',
                             host='192.168.1.70',
                             database='chat',
                             auth_plugin='mysql_native_password')
myCursor = db.cursor()

class MyThread(QThread):
    Chats = pyqtSignal(list)
    id = -1
    def run(self):
        while True:
            RefreshDb = mysql.connector.connect(user='ChatApp',
                                               password='Chatapp_project123',
                                               host='192.168.1.70',
                                               database='chat',
                                               auth_plugin='mysql_native_password')
            cr = RefreshDb.cursor()

            cr.execute(f"""select chat_Rooms_ID from chat_rooms_info where user_ID = {self.id};""")
            rooms = cr.fetchall()
            self.Chats.emit(rooms)
            time.sleep(2)



class myChatRoomWin(Ui_ChatRoomWin):
    """ Abdalla ChatRoomWindow """
    def __init__(self , id):
        myCursor.execute(f'select personal_photo from user_profile_description where user_ID = {id}')
        binary = myCursor.fetchall()[0][0]
        downloadPath = f'Icons/{id}.jpg'
        with open(downloadPath, 'wb') as file:
            file.write(binary)
            file.close()

        self.groupdata = {
            'id'        :0,
            'groupPhoto':b'',
            'photoPath' :'',
            'groupName' :'',
        }
        self.id = id
        self.win = QWidget()
        super().setupUi(self.win)
        self.win.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.win.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.close.clicked.connect(lambda : sys.exit())
        self.min.clicked.connect(lambda : self.win.showMinimized())
        self.max.clicked.connect(lambda : self.MaxButton())
        self.newChatButton.clicked.connect(lambda : self.SwitchContact())
        self.profilePhoto.clicked.connect(lambda : self.SwitchProfile())
        self.searchButton.clicked.connect(lambda: self.Search())
        MovableLabel.mainWindow = self.win

        self.contactWin = myContact(self.id)
        self.verticalLayout_5.addWidget(self.contactWin.win)

        self.ChatRooms.setMaximumHeight(16777215)
        self.contactWin.win.setMaximumHeight(0)

        self.contactWin.exitContact.clicked.connect(lambda : self.SwitchContact())
        self.contactWin.createRoomButton.clicked.connect(lambda : self.CreateRoom())

        # Story Setup
        self.statusButton.clicked.connect(lambda: self.SwitchStory())
        self.story = MainStory(self.id)
        self.gridLayout.addWidget(self.story.str, 2, 0, 1, 2)
        self.story.str.setMaximumHeight(0)
        self.story.Back.clicked.connect(lambda: self.SwitchStory())

        self.var = QWidget()
        self.room = Ui_CreateGroup()
        self.room.setupUi(self.var)
        self.var.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.var.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.room.groupPhoto.clicked.connect(lambda: self.SetGroupPhoto())
        self.room.createRoomButton.clicked.connect(lambda: self.SetGroupData())
        self.room.close.clicked.connect(lambda: self.var.hide())

        self.profilePhoto.setStyleSheet(f"""QPushButton#profilePhoto{{
                                            border-image : url(Icons/{self.id});
                                            border-radius : 35px;
                                            }}""")

        self.thr = MyThread()
        self.thr.id = self.id
        self.thr.Chats.connect(self.LoadChats)
        self.thr.start()
        # self.LoadChats()

    # def Search(self):
    #     if (self.verticalLayout_4.count() > 0):
    #         for i in reversed(range(self.verticalLayout_4.count() - 1)):
    #             self.verticalLayout_4.itemAt(0).widget().setParent(None)
    #         self.verticalLayout_4.removeItem(self.spacerItem)
    #     searching = self.searchLine.text()
    #     self.LoadChats(searching)
    #     vertical_scroll_min_value = self.scrollArea.verticalScrollBar().minimum()
    #     self.scrollArea.verticalScrollBar().setValue(vertical_scroll_min_value)

    def CreateRoom(self):
        if self.id not in Contact.adding:
            Contact.adding.append(self.id)

        if (len(Contact.adding) == 2):
            myCursor.execute("""insert into chat_rooms(chat_Room_type) 
                                values(0)""")
            db.commit()
            myCursor.execute(f"""select chat_Rooms_ID from chat_rooms;""")
            self.groupdata['id'] = myCursor.fetchall()[-1][0]
            print(self.groupdata['id'])
            for i in Contact.adding:
                current_time = datetime.datetime.now()
                current_time.strftime("%Y-%m-%d %H:%M:%S")
                myCursor.execute(f"""insert into chat_rooms_info(chat_Rooms_ID ,user_ID,last_seen )
                                     values ({self.groupdata['id']} , {i} , '{current_time}');""")
                db.commit()
            other = Contact.adding
            other.remove(self.id)
            self.groupdata['photoPath'] = f'Icons/{other[0]}.jpg'
            myCursor.execute(f"""select first_name , Last_name from chat_user where user_ID = {other[0]}""")
            nameTuple = myCursor.fetchall()[0]
            self.groupdata['groupName'] = nameTuple[0] +' '+ nameTuple[1]
            self.AddChat()

        else:
            # Default Group Photo
            self.groupdata['groupPhoto'] = ChatRoom.defaultBinary
            self.groupdata['photoPath'] = ChatRoom.defaultPhoto
            self.var.show()
        self.SwitchContact()

    def SetGroupPhoto(self):
        photo = QFileDialog.getOpenFileName(caption='Choose Profile Photo', filter='*.jpg;;*.png')
        path = photo[0]

        if path:
            with open(path, 'rb') as file:
                self.groupdata['groupPhoto'] = file.read()
            self.groupdata['photoPath'] = path
            self.room.groupPhoto.setStyleSheet(f"""border-image :url({path});
                                                  border-radius : 35px;""")
        else:
            # Setting Default Group Photo
            self.groupdata['groupPhoto'] = ChatRoom.defaultBinary
            self.groupdata['photoPath'] = ChatRoom.defaultPhoto

        path = None


    def SetGroupData(self):
        # Setting Group Name
        self.groupdata['groupName'] = self.room.groupName.text()
        self.room.groupName.clear()

        myCursor.execute(f"""insert into chat_rooms (chat_Room_type , chat_room_photo , chat_room_name)
                             values (1 , %s , %s) """ , (self.groupdata['groupPhoto'],self.groupdata['groupName']))
        db.commit()
        myCursor.execute("select chat_Rooms_ID from chat_rooms;")
        self.groupdata['id'] = myCursor.fetchall()[-1][0]
        for i in Contact.adding:
            current_time = datetime.datetime.now()
            current_time.strftime("%Y-%m-%d %H:%M:%S")
            myCursor.execute(f"""insert into chat_rooms_info(chat_Rooms_ID,user_ID,last_seen)
                                 values ({self.groupdata['id']} , {i} ,'{current_time}')""")
            db.commit()

        self.AddChat()

        # Resetting Default Group Photo
        self.groupdata['groupPhoto'] = ChatRoom.defaultBinary
        self.groupdata['photoPath'] = ChatRoom.defaultPhoto
        self.room.groupPhoto.setStyleSheet(f"""border-image :url({ChatRoom.defaultPhoto});
                                                          border-radius : 35px;""")
        self.var.hide()

    def AddChat(self):
        myCursor.execute(f"select last_seen from chat_rooms_info where user_ID = {self.id} and chat_Rooms_ID = {self.groupdata['id']}")
        lastSeen = myCursor.fetchall()[0][0]
        print('*******************************************')
        myCursor.execute(f"""select massageTime from message
                            where chat_Rooms_ID = {self.groupdata['id']} and  massageTime > '{lastSeen}' and user_ID <>{self.id} """)
        msgNum = len(myCursor.fetchall())
        print('num : ',msgNum)

        room = ChatRoom(id = self.groupdata['id'],
                        photo=self.groupdata['photoPath'],
                        name=self.groupdata['groupName'],
                        msgNum = msgNum
                        )
        room.chatRoomButton.clicked.connect(lambda: self.OpenMsg(room.Data['id'] , room.Data['photoLink'] , room.Data['name']))
        row = self.verticalLayout_4.count()
        if row > 0:
            self.verticalLayout_4.removeItem(self.spacerItem)
        self.verticalLayout_4.addWidget(room.win)
        self.spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(self.spacerItem)

    def OpenMsg(self , chatId , chatPhoto , chatName):
        print(chatId)
        # self.Search()
        MessageMain.user_ID = self.id
        MessageMain.chat_Rooms_ID = chatId
        msg = MyWindow()
        msg.Name.setText(chatName)
        msg.Image.setStyleSheet(f"""border-radius: 35px;
            border-image: url({chatPhoto});""")
        self.gridLayout_2.addWidget(msg.var,0,0)

        current_time = datetime.datetime.now()
        current_time.strftime("%Y-%m-%d %H:%M:%S")
        print("current Time : ",current_time)

        try:
            myCursor.execute(f"update chat_rooms_info set last_seen = '{current_time}' where user_ID = {self.id} and chat_Rooms_ID = {chatId};")
        except: print('could not update last seen')
        db.commit()

    def SwitchContact(self):
        if self.ChatRooms.height() == 0:
            self.contactWin.win.setMaximumHeight(0)
            self.ChatRooms.setMaximumHeight(16777215)
        else:
            self.ChatRooms.setMaximumHeight(0)
            self.contactWin.win.setMaximumHeight(16777215)

    def SwitchProfile(self):
        self.profileSetting = saveSetting(self.id)
        self.gridLayout_2.addWidget(self.profileSetting.akm,0,0)


    def LoadChats(self, rooms):
        if (self.verticalLayout_4.count() > 0):
            for i in reversed(range(self.verticalLayout_4.count() - 1)):
                self.verticalLayout_4.itemAt(0).widget().setParent(None)
            self.verticalLayout_4.removeItem(self.spacerItem)
        self.searching = self.searchLine.text()
        # vertical_scroll_min_value = self.scrollArea.verticalScrollBar().minimum()
        # self.scrollArea.verticalScrollBar().setValue(vertical_scroll_min_value)
        print('num of chats : ',len(rooms))
        for i in rooms:
            myCursor.execute(f"select chat_Room_type from chat_rooms where chat_Rooms_ID = {i[0]}")
            state = myCursor.fetchall()[0][0]
            print('state : ',state)
            if state:
                myCursor.execute(f"""select chat_room_photo , chat_room_name from chat_rooms
                                     where chat_Rooms_ID = {i[0]}""")
                groupPhoto , groupName = myCursor.fetchall()[0]
                storePath = f'Icons/room{i[0]}.jpg'
                with open(storePath,'wb') as file:
                    file.write(groupPhoto)
                    file.close()
                self.groupdata['id'] = i[0]
                self.groupdata['photoPath'] = storePath
                self.groupdata['groupName'] = groupName
            else:
                self.groupdata['id'] = i[0]
                myCursor.execute(f"""select user_ID from chat_rooms_info
                                    where user_ID <> {self.id} and chat_Rooms_ID = {i[0]};""")
                other = myCursor.fetchall()[0][0]
                myCursor.execute(f"""select first_name , Last_name from chat_user where user_ID = {other};""")
                nameTuple = myCursor.fetchall()[0]
                self.groupdata['groupName'] = nameTuple[0] + ' ' + nameTuple[1]
                self.groupdata['photoPath'] = f'Icons/{other}.jpg'
            if (self.searching in self.groupdata['groupName']):
                self.AddChat()

    def MaxButton(self):
        if self.win.isMaximized():
            self.win.showNormal()
        else:
            self.win.showMaximized()

    def SwitchStory(self):
        if self.story.str.maximumHeight() == 0:
            self.chatSide.setMaximumHeight(0)
            self.controlSide.setMaximumHeight(0)
            self.story.str.setMaximumHeight(16777215)
        else:
            self.chatSide.setMaximumHeight(16777215)
            self.controlSide.setMaximumHeight(16777215)
            self.story.str.setMaximumHeight(0)

if __name__ == "__main__":
    print(myChatRoomWin.__doc__)
    app = QtWidgets.QApplication(sys.argv)
    ui = myChatRoomWin(56)
    ui.win.show()
    sys.exit(app.exec_())