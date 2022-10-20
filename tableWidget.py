from PyQt5.QtGui import QDoubleValidator
from PyQt5.QtWidgets import QHeaderView, QTableWidget, \
    QTableWidgetItem, QFileDialog, QMessageBox, QLineEdit, QComboBox
from xlsxwriter import Workbook


# Кастомная таблица (произвольные размеры и название).Удаление/Добавление/Сохранение/Проверка на пустоту ячеек
class TableWidget(QTableWidget):
    def __init__(self, row, col, name):
        super().__init__(row, col)
        self.setHorizontalHeaderLabels(name)
        self.verticalHeader().setDefaultSectionSize(50)
        self.horizontalHeader().setDefaultSectionSize(899 / col)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)

        float_element = QLineEdit()
        float_element.setValidator(QDoubleValidator(0.99, 99.99, 4))
        self.setCellWidget(0, 1, float_element)

    # Добавить строку таблицы
    def _addRow(self):
        self.insertRow(self.rowCount())
        float_element = QLineEdit()
        float_element.setValidator(QDoubleValidator(0.99, 99.99, 4))
        self.setCellWidget(self.rowCount() - 1, 1, float_element)

    # Удалить строку таблицы
    def _removeRow(self):
        if self.rowCount() > 1:
            self.removeRow(self.rowCount() - 1)

    def _copyRow(self):
        self.insertRow(self.rowCount())
        rowCount = self.rowCount()
        columnCount = self.columnCount()

        for j in range(columnCount):
            if not self.item(rowCount - 2, j) is None:
                self.setItem(rowCount - 1, j, QTableWidgetItem(self.item(rowCount - 2, j).text()))

    # Проверка ячеек на пустоту
    def isEmptys(self):
        rowCount = self.rowCount()
        for i in range(rowCount):
            try:
                if not (self.item(i, 0).text() and self.cellWidget(i, 1).text()):
                    return False
            except:
                return False
        return True

    # Сохранение таблицы в ексель
    def tableSave(self):
        fileName, ok = QFileDialog.getSaveFileName(
            self,
            "Сохранить файл",
            ".",
            "All Files(*.xlsx)"
        )
        if not fileName:
            return

        model = self.model()
        _list = [[self.horizontalHeaderItem(i).text() for i in range(model.columnCount())]]
        for row in range(model.rowCount()):
            _r = []
            for column in range(model.columnCount()):
                _r.append("{}".format(model.index(row, column).data() or ""))
            _list.append(_r)
        workbook = Workbook(fileName)
        worksheet = workbook.add_worksheet()
        for r, row in enumerate(_list):
            for c, col in enumerate(row):
                worksheet.write(r, c, col)
        workbook.close()
        QMessageBox.information(
            self,
            "Успешно!",
            f"Данные сохранены в файле: \n{fileName}"
        )
