import datetime
import random
import sys
from StoryUi import *
from PyQt5.QtWidgets import QWidget , QApplication ,QLabel

class Story(Ui_Story):

    def __init__(self , id: int , name ,date , txt= None , photo= None):  # type = 1 for txt , 0 for image
        self.wid = QWidget()
        super().setupUi(self.wid)
        self.storyTxt = txt
        self.photo = photo
        self.id = id
        self.PersonalPhoto.setStyleSheet(f"""border-image: url(Icons/{id}.jpg);
                                             border-radius: 40px;""")
        self.ContactName.setText(name)
        self.StoryDate.setText(str(date))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    story = Story(9,'abdalla',date=str(datetime.datetime.now()))
    story.wid.show()
    sys.exit(app.exec_())