import datetime
import sys
import random
import time
from MainStoryUi import *
from StoryTextUi import *
from Story import *
from PyQt5.QtWidgets import QWidget , QApplication , QFileDialog
import mysql.connector
from PyQt5 import QtCore
import PyQt5
from PyQt5.QtCore import QThread
db = mysql.connector.connect(user='ChatApp',
                             password='Chatapp_project123',
                             host='192.168.1.70',
                             database='chat',
                             auth_plugin='mysql_native_password')
crs = db.cursor()

ShowNextStory = True

class ProgressBarThread(QThread):
    update_progress_bar = PyQt5.QtCore.pyqtSignal(int)
    def run(self):
        global ShowNextStory
        ShowNextStory = False
        for value in range(0, 101, 3):
            time.sleep(0.1)
            self.update_progress_bar.emit(value)
        ShowNextStory = True

class MainStory(Ui_MainStoriesWindow):
    def __init__(self,id):
        self.id = id
        self.str = QWidget()
        super().setupUi(self.str)

        self.storyText = Ui_AddTextStoryWindow()
        self.strTxt = QWidget()
        self.storyText.setupUi(self.strTxt)
        # Buttons Setup
        self.AddStoryText.clicked.connect(lambda: self.strTxt.show())
        self.storyText.SubmitButton.clicked.connect(lambda: self.AddText())
        self.AddStoryImage.clicked.connect(lambda: self.AddImage())

        self.OwnerImage.setStyleSheet(f"""border-image: url(Icons/{self.id}.jpg);
                                            border-radius: 40;""")
        self.CheckStoryTime()
        self.LoadStories()

    def callProgressBarThread(self):
        self.Worker = ProgressBarThread()
        self.Worker.start()
        self.Worker.update_progress_bar.connect(self.UpdateProgressBar)
        self.Worker.finished.connect(self.ClearStoryDisplay)

    def UpdateProgressBar(self, value):
        self.StoryDuration.setValue(value)

    def ClearStoryDisplay(self):
        self.Display.setStyleSheet("border-image: url(:Icons/WhatsappWebStoryPage.jpg);\n"
                                   "font: 14pt \"Arial\";\n"
                                   "color: white;")
        self.Display.setText('')
        self.StoryDuration.setValue(0)

    def CheckStoryTime(self):
        CurrTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        CurrTime = datetime.datetime.strptime(CurrTime, '%Y-%m-%d %H:%M:%S')
        crs.execute('select story_time from story')
        StoriesTime = crs.fetchall()
        for tup in StoriesTime:
            if ((CurrTime - tup[0]).days >= 1):
                crs.execute(f"delete from story where story_time = '{tup[0]}'")
                db.commit()

    def AddText(self):
        txt = self.storyText.TextEntry.toPlainText()
        self.storyText.TextEntry.clear()
        print(txt)
        if txt:
            current_time = datetime.datetime.now()
            current_time.strftime("%Y-%m-%d %H:%M:%S")
            crs.execute(f""" insert into story(user_ID ,story_time ,story_text)
                             values ({self.id} , '{current_time}' , '{txt}')""")
            db.commit()
            self.strTxt.close()


    def AddImage(self):
        image = QFileDialog.getOpenFileName(caption='Choose Profile Photo')
        path , extension = image
        print(path , extension)
        if path:
            with open(path, 'rb') as file:
                binary = file.read()

            current_time = datetime.datetime.now()
            current_time.strftime("%Y-%m-%d %H:%M:%S")
            crs.execute(f"""insert into story(user_ID ,story_time ,story_photo)
                            values({self.id} , '{current_time}' ,%s )""",(binary,))
            db.commit()

    def LoadStories(self):
        crs.execute(f"select contact from contacts where user_ID = {self.id};")
        contacts = crs.fetchall()
        for num in contacts:
            crs.execute(f"select user_Id , first_name , Last_name from chat_user where mobile_number = {num[0]}")
            contact_id ,first ,last = crs.fetchall()[0]
            contact_name = first + ' ' + last
            print(contact_id)
            crs.execute(f"select * from story where user_ID = {contact_id}")
            storyData = crs.fetchall()
            # print('storyData ',storyData)
            if storyData:
                print(contact_id , " has story")
                for i in storyData:
                    if not i[2] is None:
                        self.GetStoryTxt(contact_id,contact_name , i[1] ,txt=i[2])
                    elif not i[3] is None:
                        bin = i[3]
                        self.GetStoryPhoto(contact_id,contact_name, i[1] ,bin=bin)

        self.spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.scrollAreaContent.addItem(self.spacerItem)

    def GetStoryTxt(self,id,name,date,txt):
        if ShowNextStory:
            contactStory = Story(id, name, date, txt=txt)
            contactStory.PersonalPhoto.clicked.connect(lambda: self.ShowTxt(contactStory.storyTxt))
            self.scrollAreaContent.addWidget(contactStory.wid)

    def GetStoryPhoto(self,id,name,date,bin):
        if ShowNextStory:
            contactStory = Story(id, name, date, photo=bin)
            contactStory.PersonalPhoto.clicked.connect(lambda: self.ShowPhoto(contactStory.photo, contactStory.id))
            self.scrollAreaContent.addWidget(contactStory.wid)

    def ShowTxt(self ,storyTxt):
        global ShowNextStory
        if ShowNextStory:
            r = random.randint(0, 254)
            g = random.randint(0, 254)
            b = random.randint(0, 254)

            self.Display.setStyleSheet(f"background-color: rgb({r}, {g}, {b});\n"
                                                   "font: 20pt \"Arial\";\n"
                                                   "color: white;")
            self.Display.setText(storyTxt)
            self.callProgressBarThread()

    def ShowPhoto(self , binary , contact_id):
        global ShowNextStory
        if ShowNextStory:
            print(type(binary))
            if not binary is None:
                path = f'Icons/story{contact_id}.jpg'
                with open(path, 'wb') as file:
                    file.write(binary)
                    file.close()
                self.Display.clear()
                self.Display.setStyleSheet(f"""image:url({path});
                                               font: 20pt "Arial";
                                               color: white;""")
                self.callProgressBarThread()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    story = MainStory(11)
    story.str.show()
    sys.exit(app.exec_())