from PySide6.QtWidgets import QMainWindow
from PySide6.QtWidgets import QMainWindow,\
                                QPushButton,QVBoxLayout,\
                                QWidget
from libs.windows import embedding as emb
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('uSearch by Junting')
        self.setGeometry(150,100,300,400) #left, top, width, height

        layout = QVBoxLayout()
        #button for embedding
        b_embd = QPushButton('Create embedding')
        b_embd.clicked.connect(self.embd_click)
        #button for semantic search
        b_search = QPushButton('Semantic Search')
        #button for QnA bot
        b_qna = QPushButton('QnA Bot')
        #button for close
        b_close = QPushButton('Quit')

        layout.addWidget(b_embd)
        layout.addWidget(b_search)
        layout.addWidget(b_qna)
        layout.addWidget(b_close)
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
    def embd_click(self):
        global emb_w 
        emb_w = emb.EmbeddingWidget(self)
        emb_w.show()
        self.hide()
    def search_click(self):
        print('create semantic search place holder')
    def qna_click(self):
        print('create qna bot place holder')
    def close_click(self):
        print('close app place holder')