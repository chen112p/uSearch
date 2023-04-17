import os
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem
import pickle
class MyWindow(QMainWindow):
    def __init__(self,app):
        super().__init__()
        self.app = app
        # Create a QTableWidget object with 2 columns
        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(2)

        # Set the header data for the table
        self.table_widget.setHorizontalHeaderLabels(["File Name", "Status"])

        # Set the main window widget
        self.setCentralWidget(self.table_widget)

    def load_files(self, file_paths):
        # Add rows to the table for each file path
        for file_path in file_paths:
            row_count = self.table_widget.rowCount()
            self.table_widget.insertRow(row_count)

            # Set the file name in the first column
            file_name_item = QTableWidgetItem(os.path.basename(file_path))
            self.table_widget.setItem(row_count, 0, file_name_item)

            # Set the status to "Loading..." in the second column
            status_item = QTableWidgetItem("Loading...")
            self.table_widget.setItem(row_count, 1, status_item)

            # Refresh the view to show the updated status
            self.table_widget.viewport().update()

            # Load the file (this is just an example, you'll need to replace this with your own code)
            try:
                with open(file_path, 'rb') as f:
                    a = pickle.load(f)
                file_loaded_successfully=True
                print('fdsa')
            except:
                file_loaded_successfully=False
                print('asdf')


            # Update the status to "Loaded" or "Failed" depending on the result
            if file_loaded_successfully:
                status_item.setData(Qt.DisplayRole, "Loaded")
                self.app.processEvents()
            else:
                status_item.setData(Qt.DisplayRole, "Failed")
                self.app.processEvents()

            # Refresh the view to show the updated status
            self.table_widget.viewport().update()

if __name__ == '__main__':
    app = QApplication([])
    window = MyWindow(app)
    window.show()

    # Call the load_files method to load the files and update their status
    file_paths = ["saved_embeddings//Lignarolo et al. - Shape morphing wind-responsive facade systems real.usc", 
                  "saved_embeddings//Principe, Codina, Henke - 2010 - The dissipative structure of vaiational multiscale methods for incompressible flows.usc", 
                   "saved_embeddings//Schatzmann and Britter - 2011 - Quality assurance and improvement of micro-scale m.usc"]
    window.load_files(file_paths)

    app.exec()
