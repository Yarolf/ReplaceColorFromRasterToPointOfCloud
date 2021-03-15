import gdal
import Coordinates
from Keywords import Elements, Properties, Channel, PixelPosition
from progress.bar import IncrementalBar

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


def get_geotiff_coord(raster, x_pixel, y_pixel):
    world_coord_x = raster.A * x_pixel + raster.C * y_pixel + raster.E
    world_coord_y = raster.D * x_pixel + raster.B * y_pixel + raster.F
    world_coordinate = Coordinates.WorldCoordinate(world_coord_x, world_coord_y)
    return world_coordinate


def print_percent(prev_percent, i, data_count):
    percent = i / (data_count / 100)
    percent = round(percent, 1)
    if prev_percent != percent:
        print(percent, '%')
    return percent


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
            x = (cloud_point_x - self.E) / self.A
            x = round(x)
            y = (cloud_point_y - self.F) / self.B
            y = round(y)
        if (0 <= x < max_x) and (0 <= y < max_y):
            return x, y
        return PixelPosition.NOT_MATCHED.value, PixelPosition.NOT_MATCHED.value

    def __write_color_from_one_channel_raster(self, ply_data, i, x, y):
        ply_data[Elements.VERTEX.value].data[Properties.RED.value][i] = self.raster_array[y][x]
        ply_data[Elements.VERTEX.value].data[Properties.GREEN.value][i] = 0
        ply_data[Elements.VERTEX.value].data[Properties.BLUE.value][i] = 0

    def __write_color_from_three_channel_raster(self, ply_data, i, x, y):
        ply_data[Elements.VERTEX.value].data[Properties.RED.value][i] = \
            self.raster_array[Channel.RED.value][y][x]
        ply_data[Elements.VERTEX.value].data[Properties.GREEN.value][i] = \
            self.raster_array[Channel.GREEN.value][y][x]
        ply_data[Elements.VERTEX.value].data[Properties.BLUE.value][i] = \
            self.raster_array[Channel.BLUE.value][y][x]

    def __init__(self, path=''):
        self.raster = gdal.Open(path)
        self.raster_array = self.raster.ReadAsArray()
        self.E, self.A, self.C, self.F, self.D, self.B = self.raster.GetGeoTransform()

    def replace_color_to(self, ply_data):
        i = 0
        count_matched = 0
        data_count = ply_data[Elements.VERTEX.value].count
        # bar = IncrementalBar('Countdown', max=data_count)
        _prev_percent = -1
        band_count = self.raster.RasterCount

        while i < data_count:
            cloud_point_x = ply_data[Elements.VERTEX.value].data[Properties.X.value][i]
            cloud_point_y = ply_data[Elements.VERTEX.value].data[Properties.Y.value][i]
            x, y = self.__find_appropriate_pixel(cloud_point_x, cloud_point_y)
            # INFO координаты в массиве почему-то поменяны местами: raster_array[y][x]!!!
            if x != PixelPosition.NOT_MATCHED.value and y != PixelPosition.NOT_MATCHED.value:
                count_matched += 1
                # TODO сделать делегат на функцию записи цвета
                if band_count == 1:
                    self.__write_color_from_one_channel_raster(ply_data, i, x, y)
                else:
                    self.__write_color_from_three_channel_raster(ply_data, i, x, y)
            # bar.next()
            _prev_percent = print_percent(_prev_percent, i, data_count)
            i += 1
        # bar.finish()
        print('Всего точек:', data_count)
        count_mismatched = data_count - count_matched
        return count_matched, count_mismatched, ply_data

# START HELP function Проверка совпадения координат из облака точек с координатами растра
    def check_match(self, ply_data):
        i = 0
        count_matched = 0
        data_count = ply_data[Elements.VERTEX.value].count
        # bar = IncrementalBar('Countdown', max=data_count)
        _prev_percent = -1

        while i < data_count:
            cloud_point_x = ply_data[Elements.VERTEX.value].data[Properties.X.value][i]
            cloud_point_y = ply_data[Elements.VERTEX.value].data[Properties.Y.value][i]
            x, y = self.__find_appropriate_pixel(cloud_point_x, cloud_point_y)
            if x != PixelPosition.NOT_MATCHED.value and y != PixelPosition.NOT_MATCHED.value:
                count_matched += 1
            # bar.next()
            _prev_percent = print_percent(_prev_percent, i, data_count)
            i += 1
        # bar.finish()
        print('Всего точек:', data_count)
        count_mismatched = data_count - count_matched
        return count_matched, count_mismatched
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
