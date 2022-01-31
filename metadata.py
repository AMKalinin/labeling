from datetime import datetime


def data_project(project_name: str, user: str, classes: str, description: str):
    metadata = {'Name project': project_name,
                'Creator': user,
                'Creation time': str(datetime.now())[:-10],
                'Time of last change': str(datetime.now())[:-10],
                'List classes': classes,
                'Description': description}
    return metadata


def data_object(id: int, type: str, user: str, cod_class: int, points: list):
    metadata = {'Id': id,
                'Type': type,
                'FIO': user,
                'Time': str(datetime.now())[:-10],
                'Class': cod_class,
                'Param': points}
    return metadata


def data_image(id: int, size_w: int, size_h: int, object_count: int, objects=[],
               signature_1='None', signature_2='None', status='None'):

    metadata = {'id target': id,
                'Signature 1': signature_1,
                'Signature 2': signature_2,
                'Status': status,
                'Time of last change': str(datetime.now())[:-10],
                'Size x': size_w,
                'Size y': size_h,
                'Number of objects': object_count,
                'Objects': objects}

    return metadata
