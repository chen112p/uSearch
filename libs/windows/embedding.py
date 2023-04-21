from PySide6.QtWidgets import QApplication,QWidget,QPushButton,QGridLayout,\
                        QTableWidget,QTableWidgetItem,\
                        QHeaderView,QFileDialog
from PySide6.QtGui import QColor
from PySide6.QtCore import Qt
import os,pickle,time
from libs.windows import search,question_answer
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
            self.setColor(value,value_item)
            row += 1
        self.setHorizontalHeaderLabels(horHeaders)
    def setColor(self,value,value_item):
        #for creating embeddings
        if value == 'Pending':
            value_item.setForeground(QColor(Qt.magenta))
        elif value == 'Creating':
            value_item.setForeground(QColor(Qt.blue))
        elif value == 'Saved':
            value_item.setForeground(QColor(Qt.green))
        #for loading embeddings
        elif value == 'Loaded':
            value_item.setForeground(QColor(Qt.blue))
        #shared colors
        elif value == 'Failed':
            value_item.setForeground(QColor(Qt.red))

class EmbeddingWidget(QWidget):
    def __init__(self,MainWindow):
        super().__init__()
        self.main_windows = MainWindow
        self.setWindowTitle('uSearch - Create Embeddings')
        self.setGeometry(400,100,500,500)
        self.layout = QGridLayout()
        #initialize loaded files and the table
        self.f_all = {}
        self.t_fileload = TableView(self.f_all)
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
        #add buttons to layout
        self.layout.addWidget(b_load,0,0)
        self.layout.addWidget(b_create, 1, 0)
        self.layout.addWidget(b_refresh, 4,2)
        self.layout.addWidget(b_back, 4,3)
        #add the table block to layout
        self.layout.addWidget(self.t_fileload, 0,1,3,3)
        self.setLayout(self.layout)
    def __load_file(self):
        file_paths, _ = QFileDialog.getOpenFileNames(self, 'Open Files', '', 'PDF files (*.pdf);;All files (*.*)')
        for i_f, fp in enumerate(file_paths):
            self.f_all[fp] = 'Pending'
        self.__refresh()
    def __refresh(self):
        self.t_fileload.clearContents()
        self.t_fileload.setRowCount(len(self.f_all))
        #self.t_fileload.setColumnCount(2)
        row = 0
        for key, value in self.f_all.items():
            key_item = QTableWidgetItem(key)
            value_item = QTableWidgetItem(str(value))
            self.t_fileload.setItem(row, 0, key_item)
            self.t_fileload.setItem(row, 1, value_item)
            self.t_fileload.setColor(value,value_item)
            row += 1       
        self.layout.update()
        QApplication.processEvents()
    def __back(self):
        self.close()
        self.main_windows.show()
    def __create_embeddings(self):
        from langchain.document_loaders import PyPDFLoader
        from langchain.text_splitter import RecursiveCharacterTextSplitter
        from langchain.vectorstores import FAISS
        from langchain.embeddings.openai import OpenAIEmbeddings
        for i_fp,fp in enumerate(self.f_all.keys()):
            fname,fext = os.path.splitext(os.path.split(fp)[-1])
            #try:
                #load pdf (assuming all files are pdf)
            pdf_loader = PyPDFLoader(fp)
            doc = pdf_loader.load()
            #split pdf into hard coded ~500 words a chunck
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0,length_function = len_)
            texts = text_splitter.split_documents(doc)
            #create embedded text chunks
            embeddings = OpenAIEmbeddings(model='text-embedding-ada-002')
            doc_emb = FAISS.from_documents(texts,embeddings)
            embedding_path = os.path.join('saved_embeddings')
            if os.path.exists(embedding_path)!= True:
                os.makedirs(embedding_path)
            with open(os.path.join(embedding_path,fname+'.usc'), 'wb') as f:
                pickle.dump(doc_emb, f)
            self.f_all[fp] = 'Saved'
            self.__refresh()
            #except:
            #    self.f_all[fp] = 'Failed'
            #    self.__refresh() 
class LoadEmbeddingWidget(QWidget):
    def __init__(self,MainWindow,next_):
        #next parameter tells whether the next step is a semantic search or qna bot
        self.next_ = next_
        super().__init__()
        self.main_windows = MainWindow
        self.setWindowTitle('uSearch - Load Embeddings')
        self.setGeometry(400,100,500,500)
        self.layout = QGridLayout()
        #initialize loaded file names
        self.f_all = {}
        self.t_fileload = TableView(self.f_all)
        self.__refresh()
        #add files
        b_add = QPushButton('Add embedded files')
        b_add.clicked.connect(self.__add)
        #clear all button
        b_clear = QPushButton('Clear all')
        b_clear.clicked.connect(self.__clear)
        #search button
        if self.next_ =='semantic_search':
            b_search_txt = 'Search'
        elif self.next_ =='qna':
            b_search_txt = 'QnA'
        b_search = QPushButton(b_search_txt)
        b_search.clicked.connect(self.__search)
        #back button
        b_back = QPushButton('Back')
        b_back.clicked.connect(self.__back)

        self.layout.addWidget(b_add,0,0)
        self.layout.addWidget(b_clear, 1, 0)
        self.layout.addWidget(b_search, 4, 2)
        self.layout.addWidget(b_back, 4,3)
        #add the table block to layout
        self.layout.addWidget(self.t_fileload, 0,1,4,3)
        self.setLayout(self.layout)
    def __add(self):
        file_paths, _ = QFileDialog.getOpenFileNames(self, 'Open Files', '', 'USC files (*.usc);;All files (*.*)')
        for i_f, fp in enumerate(file_paths):
            self.f_all[fp] = {'obj': None, 'status': 'Pending'}
            self.__refresh()
        for i_f, fp in enumerate(file_paths):
            try:
                with open(fp, 'rb') as f:
                    self.f_all[fp] = {'obj': pickle.load(f), 'status': 'Loaded'}
            except:
                self.f_all[fp] = {'obj': pickle.load(f), 'status': 'Error'}
            self.__refresh()
    def __clear(self):
        self.f_all = {}
        self.__refresh()
    def __search(self):
        if self.next_ =='semantic_search':
            global semsearch_w 
            semsearch_w = search.SemanticSearchWidget(self)
            semsearch_w.show()
            self.hide()
        elif self.next_ == 'qna':
            global qna_bot
            qna_bot = question_answer.QnAWidget(self)
            qna_bot.show()
            self.hide()
    def __back(self):
        self.close()
        self.main_windows.show()
    def __refresh(self):
        self.t_fileload.setRowCount(len(self.f_all))
        self.t_fileload.setColumnCount(2)
        row = 0
        for key, value in self.f_all.items():
            key_item = QTableWidgetItem(key)
            value_item = QTableWidgetItem(str(value['status']))
            self.t_fileload.setItem(row, 0, key_item)
            self.t_fileload.setItem(row, 1, value_item)
            self.t_fileload.setColor(value['status'],value_item)
            row += 1       
        self.t_fileload.viewport().update()
        self.layout.update()
        QApplication.processEvents()