from plyfile import PlyData, PlyElement
import os


def read_ply(path=''):
    # время чтения из ascii примерно минута, из бинарного меньше секунды
    with open(path, 'rb') as file:
        ply_data = PlyData.read(file)  # содержит считанные данные с файла в массиве
    return ply_data


def save_ply(ply_data, binary=False, name='unnamed'):
    # время записи ascii примерно минута, а бинарного меньше секунды
    PlyData(ply_data, text=not binary).write(name)


def convert_to_ascii(path, name):
    in_full_path = os.path.join(path, name)
    out_full_path = os.path.join(path, 'converted to ASCII ' + name)
    ply_data = read_ply(in_full_path)
    save_ply(ply_data, binary=False, name=out_full_path)
