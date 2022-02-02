import numpy as np
import time
import copy
import os

import sys

sys.setrecursionlimit(1000000000)


def dropping_sand(grid):
    if (len(grid) % 2) == 0:
        colomn = int(len(grid) / 2 - 1)
    if (len(grid) % 2) == 1:
        colomn = int((len(grid) - 1) / 2)
    grid[colomn] += 1
    return grid


def find_coordinates_left(grid):
    coordinates_left = []
    for x in range(1, grid.shape[0]):
        if grid[x] - grid[x - 1] > 2:
            coordinates_left.append(x)
    if grid[0] > 2:
        coordinates_left.append(0)
    return coordinates_left


def find_coordinates_right(grid):
    coordinates_right = []
    for x in range(grid.shape[0] - 1):
        if grid[x] - grid[x + 1] > 2:
            coordinates_right.append(x)
    if grid[-1] > 2:
        coordinates_right.append(len(grid) - 1)
    return coordinates_right


def find_coordinates(grid):
    coordinates_left = find_coordinates_left(grid)
    coordinates_right = find_coordinates_right(grid)

    return coordinates_left, coordinates_right


def verify_if_out_of_matrix(point, grid_size_number):
    if point > (grid_size_number - 1) or point < 0:
        return False
    return True


def avalanche_separate_left(grid, singlecoordinate, grid_size_number, index_of_site):
    grid[singlecoordinate] -= 1
    index_of_site.append(singlecoordinate)
    grid_left = singlecoordinate - 1

    if verify_if_out_of_matrix(grid_left, grid_size_number):
        grid[grid_left] += 1
        index_of_site.append(grid_left)

    return grid, index_of_site


def avalanche_separate_right(grid, singlecoordinate, grid_size_number, index_of_site):
    grid[singlecoordinate] -= 1
    index_of_site.append(singlecoordinate)
    grid_right = singlecoordinate + 1

    if verify_if_out_of_matrix(grid_right, grid_size_number):
        grid[grid_right] += 1
        index_of_site.append(grid_right)

    return grid, index_of_site


def avalanche_separate(grid, coordinates_left, coordinates_right, grid_size_number, index_of_site):
    for single_coordinate_left in coordinates_left:
        grid, index_of_site = avalanche_separate_left(grid, single_coordinate_left, grid_size_number, index_of_site)
    for single_coordinate_right in coordinates_right:
        grid, index_of_site = avalanche_separate_right(grid, single_coordinate_right, grid_size_number, index_of_site)

    return grid, index_of_site


def avalanche(grid, coordinates_left, coordinates_right, grid_size_number, index_of_site):
    grid, index_of_site = avalanche_separate(grid, coordinates_left, coordinates_right, grid_size_number, index_of_site)

    coordinates_left, coordinates_right = find_coordinates(grid)

    if not (coordinates_left == [] and coordinates_right == []):
        grid, index_of_site = avalanche(grid, coordinates_left, coordinates_right, grid_size_number, index_of_site)

    return grid, index_of_site


def save_data(grid_size_number, repeat_times, critical_number, site_number_total, number_of_grains_total):
    save_folder = r'D:\Study\Physics\sandpiles\data'
    t = time.strftime('%Y_%m_%d_%H%M%S', time.localtime())
    save_path = os.path.join(save_folder,
                             '1D_fixed' + str(grid_size_number) + '_' + str(repeat_times) + '_' + t + '.txt')

    text = [grid_size_number, '\n', repeat_times, '\n', critical_number, '\n', site_number_total, '\n',
            number_of_grains_total]
    with open(save_path, 'w+') as txt:
        for item in text:
            txt.write(str(item))
    print('The data is saved')
    return True


if __name__ == '__main__':
    grid_size_number_list = [10, 30, 50, 100, 200, 400, 800]

    for grid_size_number in grid_size_number_list:
        grid = np.zeros(grid_size_number, int)

        number_of_grains_total = []
        site_number_total = []

        repeat_times = 200000
        critical_state = 0
        critical_number_50_plus = None

        last_grid = copy.copy(grid)
        for i in range(repeat_times):

            grid = dropping_sand(grid)

            index_of_site = []
            coordinates_left, coordinates_right = find_coordinates(grid)
            grid, index_of_site = avalanche(grid, coordinates_left, coordinates_right, grid_size_number, index_of_site)

            site_number_total.append(len(list(dict.fromkeys(index_of_site))))
            number_of_grains_total.append(np.sum(grid))

            if critical_state != 50:
                if all([grid[a] == last_grid[a]
                        for a in range(grid_size_number)]):
                    critical_number_50_plus = i
                    critical_state += 1
                else:
                    critical_state = 0
            else:
                break
            print(grid)
            last_grid = copy.copy(grid)

        if critical_number_50_plus is not None:
            print('The grid reached critical state at ', critical_number_50_plus - 50)

        save_data(grid_size_number, repeat_times, critical_number_50_plus - 50, site_number_total,
                  number_of_grains_total)

