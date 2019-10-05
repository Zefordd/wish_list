import sys

from PyQt5 import QtCore, QtWidgets

import DatabaseUtils


class Ui_MainWindow(QtWidgets.QMainWindow):
    def __init__(self, database, tableName):
        QtWidgets.QWidget.__init__(self)
        self.dbu = DatabaseUtils.DatabaseUtils(database, tableName)
        self.setupUi(self)
        self.load_data()
        self.resize_table()
        

    def load_data(self):
        columns = self.dbu.get_columns()
        table = self.dbu.get_table()
        col_names = [c[0] for c in columns[1:]]

        self.tableWidget.setHorizontalHeaderLabels(col_names)
        self.tableWidget.setRowCount(len(table))

        for row_num, row_data in enumerate(table):
            for col_num, item in enumerate(row_data[1:]):  # ignore id column
                self.tableWidget.setItem(row_num, col_num, 
                                         QtWidgets.QTableWidgetItem(str(item)))

        
    def resize_table(self):
        header = self.tableWidget.horizontalHeader()  
        header.setSectionResizeMode(1)


    def add_row(self):  # TODO: add exeption when price not float
        name = self.name.text()
        price = self.price.text()
        description = self.description.text()
        link = self.link.text()
        self.dbu.add_entry(name, price, description, link)
        self.load_data()


    def delete_row(self):  # TODO: row_num must be int
        row_num = int(self.RowToDel.text()) - 1
        row_id = self.dbu.get_table()[row_num][0]
        self.dbu.delete_entry(row_id)
        self.load_data()


    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(868, 669)
        self.widget = QtWidgets.QWidget(Form)
        self.widget.setGeometry(QtCore.QRect(150, 90, 556, 284))
        self.widget.setObjectName("widget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.name = QtWidgets.QLineEdit(self.widget)
        self.name.setObjectName("name")
        self.horizontalLayout.addWidget(self.name)
        self.price = QtWidgets.QLineEdit(self.widget)
        self.price.setObjectName("price")
        self.horizontalLayout.addWidget(self.price)
        self.description = QtWidgets.QLineEdit(self.widget)
        self.description.setObjectName("description")
        self.horizontalLayout.addWidget(self.description)
        self.link = QtWidgets.QLineEdit(self.widget)
        self.link.setObjectName("link")
        self.horizontalLayout.addWidget(self.link)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.AddRow = QtWidgets.QPushButton(self.widget)
        self.AddRow.setObjectName("AddRow")
        self.verticalLayout.addWidget(self.AddRow)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.tableWidget = QtWidgets.QTableWidget(self.widget)
        self.tableWidget.setMaximumSize(QtCore.QSize(554, 192))
        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setObjectName("tableWidget")
        self.verticalLayout_2.addWidget(self.tableWidget)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.DelLineBtn = QtWidgets.QPushButton(self.widget)
        self.DelLineBtn.setObjectName("DelLineBtn")
        self.horizontalLayout_2.addWidget(self.DelLineBtn)
        self.RowToDel = QtWidgets.QLineEdit(self.widget)
        self.RowToDel.setObjectName("RowToDel")
        self.horizontalLayout_2.addWidget(self.RowToDel)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.price.raise_()
        self.description.raise_()
        self.link.raise_()
        self.tableWidget.raise_()
        self.tableWidget.raise_()
        self.tableWidget.raise_()
        self.RowToDel.raise_()
        self.tableWidget.raise_()

        self.AddRow.clicked.connect(self.add_row)
        self.DelLineBtn.clicked.connect(self.delete_row)

        quit = QtWidgets.QAction("Quit", self)
        quit.triggered.connect(self.close)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)


    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.AddRow.setText(_translate("Form", "Add Wish"))
        self.DelLineBtn.setText(_translate("Form", "Delete line number"))


    def closeEvent(self, event):
        self.dbu.on_close()


if __name__ == '__main__':
    db = 'wish_list'
    tableName = 'wish_list'
    
    app = QtWidgets.QApplication(sys.argv)
    myapp = Ui_MainWindow(db, tableName)
    myapp.show()
    sys.exit(app.exec_())
