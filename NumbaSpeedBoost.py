from numba import njit, prange


@njit(fastmath=True, parallel=True)
def check_match_parallel(cloud_points_x, cloud_points_y, max_x, max_y, A, B, C, D, E, F):
    count_matched = 0
    count = cloud_points_x.shape[0]
    for i in prange(count):
        y = A * (cloud_points_y[i] - F) - B * B * D * (cloud_points_x[i] + E)
        y = round(y / (B * (A + B * D * C)))
        x = round((cloud_points_x[i] - C * y - E) / A)
        if (0 <= x < max_x) and (0 <= y < max_y):
            count_matched += 1
    count_mismatched = count - count_matched
    return count_matched, count_mismatched


@njit(fastmath=True, parallel=True)
def replace_color_from_one_channel_parallel(
        cloud_points_x, cloud_points_y,
        ply_red_channels, ply_green_channels, ply_blue_channels,
        max_x, max_y,
        A, B, C, D, E, F,
        raster_grey_np_arr):

    count_replaced = 0
    count = cloud_points_y.shape[0]

    for i in prange(count):
        y = A * (cloud_points_y[i] - F) - B * B * D * (cloud_points_x[i] + E)
        y = round(y / (B * (A + B * D * C)))
        x = round((cloud_points_x[i] - C * y - E) / A)
        if (0 <= x < max_x) and (0 <= y < max_y):
            # INFO координаты в массиве поменяны местами: raster_array[y][x]!!!
            # (не знаю почему, но так сделали в библиотеке)
            ply_red_channels[i] = raster_grey_np_arr[y][x]
            ply_green_channels[i] = raster_grey_np_arr[y][x]
            ply_blue_channels[i] = raster_grey_np_arr[y][x]
            count_replaced += 1
    count_mismatched = count - count_replaced
    return count_replaced, count_mismatched


@njit(fastmath=True, parallel=True)
def replace_color_from_three_channel_parallel(
        cloud_points_x, cloud_points_y,
        ply_red_channels, ply_green_channels, ply_blue_channels,
        max_x, max_y,
        A, B, C, D, E, F,
        raster_red_np_arr, raster_green_np_arr, raster_blue_np_arr):

    count_replaced = 0
    count = cloud_points_x.shape[0]

    for i in prange(count):
        y = A * (cloud_points_y[i] - F) - B * B * D * (cloud_points_x[i] + E)
        y = round(y / (B * (A + B * D * C)))
        x = round((cloud_points_x[i] - C * y - E) / A)
        if (0 <= x < max_x) and (0 <= y < max_y):
            # INFO координаты в массиве поменяны местами: raster_array[y][x]!!!
            # (не знаю почему, но так сделали в библиотеке)
            ply_red_channels[i] = raster_red_np_arr[y][x]
            ply_green_channels[i] = raster_green_np_arr[y][x]
            ply_blue_channels[i] = raster_blue_np_arr[y][x]
            count_replaced += 1
    count_mismatched = count - count_replaced
    return count_replaced, count_mismatched
