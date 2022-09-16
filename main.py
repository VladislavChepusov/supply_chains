import random

from PyQt5.QtWidgets import QFileDialog, QDialog, QApplication, QWidget, QMainWindow, QVBoxLayout, QHBoxLayout, \
    QFormLayout, QComboBox, QPushButton, QInputDialog, QLineEdit, QLabel
import sys
import os
from QGraphViz.QGraphViz import QGraphViz, QGraphVizManipulationMode
from QGraphViz.DotParser import Graph, GraphType
from QGraphViz.Engines import Dot
from PyQt5.QtGui import QFontMetrics, QFont, QImage

sys.path.insert(1, os.path.dirname(__file__) + "/..")
print(sys.path)
Parent_node = ''

if __name__ == "__main__":
    # Create QT application
    app = QApplication(sys.argv)



    def node_selected(node):
        if (qgv.manipulation_mode == QGraphVizManipulationMode.Node_remove_Mode):
            print("Node {} removed".format(node))
            print("__________________________")
        else:
            global Parent_node
            Parent_node = node

            print(f"infa = {Parent_node}")
            print("Node selected {}".format(node))
            print("Node selected {}".format(node.name))
            print("Node selected {}".format(node.kwargs['label']))
            # print("Node selected {}".format(node.kwargs['jopa']))


    # бесполезная хуйня для  меня
    # def edge_selected(edge):
    #     if (qgv.manipulation_mode == QGraphVizManipulationMode.Edge_remove_Mode):
    #         print("Edge {} removed".format(edge))
    #     else:
    #         print("Edge selected {}".format(edge))



    # Полезная хуйня для меня (двойнок лик по вершине )
    def node_invoked(node):
        print("Node double clicked")
        print(f"{node.name}|{node.kwargs['label']}|{node.kwargs['jopa']}")




    # удалить потом
    # def edge_invoked(node):
    #     print("Edge double clicked")


    # Полезно
    def node_removed(node):
        print("Node removed")


    # Бесполезно(наверное)
    # def edge_removed(node):
    #     print("Edge removed")


    # Create QGraphViz widget
    # Дефолтная застановка
    show_subgraphs = True
    qgv = QGraphViz(
        show_subgraphs=show_subgraphs,
        auto_freeze=True,  # show autofreeze capability/показать возможность автозаморозки
        node_selected_callback=node_selected,
        #edge_selected_callback=edge_selected,
        node_invoked_callback=node_invoked,
        #edge_invoked_callback=edge_invoked,
        node_removed_callback=node_removed,
        #edge_removed_callback=edge_removed,

        # подсветка узлов и связей
        hilight_Nodes=True,
        hilight_Edges=True
    )
    qgv.setStyleSheet("background-color:white;")

    # Create A new Graph using Dot layout engine/Создайте новый график, используя механизм компоновки Dot
    qgv.new(Dot(Graph("Main_Graph"), show_subgraphs=show_subgraphs, font=QFont("Arial", 12), margins=[20, 20]))
    # Define sone graph
    n1 = qgv.addNode(qgv.engine.graph, "1", label="X1.1", fillcolor="red",jopa='lol')
    # n2 = qgv.addNode(qgv.engine.graph, "Node2", label="N2", fillcolor="blue:white:red")
    # n3 = qgv.addNode(qgv.engine.graph, "Node3", label="N3", shape="diamond", fillcolor="orange")
    # n4 = qgv.addNode(qgv.engine.graph, "Node4", label="N4", shape="diamond", fillcolor="white")
    # n5 = qgv.addNode(qgv.engine.graph, "Node5", label="N5", shape="polygon", fillcolor="red", color="white")

    # qgv.addEdge(n1, n2, {})
    # qgv.addEdge(n3, n2, {})
    # qgv.addEdge(n2, n4, {"width": 2})
    # qgv.addEdge(n4, n5, {"width": 4})

    # Build the graph (the layout engine organizes where the nodes and connections are)
    # Постройте граф (механизм компоновки организует расположение узлов и соединений)
    qgv.build()

    # Save it to a file to be loaded by Graphviz if needed
    #qgv.save("test.gv")

    # Задание формочки
    w = QMainWindow()
    w.setWindowTitle('Привер')
    # Create a central widget to handle the QGraphViz object
    wi = QWidget()
    wi.setLayout(QVBoxLayout())
    w.setCentralWidget(wi)
    # Add the QGraphViz object to the layout
    wi.layout().addWidget(qgv)
    # Add a horizontal layout (a pannel to select what to do)
    # добавить горизонтальный макет (панель для выбора того, что делать)
    hpanel = QHBoxLayout()
    wi.layout().addLayout(hpanel)



    def manipulate():
        qgv.manipulation_mode = QGraphVizManipulationMode.Nodes_Move_Mode


    def save():
        fname = QFileDialog.getSaveFileName(qgv, "Save", "", "*.json")
        if (fname[0] != ""):
            qgv.saveAsJson(fname[0])


    def new():
        qgv.engine.graph = Graph("MainGraph")
        qgv.build()
        qgv.repaint()


    def load():
        fname = QFileDialog.getOpenFileName(qgv, "Open", "", "*.json")
        if (fname[0] != ""):
            qgv.loadAJson(fname[0])

    def rem_node():
        qgv.manipulation_mode = QGraphVizManipulationMode.Node_remove_Mode
        for btn in buttons_list:
            btn.setChecked(False)
        btnRemNode.setChecked(True)

    def add_node_сhild():
        if Parent_node != '':
            new_node = qgv.addNode(qgv.engine.graph, random.random(), label=f"{random.random()}",jopa='2')
        #qgv.addNode(qgv.engine.graph, 'pizda', label='pizda', jopa='pizda')
            qgv.addEdge(Parent_node, new_node, {"width": 2})
            qgv.build()
        else:
            print("end")
            pass








    def add_node():
        dlg = QDialog()
        dlg.ok = False
        dlg.node_name = ""
        dlg.node_label = ""
        dlg.node_type = "None"
        dlg.node_jopa = ""

        # Layouts
        main_layout = QVBoxLayout()
        l = QFormLayout()
        buttons_layout = QHBoxLayout()

        main_layout.addLayout(l)
        main_layout.addLayout(buttons_layout)
        dlg.setLayout(main_layout)

        leNodeName = QLineEdit()
        leNodeLabel = QLineEdit()
        cbxNodeType = QComboBox()
        leImagePath = QLineEdit()
        leNodeJopa = QLineEdit()

        pbOK = QPushButton()
        pbCancel = QPushButton()

        cbxNodeType.addItems(["None", "circle", "box"])
        pbOK.setText("&OK")
        pbCancel.setText("&Cancel")

        l.setWidget(0, QFormLayout.LabelRole, QLabel("Node Name"))
        l.setWidget(0, QFormLayout.FieldRole, leNodeName)

        l.setWidget(1, QFormLayout.LabelRole, QLabel("Node Label"))
        l.setWidget(1, QFormLayout.FieldRole, leNodeLabel)

        l.setWidget(2, QFormLayout.LabelRole, QLabel("Node Type"))
        l.setWidget(2, QFormLayout.FieldRole, cbxNodeType)

        l.setWidget(3, QFormLayout.LabelRole, QLabel("Node Image"))
        l.setWidget(3, QFormLayout.FieldRole, leImagePath)

        l.setWidget(4, QFormLayout.LabelRole, QLabel("Node jopa"))
        l.setWidget(4, QFormLayout.FieldRole, leNodeJopa)

        def ok():
            dlg.OK = True
            dlg.node_name = leNodeName.text()
            dlg.node_label = leNodeLabel.text()
            dlg.node_jopa = leNodeJopa.text()
            if (leImagePath.text()):
                dlg.node_type = leImagePath.text()
            else:
                dlg.node_type = cbxNodeType.currentText()
            dlg.close()

        def cancel():
            dlg.OK = False
            dlg.close()

        pbOK.clicked.connect(ok)
        pbCancel.clicked.connect(cancel)

        buttons_layout.addWidget(pbOK)
        buttons_layout.addWidget(pbCancel)
        dlg.exec_()
        # node_name, okPressed = QInputDialog.getText(wi, "Node name","Node name:", QLineEdit.Normal, "")
        if dlg.OK and dlg.node_name != '':
            qgv.addNode(qgv.engine.graph, dlg.node_name, label=dlg.node_label, shape=dlg.node_type,jopa =dlg.node_jopa)
            qgv.build()



    # def rem_edge():
    #     qgv.manipulation_mode = QGraphVizManipulationMode.Edge_remove_Mode
    #     for btn in buttons_list:
    #         btn.setChecked(False)
    #     btnRemEdge.setChecked(True)
    #
    #
    # def add_edge():
    #     qgv.manipulation_mode = QGraphVizManipulationMode.Edges_Connect_Mode
    #     for btn in buttons_list:
    #         btn.setChecked(False)
    #     btnAddEdge.setChecked(True)


    # Add buttons
    btnNew = QPushButton("New")
    btnNew.clicked.connect(new)

    btnOpen = QPushButton("Load")
    btnOpen.clicked.connect(load)

    btnSave = QPushButton("Save")
    btnSave.clicked.connect(save)

    hpanel.addWidget(btnNew)
    hpanel.addWidget(btnOpen)
    hpanel.addWidget(btnSave)

    buttons_list = []

    btnManip = QPushButton("Manipulate")
    btnManip.setCheckable(True)
    btnManip.setChecked(True)
    btnManip.clicked.connect(manipulate)
    hpanel.addWidget(btnManip)
    buttons_list.append(btnManip)

    btnAddNode = QPushButton("Add Node/Добавить узел")
    btnAddNode.clicked.connect(add_node)
    hpanel.addWidget(btnAddNode)
    buttons_list.append(btnManip)

    btnRemNode = QPushButton("Rem Node/Удалить узел")
    btnRemNode.setCheckable(True)
    btnRemNode.clicked.connect(rem_node)
    hpanel.addWidget(btnRemNode)
    buttons_list.append(btnRemNode)


    btnAddChild = QPushButton("Добавить дочь")
    btnAddChild.setCheckable(True)
    btnAddChild.clicked.connect(add_node_сhild)
    hpanel.addWidget(btnAddChild)
    buttons_list.append(btnAddChild)

    # btnAddEdge = QPushButton("Add Edge/Связь")
    # btnAddEdge.setCheckable(True)
    # btnAddEdge.clicked.connect(add_edge)
    # hpanel.addWidget(btnAddEdge)
    # buttons_list.append(btnAddEdge)
    #
    # btnRemEdge = QPushButton("Rem Edge/Связь")
    # btnRemEdge.setCheckable(True)
    # btnRemEdge.clicked.connect(rem_edge)
    # hpanel.addWidget(btnRemEdge)
    # buttons_list.append(btnRemEdge)

    w.showMaximized()
    sys.exit(app.exec_())
