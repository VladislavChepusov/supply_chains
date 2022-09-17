from PyQt5.QtWidgets import QApplication, QWidget, QHeaderView, QAbstractItemView, QPushButton, QTableWidget, \
                            QTableWidgetItem, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import Qt


class TableWidget(QTableWidget):
    def __init__(self):
        super().__init__(1, 2)
        name = ["Имя","Цена"]
        self.setHorizontalHeaderLabels(name)
        self.verticalHeader().setDefaultSectionSize(50)
        self.horizontalHeader().setDefaultSectionSize(250)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
    # Добавить строку таблицы
    def _addRow(self):
        rowCount = self.rowCount()
        self.insertRow(rowCount )
    # Удалить строку таблицы
    def _removeRow(self):
        if self.rowCount() > 1:
            self.removeRow(self.rowCount()-1)

    def _copyRow(self):
        self.insertRow(self.rowCount())
        rowCount = self.rowCount()
        columnCount = self.columnCount()

        for j in range(columnCount):
            if not self.item(rowCount-2, j) is None:
                self.setItem(rowCount-1, j, QTableWidgetItem(self.item(rowCount-2, j).text()))
