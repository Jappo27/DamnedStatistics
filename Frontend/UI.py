import time
from PyQt5.QtWidgets import (
    QApplication, QGridLayout, QScrollArea, QVBoxLayout,
    QWidget, QPushButton, QMessageBox, QFileDialog, QMenu,
    QTabWidget, QTableWidget, QTableWidgetItem, QHeaderView,
    QTextEdit, QSizePolicy, QAbstractItemView, QLineEdit, QLabel
)
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QFile, QTextStream
#https://ai.google.dev/gemini-api/docs/quickstart?lang=python
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QObject, QThread
from PyQt5 import QtGui
import os
from sys import path
path.append("Backend")
from backend import backend
import threading
from google import genai

from PyQt5.QtCore import QThread, pyqtSignal

class ResponseThread(QThread):
    response_received = pyqtSignal(str)

    def __init__(self, prompt, key):
        super().__init__()
        self.prompt = prompt
        self.key = key

    def run(self):
        try:
            if self.prompt and self.key:
                client = genai.Client(api_key=self.key)
                response = client.models.generate_content(
                    model="gemini-2.0-flash", contents=self.prompt
                )
                with open("output/response.txt", 'w') as f:
                    f.write(response.text)
                self.response_received.emit(response.text)
        except Exception as e:
            self.response_received.emit(f"There was an error: {str(e)}")

    def genResponse(self, Base, GeminiAPIKey):
        if self.ResponsePop:
            self.ResponsePop.close()
        
        self.thread = ResponseThread(Base.Prompt.toPlainText(), GeminiAPIKey.text())
        self.thread.response_received.connect(self.getReponse)
        self.thread.start()

    def getReponse(self, response):
        try:
            self.ResponsePop = AnotherWindow(response)
        except Exception as e:
            self.create_message(f"There was an error: {str(e)}")

class ComboBoxState(QObject):
    def __init__(self):
        super().__init__()
        self.items = []  # This stores the objects in the combo box
        self.selected = None  # Currently selected object

    def add_item(self, Name):
        """Add an item and its display name."""
        self.items.append(Name)

    def remove_item(self, Name):
        """Remove an item and its display name."""
        self.items.remove(Name)

    def update_selected(self, index):
        """Update the currently selected object."""
        if 0 <= index < len(self.items):  # Ensure valid index
            self.selected_index = index

    def count(self):
        """Return the number of items."""
        return len(self.items)
    
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QScrollArea
from PyQt5 import QtGui

class AnotherWindow(QWidget):
    """
    This "window" is a QWidget. If it has no parent, it
    will appear as a free-floating window as we want.
    """
    def __init__(self, text):
        super().__init__()
        self.setWindowTitle(" ")
        self.setWindowIcon(QtGui.QIcon('Graph.jpg'))
        layout = QVBoxLayout()
        
        # Create scroll area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        # Create content widget
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        self.label = QLabel("Another Window")
        self.label.setText(text)

        content_layout.addWidget(self.label)
        scroll_area.setWidget(content_widget)
        layout.addWidget(scroll_area)
        self.setLayout(layout)
        self.show()

class HomePage(QWidget):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self.setWindowTitle("Damned Statistics")
        self.setWindowIcon(QtGui.QIcon('Graph.jpg'))
        self.resize(1350, 700)
        self.files = ComboBoxState()
        self.ResponsePop = None
        self.resetResponse()
        
        #NavBar
        NavBar = QTabWidget()
        # NAVBAR: Add all other tabs first
        Base = BasePage()
        NavBar.addTab(Base, "Base")

        # StatusBar
        StatusBar = QScrollArea()
        StatusBar.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        content_widget = QWidget()
        ScrollLayout = QVBoxLayout(content_widget)
        ScrollLayout.setAlignment(Qt.AlignTop)
        StatusBar.setWidget(content_widget)
        StatusBar.setWidgetResizable(True)
        StatusBar.setStyleSheet("QScrollArea { border: 1px solid black; }")

        # Adding Buttons
        Import = QPushButton('Import file', self)
        Delete = QPushButton('Delete file', self)
        
        Import.clicked.connect(lambda: self.addFile(ScrollLayout, NavBar))
        Delete.clicked.connect(lambda: self.removeFile(ScrollLayout, NavBar))
        ScrollLayout.addWidget(Import)
        ScrollLayout.addWidget(Delete)

        #Tablebar
        TableWidget = QWidget()
        TableButtons = QVBoxLayout(TableWidget)
        TableButtons.setAlignment(Qt.AlignTop)
        GeminiAPIKey = QLineEdit("", self)
        TableAddR = QPushButton('Add Row', self)
        TableAddC = QPushButton('Add Column', self)
        TableDelR = QPushButton('Delete Row', self)
        TableDelC = QPushButton('Delete Column', self)
        TableExport = QPushButton('Export Table', self)
        DataExport = QPushButton('Add Selected data to Prompt', self)
        ExportResponse = QPushButton('Export Response', self)

        GeminiAPIKey.setPlaceholderText("Gemini API Key")
        self.getKey(GeminiAPIKey)
        GeminiAPIKey.editingFinished.connect(lambda: self.writeKey(GeminiAPIKey))

        TableAddR.clicked.connect(lambda: NavBar.widget(NavBar.currentIndex()).addRow())
        TableAddC.clicked.connect(lambda: NavBar.widget(NavBar.currentIndex()).addColumn())
        TableDelR.clicked.connect(lambda: NavBar.widget(NavBar.currentIndex()).deleteRow())
        TableDelC.clicked.connect(lambda: NavBar.widget(NavBar.currentIndex()).deleteColumn())
        DataExport.clicked.connect(lambda: NavBar.widget(NavBar.currentIndex()).addData(Base.Prompt))

        ExportResponse.clicked.connect(lambda: self.export_Response())
        TableExport.clicked.connect(lambda: self.export_Table(NavBar.widget(NavBar.currentIndex()).keys, NavBar.widget(NavBar.currentIndex()).values))

        Base.Run.clicked.connect(lambda: self.genResponse(Base, GeminiAPIKey))

        TableButtons.addWidget(GeminiAPIKey, 0)
        TableButtons.addWidget(ExportResponse, 1)
        TableButtons.addWidget(TableAddR, 2)
        TableButtons.addWidget(TableAddC, 3)
        TableButtons.addWidget(TableDelR, 4)
        TableButtons.addWidget(TableDelC, 5)
        TableButtons.addWidget(TableExport, 6)
        TableButtons.addWidget(DataExport, 7)

        for i in range(2, TableButtons.count()):
            TableButtons.itemAt(i).widget().setVisible(False)

        NavBar.currentChanged.connect(lambda: self.Indexchanged(NavBar, TableButtons))

        # Layout of Main Page
        main_layout = QGridLayout(self)
        main_layout.addWidget(StatusBar, 1, 0, 2, 2)
        main_layout.addWidget(NavBar, 1, 2, 1, 8)
        main_layout.addWidget(TableWidget, 1, 10, 1, 2)
        self.setLayout(main_layout)
    
    def resetResponse(self):
        with open("output/response.txt", 'w') as f:
            f.write("")
        
    def getKey(self, field):
        with open("Backend/key.txt", 'r') as f:
            if f:
                field.setText(f.read())

    def writeKey(self, field):
        with open("Backend/key.txt", 'w') as f:
            f.write(field.text())

    def genResponse(self, Base, GeminiAPIKey):
        if self.ResponsePop:
            self.ResponsePop.close()
        self.thread = ResponseThread(Base.Prompt.toPlainText(), GeminiAPIKey.text())
        self.thread.response_received.connect(self.getReponse)
        self.thread.start()
    
    def getReponse(self):
        try: 
            with open("output/response.txt", 'r') as f:
                response = f.read() 
            self.ResponsePop = AnotherWindow(response)
        except Exception as e:
            self.create_message(f"There was an error: {str(e)}")

    def Indexchanged(self, Navbar, TableButtons):
        if Navbar.currentIndex() != 0:
            for i in range(2, TableButtons.count()):
                TableButtons.itemAt(i).widget().setVisible(True)
            TableButtons.itemAt(1).widget().setVisible(False)
        else:
            for i in range(2, TableButtons.count()):
                TableButtons.itemAt(i).widget().setVisible(False)
            TableButtons.itemAt(1).widget().setVisible(True)

    def export_Response(self):
        try:
            export_path = QFileDialog.getExistingDirectory(self, "Select Folder")

            if export_path:
                file_name = "response.txt"
                file_path = os.path.join(export_path, file_name)

                with open(file_path, "w") as export_file:
                    with open("output/response.txt", "r") as response_file:
                        export_file.write(str(response_file.read()))

                self.create_message(f"File successfully saved to: {file_path}")

        except Exception as e:
            self.create_message(f"There was an error: {str(e)}")


    def export_Table(self, keys, data):
        line = f""
        for header in keys:
            line += f"{header},"
        line = line[:-1]
        line = f"{line}\n"

        row = f""
        for record in data:
            for value in record:
                row += f"{value},"
            row = row[:-1]
            row = f"{row}\n"

        try:
            export_path = QFileDialog.getExistingDirectory(self, "Select Folder")

            if export_path:
                file_name = "output.csv"
                file_path = os.path.join(export_path, file_name)

                with open(file_path, "w") as export_file:
                    export_file.write(str(line))
                    export_file.write(str(row))

                self.create_message(f"File successfully saved to: {file_path}")

        except Exception as e:
            self.create_message(f"There was an error: {str(e)}")

    def addMenu(self, button):
        """Add a menu with options."""
        menu = QMenu()
        incexc = menu.addAction("Option 1")
        ground = menu.addAction("Option 2")
                                
        incexc.setCheckable(True)
        incexc.setChecked(True)
        ground.setCheckable(True)
                                
        button.setMenu(menu)
        
    def addCSV(self, path, ScrollLayout, NavBar):
        """Add a CSV file button to the layout."""
        button = QPushButton(f"File: {os.path.basename(path)}")
        #self.addMenu(button)
        NavBar.insertTab(self.files.count()+1, Page(path), f"{os.path.basename(path)}")
        ScrollLayout.addWidget(button)
        self.storeCSV(path)
        
    def storeCSV(self, path):
        Name = os.path.basename(os.path.normpath(path))
        self.files.add_item(Name)

    def create_message_box(self, box_text, buttons):
        """Modular function to create a QMessageBox."""
        message_box = QMessageBox()
        message_box.setWindowTitle(" ")
        message_box.setWindowIcon(QtGui.QIcon('Graph.jpg'))
        message_box.setText(box_text)
        
        button_objects = {}
        for label, role in buttons:
            button = message_box.addButton(label, role)
            button_objects[label] = button
        
        message_box.exec()
        return message_box.clickedButton(), button_objects
    
    def create_message(self, box_text):
        """Modular function to create a QMessageBox."""
        message_box = QMessageBox()
        message_box.setWindowTitle(" ")
        message_box.setWindowIcon(QtGui.QIcon('Graph.jpg'))
        message_box.setText(box_text)

        message_box.exec()
        return

    def addFile(self, ScrollLayout, NavBar):
        """Handle file or folder import."""
        try:
            box_text = "How would you like to import objects?"
            buttons = [
                ("Import Files", QMessageBox.ActionRole),
                ("Folder", QMessageBox.ActionRole),
                ("Cancel", QMessageBox.RejectRole)
            ]

            action, button_objects = self.create_message_box(box_text, buttons)

            # Handle the user's choice
            if action == button_objects["Import Files"]:
                # File import dialog
                paths, _ = QFileDialog.getOpenFileNames(
                    self,
                    'Open files',    # Dialog title
                    'c:\\',          # Initial directory
                    'CSV Files (*.csv)'  # File filter
                )
                if not paths:  # No files selected
                    return

                for path in paths:
                    self.addCSV(path, ScrollLayout, NavBar)
            
            elif action == button_objects["Folder"]:
                # Folder import dialog
                folder_path = QFileDialog.getExistingDirectory(self, 'Select Folder', 'c:\\')
                if not folder_path:  # No folder selected
                    return
                
                supported_extensions = ['.csv']
                
                for root, _, files in os.walk(folder_path):
                    for file in files:
                        if any(file.lower().endswith(ext) for ext in supported_extensions):
                            self.addCSV(os.path.join(root, file), ScrollLayout, NavBar)
                                
        except Exception as e:
            print(f"An error occurred: {e}")
            
    def removeFile(self, ScrollLayout, NavBar):
        try:
            if (not self.files.items):
                warning_text = "Warning"
                warning_msg = "There are no objects to delete."
                return QMessageBox.warning(self, warning_text, warning_msg)

            box_text = "Select an object to remove from below:"
            buttons = []
            
            for key in self.files.items:
                buttons.append((str(key), QMessageBox.ActionRole)) 
            cancel_button = buttons.append(("Cancel", QMessageBox.ActionRole))

            action, button_objects = self.create_message_box(box_text, buttons)
        
            index = 0
            Keyi = None

            for key in self.files.items:
                if action == button_objects[key]:
                    Keyi = key
                    break
                index+=1
            
            element = ScrollLayout.takeAt(index+2).widget() # +2 to account for import / delete
            if element is not None:
                element.deleteLater()
            NavBar.removeTab(index+1) # +1 for base
            self.files.remove_item(Keyi)
            
        except Exception as e:
            print(f"An error occurred: {e}")

class BasePage(QWidget):
    def __init__(self, csv=None, parent: QWidget = None):
        super().__init__(parent)
        
        self.Prompt = QTextEdit(self)
        self.Prompt.setText(" ")
        self.Prompt.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        self.Prompt.setWordWrapMode(QtGui.QTextOption.WrapAtWordBoundaryOrAnywhere)
        self.Prompt.setAlignment(Qt.AlignLeft)
        font = QFont("Arial", 12)  # Set font family and size
        self.Prompt.setFont(font)

        self.Run = QPushButton("Submit", self)
        self.Run.setFixedSize(100, 35)

        self.getPrompt(self.Prompt)

        layout = QVBoxLayout()
        layout.addWidget(self.Prompt, 0)
        self.Prompt.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.Run, 1)
        self.setLayout(layout)

    def getPrompt(self, field):
        with open("Backend/prompt.txt", 'r') as f:
            if f:
                field.setText(f.read())

    def writePrompt(self, field):
        with open("Backend/prompt.txt", 'w') as f:
            f.write(field.text())
            
class Page(QWidget):
    def __init__(self, csv=None, parent: QWidget = None):
        super().__init__(parent)

        if csv:
            self.data = csv
            self.keys, self.values = backend.harvest(self.data)
            self.createTable()
            self.layout = QVBoxLayout()
            self.layout.addWidget(self.tableWidget)
            self.setLayout(self.layout)

    def createTable(self):
        self.tableWidget = QTableWidget()

        self.selected_rows = set()
        self.selected_columns = set()

        self.tableWidget.setRowCount(len(self.values))
        self.tableWidget.setColumnCount(len(self.keys))
        self.tableWidget.setHorizontalHeaderLabels(self.keys)

        self.tableWidget.horizontalHeader().sectionClicked.connect(lambda: self.toggle_column_selection(self.tableWidget.currentColumn()))
        self.tableWidget.verticalHeader().sectionClicked.connect(lambda: self.toggle_row_selection(self.tableWidget.currentRow()))

        self.tableWidget.itemChanged.connect(self.update_values)
        self.tableWidget.horizontalHeader().sectionDoubleClicked.connect(self.changeHorizontalHeader)
        
        for i, row in enumerate(self.values):  
            for j, value in enumerate(row):
                self.tableWidget.setItem(i, j, QTableWidgetItem(value))
                
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    @QtCore.pyqtSlot(int)
    def changeHorizontalHeader(self, index):
        it = self.tableWidget.horizontalHeaderItem(index)
        if it is None:
            val = self.tableWidget.model().headerData(index, QtCore.Qt.Horizontal)
            it = QtWidgets.QTableWidgetItem(str(val))
            self.tableWidget.setHorizontalHeaderItem(index, it)
        oldHeader = it.text()
        newHeader, okPressed  = QtWidgets.QInputDialog.getText(self,
            ' Change header label for column %d', "Your name:", 
            QtWidgets.QLineEdit.Normal, oldHeader)
        if okPressed:
            it.setText(newHeader)
            self.keys[index] = newHeader 

    def update_values(self, item):
        row = item.row()
        col = item.column()
        self.values[row][col] = item.text()
    
    def addRow(self):
        try:
            record = ["" for i in range(self.tableWidget.columnCount())]
            insRow = self.tableWidget.currentRow()
            if insRow == -1:
                insRow = 0
            self.values.insert(insRow, record)
            self.tableWidget.insertRow(insRow)
        except Exception as e:
            print(f"An error occurred: {e}")
    
    def addColumn(self):
        try:
            insCol = self.tableWidget.currentColumn() 
            if insCol == -1:
                insCol = 0
            for i in range(len(self.values)):
                self.values[i].insert(insCol, "")
            self.tableWidget.insertColumn(insCol)
        except Exception as e:
            print(f"An error occurred: {e}")

    def deleteRow(self):
        try:
            if self.tableWidget.rowCount() != 0:
                delRow = self.tableWidget.currentRow()
                if delRow == -1:
                    delRow = 0
                self.values.pop(delRow)
                self.tableWidget.removeRow(delRow)
        except Exception as e:
            print(f"An error occurred: {e}")
    
    def deleteColumn(self):
        try:
            if self.tableWidget.columnCount() != 0:
                delCol = self.tableWidget.currentColumn()
                if delCol == -1:
                    delCol = 0
                for i in range(len(self.values)):
                    self.values[i].pop(delCol)
                self.tableWidget.removeColumn(delCol)

        except Exception as e:
            print(f"An error occurred: {e}")

    def addData(self, location):
        try:
            data = f"Data: ["
            labels = f"["
            for i in range(self.tableWidget.columnCount()):
                label = self.tableWidget.horizontalHeaderItem(i).text()
                labels = f"{labels}{label},"
            labels = labels[:-1]
            labels =f"{labels}]"
            data = ""

            # Get the number of rows and columns
            row_count = self.tableWidget.rowCount()
            col_count = self.tableWidget.columnCount()

            for row in range(row_count):
                row_data = []
                row_has_selection = False

                for col in range(col_count):
                    item = self.tableWidget.item(row, col)
                    if item:
                        if item.isSelected():
                            row_has_selection = True
                            row_data.append(item.text())
                        else:
                            row_data.append("NI")

                if row_has_selection:
                    data += ",".join(row_data) + "\n"

            data = f"{data[:-1]}]"
            Text = location.toPlainText()
            data = f"\n[Structure: {labels} \n{data}]"
            location.setText(f"{Text} {data}")
        except Exception as e:
            print(f"An error occurred: {e}")

    def select_row(self, row):
        self.selected_rows.add(row)
        self.update_selection()

    def select_column(self, column):
        self.selected_columns.add(column)
        self.update_selection()

    def toggle_row_selection(self, row):
        if row in self.selected_rows:
            self.selected_rows.remove(row)
        else:
            self.selected_rows.add(row)
        self.update_selection()

    def toggle_column_selection(self, column):
        if column in self.selected_columns:
            self.selected_columns.remove(column)
        else:
            self.selected_columns.add(column)

    def update_selection(self):
        self.tableWidget.clearSelection() 
        for row in self.selected_rows:
            for col in range(self.tableWidget.columnCount()):
                item = self.tableWidget.item(row, col)
                if item:
                    item.setSelected(True)
        for col in self.selected_columns:
            for row in range(self.tableWidget.rowCount()):
                item = self.tableWidget.item(row, col)
                if item:
                    item.setSelected(True)


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    file = QFile("Style.qss")  # Ensure the path is correct
    if file.open(QFile.ReadOnly | QFile.Text):
        stream = QTextStream(file)
        app.setStyleSheet(stream.readAll())
    file.close()

    main_window = HomePage()
    main_window.show()
    
    sys.exit(app.exec_())