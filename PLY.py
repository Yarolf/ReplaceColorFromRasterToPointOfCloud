from plyfile import PlyData, PlyElement
import os


def read_ply(path=''):
    """
    Предпочтительнее по скорости читать бинарный файл
    """
    # время чтения из ascii примерно минута, из бинарного меньше секунды
    with open(path, 'rb') as file:
        ply_data = PlyData.read(file)  # содержит считанные данные с файла в массиве
    return ply_data


def save_ply(ply_data, binary=False, path='', name='unnamed'):
    """
    Предпочтительнее по скорости сохранять бинарный файл
    """
    # время записи ascii примерно минута, а бинарного меньше секунды
    if not os.path.exists(path):
        os.mkdir(path)
    out_full_ply_file_path = os.path.join(path, name)
    PlyData(ply_data, text=not binary).write(out_full_ply_file_path)


def convert_to_ascii(path, name):
    """
    Читает бинарный файл облака точек и сохраняет его в ASCII
    """
    in_full_path = os.path.join(path, name)
    out_full_path = os.path.join(path, 'converted to ASCII ' + name)
    ply_data = read_ply(in_full_path)
    save_ply(ply_data, binary=False, name=out_full_path)
