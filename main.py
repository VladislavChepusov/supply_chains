import random
from PyQt5.QtWidgets import QFileDialog, QDialog, QApplication, QWidget, QMainWindow, QVBoxLayout, QHBoxLayout, \
    QFormLayout, QComboBox, QPushButton, QInputDialog, QLineEdit, QLabel
import sys
import os
from QGraphViz.QGraphViz import QGraphViz, QGraphVizManipulationMode
from QGraphViz.DotParser import Graph, GraphType
from QGraphViz.Engines import Dot
from PyQt5.QtGui import QFontMetrics, QFont, QImage

from scm_firm import scm_firm
from tableWidget import TableWidget

sys.path.insert(1, os.path.dirname(__file__) + "/..")
print(sys.path)
Parent_node = ''
Number_node = 1

if __name__ == "__main__":
    # Создание приложения QT
    app = QApplication(sys.argv)


    # выделение узла
    def node_selected(node):
        if (qgv.manipulation_mode == QGraphVizManipulationMode.Node_remove_Mode):
            print(f"Узел {node.name} был удален")
            print("__________________________")
        else:
            global Parent_node
            Parent_node = node
            print(f"infa родительский узел) = {Parent_node}")


    # Событие двойного нажатия на вершину
    # ПРОВЕРЯТЬ ДАННЫЕ
    # ПОДГРУЖАТЬ СТАРЫЕ ДАННЫЕ
    # НОМАРЛЬНОЕ ПРЕДСТАВЛЕНИЕ ДАННЫХ
    def node_invoked(node):
        print(f"Двоеное нажатие на вершины {node.name}")
        dlg = QDialog()
        dlg.ok = False
        dlg.setWindowTitle(f'Фирмы узла {node.kwargs["label"]}')

        main_layout = QVBoxLayout()
        l = QFormLayout()
        buttons_layout = QHBoxLayout()
        table = TableWidget()
        main_layout.addWidget(table)
        main_layout.addLayout(l)
        main_layout.addLayout(buttons_layout)
        dlg.setLayout(main_layout)
        dlg.resize(900, 900)

        firm_list = []


        def ok():
            dlg.OK = True
            rowCount = table.rowCount()
            #columnCount = table.columnCount()
            for i in range(rowCount):
                firm_list.append([table.item(i,0).text(),table.item(i,1).text()])
            dlg.close()

        def cancel():
            dlg.OK = False
            dlg.close()

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

        dlg.exec_()
        if dlg.OK and firm_list:
            print(f'firm_list = {firm_list}')
            node.kwargs['firms'] = firm_list







    def node_removed(node):
        print("Вершина удалена")


    # QGraphViz виджет
    show_subgraphs = False
    qgv = QGraphViz(
        show_subgraphs=show_subgraphs,
        auto_freeze=True,
        node_selected_callback=node_selected,
        # edge_selected_callback=edge_selected,
        node_invoked_callback=node_invoked,
        # edge_invoked_callback=edge_invoked,
        node_removed_callback=node_removed,
        # edge_removed_callback=edge_removed,
        # подсветка узлов и связей
        hilight_Nodes=True,
        hilight_Edges=False
    )

    qgv.setStyleSheet("background-color:white;")
    # Создайте новый график, используя механизм компоновки Dot
    qgv.new(Dot(Graph("Main_Graph"), show_subgraphs=show_subgraphs, font=QFont("Arial", 12), margins=[20, 20]))
    # Добавляем первый узел
    qgv.addNode(qgv.engine.graph, 1, label=f"X1.1", firms=[], fillcolor="#b1b0af")

    # n5 = qgv.addNode(qgv.engine.graph, "Node5", label="N5", shape="polygon", fillcolor="red", color="white")
    # qgv.addEdge(n2, n4, {"width": 2})

    # Постройте граф (механизм компоновки организует расположение узлов и соединений)
    qgv.build()

    # Задание формочки
    w = QMainWindow()
    w.setWindowTitle('SCM v1.0')
    # Create a central widget to handle the QGraphViz object
    wi = QWidget()
    wi.setLayout(QVBoxLayout())
    w.setCentralWidget(wi)
    # Add the QGraphViz object to the layout
    wi.layout().addWidget(qgv)
    # добавить горизонтальный макет (панель для выбора того, что делать)
    hpanel = QHBoxLayout()
    wi.layout().addLayout(hpanel)


    def manipulate():
        qgv.manipulation_mode = QGraphVizManipulationMode.Nodes_Move_Mode


    def save():
        fname = QFileDialog.getSaveFileName(qgv, "Save", "", "*.json")
        if fname[0] != "":
            qgv.saveAsJson(fname[0])


    def new():
        qgv.engine.graph = Graph("MainGraph")
        global Number_node
        Number_node = 1
        qgv.addNode(qgv.engine.graph, 1, label=f"X1.1", firms=[], fillcolor="grey")
        qgv.build()
        qgv.repaint()


    def load():
        fname = QFileDialog.getOpenFileName(qgv, "Open", "", "*.json")
        if (fname[0] != ""):
            qgv.loadAJson(fname[0])


    # Дописать удаление лчоерний улов и пересчет
    def rem_node():
        qgv.manipulation_mode = QGraphVizManipulationMode.Node_remove_Mode
        for btn in buttons_list:
            btn.setChecked(False)
        btnRemNode.setChecked(True)


    def add_node_сhild():
        if Parent_node != '':
            global Number_node
            Number_node += 1
            new_node = qgv.addNode(qgv.engine.graph, Number_node, label=f"X{Number_node}.{Parent_node.name}",
                                   firms=[], fillcolor="#b1b0af")
            qgv.addEdge(Parent_node, new_node, {"width": 3})
            qgv.build()
        else:
            print("end")
            pass


    # Добавить кнопки
    btnNew = QPushButton("Стереть")
    btnNew.clicked.connect(new)

    btnOpen = QPushButton("Загрузить")
    btnOpen.clicked.connect(load)

    btnSave = QPushButton("Сохранить")
    btnSave.clicked.connect(save)

    hpanel.addWidget(btnNew)
    hpanel.addWidget(btnOpen)
    hpanel.addWidget(btnSave)

    buttons_list = []

    btnManip = QPushButton("Управление")
    btnManip.setCheckable(True)
    btnManip.setChecked(True)
    btnManip.clicked.connect(manipulate)
    hpanel.addWidget(btnManip)
    buttons_list.append(btnManip)

    btnAddChild = QPushButton("Добавить дочерний узел")
    btnAddChild.setCheckable(True)
    btnAddChild.clicked.connect(add_node_сhild)
    hpanel.addWidget(btnAddChild)
    buttons_list.append(btnAddChild)

    btnRemNode = QPushButton("Удалить узел")
    btnRemNode.setCheckable(True)
    btnRemNode.clicked.connect(rem_node)
    hpanel.addWidget(btnRemNode)
    buttons_list.append(btnRemNode)

    w.showMaximized()
    sys.exit(app.exec_())
