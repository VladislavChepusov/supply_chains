import sys
from IPython.external.qt_for_kernel import QtCore, QtGui
from PyQt5.QtGui import QFont, QDoubleValidator
from PyQt5.QtWidgets import QFileDialog, QDialog, QApplication, QWidget, QMainWindow, QVBoxLayout, QHBoxLayout, \
    QFormLayout, QPushButton, QLineEdit, QLabel, QTableWidgetItem
from QGraphViz.DotParser import Graph
from QGraphViz.Engines import Dot
from QGraphViz.QGraphViz import QGraphViz, QGraphVizManipulationMode
from calculations import all_calculation_fun, type_node, daughters_map
from tableWidget import TableWidget

Parent_node = ''
Number_node = 1

if __name__ == "__main__":
    # Создание приложения QT
    app = QApplication(sys.argv)

    # Выделение узла
    def node_selected(node):
        if qgv.manipulation_mode == QGraphVizManipulationMode.Node_remove_Mode:
            print(f"Удалили  {node.name}")
        else:
            global Parent_node
            Parent_node = node

    # Событие двойного нажатия на вершину
    def node_invoked(node):
        global dlg
        print(f"Двойное нажатие на вершины {node.name}")
        validator = QDoubleValidator(0.99, 99.99, 4)
        if type_node(node.name, daughters_map(qgv.engine.graph.toDICT()["edges"])) == 3:
            dlg = QDialog()
            dlg.ok = False
            dlg.setWindowTitle(f'Задать значения рынка # {node.name}')

            dlg.A = ""
            dlg.B = ""

            main_layout = QVBoxLayout()
            l = QFormLayout()
            buttons_layout = QHBoxLayout()
            main_layout.addLayout(l)
            main_layout.addLayout(buttons_layout)
            dlg.setLayout(main_layout)
            leA = QLineEdit()
            leB = QLineEdit()

            l.setWidget(0, QFormLayout.LabelRole, QLabel("A="))
            l.setWidget(0, QFormLayout.FieldRole, leA)
            l.setWidget(1, QFormLayout.LabelRole, QLabel("B="))
            l.setWidget(1, QFormLayout.FieldRole, leB)
            # Установить валидатор ток для чисел с плавающей запятой
            # до 4-х символов после запятой
            leA.setValidator(validator)
            leB.setValidator(validator)
            # Загрузка старых цен
            try:
                leA.setText(str(node.kwargs['level_price'][0]).replace('.', ','))
                leB.setText(str(node.kwargs['level_price'][1]).replace('.', ','))
            except:
                pass
            buttOK = QPushButton()
            buttCancel = QPushButton()
            buttOK.setText("&Сохранить")
            buttCancel.setText("&Отменить")

            def cancel():
                if dlg.B != '' and dlg.A != '':
                    dlg.ok = True
                else:
                    dlg.ok = False
                dlg.close()

            def ok():
                if leA.text() != "" and leB.text() != "":
                    dlg.ok = True
                    dlg.A = leA.text()
                    dlg.B = leB.text()
                    dlg.close()

            buttOK.clicked.connect(ok)
            buttCancel.clicked.connect(cancel)
            buttons_layout.addWidget(buttOK)
            buttons_layout.addWidget(buttCancel)

            dlg.setFixedSize(700, 100)
            dlg.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)
            dlg.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, False)
            dlg.exec_()
            if dlg.ok and dlg.A != '' and dlg.B != '':
                A = float(dlg.A.replace(',', '.'))
                B = float(dlg.B.replace(',', '.'))
                node.kwargs['level_price'] = [A, B]

        if type_node(node.name, daughters_map(qgv.engine.graph.toDICT()["edges"])) != 3 or dlg.ok:
            dlg = QDialog()
            dlg.ok = False
            dlg.setWindowTitle(f'Фирмы узла {node.kwargs["label"]}')
            main_layout = QVBoxLayout()
            l = QFormLayout()
            buttons_layout = QHBoxLayout()
            table = TableWidget(1, 2, ["Название фирмы", "Издержки за ед.п"])
            main_layout.addWidget(table)
            main_layout.addLayout(l)
            main_layout.addLayout(buttons_layout)
            dlg.setLayout(main_layout)
            dlg.resize(900, 900)
            firm_list = []

            def cancel():
                dlg.ok = False
                dlg.close()

            def ok():
                if table.isEmptys():
                    dlg.ok = True
                    rowCount = table.rowCount()
                    for i in range(rowCount):
                        firm_list.append({'name_firm': table.item(i, 0).text(),
                                          'cost_firm': float(table.cellWidget(i, 1).text().replace(',', '.'))}
                                         )
                    dlg.close()

            # Загрузка старых данных
            if node.kwargs['firms']:
                for i in range(len(node.kwargs['firms'])):
                    table.setItem(i, 0, QTableWidgetItem(node.kwargs['firms'][i]['name_firm']))
                    table.cellWidget(i, 1).setText(str(node.kwargs['firms'][i]['cost_firm']).replace('.', ','))
                    table._addRow()
                table._removeRow()

            pbOK = QPushButton()
            pbCancel = QPushButton()
            pbAdd = QPushButton()
            pbDelete = QPushButton()
            pbOK.setText("&Сохранить")
            pbCancel.setText("&Отменить")
            pbAdd.setText("&Добавить строку")
            pbDelete.setText("&Удалить строку")
            pbOK.clicked.connect(ok)
            pbCancel.clicked.connect(cancel)
            pbAdd.clicked.connect(table._addRow)
            pbDelete.clicked.connect(table._removeRow)
            buttons_layout.addWidget(pbOK)
            buttons_layout.addWidget(pbCancel)
            buttons_layout.addWidget(pbAdd)
            buttons_layout.addWidget(pbDelete)
            dlg.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)
            dlg.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, False)
            dlg.exec_()

            if dlg.ok and firm_list:
                node.kwargs['firms'] = firm_list

    # Удаление вершин от листьев к родителям (снизу вверх)
    def node_removed(node):
        map_ = daughters_map(qgv.engine.graph.toDICT()["edges"])
        if node.name in map_:  # node in dict
            list_ = deletionList(map_, node.name, [])
            for _ in reversed(list_):
                qgv.removeNode(qgv.engine.graph.findNode(_))
                qgv.build()

    # Список последовательного удаления
    def deletionList(dict_, parent_name, list_=None):
        if list_ is None:
            list_ = []
        if parent_name in dict_:
            for node in dict_[parent_name]:
                list_.append(node)
                if node in dict_:
                    deletionList(dict_, node, list_)
                else:
                    continue
        return list_


    # QGraphViz виджет
    ShowSubGraphs = False
    qgv = QGraphViz(
        show_subgraphs=ShowSubGraphs,
        auto_freeze=True,
        node_selected_callback=node_selected,
        node_invoked_callback=node_invoked,
        node_removed_callback=node_removed,
        hilight_Nodes=True,
        hilight_Edges=False
    )

    qgv.setStyleSheet("background-color:white;")
    # Создайте новый график, используя механизм компоновки Dot
    qgv.new(Dot(Graph("Main_Graph"), show_subgraphs=ShowSubGraphs, font=QFont("Arial", 12), margins=[20, 20]))
    # Добавляем первый узел
    qgv.addNode(qgv.engine.graph, 1, label=f"X1.1", firms=[], level_price=[], fillcolor="#b1b0af")
    # Постройте граф (механизм компоновки организует расположение узлов и соединений)
    qgv.build()
    # Задание формочки
    w = QMainWindow()
    w.setWindowTitle('SCM v1.1')
    # Create a central widget to handle the QGraphViz object
    wi = QWidget()
    wi.setLayout(QVBoxLayout())
    w.setCentralWidget(wi)
    # Add the QGraphViz object to the layout
    wi.layout().addWidget(qgv)
    # добавить горизонтальный макет (панель для выбора того, что делать)
    hpanel = QHBoxLayout()
    wi.layout().addLayout(hpanel)

    # Манипуляция рисунком
    def manipulate():
        off_button()
        btnManip.setCheckable(True)
        btnManip.setChecked(True)
        qgv.manipulation_mode = QGraphVizManipulationMode.Nodes_Move_Mode

    # Сохранение данных в json
    def save():
        fname = QFileDialog.getSaveFileName(qgv, "Save", "", "*.json")
        if fname[0] != "":
            qgv.saveAsJson(fname[0])

    # получить структуру данных
    def CalculationsOfIndicators():
        graph_dic = qgv.engine.graph.toDICT()
        calculation = all_calculation_fun(graph_dic)

        # for key, value in calculation.items():
        #     print("{0}: {1}".format(key, value))
        dlg = QDialog()
        dlg.ok = False
        dlg.setWindowTitle(f'Итоговый расчет')
        main_layout = QVBoxLayout()
        l = QFormLayout()
        buttons_layout = QHBoxLayout()
        table = TableWidget(0, 4, ["Фирма", "Издержки", "Объем", "Прибыль"])

        def add_visual(items, gluing):
            rowPosition = table.rowCount()
            table.insertRow(rowPosition)
            [item.setFlags(QtCore.Qt.ItemIsEnabled) for item in items]
            if gluing:
                table.setSpan(rowPosition, 0, 1, 4)
                table.setItem(rowPosition, 0, items[0])
            else:
                for i in range(len(items)):
                    table.setItem(rowPosition, i, items[i])

        for i in calculation:
            level = [QtGui.QTableWidgetItem(f"Узел №{i}")]
            add_visual(level, True)
            price1 = [QtGui.QTableWidgetItem(f"Цена на узле №{i} = {calculation[i]['price']}")]
            add_visual(price1, True)

            le = len(calculation[i]['cost'])
            for j in range(le):
                data = [QtGui.QTableWidgetItem(f"{calculation[i]['name_firm'][j]} "),
                        QtGui.QTableWidgetItem(f"{calculation[i]['cost'][j]}"),
                        QtGui.QTableWidgetItem(f"{calculation[i]['value'][j]}"),
                        QtGui.QTableWidgetItem(f"{calculation[i]['profit'][j]}")]
                add_visual(data, False)

        main_layout.addWidget(table)
        main_layout.addLayout(l)
        main_layout.addLayout(buttons_layout)
        dlg.setLayout(main_layout)
        dlg.resize(900, 900)
        dlg.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)
        dlg.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, False)

        pbCancel = QPushButton()
        pbCancel.setText("&Ок")
        pbCancel.clicked.connect(dlg.close)
        buttons_layout.addWidget(pbCancel)

        pbExcel = QPushButton()
        pbExcel.setText("&Экспорт в Excel")
        pbExcel.clicked.connect(table.tableSave)
        buttons_layout.addWidget(pbExcel)
        dlg.exec_()

    # Стирание всей цепи
    def new():
        off_button()
        btnManip.setCheckable(True)
        btnManip.setChecked(True)
        qgv.engine.graph = Graph("MainGraph")
        global Number_node
        Number_node = 1
        qgv.addNode(qgv.engine.graph, 1, label=f"X1.1", firms=[], level_price=[], fillcolor="grey")
        qgv.build()
        qgv.repaint()

    # Загрузка данных из json
    def load():
        off_button()
        btnManip.setCheckable(True)
        btnManip.setChecked(True)
        fname = QFileDialog.getOpenFileName(qgv, "Open", "", "*.json")
        if fname[0] != "":
            qgv.loadAJson(fname[0])
            graph_js = qgv.engine.graph.toDICT()
            global Number_node
            Number_node = len(graph_js['nodes'])

    # Удаление вершины(включить режим)
    def rem_node():
        off_button()
        qgv.manipulation_mode = QGraphVizManipulationMode.Node_remove_Mode
        btnRemNode.setCheckable(True)
        btnRemNode.setChecked(True)

    # Добавление дочернего узла
    def add_node_child():
        off_button()
        btnAddChild.setCheckable(False)
        if Parent_node != '':
            global Number_node
            Number_node += 1
            new_node = qgv.addNode(qgv.engine.graph, Number_node, label=f"X{Number_node}.{Parent_node.name}",
                                   firms=[], level_price=[], fillcolor="#b1b0af")
            qgv.addEdge(Parent_node, new_node, {"width": 3})
            qgv.build()


    def off_button():
        qgv.manipulation_mode = QGraphVizManipulationMode.Nodes_Move_Mode
        for btn in buttons_list:
            btn.setChecked(False)
            btn.setCheckable(False)


    # Добавить кнопки
    btnNew = QPushButton("Заново")
    btnNew.clicked.connect(new)
    btnOpen = QPushButton("Загрузить")
    btnOpen.clicked.connect(load)
    btnSave = QPushButton("Сохранить")
    btnSave.clicked.connect(save)
    btndddd = QPushButton("Рассчитать")
    btndddd.clicked.connect(CalculationsOfIndicators)

    hpanel.addWidget(btnNew)
    hpanel.addWidget(btnOpen)
    hpanel.addWidget(btnSave)
    hpanel.addWidget(btndddd)

    buttons_list = []

    btnManip = QPushButton("Управление")
    btnManip.setCheckable(True)
    btnManip.setChecked(True)
    btnManip.clicked.connect(manipulate)
    hpanel.addWidget(btnManip)
    buttons_list.append(btnManip)

    btnAddChild = QPushButton("Добавить дочерний узел")
    btnAddChild.setCheckable(True)
    btnAddChild.clicked.connect(add_node_child)
    hpanel.addWidget(btnAddChild)
    # buttons_list.append(btnAddChild)

    btnRemNode = QPushButton("Удалить узел")
    btnRemNode.setCheckable(True)
    btnRemNode.clicked.connect(rem_node)
    hpanel.addWidget(btnRemNode)
    buttons_list.append(btnRemNode)

    w.showMaximized()
    sys.exit(app.exec_())
