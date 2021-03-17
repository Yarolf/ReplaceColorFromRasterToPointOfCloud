from numba import njit, prange


@njit(fastmath=True, cache=True, parallel=True)
def check_match_parallel(x_points, y_points, max_x, max_y, E, A, F, B, C, D):
    count_matched = 0
    count = x_points.shape[0]
    # TODO вывести уравнение для C != 0 или D != 0
    if C != 0 or D != 0:
        return 0, count
    for i in prange(count):
        x = round((x_points[i] - E) / A)
        y = round((y_points[i] - F) / B)
        if (0 <= x < max_x) and (0 <= y < max_y):
            count_matched += 1
    count_mismatched = count - count_matched
    return count_matched, count_mismatched


@njit(fastmath=True, cache=True)
def __replace_from_three_channel_raster():
    pass


@njit(fastmath=True, cache=True)
def __replace_from_one_channel_raster(ply_red_channels, ply_green_channels, ply_blue_channels, raster_color_np_arr, i, x, y):
    ply_red_channels[i] = raster_color_np_arr[y][x]  # для одноканального
    ply_green_channels[i] = 0
    ply_blue_channels[i] = 0


@njit(fastmath=True, cache=True, parallel=True)
def replace_color_parallel(
        x_ply_points, y_ply_points,
        ply_red_channels, ply_green_channels, ply_blue_channels,
        max_x, max_y,
        E, A, F, B, C, D,
        raster_red_np_arr=0, raster_green_np_arr=0, raster_blue_np_arr=0):

    count_replaced = 0
    count = x_ply_points.shape[0]
    # TODO вывести уравнение для C != 0 или D != 0
    if C != 0 or D != 0:
        return 0, count

    for i in prange(count):
        x = round((x_ply_points[i] - E) / A)
        y = round((y_ply_points[i] - F) / B)
        if (0 <= x < max_x) and (0 <= y < max_y):
            # TODO replace color from three channel raster
            # INFO координаты в массиве поменяны местами: raster_array[y][x]!!!
            # (не знаю почему, но так сделали в библиотеке)
            if raster_green_np_arr == 0:
                __replace_from_one_channel_raster(ply_red_channels, ply_green_channels, ply_blue_channels,
                                                  raster_red_np_arr, i, x, y)
            else:
                __replace_from_three_channel_raster()
            count_replaced += 1
    count_mismatched = count - count_replaced
    return count_replaced, count_mismatched
