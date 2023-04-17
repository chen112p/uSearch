from PySide6.QtWidgets import QMainWindow,QWidget,QPushButton,QGridLayout,\
                        QTableView,QLineEdit,QLabel,QApplication,QHeaderView
from PySide6.QtGui import QStandardItemModel,QStandardItem

from PySide6.QtCore import Qt
   
class QnAWidget(QWidget):
    def __init__(self,embd_window):
        super().__init__()
        self.embd_window = embd_window
        self.setWindowTitle('uSearch - QnA bot')
        self.setGeometry(400,100,1200,500)
        self.layout = QGridLayout()
        #initialize semantic search result
        self.search_result = {}
        #user input
        l_textbox = QLabel('Query:')
        self.tb_textbox = QLineEdit()
        self.tb_textbox.returnPressed.connect(self.__go)
        #Go button
        b_go = QPushButton('Go')
        b_go.clicked.connect(self.__go)
        #llm output:
        l_response = QLabel('Response:')
        self.response = ''
        self.l_qna_output = QLabel(self.response)
        self.l_qna_output.setStyleSheet("background-color: white;")
        self.l_qna_output.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.l_qna_output.setWordWrap(True)
        #cost output:
        l_cost_label = QLabel('Cumulative cost:')
        self.curr_cost = 0
        self.l_show_cost = QLabel('${}'.format(self.curr_cost))
        #show reference button
        b_show_ref = QPushButton('Show reference')
        b_show_ref.clicked.connect(self.__show_ref)
        
        #show promt
        #b_show_prompt = QPushButton('Show prompt')
        #b_show_prompt.clicked.connect(self.__show_prompt)
        
        #ask user to input number of results expected (default value 4)
        #l_num_result = QLabel('# of result:')
        #self.tb_num_result = QLineEdit()
        #self.tb_num_result.setText('4')
        #self.tb_num_result.setValidator(QIntValidator())
        #self.tb_num_result.returnPressed.connect(self.__go)
        #self.tb_num_result.setFixedWidth(50)
        
        #Back button
        b_back = QPushButton('Back')
        b_back.clicked.connect(self.__back)
        
        #add user input box
        self.layout.addWidget(l_textbox,0,0)
        self.layout.addWidget(self.tb_textbox,1,0,1,8)
        #add response
        self.layout.addWidget(l_response,2,0)
        self.layout.addWidget(self.l_qna_output,3,0,11,10)

        #add number of results
        #self.layout.addWidget(l_num_result,0,9)
        #self.layout.addWidget(self.tb_num_result,1,9)

        #add cost labels
        self.layout.addWidget(l_cost_label,14,0)
        self.layout.addWidget(self.l_show_cost,14,1)
        #add buttons to layout
        self.layout.addWidget(b_go,1,8)
        #self.layout.addWidget(b_show_prompt,14,7)
        self.layout.addWidget(b_show_ref,14,8)
        self.layout.addWidget(b_back,14,9)
           
        self.setLayout(self.layout)
    def __go(self):
        from langchain.callbacks import get_openai_callback
        from langchain.chains.question_answering import load_qa_chain
        from langchain.chat_models import ChatOpenAI
        from langchain.chains.qa_with_sources import load_qa_with_sources_chain
        user_input = self.tb_textbox.text()
        num_result = 4
        #num_result = int(self.tb_num_result.text())
        #unpack embeddings from the dictionary
        for i_f,fn in enumerate(self.embd_window.f_all.keys()): 
            if i_f == 0:
                docs_emb = self.embd_window.f_all[fn]['obj']
            else:
                docs_emb.merge_from(self.embd_window.f_all[fn]['obj'])
        matches = docs_emb.similarity_search(user_input,k=num_result) 
        for i_m, match in enumerate(matches):
            self.search_result[i_m+1] = {'source': match.metadata['source'],
                                        'page_number': str(match.metadata['page']),
                                        'text': match.page_content.replace('\n',' ')}
        #call openai
        llm = ChatOpenAI(temperature=0,model_name='gpt-3.5-turbo')
        #chain = load_qa_chain(llm, chain_type="stuff", verbose=False)#, return_intermediate_steps=True)
        chain = load_qa_with_sources_chain(llm, chain_type="stuff", verbose=False)#, return_intermediate_steps=True)
        with get_openai_callback() as cb:
            self.response = chain.run(input_documents  = matches , question = user_input, return_only_output=True)
            self.curr_cost += cb.total_cost
        self.__refresh()
    def __show_ref(self):
        global table_window
        table_window = QMainWindow()
        table_window.setGeometry(450,150,1200,500)
        table_window.setWindowTitle("uSearch - Search Table")
        # Create a table view and set its data
        table_view = QTableView()
        model = QStandardItemModel()
        model.setHorizontalHeaderLabels(['File name','page', 'Text'])
        for i_v, value in enumerate(self.search_result.values()):
            curr_row = [QStandardItem(value['source']),
                        QStandardItem(value['page_number']),
                        QStandardItem(value['text'])]
            model.append(curr_row)
        table_view.setModel(model)
        table_view.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        table_window.setCentralWidget(table_view)
        # Show the new window
        table_window.show()
    def __show_prompt(self):
        pass
    def __back(self):
        self.close()
        self.embd_window.show()
    def __refresh(self):
        self.l_qna_output.setText(self.response)
        self.l_show_cost.setText('${}'.format(self.curr_cost))
