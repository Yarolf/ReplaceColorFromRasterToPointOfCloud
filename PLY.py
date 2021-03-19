from plyfile import PlyData, PlyElement
import os


def read_ply(path=''):
    """
    Предпочтительнее по скорости читать бинарный файл
    """
    with open(path, 'rb') as file:
        ply_data = PlyData.read(file)  # содержит считанные данные с файла в массиве
    return ply_data


def save_ply(ply_data, path, name='unnamed', binary=False):
    """
    Предпочтительнее по скорости сохранять бинарный файл
    """
    if not os.path.exists(path):
        os.mkdir(path)
    out_full_ply_file_path = os.path.join(path, name)
    PlyData(ply_data, text=not binary).write(out_full_ply_file_path)


def convert_to_ascii(path, name):
    """
    Читает бинарный файл облака точек и сохраняет его в ASCII
    """
    in_full_path = os.path.join(path, name)
    out_file_name = 'converted to ASCII ' + name
    print('Читаю файл ...')
    ply_data = read_ply(in_full_path)
    print('Конвертирую файл ...')
    save_ply(ply_data, binary=False, path=path, name=out_file_name)
