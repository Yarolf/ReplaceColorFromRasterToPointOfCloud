import os

import PLY
import TIFF
from Keywords import Method
import time

''' РАСТР '''
start = time.time()
geotiff_file_path = r'D:\Python projects\ReplaceColorFromRasterToPointOfCloud\Files\Raster'
geotiff_file_name = r'curvature.tif'

print('Читаю растр ...')
start = time.time()
geotiff_full_path = os.path.join(geotiff_file_path, geotiff_file_name)
geotiff_file = TIFF.Raster(path=geotiff_full_path)
print('Готово!')

end = time.time() - start
minutes = int(end / 60)
seconds = int(end % 60)
print('Elapsed time: ', minutes, 'min', seconds, 'sec\n')

''' ОБЛАКО ТОЧЕК '''

start = time.time()
ply_file_path = r'D:\Python projects\ReplaceColorFromRasterToPointOfCloud\Files\Point of cloud\NEW\obj'
in_ply_file_name = r'object_gaus_cruger 18 + normals.ply'
out_ply_file_name = 'Replaced Colors ' + in_ply_file_name

print('Читаю облако точек ...')
in_full_ply_file_name = os.path.join(ply_file_path, in_ply_file_name)
ply_data = PLY.read_ply(in_full_ply_file_name)
print('Готово!')

end = time.time() - start
minutes = int(end / 60)
seconds = int(end % 60)
print('Elapsed time: ', minutes, 'min', seconds, 'sec\n')

'''ПРОВЕРКА СОВПАДЕНИЙ ИЛИ ПЕРЕНОС ЦВЕТА'''
start = time.time()
# если нужно просто проверить, без переноса, то
# print('Проверяю наличие совпадающих точек ...')
# count_matched, count_mismatched = geotiff_file.check_match(ply_data, Method.FAST.value)
# print('Найдено точек: ', count_matched)
# print('Не удалось сопоставить: ', count_mismatched)

print('Переношу цвет из растра в облако точек ...')
count_replaced, count_mismatched = geotiff_file.replace_color_to(ply_data, Method.FAST.value)
print('Перенесено точек: ', count_replaced)
print('Не удалось сопоставить точек: ', count_mismatched)
end = time.time() - start
minutes = int(end / 60)
seconds = int(end % 60)
print('Elapsed time: ', minutes, 'min', seconds, 'sec\n')

'''ЭКСПОРТ ОБЛАКА ТОЧЕК'''
# start = time.time()
# out_ply_file_path = os.path.join(ply_file_path, 'Exported')
# print('Сохраняю файл в папку: ', out_ply_file_path)
# PLY.save_ply(ply_data, binary=True, path=out_ply_file_path, name=out_ply_file_name)
# print('Готово!')

# end = time.time() - start
# minutes = int(end / 60)
# seconds = int(end % 60)
# print('Elapsed time: ', minutes, 'min', seconds, 'sec')

# PLY.convert_to_ascii(ply_file_path, in_ply_file_name)

