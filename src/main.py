import numpy as np
import matplotlib.animation as animation
import matplotlib.pyplot as plt
from typing import Iterable


HEALTY = 0
ZOMBIE = 1
EMPTY = -1
WIN = 30
PARKED = 0
TRIES = 0


def seed_zombies_at_center(grid: np.array, _: int):
    """
    For a 100 x 100 grid
    """
    for i in range(45, 55):
        for j in range(45, 55):
            grid[i, j] = ZOMBIE


def seed_healty(grid: np.array, size: int, probability: float) -> None:
    """
    Using a pseudo random probability set cells as healty humans
    """
    for i in range(size):
        for j in range(size):
            if np.random.random() < probability:
                grid[i, j] = HEALTY


def get_infected(neighbors: list[int], density: float) -> bool:
    k = len([x for x in neighbors if x == ZOMBIE])

    if k == 0:
        return False

    zombie_probability = 1 - density**k
    return np.random.random() >= zombie_probability


def border_zombies(grid, size) -> int:
    """
    Count zombies that reach the border for the grid
    """
    counter = 0
    for i in range(size):
        if grid[i, 0] == ZOMBIE:
            counter += 1

        if grid[i, size - 1] == ZOMBIE:
            counter += 1

    return counter


def zombies_win(grid, size) -> bool:
    """
    Zombies  win if they reach the left or right borders of the grid
    """
    for i in range(size):
        if ZOMBIE in (grid[i, 0], grid[i, size - 1]):
            return True
    return False


def simulate(frameNum, img, grid, size: int, density: float) -> Iterable:
    """
    If a HEALTY person has three Zombies neighbors it became Zombie
    """
    next_grid = grid.copy()
    global PARKED
    global TRIES

    if zombies_win(grid, size):
        plt.text(50, 50, 'Zombies Win!', dict(size=30),
                 horizontalalignment='center', verticalalignment='center',
                 color='red')
        plt.text(50, 60, f'Probabilidad: {border_zombies(grid, size)/TRIES}',
                 dict(size=30),
                 horizontalalignment='center', verticalalignment='center',
                 color='red')
    elif PARKED >= WIN:
        plt.text(50, 50, 'Spread stopped', dict(size=30),
                 horizontalalignment='center', verticalalignment='center',
                 color='blue')
    else:
        for i in range(size):
            for j in range(size):
                # sum the values in the cell axis to know his destiny
                neighbors = [grid[i, (j - 1) % size],
                             grid[i, (j + 1) % size],
                             grid[(i - 1) % size, j],
                             grid[(i + 1) % size, j],
                             grid[(i - 1) % size, (j - 1) % size],
                             grid[(i - 1) % size, (j + 1) % size],
                             grid[(i + 1) % size, (j - 1) % size],
                             grid[(i + 1) % size, (j + 1) % size]]

                if grid[i, j] == HEALTY and get_infected(neighbors, density):
                    next_grid[i, j] = ZOMBIE

        img.set_data(next_grid)

        if np.array_equal(grid, next_grid):
            PARKED += 1
        else:
            PARKED = 0  # we reset the counter if the grids are not equal

        grid[:] = next_grid[:]
        plt.title(f"Simulación: {frameNum}")
        plt.legend()
        TRIES += 1
    return img,


def zombie_attak(human_density: float):
    world_size = 100
    update_interval = 200
    world_grid = np.full((world_size, world_size), EMPTY)
    seed_healty(world_grid, world_size, human_density)
    seed_zombies_at_center(world_grid, world_size)
    fig, ax = plt.subplots()
    img = ax.imshow(world_grid, interpolation='nearest', cmap='viridis')
    _ = animation.FuncAnimation(fig,
                                simulate,
                                fargs=(img, world_grid, world_size, human_density),  # noqa: E501
                                frames=100000,
                                interval=update_interval)
    plt.show()


if __name__ == '__main__':
    human_density = float(input('Densidad de humanos saludables: '))
    zombie_attak(human_density)
