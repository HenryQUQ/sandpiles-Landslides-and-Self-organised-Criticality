import numpy as np
from matplotlib import pyplot as plt
import seaborn
import os
import time

import sys

sys.setrecursionlimit(1000000000)

fig = plt.figure()

plt.ion()


def dropping_sand(grid):
    colomn = np.random.randint(0, grid.shape[0])
    row = np.random.randint(0, grid.shape[0])
    grid[colomn, row] += 1
    return grid


def find_coordinates(grid):
    coordinates = []
    for x in range(grid.shape[0]):
        for y in range(grid.shape[0]):
            if not grid[x, y] < 4:
                coordinates.append((x, y))

    return coordinates


def verify_if_out_of_matrix(site, number_of_size):
    for coor in site:
        if coor > (number_of_size - 1) or coor < 0:
            return False
    return True


def avalanche_separate(grid, singlecoordinate, size_number, index_of_site):
    grid[singlecoordinate] -= 4
    index_of_site.append(singlecoordinate)
    grid_top = (singlecoordinate[0] - 1, singlecoordinate[1])
    grid_bottom = (singlecoordinate[0] + 1, singlecoordinate[1])
    grid_left = (singlecoordinate[0], singlecoordinate[1] - 1)
    grid_right = (singlecoordinate[0], singlecoordinate[1] + 1)

    for point in [grid_top, grid_bottom, grid_left, grid_right]:
        if verify_if_out_of_matrix(point, size_number):
            grid[point] += 1

    return grid, index_of_site


def plot_grid(grid):
    ax = seaborn.heatmap(grid, cmap='YlGnBu', vmin=0, vmax=4, xticklabels=2, yticklabels=2, cbar=False)
    plt.plot()
    plt.pause(100)


def avalanche(grid, coordinates, size_number, index_of_site):
    for single_coordinate in coordinates:
        grid, index_of_site = avalanche_separate(grid, single_coordinate, size_number, index_of_site)
    coordinates = find_coordinates(grid)
    plot_grid(grid)

    if not coordinates == []:
        grid, index_of_site = avalanche(grid, coordinates, grid_size_number, index_of_site)

    return grid, index_of_site


def verify_finish(grid):
    if all([number == 3 for list in grid for number in list]):
        return True
    else:
        return False


def save_data(grid_size_number, repeat_times, critical_number, site_number_total):
    save_folder = r'D:\Study\Physics\sandpiles\data'
    t = time.strftime('%Y_%m_%d_%H%M%S', time.localtime())
    save_path = os.path.join(save_folder, str(grid_size_number) + '_' + str(repeat_times) + '_' + t + '.txt')

    text = [grid_size_number, '\n', repeat_times, '\n', critical_number, '\n', site_number_total]
    with open(save_path, 'w+') as txt:
        for item in text:
            txt.write(str(item))
    print('The data is saved')
    return True


def save_density(grid_size_number, repeat_times, critical_number, density_total):
    save_folder = r'D:\Study\Physics\sandpiles\data'
    t = time.strftime('%Y_%m_%d_%H%M%S', time.localtime())
    save_path = os.path.join(save_folder,
                             'density_' + str(grid_size_number) + '_' + str(repeat_times) + '_' + t + '.txt')

    text = [grid_size_number, '\n', repeat_times, '\n', critical_number, '\n', density_total]
    with open(save_path, 'w+') as txt:
        for item in text:
            txt.write(str(item))
    print('The data is saved')
    return True


if __name__ == '__main__':

    grid_size_number_list = [50]
    for grid_size_number in grid_size_number_list:

        grid = np.zeros((grid_size_number, grid_size_number), int)
        ax = seaborn.heatmap(grid, cmap='YlGnBu', vmin=0, vmax=4, xticklabels=2, yticklabels=2)
        plt.xlabel('n')
        plt.ylabel('m')
        plt.title('Grid for Model 4.1.1 after 200000 Grains Dropped')
        site_number_total = []
        critical_state = False
        critical_number = None
        repeat_times = 200000

        desity_total = []

        for i in range(repeat_times):

            index_of_site = []

            grid = dropping_sand(grid)
            coordinates = find_coordinates(grid)
            grid, index_of_site = avalanche(grid, coordinates, grid_size_number, index_of_site)
            site_number_total.append(len(list(dict.fromkeys(index_of_site))))

            if verify_finish(grid) and critical_state is False:
                critical_number = i
                critical_state = True
            desity_total.append(np.sum(grid))

            print(i, '\n', grid)

        if not (critical_number is None):
            print('The grid reached critical state at ', critical_number, 'time.')

        print(grid_size_number, repeat_times, critical_number, site_number_total)
        plot_grid(grid)
        save_density(grid_size_number, repeat_times, critical_number, desity_total)
        save_data(grid_size_number, repeat_times, critical_number, site_number_total)
