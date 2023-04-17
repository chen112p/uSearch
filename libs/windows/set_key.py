from PySide6.QtWidgets import QMessageBox,QGridLayout,\
                                QPushButton,QLineEdit,QDialog
class KeyInputDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setWindowTitle("uSearch - Enter OpenAI API key")
        self.setGeometry(400,100,500,100)
        self.layout = QGridLayout()
        #self.l_instruction = QLabel('API key')
        self.lineEdit = QLineEdit()
        self.lineEdit.returnPressed.connect(self.__ok)
        self.ok_button = QPushButton("OK")
        self.ok_button.clicked.connect(self.__ok)
        self.save_default_button = QPushButton("Save as Default")
        self.save_default_button.clicked.connect(self.__save_default)
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.__cancel)
        
        self.layout.addWidget(self.lineEdit,0,0,1,3)
        self.layout.addWidget(self.ok_button,1,0)
        self.layout.addWidget(self.save_default_button,1,1)
        self.layout.addWidget(self.cancel_button,1,2)
        self.setLayout(self.layout)
    def __save_default(self):
        import tempfile,os
        file_path = os.path.join(tempfile.gettempdir(),'.uSearch.key')
        with open(file_path,'w') as f:
            f.write(self.lineEdit.text())
            f.close()
        with open('.keypath','w') as f:
            f.write(file_path)
            f.close()
        self.__confirm(file_path)
        self.__ok()
    def __ok(self):
        import openai
        openai.api_key = self.lineEdit.text()
        self.parent.check_key()
        self.close()
    def __cancel(self):
        self.close()
    def __confirm(self,temp_path):
        fs_message = QMessageBox()
        fs_message.setIcon(QMessageBox.Information)
        fs_message.setText('Accepted: API key is saved as:\n"{}"!'.format(temp_path))
        fs_message.setWindowTitle("Default API key")
        fs_message.exec_()