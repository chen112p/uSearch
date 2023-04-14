from langchain.document_loaders import PyPDFLoader

import os
pdf_loader = PyPDFLoader(os.path.join('test_samples','Wind_Load_Characteristics_of_Twin-Tower.pdf'))
doc = pdf_loader.load()
print(doc)