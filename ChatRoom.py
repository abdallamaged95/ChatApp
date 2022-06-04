import subprocess
import sys
from PyQt5 import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from Mycontact import *
import MessageMain
import MessageUI
from ChatRoomWin import *
from movableLabel import *
from ChatRoomUi import *
from MessageMain import *
from saveSetting import saveSetting

class ChatRoom(Ui_ChatRoom):
    defaultPhoto = r'Icons/clipart4208228.png'
    defaultBinary = b''

    def __init__(self, id ,msgNum ,photo = '', name = ''):
        with open(ChatRoom.defaultPhoto, 'rb') as file:
            ChatRoom.defaultBinary = file.read()
        self.win = QWidget()
        self.Data = {
            'id'       : id,
            'photoLink':photo,
            'name'     :name,
        }
        super().setupUi(self.win)
        self.chatRoomButton.setText(self.Data['name'])
        self.chatRoomPhoto.setStyleSheet(f"""border-image:url({self.Data['photoLink']});
                                                border-radius: 30px;""")

        if (msgNum):
            self.msgCounter.setText(str(msgNum))
        else:
            self.msgCounter.setStyleSheet("""background-color : #111b21;
                                             border-radius : 13px;""")

# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     mine = ChatRoom()
#     mine.win.show()
#     sys.exit(app.exec_())