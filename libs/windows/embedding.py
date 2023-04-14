from PySide6.QtWidgets import QWidget,QPushButton,QGridLayout,\
                        QTableWidget,QTableWidgetItem,\
                        QHeaderView,QFileDialog 
from PySide6.QtGui import QColor
from PySide6.QtCore import Qt
import os
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
os.environ['OPENAI_API_KEY'] = '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'
def len_(text):
    return(len(text.split(' ')))
def sel_key_by_val(dict_, val_):
    return([key for key, value in dict_.items() if val_ == 'a'])
class TableView(QTableWidget):
    def __init__(self,data):
        super().__init__()
        self.data = data
        self.setRowCount(len(data))
        self.setColumnCount(2)
        self.setData()
        header = self.horizontalHeader()       
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        self.resizeRowsToContents()
    def setData(self): 
        horHeaders = ['file name','status']
        row = 0
        for key, value in self.data.items():
            key_item = QTableWidgetItem(key)
            value_item = QTableWidgetItem(str(value))
            self.setItem(row, 0, key_item)
            self.setItem(row, 1, value_item)
            if value == 'Pending':
                value_item.setForeground(QColor(Qt.magenta))
            elif value == 'Creating':
                value_item.setForeground(QColor(Qt.blue))
            elif value == 'Saved':
                value_item.setForeground(QColor(Qt.green))
            elif value == 'Failed':
                value_item.setForeground(QColor(Qt.red))
            row += 1
        self.setHorizontalHeaderLabels(horHeaders)

class EmbeddingWidget(QWidget):
    def __init__(self,MainWindow):
        super().__init__()
        self.main_windows = MainWindow
        self.setWindowTitle('uSearch - Create Embeddings')
        self.setGeometry(400,100,500,500)
        self.layout = QGridLayout()
        #initialize loaded files
        self.f_all = {}
        self.__refresh()
        
        
        #load files (pdf only)
        b_load = QPushButton('Load files')
        b_load.clicked.connect(self.__load_file)
        #create embeddings using openai
        b_create = QPushButton('Create embeddings')
        b_create.clicked.connect(self.__create_embeddings)
        #refresh button
        b_refresh = QPushButton('Refresh')
        b_refresh.clicked.connect(self.__refresh)
        #back button
        b_back = QPushButton('Back')
        b_back.clicked.connect(self.__back)

        self.layout.addWidget(b_load,0,0)
        self.layout.addWidget(b_create, 1, 0)
        #self.layout.addWidget(b_save, 2,0)
       
        self.layout.addWidget(b_refresh, 2,2)
        self.layout.addWidget(b_back, 2,3)
        self.setLayout(self.layout)
    def __load_file(self):
        def open_file_dialog():
            # create a file dialog and get the selected file paths
            file_paths, _ = QFileDialog.getOpenFileNames(self, 'Open Files', '', 'Text files (*.pdf);;All files (*.*)')
            return(file_paths)
        file_paths = open_file_dialog()
        for i_f, fp in enumerate(file_paths):
            self.f_all[fp] = 'Pending'
        self.__refresh()
    def __refresh(self):
        self.layout.addWidget(TableView(self.f_all), 0,1,2,3)
    def __back(self):
        self.close()
        self.main_windows.show()
    def __create_embeddings(self):
        for i_fp,fp in enumerate(self.f_all.keys()):
            self.f_all[fp] = 'Creating'
            self.__refresh()
            pdf_path = fp
            fname,fext = os.path.splitext(os.path.split(pdf_path)[-1])
            try:
                #load pdf (assuming all files are pdf)
                pdf_loader = PyPDFLoader(pdf_path)
                doc = pdf_loader.load()
                #split pdf into hard coded ~500 words a chunck
                text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0,length_function = len_)
                texts = text_splitter.split_documents(doc)

                #create embedded text chunks
                embeddings = OpenAIEmbeddings(model='text-embedding-ada-002')
                doc_emb = FAISS.from_documents(texts,embeddings)
                embedding_path = os.path.join('saved_embeddings',fname)
                if os.path.exists(embedding_path)!= True:
                    os.makedirs(embedding_path)
                else:
                    import shutil
                    shutil.rmtree(embedding_path)
                doc_emb.save_local(embedding_path)
                self.f_all[fp] = 'Saved'
                self.__refresh()
            except:
                self.f_all[fp] = 'Failed'
                self.__refresh()
    