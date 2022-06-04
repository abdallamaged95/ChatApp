# Import Libraries
import os

import Message
import datetime
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from MessageUI import *
from Message import *
import mysql.connector
import sys
import time
from playsound import *
from gtts import gTTS
# Initialize User_ID, Chat_Rooms_ID
user_ID = 1
chat_Rooms_ID = 2
#  Connect to Database
db = mysql.connector.connect(user='ChatApp',
                             password='Chatapp_project123',
                             host='192.168.1.70',
                             database='chat',
                             auth_plugin='mysql_native_password')
myCursor = db.cursor()


# Get All Messages In This ChatRoom, ChatRoom Type And Last seen For Another Users
def database():
    myCursor.execute(
        f"select message_ID, user_ID, messageText, massageTime from message where chat_Rooms_ID = {chat_Rooms_ID};")
    database_msg = myCursor.fetchall()

    myCursor.execute(
        f"select last_seen from chat_rooms_info where chat_Rooms_ID = {chat_Rooms_ID} and user_ID <> {user_ID} ;")
    last_seen = myCursor.fetchall()

    myCursor.execute(f"select chat_Room_type from chat_rooms;")
    chatroom_type = myCursor.fetchall()[0][0]
    if chatroom_type == 0:
        last_seen = last_seen[0][0]
    return database_msg, last_seen, chatroom_type


# Check Message Seen Or Not To Update Database
def check(sign):
    if sign == "✓✓":
        sign = 1
    elif sign == "✓":
        sign = 0
    return sign


# Check Message Seen Or Not
def time_check(last_seen, time_of_msg, sign):
    if (last_seen - time_of_msg) < 0:
        sign = "✓"
    elif (last_seen - time_of_msg) >= 0:
        sign = "✓✓"
    return sign


# Always Refresh Data In RealTime
class Thread(QThread):
    data = pyqtSignal(tuple)

    def run(self):
        while True:

            thread_db = mysql.connector.connect(user='ChatApp',
                                         password='Chatapp_project123',
                                         host='192.168.1.70',
                                         database='chat',
                                         auth_plugin='mysql_native_password')
            thread_cursor = thread_db.cursor()

            thread_cursor.execute(
                f"select message_ID, user_ID, messageText, massageTime "
                f"from message where chat_Rooms_ID = {chat_Rooms_ID};")
            database_msg = thread_cursor.fetchall()

            thread_cursor.execute(
                f"""select last_seen from chat_rooms_info where chat_Rooms_ID
                = {chat_Rooms_ID} and user_ID <> {user_ID} ;""")
            last_seen = thread_cursor.fetchall()

            thread_cursor.execute(f"select chat_Room_type from chat_rooms;")
            chatroom_type = thread_cursor.fetchall()[0][0]

            if chatroom_type == 0:
                last_seen = last_seen[0][0]

            signal = (database_msg, last_seen, chatroom_type )

            time.sleep(1)
            self.data.emit(signal)


class MyWindow(Ui_Form):
    msgCount = 0
    def __init__(self):
        # Create Widget
        self.var = QWidget()
        super().setupUi(self.var)

        self.thread = Thread()

        self.Emojis_window_Animation = QPropertyAnimation(self.Emojis_window, b'maximumHeight')
        self.Send_message_bar_Animation = QPropertyAnimation(self.Send_message_bar, b'maximumHeight')

        self.set_emojis_buttons()

        database_msg, last_seen, chatroom_type = database()
        self.Hear_button.clicked.connect(lambda: self.PlayMsg())
        self.Send_button.clicked.connect(lambda: self.send(chatroom_type, last_seen))

        self.load_data()

        self.Undo.clicked.connect(lambda: self.undo())

    def load_data(self):
        self.thread.data.connect(self.msg_gui)
        self.thread.start()
    def PlayMsg(self):
        MyWindow.msgCount += 1
        myCursor.execute(
            f"select message_ID, messageText from message where chat_Rooms_ID = {chat_Rooms_ID} and user_ID <> {user_ID} ;")
        msgId ,msgTxt = myCursor.fetchall()[-1]
        mytext = msgTxt
        language = 'en'
        myobj = gTTS(text=mytext, lang=language, slow=False)
        path = f"Voice/msg{msgId}_{MyWindow.msgCount}.mp3"
        myobj.save(path)
        playsound(path)


    def set_emojis_buttons(self):
        self.Emoji_button.clicked.connect(self.emoji_window_animation)
        self.rolling_on_the_floor_laughing.clicked.connect(lambda: self.add_emoji("🤣"))
        self.slightly_smiling_face.clicked.connect(lambda: self.add_emoji("🙂"))
        self.melting_face.clicked.connect(lambda: self.add_emoji("🫠"))
        self.smiling_face_with_hearts.clicked.connect(lambda: self.add_emoji("🥰"))
        self.star_struck.clicked.connect(lambda: self.add_emoji("🤩"))
        self.smiling_face_with_tear.clicked.connect(lambda: self.add_emoji("🥲"))
        self.nauseated_face.clicked.connect(lambda: self.add_emoji("🤢"))
        self.sneezing_face.clicked.connect(lambda: self.add_emoji("🤧"))
        self.hot_face.clicked.connect(lambda: self.add_emoji("🥵"))
        self.clown_face.clicked.connect(lambda: self.add_emoji("🤡"))
        self.see_no_evil_monkey.clicked.connect(lambda: self.add_emoji("🙈"))
        self.love_letter.clicked.connect(lambda: self.add_emoji("💌"))
        self.revolving_hearts.clicked.connect(lambda: self.add_emoji("💞"))
        self.blue_heart.clicked.connect(lambda: self.add_emoji("💙"))
        self.black_heart.clicked.connect(lambda: self.add_emoji("🖤"))
        self.backhand_index_pointing_left.clicked.connect(lambda: self.add_emoji("👈"))
        self.backhand_index_pointing_right.clicked.connect(lambda: self.add_emoji("👉"))
        self.thumbs_up.clicked.connect(lambda: self.add_emoji("👍"))
        self.man_facepalming.clicked.connect(lambda: self.add_emoji("🤦"))
        self.eagle.clicked.connect(lambda: self.add_emoji("🦅"))
        self.salt.clicked.connect(lambda: self.add_emoji("🧂"))
        self.fire.clicked.connect(lambda: self.add_emoji("🔥"))
        self.laptop.clicked.connect(lambda: self.add_emoji("💻"))
        self.flag_palestinian_territories.clicked.connect(lambda: self.add_emoji("🇵🇸"))

    def emoji_window_animation(self):

        # Choose Type of Animation
        self.Emojis_window_Animation.setEasingCurve(QEasingCurve.OutQuart)
        self.Send_message_bar_Animation.setEasingCurve(QEasingCurve.OutQuart)

        # Set Duration To Start And End in it
        self.Emojis_window_Animation.setDuration(900)
        self.Send_message_bar_Animation.setDuration(900)

        if self.Emojis_window.height() == 0:
            self.Send_message_bar_Animation.setStartValue(80)
            self.Emojis_window_Animation.setStartValue(0)

            self.Emojis_window_Animation.setEndValue(90)
            self.Send_message_bar_Animation.setEndValue(170)

        else:
            self.Send_message_bar_Animation.setStartValue(170)
            self.Emojis_window_Animation.setStartValue(90)

            self.Send_message_bar_Animation.setEndValue(80)
            self.Emojis_window_Animation.setEndValue(0)

        self.Emojis_window_Animation.start()
        self.Send_message_bar_Animation.start()

    def add_emoji(self, emoji_to_add):

        self.plainTextEdit.moveCursor(QtGui.QTextCursor.End)
        self.plainTextEdit.insertPlainText(emoji_to_add)

    def send(self, chatroom_type, last_seen):

        # Get Message From plainTextEdit
        msg = self.plainTextEdit.toPlainText()
        self.plainTextEdit.clear()

        if msg == "":
            self.plainTextEdit.setPlaceholderText("Enter valid text")

        else:
            self.plainTextEdit.setPlaceholderText("Type a message")

            current_time = datetime.datetime.now()
            current_time.strftime("%Y-%m-%d %H:%M:%S")

            msg_widget, checkmark = self.msg_check(current_time, chatroom_type, last_seen, msg, 0, -1, -1, -1)

            myCursor.execute(
                f"insert into message (user_ID, chat_Rooms_ID,messageText, massageTime) values"
                f" ( {user_ID}, {chat_Rooms_ID}, '{msg}', '{current_time}');")
            db.commit()

            message_time = current_time.strftime("%H:%M:%S")
            message_date = current_time.strftime("%Y-%m-%d")

            checkmark = check(checkmark)

            myCursor.execute(f"select message_ID from message")
            msgID = myCursor.fetchall()[-1][0]

            myCursor.execute(f"insert into status (message_ID, staus_type, time_of_message, date_of_message) "
                             f"values ({msgID},{checkmark},'{message_time}','{message_date}');")
            db.commit()

            self.gridLayout_5.addWidget(msg_widget, 0, Qt.AlignRight)

            vertical_scroll_max_value = self.scrollArea.verticalScrollBar().maximum()
            self.scrollArea.verticalScrollBar().setValue(vertical_scroll_max_value)

    def msg_gui(self, data):

        database_msg = data[0]
        last_seen = data[1]
        chatroom_type = data[2]
        index = 0

        # Clear Widgets
        for i in reversed(range(self.gridLayout_5.count())):
            self.gridLayout_5.itemAt(0).widget().setParent(None)

        while index < database_msg.__len__():

            msg = database_msg[index][2]
            time_of_msg = str(database_msg[index][3])
            time_of_msg = datetime.datetime.strptime(time_of_msg, '%Y-%m-%d %H:%M:%S')

            msg_widget, checkmark = self.msg_check(time_of_msg, chatroom_type, last_seen, msg, 0, -1, database_msg,
                                                   index)

            if (user_ID == database_msg[index][1]) and (msg != "Message deleted"):
                msg_widget.setStyleSheet("QLabel#msg\n"
                                         "{\n"
                                         "background-color: rgb(7, 94, 84);\n"
                                         "color: #fff;\n"
                                         "border-top-left-radius: 0.7em;\n"
                                         "border-top-right-radius: 0.1em;\n"
                                         "margin-top: 1.1em;\n"
                                         "margin-right: 1em;\n"
                                         "margin-left: 1em;\n"
                                         "}\n"
                                         "\n"
                                         "QLabel#time\n"
                                         "{\n"
                                         "background-color: rgb(7, 94, 84);\n"
                                         "color: #fff;\n"
                                         "margin-right: 1em;\n"
                                         "margin-left: 1em;\n"
                                         "margin-bottom: 1em;\n"
                                         "border-bottom-right-radius: 0.7em;\n"
                                         "border-bottom-left-radius: 0.7em;\n"
                                         "}")
                self.gridLayout_5.addWidget(msg_widget, 0, Qt.AlignRight)

            elif (user_ID == database_msg[index][1]) and (msg == "Message deleted"):
                msg_widget.setStyleSheet("QLabel#msg\n"
                                         "{\n"
                                         "background-color: rgb(7, 94, 84);\n"
                                         "color: #fff;\n"
                                         "border-radius: 1em;\n"
                                         "border-top-right-radius: 0.1em;\n"
                                         "margin: 1em;\n"
                                         "}\n")
                self.gridLayout_5.addWidget(msg_widget, 0, Qt.AlignRight)

            elif (user_ID != database_msg[index][1]) and (msg != "Message deleted"):
                msg_widget.setStyleSheet("QLabel#msg\n"
                                         "{\n"
                                         "background-color: rgb(39, 52, 67);\n"
                                         "color: #fff;\n"
                                         "border-top-left-radius: 0.1em;\n"
                                         "border-top-right-radius: 0.7em;\n"
                                         "margin-top: 1.1em;\n"
                                         "margin-right: 1em;\n"
                                         "margin-left: 1em;\n"
                                         "}\n"
                                         "\n"
                                         "QLabel#time\n"
                                         "{\n"
                                         "background-color: rgb(39, 52, 67);\n"
                                         "color: #fff;\n"
                                         "margin-right: 1em;\n"
                                         "margin-left: 1em;\n"
                                         "margin-bottom: 1em;\n"
                                         "border-bottom-right-radius: 0.7em;\n"
                                         "border-bottom-left-radius: 0.7em;\n"
                                         "}")
                self.gridLayout_5.addWidget(msg_widget, 0, Qt.AlignLeft)

            elif (user_ID != database_msg[index][1]) and (msg == "Message deleted"):
                msg_widget.setStyleSheet("QLabel#msg\n"
                                         "{\n"
                                         "background-color: rgb(39, 52, 67);\n"
                                         "color: #fff;\n"
                                         "border-radius: 0.7em;\n"
                                         "border-top-left-radius: 0.1em;\n"
                                         "margin: 1em;\n"
                                         "}\n")
                self.gridLayout_5.addWidget(msg_widget, 0, Qt.AlignLeft)

            index = index + 1

    def msg_check(self, time_of_msg, chatroom_type, last_seen, msg, undo, i, database_msg, index):
        timestamp_of_msg = time_of_msg.timestamp()
        counter = 0
        checkmark = ""

        if chatroom_type == 0:
            timestamp_last_seen = last_seen.timestamp()

            checkmark = time_check(timestamp_last_seen, timestamp_of_msg, checkmark)

        elif chatroom_type == 1:

            while counter < last_seen.__len__():

                last_seen = last_seen[counter][0]
                timestamp_last_seen = last_seen.timestamp()

                checkmark = time_check(timestamp_last_seen, timestamp_of_msg, checkmark)

                if checkmark == "✓":
                    break
                counter = counter + 1

        time_of_msg = time_of_msg.strftime("%I:%M %p")

        msg_widget = QtWidgets.QWidget()
        msg_ui = Message.Ui_Message_2()
        msg_ui.setupUi(msg_widget)

        msg_ui.time.setText(checkmark + "   " + str(time_of_msg))
        msg_ui.time.adjustSize()
        width_time = msg_ui.time.width()

        msg_ui.msg.setText(msg)

        msg_ui.msg.adjustSize()
        width = msg_ui.msg.width()

        if width_time > width:
            width = width_time

        height = msg_ui.msg.height() + 35

        if msg == "Message deleted":
            msg_ui.time.setText("")
            msg_ui.time.setMaximumSize(0, 0)
            height = msg_ui.msg.height()

        msg_ui.containter.setMaximumSize(width, height)
        msg_ui.Message_frame.setMaximumSize(width, height)
        msg_widget.setMinimumSize(width, height)

        if undo and i != -1:
            msg_ui.msg.setStyleSheet("QLabel#msg\n"
                                     "{\n"
                                     "background-color: rgb(7, 94, 84);\n"
                                     "color: #fff;\n"
                                     "border-radius: 0.7em;\n"
                                     "border-top-right-radius: 0.1em;\n"
                                     "margin: 1em;\n"
                                     "}\n")
            self.gridLayout_5.insertWidget(i, msg_widget, 0, Qt.AlignRight)

            if database_msg != -1 and index != -1:
                checkmark = check(checkmark)
                msg_id = database_msg[index][0]

                myCursor.execute(f"update status set staus_type = {checkmark} where message_ID = {msg_id};")
                db.commit()

        return msg_widget, checkmark

    def undo(self):
        myCursor.execute(f"select message_ID, messageText from message where user_ID = {user_ID};")
        undo_database = myCursor.fetchall()[-1]

        if undo_database[1] == "Message deleted":
            self.plainTextEdit.setPlaceholderText("Message already deleted")

        elif(undo_database[1] != ""):
            i = self.gridLayout_5.__len__() - 1
            self.plainTextEdit.setPlaceholderText("Type a message")

            myCursor.execute(f"delete from status where message_ID = {undo_database[0]};")
            db.commit()

            myCursor.execute(
                f"update message set messageText = 'Message deleted' where message_ID = {undo_database[0]};")
            db.commit()

            current_time = datetime.datetime.now()
            current_time.strftime("%Y-%m-%d %H:%M:%S")

            while i >= 0:
                if (self.gridLayout_5.itemAt(i).widget().pos().x()) > 400:
                    self.gridLayout_5.itemAt(i).widget().setMinimumSize(0, 0)
                    self.gridLayout_5.itemAt(i).widget().setMaximumSize(0, 0)

                    self.msg_check(current_time, 0, current_time, "Message deleted", 1, i, -1, -1)
                    break

                i = i - 1


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = MyWindow()
    ui.var.show()
    sys.exit(app.exec_())
