"""

Модуль для работы с файлами формата .hdf5
В нем описаны алгоритмы для управление файлом (Создание, чтение и редактирование)

__init__ - создание экземпляра класса для хранения имени и пути проекта.
            создание копии проекта, над которым будет происходить дальнейшая работа.

creat_file(user_name: str, classes: str, description: str) - создание файла
            user_name - переменная имени пользователя, создавшего проект
            classes - переменная, хранящая коды спользованных классов в проекте
            description - описание прокта

add_images( list_images) -

"""

import h5py
import os
import os.path
import shutil
import metadata
import json
from PyQt5.QtWidgets import QFileDialog
import cv2


class project:
    name = 'no name'
    path = 'no path'
    name_tmp = 'no name'
    path_tmp = 'no path'

    def __init__(self, project_name: str):
        self.name = project_name
        self.name_tmp = project_name + '_tmp'
        if project_name[-5:] == '.hdf5':
            self.path = '__projects/' + self.name #+ '.hdf5'
            self.path_tmp = '__projects/' + self.name_tmp# + '.hdf5'
        else:
            self.path = '__projects/' + self.name + '.hdf5'
            self.path_tmp = '__projects/' + self.name_tmp + '.hdf5'

    def read_info_project(self):
        with h5py.File(self.path, 'r') as hf:
            tmp = []
            for k in hf.attrs.keys():
                tmp.append([k, hf.attrs[k]])
        return dict(tmp)

    def creat_clone_proj(self):
        shutil.copyfile(self.path, self.path_tmp)

    def creat_project(self, user_name: str, classes: str, description: str):
        with h5py.File(self.path, 'w') as hf:
            hf.create_group('features')
            # hf.create_group('targets')
            # hf.create_dataset('Project info', data=json.dumps(metadata.data_project(self.name, user_name,
            #                                                                        classes, description)))
            hf.attrs.update(metadata.data_project(self.name, user_name, classes, description))

    def add_images(self, qwidget):
        list_images = self.get_file_name(qwidget)[0]
        with h5py.File(self.path, 'a') as hf:
            features = hf.get('features')
            # targets = hf.get('targets')
            for i in range(len(list_images)):
                img = cv2.imread(list_images[i])
                height, width, channel = img.shape
                im = features.create_dataset('img' + str(i), data=img)
                # targets.create_dataset('img' + str(i), data=metadata.data_image(i, width, height, count))
                im.attrs.update(metadata.data_image(i, width, height, 0))

    def read_images(self, index: int):
        with h5py.File(self.path_tmp, 'r') as hf:
            img = hf.get('features/' + 'img' + str(index))
        return img

    def update_project_info(self):
        with h5py.File(self.path_tmp, 'r+') as hf:
            hf.attrs['Time of last change'] = str(metadata.datetime.now())[:-10]

    def update_image_info(self, index: int, object_count=None, objects=None,
                          signature_1=None, signature_2=None, status=None):
        with h5py.File(self.path_tmp, 'r+') as hf:
            hf.attrs['Time of last change'] = str(metadata.datetime.now())[:-10]
            img = hf.get('feature/img' + str(index))
            if object_count is not None:
                img.attrs['Number of objects'] = object_count
            if objects is not None:
                current_obj = list(img.attrs['Objects'])
                current_obj.append(json.dumps(objects))
                img.attrs['Objects'] = current_obj
            if signature_1 is not None:
                img.attrs['Signature 1'] = signature_1
            if signature_2 is not None:
                img.attrs['Signature 2'] = signature_2
            if status is not None:
                img.attrs['Status'] = status
            img.attrs['Time of last change'] = str(metadata.datetime.now())[:-10]

    def update_object_info(self, index_img: int, index_obj: int):
        with h5py.File(self.path_tmp, 'r+') as hf:
            img = hf.get('feature/img' + str(index_img))
            '''
            ДОДЕЛАТЬ
            
            '''

    def get_file_name(self, qwidget):
        file_filter = 'JPEG File (*.jpeg);; JPG File (*.jpg);; PNG File (*.png);; All Files (*.*) '
        list_images = QFileDialog.getOpenFileNames(parent=qwidget,
                                                   caption='Select',
                                                   directory=os.getcwd(),
                                                   filter=file_filter,
                                                   initialFilter='All Files (*.*)')
        return list_images

    def save_project(self):
        os.remove(self.path)
        shutil.copyfile(self.path_tmp, self.path)
        os.remove(self.path_tmp)
