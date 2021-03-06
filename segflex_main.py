from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtWidgets import (QApplication, QVBoxLayout, QGroupBox, QMainWindow, QFrame, QGridLayout,
                             QPushButton, QHBoxLayout, QTabWidget, QWidget, QLabel, QDialog,
                             QPlainTextEdit, QLineEdit, QMenu,
                             QScrollArea, QToolButton, QSizePolicy, QComboBox)

import segflex_new_project
import segflex_project_as_widget as project
import os
import json
import segflex_classifier as classifier
import hdf_work


class main_window(QMainWindow):

    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent, flags=QtCore.Qt.Window)

        # super(main_window, self).__init__( parent) #? toje rabotaet

        self.adjust_main_window()
        # self.check_projects_folder()
        self.create_place_widgets_main_window()

    def check_projects_folder(self):
        path_dir = os.getcwd()
        path_dir += "/__projects"
        if not os.path.exists(path_dir):
            print("project_folder_created")
            os.mkdir(path_dir)
        projects_list = os.listdir(path_dir)
        print(projects_list)
        if not projects_list:
            return
        for proj in projects_list:  # check correct file
            if proj[-5:] == '.hdf5':
                path_project = path_dir + "/" + proj
                f = hdf_work.project(proj)
                attr = f.read_info_project()

                for key, value in attr.items():
                    if key == "Name project":
                        to_project_name = value
                    elif key == "List classes":
                        to_project_classes = value
                    elif key == "Creation time":
                        to_creation_time = value
                    elif key == "Creator":
                        to_creator = value
                    elif key == "Description":
                        to_description = value
                    elif key == "Time of last change":
                        to_last_change = value
                self.creat_proj_widget(to_project_name,
                                       to_project_classes,
                                       to_creation_time,
                                       to_creator,
                                       to_last_change)

    def creat_proj_widget(self, to_project_name, to_project_classes,
                          to_creation_time, to_creator, to_last_change):
        project_widget = project.project_as_widget(name=to_project_name,
                                                   classes=to_project_classes,
                                                   creation_time=to_creation_time,
                                                   creator=to_creator,
                                                   last_change=to_last_change)
        self.layout_SArea.addWidget(project_widget)

    def test2_create_widget(self, srcs_classes=[]):
        self.project_widget = project.project_as_widget(name="asd", classes=classifier.project_classes)
        self.layout_SArea.addWidget(self.project_widget)

    def test_create_widget(self):
        self.project_widget = project.project_as_widget(name="asd", classes=[4, 4, 4])
        self.layout_SArea.addWidget(self.project_widget)

    def create_button_group(self):
        button_group = QGroupBox()

        btn1 = QPushButton("?????????????? ?????????? ????????????")
        btn2 = QPushButton("?????????????? ????????????")
        btn3 = QPushButton("?????????????? ???????????? ???? ???????????? ??????????????????????????")

        layout = QVBoxLayout()
        layout.addWidget(btn1)
        layout.addWidget(btn2)
        layout.addWidget(btn3)
        button_group.setLayout(layout)
        self.main_layout.addWidget(button_group, 1, 1)

        btn1.clicked.connect(self.on_create_new_project_clicked)
        btn3.clicked.connect(self.test_create_widget)

    def create_button_group_2(self):
        button_group_2 = QGroupBox()

        btn1 = QPushButton("?????????????????? ??????????????")
        btn2 = QPushButton("???????????????? ??????????????????????")
        btn3 = QPushButton("?????????????? ??????????????????????")

        layout = QVBoxLayout()
        layout.addWidget(btn1)
        layout.addWidget(btn2)
        layout.addWidget(btn3)
        button_group_2.setLayout(layout)
        self.main_layout.addWidget(button_group_2, 3, 1)

    def create_button_group_3(self):
        button_group_3 = QGroupBox()

        self.btn1 = QPushButton("???????????? ????????. ????????????????")

        layout = QHBoxLayout()
        layout.addWidget(self.btn1)
        button_group_3.setLayout(layout)
        self.main_layout.addWidget(button_group_3, 0, 1)

    def create_table(self):
        table = QTabWidget()

        # a1 = project.project_as_widget(name="create_table", classes=[1,2,3])
        # a2 = project.project_as_widget(name="create_table", classes=[1,2,3])
        # a3 = project.project_as_widget(self)
        # a4 = project.project_as_widget(self)
        # a5 = project.project_as_widget(self)

        self.scrollarea = QScrollArea(self)
        # self.scrollarea.setFixedWidth(250)
        self.scrollarea.setWidgetResizable(True)

        widget = QWidget(self.scrollarea)
        self.scrollarea.setWidget(widget)
        self.layout_SArea = QVBoxLayout(widget)

        self.check_projects_folder()

        # self.layout_SArea.addWidget(a1)
        # self.layout_SArea.addWidget(a2)
        # self.layout_SArea.addWidget(a3)
        # self.layout_SArea.addWidget(a4)
        # self.layout_SArea.addWidget(a5)
        # widget.setMinimumSize(600, 400)# //skukojivaet widgeti
        # widget.adjustSize()

        tab2 = QWidget()
        tab3 = QWidget()

        table.addTab(self.scrollarea, "????????????")
        table.addTab(tab2, "????????????????????????????")
        table.addTab(tab3, "????????????????")

        # self.main_layout.addWidget(self.scrollarea, 1, 0, 3, 1)
        self.main_layout.addWidget(table, 1, 0, 3, 1)

    def create_description(self, file_description=""):  # ??????????? ??????? ???????????????????????????? ?????????????????
        description = QLabel(file_description)
        self.main_layout.addWidget(description, 2, 1)

    def on_create_new_project_clicked(self):
        self.dialog = segflex_new_project.new_project_dialog(self)
        #self.dialog.signal1.connect(self.test2_create_widget)
        self.dialog.exec_()

    def create_place_widgets_main_window(self):
        self.create_button_group()
        self.create_button_group_2()
        self.create_button_group_3()
        self.create_table()
        self.create_description("Here must be project description")

    def adjust_main_window(self):
        main_frame = QFrame()
        self.setCentralWidget(main_frame)
        self.setWindowTitle("Segmentation app. 0.3")
        self.resize(1000, 400)

        self.main_layout = QGridLayout()
        main_frame.setLayout(self.main_layout)
