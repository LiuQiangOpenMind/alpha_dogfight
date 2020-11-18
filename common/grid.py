import numpy as np


class MapGrid(object):
    """
    example:
      upleft = (-10, 10)
      right_down = (10, -10)
    --------------> x
    |
    |
    |
    y
    MapGrid的构造函数之所以要定义成这个形式，是因为要兼容path-founding这个路径规划的库
    """
    def __init__(self, up_left, right_down, x_n, y_n):
        self.up_left = up_left
        self.right_down = right_down
        self.x_n = x_n
        self.y_n = y_n

    def get_idx(self, x, y):
        """
        Args:
            x, y: real coordinates.
        Retuns:
            x_idx, y_idx: the grid where the real coordinates are.
        """
        x_len = np.abs(self.right_down[0] - self.up_left[0])
        x_idx = int(np.abs(x - self.up_left[0]) * self.x_n / x_len)
        y_len = np.abs(self.right_down[1] - self.up_left[1])
        y_idx = int(np.abs(y - self.up_left[1]) * self.y_n / y_len)
        # assert x_idx >= 0 and x_idx < self.x_n
        # assert y_idx >= 0 and y_idx < self.y_n
        return x_idx, y_idx

    def get_center(self, x_idx, y_idx):
        """Get center point of a box according to index.
        Args:
            x_idx: the x index of a grid.
            y_idx: the y index of a grid.
        Returns:
            The center point of the grid.
        """
        # assert x_idx >= 0 and x_idx < self.x_n
        # assert y_idx >= 0 and y_idx < self.y_n
        x_delta_per_grid = (self.right_down[0] - self.up_left[0]) / self.x_n
        y_delta_per_grid = (self.right_down[1] - self.up_left[1]) / self.y_n

        center_point_x = self.up_left[0] + (x_idx + 0.5) * x_delta_per_grid
        center_point_y = self.up_left[1] + (y_idx + 0.5) * y_delta_per_grid
        return center_point_x, center_point_y

    def get_length_per_grid(self, axis=0):
        if axis == 0:
            return np.abs(self.right_down[0] - self.up_left[0]) / self.x_n
        else:
            return np.abs(self.right_down[1] - self.up_left[1]) / self.y_n

    def is_idx_valid(self, x_idx, y_idx):
        return x_idx >= 0 and x_idx < self.x_n and y_idx >= 0 and y_idx < self.y_n


def test_check_tuple(tuple_, expected):
    if tuple_[0] == expected[0] and tuple_[1] == expected[1]:
        return True
    print("your tuple {}, expected {}".format(tuple_, expected))
    return False


def test_get_idx():
    up_left = (0, 0)
    right_down = (5, 5)
    grid = MapGrid(up_left, right_down, 5, 5)
    assert(test_check_tuple(grid.get_idx(0, 0), (0, 0)))
    assert(test_check_tuple(grid.get_idx(0.5, 0.5), (0, 0)))
    assert(test_check_tuple(grid.get_idx(2.5, 2.5), (2, 2)))
    assert(test_check_tuple(grid.get_idx(4.5, 4.5), (4, 4)))

    up_left = (-5, 5)
    right_down = (5, -5)
    grid = MapGrid(up_left, right_down, 10, 10)
    assert(test_check_tuple(grid.get_idx(0, 0), (5, 5)))
    assert(test_check_tuple(grid.get_idx(3.5, 3.5), (8, 1)))
    assert(test_check_tuple(grid.get_idx(-3.5, -3.5), (1, 8)))


def test_get_center():
    up_left = (0, 0)
    right_down = (5, 5)
    grid = MapGrid(up_left, right_down, 5, 5)
    assert(test_check_tuple(grid.get_center(0, 0), (0.5, 0.5)))
    assert(test_check_tuple(grid.get_center(1, 3), (1.5, 3.5)))

    up_left = (-5, 5)
    right_down = (5, -5)
    grid = MapGrid(up_left, right_down, 10, 10)
    assert(test_check_tuple(grid.get_center(5, 5), (0.5, -0.5)))


if __name__ == "__main__":
    test_get_idx()
    test_get_center()
