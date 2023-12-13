import sqlite3
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QMessageBox, QDialog


class EditDB(QDialog):
    def __init__(self):
        super(EditDB, self).__init__()
        uic.loadUi("addEditCoffeeForm.ui", self)

    def accept(self):
        con = sqlite3.connect('coffee.sqlite')
        cur = con.cursor()
        cur.execute('INSERT INTO coffee(Name, Roasting, Type, Taste, Price, Size) VALUES (?,?,?,?,?,?)',
                    [self.NameLineEdit.text(), self.RoastingLineEdit.text(), self.TypeLineEdit.text(),
                     self.TasteLineEdit.text(), self.PriceLineEdit.text(), self.SizeLineEdit.text()])
        con.commit()
        con.close()


class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        uic.loadUi("main.ui", self)

        con = sqlite3.connect('coffee.sqlite')
        cur = con.cursor()
        cur.execute(f"""SELECT * FROM coffee""")
        db = cur.fetchall()
        self.tableWidget.setColumnCount(len(db[0]) - 1)
        self.tableWidget.setRowCount(len(db))
        self.tableWidget.setHorizontalHeaderLabels(["Name", "Roasting", "Type", "Taste", "Price", "Size"])
        for i, elemi in enumerate(db):
            for j, elemj in enumerate(elemi[1:]):
                self.tableWidget.setItem(i, j, QTableWidgetItem(elemj))
        con.close()

        self.pushButton.clicked.connect(self.up)

    def up(self):
        super(Window, self).__init__()
        uic.loadUi("addEditCoffeeForm.ui", self)
        self.show()

        self.pushButton_2.clicked.connect(self.add)

    def add(self):
        con = sqlite3.connect('coffee.sqlite')
        cur = con.cursor()
        if self.lineEdit.text() and self.lineEdit_2.text() and self.lineEdit_3.text() and self.lineEdit_4.text() and self.lineEdit_5.text() and self.lineEdit_6.text():
            if (self.lineEdit.text(), ) not in cur.execute('SELECT Name FROM coffee').fetchall():
                cur.execute(f"""INSERT INTO coffee(Name, Roasting, Type, Taste, Price, Size) 
                VALUES('{self.lineEdit.text()}', '{self.lineEdit_2.text()}', '{self.lineEdit_3.text()}', 
                '{self.lineEdit_4.text()}', {self.lineEdit_5.text()}, {self.lineEdit_6.text()})""").fetchall()
                con.commit()

            else:
                cur.execute(
                    f"""UPDATE coffee
                        SET Roasting = '{self.lineEdit_2.text()}',
                            Type = '{self.lineEdit_3.text()}',
                            Taste = '{self.lineEdit_4.text()}',
                            Price = {self.lineEdit_5.text()},
                            Size = {self.lineEdit_6.text()}
                        WHERE Name = '{self.lineEdit.text()}'""").fetchall()
                con.commit()
            con = sqlite3.connect('coffee.sqlite')
            cur = con.cursor()
            cur.execute(f"""SELECT * FROM coffee""")
            db = cur.fetchall()
            self.tableWidget.setColumnCount(len(db[0]) - 1)
            self.tableWidget.setRowCount(len(db))
            for i, elemi in enumerate(db):
                for j, elemj in enumerate(elemi[1:]):
                    self.tableWidget.setItem(i, j, QTableWidgetItem(elemj))
            con.close()
        else:
            self.label_8.setText('Заполните все поля')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec())
