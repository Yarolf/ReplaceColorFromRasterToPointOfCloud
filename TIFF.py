import gdal
import numpy as np
import NumbaSpeedBoost
# from progress.bar import IncrementalBar
from Progress import Progress

from Keywords import Element, Property, Channel, PixelPosition, Method

''' INFO
E - параметр сдвига (x координата центра левого верхнего пикселя)
A - масштаб растра по оси X; размер пиксела по оси X (например в 1 единице растра - 20 метров)
C -  параметр поворота (обычно равен нулю)
F - параметр сдвига (y координата центра левого верхнего пикселя)
D -  параметр поворота (обычно равен нулю)
B - масштаб растра по оси Y; отрицательный размер пиксела по оси Y

Получение координат каждого пикселя
x = Ax + Cy + E
y = Dx + By + F
'''


class Raster:
    raster = 0
    raster_array = 0
    E = 0
    A = 0
    C = 0
    F = 0
    D = 0
    B = 0

    def __find_appropriate_pixel(self, cloud_point_x, cloud_point_y):
        max_x = self.raster.RasterXSize
        max_y = self.raster.RasterYSize

        if self.C == 0 and self.D == 0:
            x = round((cloud_point_x - self.E) / self.A)
            y = round((cloud_point_y - self.F) / self.B)
            if (0 <= x < max_x) and (0 <= y < max_y):
                return x, y
        return PixelPosition.NOT_MATCHED.value, PixelPosition.NOT_MATCHED.value

    def __write_color_from_one_channel_raster(self, ply_data, i, x, y):
        # INFO координаты в массиве поменяны местами: raster_array[y][x]!!!
        # (не знаю почему, но так сделали в библиотеке)
        ply_data[Element.VERTEX.value].data[Property.RED.value][i] = self.raster_array[y][x]
        ply_data[Element.VERTEX.value].data[Property.GREEN.value][i] = 0
        ply_data[Element.VERTEX.value].data[Property.BLUE.value][i] = 0

    def __write_color_from_three_channel_raster(self, ply_data, i, x, y):
        # INFO координаты в массиве поменяны местами: raster_array[y][x]!!!
        # (не знаю почему, но так сделали в библиотеке)
        ply_data[Element.VERTEX.value].data[Property.RED.value][i] = \
            self.raster_array[Channel.RED.value][y][x]
        ply_data[Element.VERTEX.value].data[Property.GREEN.value][i] = \
            self.raster_array[Channel.GREEN.value][y][x]
        ply_data[Element.VERTEX.value].data[Property.BLUE.value][i] = \
            self.raster_array[Channel.BLUE.value][y][x]

    def __init__(self, path=''):
        self.raster = gdal.Open(path)
        self.raster_array = self.raster.ReadAsArray()
        self.E, self.A, self.C, self.F, self.D, self.B = self.raster.GetGeoTransform()

    def __replace_color_slow(self, ply_data):
        """
        Перемещает цвет пикселя из растра в сопоставленную по координатам точку из облака точек без ускорения numba \n
        Для более быстрого переноса использовать "replace_color_from_one_channel_parallel"
        """
        i = 0
        count_matched = 0
        data_count = ply_data[Element.VERTEX.value].count
        # bar = IncrementalBar('Countdown', max=data_count)
        progress = Progress(data_count)
        band_count = self.raster.RasterCount
        if band_count == 1:
            write_color = self.__write_color_from_one_channel_raster
        else:
            write_color = self.__write_color_from_three_channel_raster
        while i < data_count:
            cloud_point_x = ply_data[Element.VERTEX.value].data[Property.X.value][i]
            cloud_point_y = ply_data[Element.VERTEX.value].data[Property.Y.value][i]
            x, y = self.__find_appropriate_pixel(cloud_point_x, cloud_point_y)
            if x != PixelPosition.NOT_MATCHED.value and y != PixelPosition.NOT_MATCHED.value:
                count_matched += 1
                write_color(ply_data, i, x, y)
            # bar.next()
            progress.step()
            i += 1
        # bar.finish()
        progress.reset()
        print('Всего точек:', data_count)
        count_mismatched = data_count - count_matched
        return count_matched, count_mismatched

    def __replace_color_fast(self, ply_data):
        """
        Перемещает цвет пикселя из растра в сопоставленную по координатам точку из облака точек с использованием numba\n
        При возникновении ошибок использовать "replace_color_slow"
        """

        # numba не работает с классами, поэтому приходится разбивать всё по переменным и numpy массивам
        x_ply_points = np.array(ply_data[Element.VERTEX.value].data[Property.X.value])
        y_ply_points = np.array(ply_data[Element.VERTEX.value].data[Property.Y.value])
        ply_red_channels = np.array(ply_data[Element.VERTEX.value].data[Property.RED.value])
        ply_green_channels = np.array(ply_data[Element.VERTEX.value].data[Property.GREEN.value])
        ply_blue_channels = np.array(ply_data[Element.VERTEX.value].data[Property.BLUE.value])
        max_x = self.raster.RasterXSize
        max_y = self.raster.RasterYSize
        E = self.E
        A = self.A
        F = self.F
        B = self.B
        C = self.C
        D = self.D
        band_count = self.raster.RasterCount
        # prev_color = ply_data[Element.VERTEX.value].data[Property.RED.value][1000]
        # print("Проверка переноса цвета", prev_color)
        if band_count == 1:
            raster_grey_np_arr = np.array(self.raster_array)
            count_replaced, count_mismatched = \
                NumbaSpeedBoost.replace_color_from_one_channel_parallel\
                (
                    x_ply_points, y_ply_points,
                    ply_red_channels, ply_green_channels, ply_blue_channels,
                    max_x, max_y,
                    E, A, F, B, C, D,
                    raster_grey_np_arr
                )
        else:
            raster_red_np_arr = np.array(self.raster_array[Channel.RED.value])
            raster_green_np_arr = np.array(self.raster_array[Channel.GREEN.value])
            raster_blue_np_arr = np.array(self.raster_array[Channel.BLUE.value])
            count_replaced, count_mismatched = \
                NumbaSpeedBoost.replace_color_from_three_channel_parallel\
                (
                    x_ply_points, y_ply_points,
                    ply_red_channels, ply_green_channels, ply_blue_channels,
                    max_x, max_y,
                    E, A, F, B, C, D,
                    raster_red_np_arr, raster_blue_np_arr, raster_green_np_arr
                )

        ply_data[Element.VERTEX.value].data[Property.RED.value] = ply_red_channels
        ply_data[Element.VERTEX.value].data[Property.GREEN.value] = ply_green_channels
        ply_data[Element.VERTEX.value].data[Property.BLUE.value] = ply_blue_channels
        # cur_color = ply_data[Element.VERTEX.value].data[Property.RED.value][1000]
        # print("Проверка переноса цвета", cur_color)
        # print("Цвет изменился?", prev_color != cur_color)
        return count_replaced, count_mismatched

    def replace_color_to(self, ply_data, method):
        """
        Перемещает цвет пикселя из растра в сопоставленную по координатам точку из облака точек\n
        Для более быстрого просчёта использовать "Method.FAST.value"  \n
        При возникновении ошибок использовать "Method.SLOW.value"
        """
        if method == Method.SLOW.value:
            return self.__replace_color_slow(ply_data)
        if method == Method.FAST.value:
            return self.__replace_color_fast(ply_data)

# START HelpFunctions
    def __check_match_slow(self, ply_data):
        """
        Проверка совпадения координат из облака точек с координатами растра без ускорения numba \n
        Для более быстрого просчёта использовать "check_match_fast"
        """

        i = 0
        count_matched = 0
        data_count = ply_data[Element.VERTEX.value].count
        # bar = IncrementalBar('Countdown', max=data_count)
        progress = Progress(data_count)
        while i < data_count:
            cloud_point_x = ply_data[Element.VERTEX.value].data[Property.X.value][i]
            cloud_point_y = ply_data[Element.VERTEX.value].data[Property.Y.value][i]
            x, y = self.__find_appropriate_pixel(cloud_point_x, cloud_point_y)
            if x != PixelPosition.NOT_MATCHED.value and y != PixelPosition.NOT_MATCHED.value:
                count_matched += 1
            # bar.next()
            progress.step()
            i += 1
        # bar.finish()
        progress.reset()
        # print('Всего точек:', data_count)
        count_mismatched = data_count - count_matched
        return count_matched, count_mismatched

    def __check_match_fast(self, ply_data):
        """
        Проверка совпадения координат из облака точек с координатами растра с использованием numba \n
        При возникновении проблем использовать "check_match_slow"
        """
        # numba работает с numpy массивом, с питоновским массивом не работает, а кортеж только 100 элементов
        # также numba не работает с классами, поэтому нужно создавать новые numpy массивы

        x_arr = np.array(ply_data[Element.VERTEX.value].data[Property.X.value])
        y_arr = np.array(ply_data[Element.VERTEX.value].data[Property.Y.value])

        max_x = self.raster.RasterXSize
        max_y = self.raster.RasterYSize
        E = self.E
        A = self.A
        F = self.F
        B = self.B
        C = self.C
        D = self.D
        count_matched, count_mismatched = NumbaSpeedBoost.check_match_parallel(x_arr, y_arr, max_x, max_y, E, A, F, B, C, D)
        return count_matched, count_mismatched

    def check_match(self, ply_data, method):
        """
        Проверка совпадения координат из облака точек с координатами растра \n
        Для более быстрого просчёта использовать "Method.FAST.value"  \n
        При возникновении ошибок использовать "Method.SLOW.value"
        """
        if method == Method.SLOW.value:
            return self.__check_match_slow(ply_data)
        if method == Method.FAST.value:
            return self.__check_match_fast(ply_data)

    def get_geotiff_coord(self, x_pixel, y_pixel):
        """
        Получить геокоординаты конкретного пикселя растра в системе координат, заданной растром
        """
        world_coord_x = self.A * x_pixel + self.C * y_pixel + self.E
        world_coord_y = self.D * x_pixel + self.B * y_pixel + self.F
        return world_coord_x, world_coord_y
# End


''' HELPFUL INFO
имя[канал][x][y]
R правого верхнего пикселя
print(raster_array[Channel.RED.value][0][x - 1])
G правого верхнего пикселя
print(raster_array[Channel.GREEN.value][0][x - 1])
B правого верхнего пикселя
print(raster_array[Channel.BLUE.value][0][x - 1])
A правого верхнего пикселя
print(raster_array[Channel.ALPHA.value][0][x - 1])

world_coord = get_geotiff_coord(0, 0)
X мировые координаты правого верхнего пикселя
print(world_coord.x)
Y мировые координаты правого верхнего пикселя
print(world_coord.y)

print(ply_data.elements[Elements.VERTEX.value].data[Properties.RED.value])
elements 'vertex' в нём данные по всем столбцам в столбце data['red'] данные о красном столбце

Количество каналов в изображении
image.RasterCount
'''
