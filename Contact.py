from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys
from ContactUi import *

class Contact(Ui_Contact):
    adding = []
    defaultPhoto = r'Icons/clipart4208228.png'
    defaultBinary = b''

    def __init__(self , fullname : str , id : int , photo : str, about : str ,visibility: int):
        with open(Contact.defaultPhoto, 'rb') as file:
            Contact.defaultBinary = file.read()

        self.win = QWidget()
        super().setupUi(self.win)
        self.Data = {
            'fullname': fullname,
            'id'      : id ,
            'photo'   : photo,
            'about'   : about
        }
        self.Namecontact.setText(self.Data['fullname'])
        if visibility:
            self.Aboutcontact.setText(self.Data['about'])
            self.contactphoto.setStyleSheet(f"""
            border-image:url({self.Data['photo']});
            border-radius:25px;
            """)
        else:
            self.Aboutcontact.setText('')
            self.contactphoto.setStyleSheet(f"""
            border-image:url({Contact.defaultPhoto});
            border-radius:25px;
            """)
        self.state = False
        self.checkBox.clicked.connect(lambda : self.Add())

    def Add(self):
        self.state = not self.state
        print(self.state)
        if self.state:
            if self.Data['id'] not in Contact.adding :
                Contact.adding.append(self.Data['id'])
        else:
            if self.Data['id'] in Contact.adding :
                Contact.adding.remove(self.Data['id'])
        print(Contact.adding)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    var = Contact('abdalla maged', 55 , '','iam vengeance',1)
    var.win.show()
    print(Contact.adding)
    sys.exit(app.exec_())
