import os

import PLY
import TIFF
from Keywords import Method
import time
import ElapsedTime


'''Ввод данных'''
full_path = ''
while not os.path.exists(full_path):
    geotiff_file_path = input('Введите путь к растру:\n')
    geotiff_file_name = input('Введите имя растра\n')
    full_path = os.path.join(geotiff_file_path, geotiff_file_name)
    if not os.path.exists(full_path):
        print('Файл не найден!')

full_path = ''
while not os.path.exists(full_path):
    ply_file_path = input('Введите путь к 3D модели:\n')
    in_ply_file_name = input('Введите имя модели:\n')
    full_path = os.path.join( ply_file_path, in_ply_file_name)
    if not os.path.exists(full_path):
        print('Файл не найден!')

''' РАСТР '''
start = time.time()

print('Читаю растр ...')
geotiff_full_path = os.path.join(geotiff_file_path, geotiff_file_name)
geotiff_file = TIFF.Raster(path=geotiff_full_path)
print('Готово!')

ElapsedTime.print_time(start)

''' 3D Модель '''
start = time.time()
out_ply_file_name = 'Replaced Colors ' + in_ply_file_name

print('Читаю .ply файл ...')
in_full_ply_file_name = os.path.join(ply_file_path, in_ply_file_name)
ply_data = PLY.read_ply(in_full_ply_file_name)
print('Готово!')

ElapsedTime.print_time(start)


'''ПРОВЕРКА СОВПАДЕНИЙ ИЛИ ПЕРЕНОС ЦВЕТА'''
start = time.time()

# если нужно просто проверить, без переноса, то
# print('Проверяю наличие совпадающих точек ...')
# count_matched, count_mismatched = geotiff_file.check_match(ply_data, Method.FAST.value)
# print('Найдено точек: ', count_matched)
# print('Не удалось сопоставить: ', count_mismatched)

print('Переношу цвет из растра в .ply файл ...')
count_replaced, count_mismatched = geotiff_file.replace_color_to(ply_data, Method.FAST.value)
print('Перенесено точек: ', count_replaced)
print('Не удалось сопоставить точек: ', count_mismatched)

ElapsedTime.print_time(start)

'''ЭКСПОРТ ОБЛАКА ТОЧЕК'''
start = time.time()

out_ply_file_path = os.path.join(ply_file_path, 'Exported')
print('Сохраняю файл в папку: ', out_ply_file_path)
PLY.save_ply(ply_data, binary=True, path=out_ply_file_path, name=out_ply_file_name)
print('Готово!')

ElapsedTime.print_time(start)

# PLY.convert_to_ascii(ply_file_path, in_ply_file_name)

