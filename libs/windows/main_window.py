from PySide6.QtWidgets import QMainWindow
from PySide6.QtWidgets import QMainWindow,\
                                QPushButton,QGridLayout,\
                                QWidget,QLineEdit,QDialog,QDialogButtonBox,QLabel,QSizePolicy,QMessageBox
from PySide6.QtCore import Qt
from libs.windows import embedding,set_key

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('uSearch by Junting')
        self.setGeometry(150,100,300,400) #left, top, width, height
        self.key_valid = False
        #text shows if key is valid or not
        self.l_key = QLabel('')
        self.check_default_key()
        layout = QGridLayout()
        #button for setting key
        b_key = QPushButton('Set API key')
        b_key.clicked.connect(self.set_key)
        #button for embedding
        b_embd = QPushButton('Create embedding')
        b_embd.clicked.connect(self.embd_click)
        #button for semantic search
        b_search = QPushButton('Semantic Search')
        b_search.clicked.connect(self.search_click)
        #button for QnA bot
        b_qna = QPushButton('QnA Bot')
        b_qna.clicked.connect(self.qna_click)
        #button for close
        b_close = QPushButton('Quit')
        b_close.clicked.connect(self.close_click)
        #l_key.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        #l_key.setWordWrap(True)
        self.l_key.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        layout.addWidget(b_key,0,0)
        layout.addWidget(self.l_key,0,1)
        layout.addWidget(b_embd,1,0)
        layout.addWidget(b_search,2,0)
        layout.addWidget(b_qna,3,0)
        layout.addWidget(b_close,4,0)
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
    def embd_click(self):
        if self.key_valid==True:
            global emb_w 
            emb_w = embedding.EmbeddingWidget(self)
            emb_w.show()
            self.hide()
        else:
            self.error_window()
    def search_click(self):
        global lemb_w 
        lemb_w = embedding.LoadEmbeddingWidget(self,'semantic_search')
        lemb_w.show()
        self.hide()
    def qna_click(self):
        global lemb_w 
        lemb_w = embedding.LoadEmbeddingWidget(self,'qna')
        lemb_w.show()
        self.hide()
    def set_key(self):
        # Create a small window with a user input box
        global keyDialog
        keyDialog = set_key.KeyInputDialog(self)
        keyDialog.show()
    def check_default_key(self):
        import openai
        import os
        key_path_path = '.keypath'
        if os.path.exists(key_path_path):
            with open(key_path_path) as f:
                key_path = f.read()
            f.close()
        else:
            #return('Inalid API key.')
            self.l_key.setText('Invalid API key.')
        if os.path.exists(key_path):
            with open(key_path) as f:
                key = f.read()
            f.close()
            openai.api_key = key
        else:
            #return('Inalid API key.')
            self.l_key.setText('Invalid API key.')
        self.check_key()
    def check_key(self):
        import openai
        try:
            openai.Completion.create(engine='ada', prompt="Test")
            self.key_valid = True
            self.l_key.setText('Valid API key.')
            #return('Valid API key.')
        except openai.error.AuthenticationError:
            self.l_key.setText('Invalid API key.')
    def error_window(self):
        error_message = QMessageBox()
        error_message.setIcon(QMessageBox.Critical)
        error_message.setText("Error: API key is not valid!")
        error_message.setWindowTitle("API key Error")
        error_message.exec_()
    def close_click(self):
        self.close()