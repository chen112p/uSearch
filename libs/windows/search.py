from PySide6.QtWidgets import QWidget,QPushButton,QGridLayout,\
                        QTableWidget,QTableWidgetItem,\
                        QHeaderView,QLineEdit,QLabel,QApplication
from PySide6.QtGui import QIntValidator

from PySide6.QtCore import Qt
class SearchResultTable(QTableWidget):
    def __init__(self,data):
        super().__init__()
        self.data = data
        self.setRowCount(len(data))
        self.setColumnCount(4)
        self.setData()
        header = self.horizontalHeader()       
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
        self.resizeRowsToContents()
    def setData(self): 
        horHeaders = ['Score','file name','page', 'Text']
        row = 0
        self.setHorizontalHeaderLabels(horHeaders)

    
class SemanticSearchWidget(QWidget):
    def __init__(self,embd_window):
        super().__init__()
        self.embd_window = embd_window
        self.setWindowTitle('uSearch - Load Embeddings')
        self.setGeometry(400,100,1200,500)
        self.layout = QGridLayout()
        #initialize result
        self.search_result = {}
        #user input
        l_textbox = QLabel('Query:')
        self.tb_textbox = QLineEdit()
        self.tb_textbox.returnPressed.connect(self.__go)
        #Go button
        b_go = QPushButton('Go')
        b_go.clicked.connect(self.__go)
        #ask user to input number of results expected (default value 4)
        l_num_result = QLabel('# of result:')
        self.tb_num_result = QLineEdit()
        self.tb_num_result.setText('4')
        self.tb_num_result.setValidator(QIntValidator())
        self.tb_num_result.returnPressed.connect(self.__go)
        self.tb_num_result.setFixedWidth(50)
        #Back button
        b_back = QPushButton('Back')
        b_back.clicked.connect(self.__back)
        self.t_search = SearchResultTable(self.search_result)
        #add user input box
        self.layout.addWidget(l_textbox,0,0)
        self.layout.addWidget(self.tb_textbox,1,0,1,8)
        #add number of results
        self.layout.addWidget(l_num_result,0,9)
        self.layout.addWidget(self.tb_num_result,1,9)
        #add buttons to layout
        self.layout.addWidget(b_go,1,8)
        self.layout.addWidget(b_back,14,9)
        #add the table block to layout
        self.layout.addWidget(self.t_search, 2,0,12,10)
        self.setLayout(self.layout)
    def __go(self):
        user_input = self.tb_textbox.text()
        num_result = int(self.tb_num_result.text())
        #unpack embeddings from the dictionary
        for i_f,fn in enumerate(self.embd_window.f_all.keys()): 
            if i_f == 0:
                docs_emb = self.embd_window.f_all[fn]['obj']
            else:
                docs_emb.merge_from(self.embd_window.f_all[fn]['obj'])
        #print(len(docs_emb.docstore._dict.keys()))
        #search and get score
        matches = docs_emb.similarity_search_with_score(user_input,k=num_result) 
        for i_m, match in enumerate(matches):
            self.search_result[i_m+1] = {'score': str(match[1].round(4)),
                                        'source': match[0].metadata['source'],
                                        'page_number': str(match[0].metadata['page']),
                                        'text': match[0].page_content.replace('\n',' ')}
        self.__refresh()
    def __back(self):
        self.close()
        self.embd_window.show()
    def __refresh(self):
        self.t_search.setRowCount(len(self.search_result))
        self.t_search.setColumnCount(4)
        row = 0
        for i_v, value in enumerate(self.search_result.values()):
            score_item = QTableWidgetItem(value['score'])
            source_item = QTableWidgetItem(value['source'])
            page_item = QTableWidgetItem(value['page_number'])
            fn_item = QTableWidgetItem(value['text'])
            self.t_search.setItem(row, 0, score_item)
            self.t_search.setItem(row, 1, source_item)
            self.t_search.setItem(row, 2, page_item)
            self.t_search.setItem(row, 3, fn_item)

            score_item.setTextAlignment(Qt.AlignCenter)
            source_item.setTextAlignment(Qt.AlignCenter)
            page_item.setTextAlignment(Qt.AlignCenter)

            row += 1       
        self.t_search.viewport().update()
        self.layout.update()
        QApplication.processEvents()