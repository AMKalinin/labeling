import sys
from PyQt5.QtWidgets import (QWidget, QLabel, QDialog,
    QComboBox, QApplication, QListView, QVBoxLayout, QHBoxLayout, QPushButton)
from PyQt5.QtCore import pyqtSignal, QObject

import segflex_classifier as classifier
import hdf_work


class classes_choose(QDialog):
    signal1 = pyqtSignal()
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        classifier.project_classes.clear()

        self.adjust_window()
        self.create_place_combo_boxes()
        self.create_place_choose_buttons()
        self.create_place_control_buttons()

    def on_btn_ok(self, event):
        proj = hdf_work.project(self.parent().text_area_name.text())
        proj.creat_project(self.parent().parent().btn1.text(),
                           str(classifier.project_classes),
                           self.parent().text_area_description.text())
        proj.add_images(self)
        attr = proj.read_info_project()

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
        self.parent().parent().creat_proj_widget(to_project_name,
                                               to_project_classes,
                                               to_creation_time,
                                               to_creator,
                                               to_last_change)

        self.signal1.emit()
        self.deleteLater()
    
    def adjust_window(self):
        self.setWindowTitle("Выбор классов проекта")
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

    def create_place_choose_buttons(self):
        self.select_label = QLabel("Выбрано: ")
        btn_add = QPushButton("Добавить")
        btn_remove = QPushButton("Удалить")

        choose_layout = QVBoxLayout()
        choose_layout.addWidget(self.select_label)
        choose_layout.addWidget(btn_add)
        choose_layout.addWidget(btn_remove)

        btn_add.clicked.connect(self.on_btn_add)
        btn_remove.clicked.connect(self.on_btn_remove)

        self.layout.addLayout(choose_layout)        

    def create_place_control_buttons(self):
        btn_ok = QPushButton("Ок")
        btn_cancel = QPushButton("Отмена")

        control_layout = QHBoxLayout()
        control_layout.addWidget(btn_cancel)
        control_layout.addWidget(btn_ok)

        btn_ok.clicked.connect(self.on_btn_ok)

        self.layout.addLayout(control_layout)

    def create_place_combo_boxes(self):
        self.box_base = QComboBox(self)
        self.box_secondary = QComboBox(self)
        self.box_thirdly = QComboBox(self)

        combo_layout = QVBoxLayout()
        combo_layout.addWidget(self.box_base)
        combo_layout.addWidget(self.box_secondary)
        combo_layout.addWidget(self.box_thirdly)

        self.box_base.activated.connect(self.choose_secondary)
        self.box_secondary.activated.connect(self.choose_thirdly)

        self.box_base.addItems(classifier.code_base)

        self.layout.addLayout(combo_layout)

    def choose_secondary(self):
        self.box_secondary.clear()
        self.box_thirdly.clear()

        self.base_index = self.box_base.currentIndex()
        if self.base_index == 0:
            self.box_secondary.addItems(classifier.code_100)
        elif self.base_index == 1:
            self.box_secondary.addItems(classifier.code_200)
        elif self.base_index == 2:
            self.box_secondary.addItems(classifier.code_300)
        elif self.base_index == 3:
            self.box_secondary.addItems(classifier.code_400)

    def choose_thirdly(self):
        self.box_thirdly.clear()

        secondary_index = self.box_secondary.currentIndex()

        if self.base_index == 2 and secondary_index == 2:
            self.box_thirdly.addItems(classifier.code_320)
        elif self.base_index == 3 and secondary_index == 0:
            self.box_thirdly.addItems(classifier.code_490)
        elif self.base_index == 3 and secondary_index == 1:
            self.box_thirdly.addItems(classifier.code_410)
        elif self.base_index == 3 and secondary_index == 2:
            self.box_thirdly.addItems(classifier.code_420)
        elif self.base_index == 3 and secondary_index == 4:
            self.box_thirdly.addItems(classifier.code_440)
        elif self.base_index == 3 and secondary_index == 5:
            self.box_thirdly.addItems(classifier.code_450)
        elif self.base_index == 3 and secondary_index == 6:
            self.box_thirdly.addItems(classifier.code_460)

    def on_btn_add(self):
        text = self.box_thirdly.currentText()
        if text not in classifier.project_classes:
            classifier.project_classes.append(text)
        self.display_classes_list()

    def on_btn_remove(self):
        text = self.box_thirdly.currentText()
        if text in classifier.project_classes:
            classifier.project_classes.remove(text)
        self.display_classes_list()

    def display_classes_list(self):
        classifier.project_classes.sort()
        classes = " ".join(classifier.project_classes)
        self.select_label.setText("Выбрано: " + classes)
