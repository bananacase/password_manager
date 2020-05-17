import sys
import hashlib
import pickle
import keyboard
import pyperclip
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from Crypto.Cipher import AES


class Window(QWidget):
    """Class Window. 
    The constructor creates the main window, doesn't accept any values. You have to create an empty file with name 'data.pep' in the same directory for the program to work correctly"""
    
    def __init__(self): 
        super(Window, self).__init__()

        #Block fields for writing notes and changing master-password
        self.addKey = QLineEdit()
        self.addLogin = QLineEdit()
        self.addPass = QLineEdit()
        self.oldPassword = QLineEdit()
        self.oldPassword.setEchoMode(QLineEdit.PasswordEchoOnEdit)
        self.newPassword = QLineEdit()
        self.newPassword.setEchoMode(QLineEdit.PasswordEchoOnEdit)

        #Сreate a dictionary-object for storing notes, a master-password and a panel on which will display the contents of the dictionary
        self.someDict = {}
        self.password = bytes('0', encoding='utf8')
        self.mkEdit = QLineEdit()
        self.mkEdit.setEchoMode(QLineEdit.PasswordEchoOnEdit)
        self.layoutFromRead = QFormLayout()
        self.layoutFromRead.setFieldGrowthPolicy(2)

        #Font declaration block
        self.FontFromLabels = QFont("Tahoma", 16, 57)
        self.FontFromNotes = QFont("Tahoma", 10, 63)
        self.FontFromButtons = QFont("Tahoma", 10, 57)

        #Create a widget like layout, which contain other widgets. Widget for widgets mf
        self.stack0 = QWidget()
        self.stack1 = QWidget()
        self.stack2 = QWidget()
        self.stack3 = QWidget()
        self.stack4 = QWidget()
        self.stack5 = QWidget()

        #Сreate a stack class object and add our widgets
        self.Stack = QStackedWidget(self)        
        self.Stack.addWidget (self.stack0) 
        self.Stack.addWidget (self.stack1)
        self.Stack.addWidget (self.stack2)
        self.Stack.addWidget (self.stack3)
        self.Stack.addWidget (self.stack4)
        self.Stack.addWidget (self.stack5)

        #Initialize all widgets. All functions implements a certain interface that helps the user to work with notes. Yeah, front-end functions, but I describe them like widget-layout.
        self.stack0UI()  
        self.stack1UI()  
        self.stack2UI()  
        self.stack3UI()
        self.stack4UI()
        self.stack5UI()  
            
        hbox = QHBoxLayout(self)
        hbox.addSpacing(0)
        hbox.addWidget(self.Stack)

        #Initialize and show Window
        self.setLayout(hbox)
        self.display(0)
        self.setGeometry(100, 100, 20, 20)
        self.setWindowTitle('Password manager')
        self.setWindowIcon(QIcon('image\IconWindow.png'))
        self.show()

        #Shortkey for change main layout
        keyboard.add_hotkey("Escape", self.turnBack)
        
    def stack0UI(self) -> None:
        """First window-layout, when user should enter his master-password."""
        layout = QHBoxLayout()
        layout.addSpacing(800)
        butBegin = QPushButton("Начать")
        butBegin.setFont(self.FontFromButtons)
        butBegin.setToolTip("Напишите <b>правильный</b> мастер-пароль")
        butBegin.setIcon(QIcon('image\IconBegin.png'))
        butBegin.setIconSize(QSize(30, 30))
        butBegin.clicked.connect(lambda *args: self.butBegin_Click())
        butBegin.setShortcut("Return")
        lbl = QLabel("Введите мастер-пароль ниже")
        lbl.setFont(self.FontFromLabels)        
        l1 = QVBoxLayout()
        l1.addLayout(layout)
        l1.addWidget(lbl)
        l1.addWidget(self.mkEdit)
        l1.addWidget(butBegin)
        self.stack0.setLayout(l1)

    def butBegin_Click(self):
        """Function which is called when user is trying to start the program.
	Function check the correct password and password, which write a user.
        """
        if not self.mkEdit.text():
            b = QMessageBox(2, "Предупреждение!", "Вы не написали пароль", buttons = QMessageBox.Ok)
            result = b.exec_()
        else:
            self.password = bytes(self.mkEdit.text(), encoding='utf8')
            try:
            	self.LoadingAndDecrypt()
            	self.display(1)
            except pickle.UnpicklingError:
            	c = QMessageBox(2, "Предупреждение!", "Вы написали неверный пароль", buttons = QMessageBox.Ok)
            	result = c.exec_()

    def butEnd_Click(self) -> None:
        """Function which is called when user clicked a button"""
        self.DumpingAndEncrypt()
        qApp.quit()
            
    def stack1UI(self) -> None:
        """Main window-layout, which contain other widget-layout."""
        
        buttonRead = QPushButton("Прочитать")
        buttonRead.setFont(self.FontFromButtons)
        buttonRead.setToolTip("В этом разделе Вы можете прочитать ваши пароли и скопировать их")
        buttonRead.setIcon(QIcon('image\IconRead.png'))
        buttonRead.setIconSize(QSize(30, 30))
        buttonRead.setShortcut("Ctrl+1")
        buttonRead.setAutoDefault(True)
        buttonRead.clicked.connect(lambda *args: self.display(2))

        buttonWrite = QPushButton("Записать")
        buttonWrite.setFont(self.FontFromButtons)
        buttonWrite.setIcon(QIcon('image\IconWrite.png'))
        buttonWrite.setIconSize(QSize(30, 30))
        buttonWrite.setToolTip("В этом разделе Вы можете добавить новую запись")
        buttonWrite.setShortcut("Ctrl+2")
        buttonWrite.setAutoDefault(True)
        buttonWrite.clicked.connect(lambda *args: self.display(3))    

        buttonChangeMK = QPushButton("Изменить мастер-пароль")
        buttonChangeMK.setFont(self.FontFromButtons)
        buttonChangeMK.setIcon(QIcon('image\IconKey.png'))
        buttonChangeMK.setIconSize(QSize(30, 30))
        buttonChangeMK.setToolTip("В этом разделе Вы <b>поменяете</b> мастер-пароль на новый")
        buttonChangeMK.setShortcut("Ctrl+3")
        buttonChangeMK.setAutoDefault(True)
        buttonChangeMK.clicked.connect(lambda *args: self.display(4))

        buttonChangeNotes = QPushButton("Внести изменения")
        buttonChangeNotes.setFont(self.FontFromButtons)
        buttonChangeNotes.setIcon(QIcon('image\IconDelete.png'))
        buttonChangeNotes.setIconSize(QSize(30, 30))
        buttonChangeNotes.setToolTip("В этом разделе Вы можете удалить любую запись, введя название определённого сайта")
        buttonChangeNotes.setShortcut("Ctrl+4")
        buttonChangeNotes.setAutoDefault(True)
        buttonChangeNotes.clicked.connect(lambda *args: self.display(5))    

        buttonEnds = QPushButton("Выход")
        buttonEnds.setFont(self.FontFromButtons)
        buttonEnds.setIcon(QIcon('image\IconExitWindow.png'))
        buttonEnds.setIconSize(QSize(30, 30))
        buttonEnds.setToolTip("<b>Выйти из программы и сохранить все данные</b>")
        buttonEnds.setAutoDefault(True)
        buttonEnds.setShortcut("Ctrl+C")
        buttonEnds.clicked.connect(lambda *args: self.butEnd_Click())

        layout = QVBoxLayout()
        layout.addWidget(buttonRead)
        layout.addWidget(buttonWrite)
        layout.addWidget(buttonChangeMK)
        layout.addWidget(buttonChangeNotes)
        layout.addWidget(buttonEnds)
        layout.setSpacing(20)
        self.stack1.setLayout(layout)

    def stack2UI(self) -> None:
        """Widget-layout for displaying user notes"""
        layoutForHeading = QHBoxLayout()
        nameSite = QLabel("Название сайта")
        nameSite.setFont(self.FontFromLabels)
        labelLog = QLabel("Логин")
        labelLog.setFont(self.FontFromLabels)
        layoutForHeading.addWidget(labelLog)
        labelPass = QLabel("Пароль")
        labelPass.setFont(self.FontFromLabels)
        layoutForHeading.addWidget(labelPass)
        self.layoutFromRead.addRow(nameSite, layoutForHeading)
        self.stack2.setLayout(self.layoutFromRead)

    def LoadingAndDecrypt(self) -> None:
        """One of two main back-end function. 
    	This function should encoding user notes.
        """
        with open('data.pep', 'rb') as f:
            ciphered = pickle.load(f)
        key = hashlib.sha256(self.password).digest()
        try_aes = AES.new(key, AES.MODE_ECB)
        try_text = try_aes.decrypt(ciphered)
        self.someDict = pickle.loads(try_text)

    def ReadingToDict(self) -> None:
        """This function help displaying user notes with back-end."""
        while 1 < self.layoutFromRead.rowCount():
            self.layoutFromRead.removeRow(1)

        for key, value in self.someDict.items():  
            labelFromKey = QLabel(f"{key}")
            labelFromKey.setFont(self.FontFromNotes)
            loginLine = QLineEdit(f"{value[0]}")
            passwordLine = QLineEdit(f"{value[1]}")
            localplace = QHBoxLayout()
            localplace.addWidget(loginLine)
            localplace.addWidget(passwordLine)
            self.layoutFromRead.addRow(labelFromKey, localplace)

        buttonBack = QPushButton("Назад")
        buttonBack.setFont(self.FontFromButtons)
        buttonBack.setToolTip("<b>Выйти в предыдущий раздел</b>")
        buttonBack.setIcon(QIcon('image\IconBack.png'))
        buttonBack.setIconSize(QSize(30, 30))
        buttonBack.clicked.connect(lambda *args: self.display(1))

        self.layoutFromRead.addWidget(buttonBack)
        self.layoutFromRead.setSpacing(15)

    def stack3UI(self) -> None:
        """Widget-layout that help user add new note."""
        
        buttonBack = QPushButton("Назад")
        buttonBack.setFont(self.FontFromButtons)
        buttonBack.setIcon(QIcon('image\IconBack.png'))
        buttonBack.setIconSize(QSize(30, 30))
        buttonBack.setToolTip("<b>Выйти в предыдущий раздел</b>")
        buttonBack.clicked.connect(lambda *args: self.display(1))

        buttonAdd = QPushButton("Добавить учётную запись")
        buttonAdd.setFont(self.FontFromButtons)
        buttonAdd.setToolTip("При нажатии на кнопку Вы добавите новую запись")
        buttonAdd.clicked.connect(lambda *args: self.WritingToDict())

        labelName = QLabel("Название сайта")
        labelName.setFont(self.FontFromNotes)
        labelLog = QLabel("Логин")
        labelLog.setFont(self.FontFromNotes)
        labelPass = QLabel("Пароль")
        labelPass.setFont(self.FontFromNotes) 

        layout = QFormLayout()
        layout.addRow(labelName, self.addKey)
        layout.addRow(labelLog, self.addLogin)
        layout.addRow(labelPass, self.addPass)
        layout.addWidget(buttonAdd)
        layout.addWidget(buttonBack)
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)
        self.stack3.setLayout(layout)
 
    def WritingToDict(self) -> None:
        """Back-end function, that add new note from 'self.stack3UI()'."""
        if (self.addKey.text() not in self.someDict):
            self.someDict.update({self.addKey.text():[self.addLogin.text(), self.addPass.text()]})
        else:
            self.someDict.update({f"{self.addKey.text()}+{self.addLogin.text()}":[self.addLogin.text(), self.addPass.text()]})
        self.display(1)

    def DumpingAndEncrypt(self) -> None:
        """Second of two main back-end function. 
    	This function should decoding user notes."""
        right_pass = self.password
        right_key = hashlib.sha256(right_pass).digest()
        right_aes = AES.new(right_key, AES.MODE_ECB)
        ciphered = right_aes.encrypt(self.pad(pickle.dumps(self.someDict)))
        with open('data.pep', 'wb') as f:
            pickle.dump(ciphered, f)

    def stack4UI(self) -> None:
        """This widget-layout change password in there."""
        
        buttonBack = QPushButton("Назад")
        buttonBack.setFont(self.FontFromButtons)
        buttonBack.setIcon(QIcon('image\IconBack.png'))
        buttonBack.setIconSize(QSize(30, 30))
        buttonBack.setToolTip("<b>Выйти в предыдущий раздел</b>")
        buttonBack.clicked.connect(lambda *args: self.display(1))

        buttonConfirm = QPushButton("Подтвердить")
        buttonConfirm.setFont(self.FontFromButtons)
        buttonConfirm.setIcon(QIcon('image\IconConfirm.png'))
        buttonConfirm.setIconSize(QSize(30, 30))
        buttonConfirm.clicked.connect(lambda *args: self.Confirm())

        nowPass = QLabel("Текущий пароль")
        nowPass.setFont(self.FontFromNotes)
        contPass = QLabel("Новый пароль")
        contPass.setFont(self.FontFromNotes)

        layout = QFormLayout()
        layout.addRow(nowPass, self.oldPassword)
        layout.addRow(contPass, self.newPassword)
        layout.addWidget(buttonConfirm)
        layout.addWidget(buttonBack)
        layout.setSpacing(30)
        self.stack4.setLayout(layout)

    def Confirm(self) -> None:
        """This back-end function try to change master key. If old password are correctly, that master key change for a new password."""
        if bytes(self.oldPassword.text(), encoding='utf8') == self.password:
            self.password = bytes(self.newPassword.text(), encoding='utf8')
            self.display(1)
        else:
            b = QMessageBox(2, "Предупреждение!", "Вы написали неверный мастер-пароль", buttons=QMessageBox.Ok)
            result = b.exec_()

    def stack5UI(self) -> None:
        """This widget-layout must be like a editor for a user notes, but now this function only know how delete some note. That's all."""
        buttonBack = QPushButton("Назад")
        buttonBack.setFont(self.FontFromButtons)
        buttonBack.setIcon(QIcon('image\IconBack.png'))
        buttonBack.setIconSize(QSize(30, 30))
        buttonBack.setToolTip("<b>Выйти в предыдущий раздел</b>")
        buttonBack.clicked.connect(lambda *args: self.display(1))
        
        fieldDelNote = QLineEdit()
        butDelNote = QPushButton("Удалить запись")
        butDelNote.setIcon(QIcon('image\IconDelete.png'))
        butDelNote.setIconSize(QSize(30, 30))
        butDelNote.setFont(self.FontFromButtons)
        butDelNote.clicked.connect(lambda *args: self.deleteNote(fieldDelNote.text()))
        layoutDeleteNote = QHBoxLayout()
        layoutDeleteNote.addWidget(butDelNote)
        layoutDeleteNote.addWidget(fieldDelNote)

        layout = QVBoxLayout()
        layout.addLayout(layoutDeleteNote)
        layout.addWidget(buttonBack)
        self.stack5.setLayout(layout)

    def deleteNote(self, key: str) -> None:
        """Back-end function for deleting note."""
        if key and key in self.someDict:
            self.display(1)
            del self.someDict[key]
        else:
        	b = QMessageBox(2, "Предупреждение!", "Вы указали неверное название сайта. Проверьте правильность введённых данных", buttons = QMessageBox.Ok)
        	result = b.exec_()
    		
    def display(self, i: int) -> None:
        """This back-end function help to navigate through the window."""
        self.Stack.setCurrentIndex(i)
        if (i == 2): self.ReadingToDict()

    def pad(self, text: bytes) -> bytes:
        """Some function, that help a some string object be a bytes object multiple of 32."""
        while len(text) % 32 != 0:
            text += b' '
        return text

    def closeEvent(self, event) -> None:
    	if (self.Stack.currentIndex() != 0):
    		close = QMessageBox.question(self, "Выход из приложения", "Вы хотите сохранить данные перед выходом?", QMessageBox.Yes | QMessageBox.No)
    		if close == QMessageBox.Yes:
    			self.DumpingAndEncrypt()
    		else:
    			event.accept()

    def turnBack(self) -> None:
    	"""Function from shortkey Escape helps move to the main window."""
    	if (self.Stack.currentIndex() != 0) and (self.Stack.currentIndex() != 1):
    		self.display(1)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Window()
    sys.exit(app.exec_())